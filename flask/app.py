#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import response
from flask import Flask,Response,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api,Resource  # Api 구현을 위한 Api 객체 import
import flask_restx,os,subprocess,json,base64,boto3,time,yaml # pip install pyYAML
import make
from matplotlib import container
client = boto3.client('s3')
resource = boto3.resource('s3')

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록



@api.route('/')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@api.route('/example/<string:name>')  # url pattern으로 name 설정
class Example(Resource):
    def get(self, name):  # 멤버 함수의 파라미터로 name 설정
        return {"message" : "Welcome, %s!" % name}


@api.route('/infra',  methods=['POST','DELETE']) 
class Execute(Resource):
    def post(self): 
        response = Response(json.dumps("{'detail':'terraform apply command executed successfully.'}"), status=200, mimetype='application/json')

        params = request.get_json()
        # Required_information = ["user_id"]
        Required_information = ["user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key","node_group_num"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps({'detail':f"no {i} attribute in request BODY."}), status=400, mimetype='application/json') #400 오류 핸들링

        @response.call_on_close
        def on_close():
            os.environ["NodeGroupNum"] = f'{params["node_group_num"]}'
            os.environ["InstanceType"] = f'{params["instance_type"]}'
            os.environ["KUBEFORM_ACCESS_KEY_ID"] = params["Encrypted_Access_Key_ID"]
            os.environ["KUBEFORM_SECRET_ACCESS_KEY"] = params["Encrypted_Secret_Access_Key"]
            os.system("./sh/script.sh") # 쉘 스크립트 실행
            print("terraform apply done!")

            client.upload_file('.././terraform/terraform.tfstate','kube-form',f"kubeSources/{params['user_id']}/status/terraform.tfstate") # 유저의 S3 버킷에 tfstate 내용 저장

        return response

    def delete(self):
        response = Response(json.dumps({'detail':'deleted all AWS infra.'}), status=200, mimetype='application/json')
        params = request.get_json()
        # Required_information = ["user_id"]
        Required_information = ["user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps({'detail':f"no {i} attribute in request BODY."}), status=400, mimetype='application/json') #400 오류 핸들링
       
        @response.call_on_close
        def on_close():
             #aws configure
            os.environ["NAMESPACE"] = params["user_id"] + "-ns"
            os.environ["KUBEFORM_ACCESS_KEY_ID"] = params["Encrypted_Access_Key_ID"]
            os.environ["KUBEFORM_SECRET_ACCESS_KEY"] = params["Encrypted_Secret_Access_Key"]
            os.system("./sh/cluster.sh")
            os.system("./sh/kube-delete.sh")

            client.download_file('kube-form', f"kubeSources/{params['user_id']}/status/terraform.tfstate", '.././terraform/terraform.tfstate')
            os.system("./sh/delete.sh")
            bucket = resource.Bucket('kube-form')
            bucket.objects.filter(Prefix=f"kubeSources/{params['user_id']}/").delete()

        return response
        

@api.route('/cluster',  methods=['POST','GET']) 
class Execute(Resource):
    def post(self): 
        params = request.get_json()
        Required_information = ["node_group_num","container","user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key","instance_type"]
        Required_container = ["dockerURL","port","name","replicas"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps({'detail':f"no {i} attribute in request BODY." }), status=400, mimetype='application/json') #400 오류 핸들링
            if(i == "container"):
                for j in Required_container:
                    for k in params['container']:
                        if(k.get(j) is None):
                            return Response(json.dumps({'detail':f"no {j} attribute in request BODY container type."}), status=400, mimetype='application/json') #400 오류 핸들링
        #aws configure
        os.environ["KUBEFORM_ACCESS_KEY_ID"] = params["Encrypted_Access_Key_ID"]
        os.environ["KUBEFORM_SECRET_ACCESS_KEY"] = params["Encrypted_Secret_Access_Key"]
        os.system("./sh/cluster.sh") # 쉘 스크립트 실행
        print("sh script done")
        make.make_yaml(params)
        os.system("kubectl apply -f .././k8s/")

        root = 'terraform.txt'
        bucket = 'kube-form'
        target = f"kubeSources/{params['user_id']}/status/cluster/"
        path= "../k8s"

        for root,dirs,files in os.walk(path):
            for file in files:
                client.upload_file(os.path.join(root,file),bucket,target+file)

        time.sleep(10)
        stream = os.popen("kubectl get svc --no-headers -n " + params['user_id'] + "-ns | awk '{ print $1 $4; }'")
        output = stream.read()
        client.put_object(Body=output,Bucket=bucket,Key=target+'service.txt')
        return Response(json.dumps("{'detail':'terraform apply command executed successfully.'}"), status=200, mimetype='application/json')

    def get(self): 
        params = request.get_json()
        # Required_information = ["user_id"]
        Required_information = ["user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps({'detail':f"no {i} attribute in request BODY."}), status=400, mimetype='application/json') #400 오류 핸들링
            
        client.download_file('kube-form', f"kubeSources/{params['user_id']}/status/cluster/service.txt", 'service.txt')
        response = {}
        entry_points =[]

        f= open('service.txt','r')
        while True:
            line = f.readline()
            print(line[:6])
            if not line: break
            if line[:6] != '<none>': entry_points.append(line[:len(line)-1])
        f.close()

        client.download_file('kube-form',f"kubeSources/{params['user_id']}/status/terraform.tfstate", '.././terraform/terraform.tfstate')
        ret = []
        print(entry_points)
        for n in entry_points : 
            ret.append({"name" : n[:n.find("-nlb")], "entry_point" : n[n.find("-nlb")+4:]})
        response['entry_points'] = ret
        os.environ["KUBEFORM_ACCESS_KEY_ID"] = params["Encrypted_Access_Key_ID"]
        os.environ["KUBEFORM_SECRET_ACCESS_KEY"] = params["Encrypted_Secret_Access_Key"]
        os.system("./sh/output.sh") # 쉘 스크립트 실행
        print("sh script done")

        with open("output.json", 'r') as file:
            data = json.load(file)
            response['cluster_data']=data
        
        return Response(json.dumps({'detail':'terraform apply command executed successfully.', 'data' : response}), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)