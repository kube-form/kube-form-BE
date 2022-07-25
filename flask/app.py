#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,Response,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api,Resource  # Api 구현을 위한 Api 객체 import
import flask_restx
import os,subprocess,json,base64,boto3,time
from matplotlib import container
import yaml # pip install pyYAML
client = boto3.client('s3')

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


def make_yaml(params) : 
    for c in params['container']:
        with open('.././sample/deployment.yaml') as f:
            deployment_yaml = yaml.load(f, Loader=yaml.FullLoader)
        print("test")
        deployment_yaml['metadata']['name'] = c['name']
        deployment_yaml['spec']['replicas'] = c['replicas']
        deployment_yaml['spec']['selector']['matchLabels']['app'] = c['name'] + '-label'
        deployment_yaml['spec']['template']['metadata']['labels']['app'] = c['name'] + '-label'
        deployment_yaml['spec']['template']['spec']['containers'][0]['name'] = c['name']
        deployment_yaml['spec']['template']['spec']['containers'][0]['image'] = c['dockerURL']
        deployment_yaml['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = c['port']

        with open(f".././k8s/deployment-{c['name']}.yaml", 'w') as file:
            yaml.dump(deployment_yaml, file, default_flow_style=False)
        
        with open('.././sample/service.yaml') as f:
            service_yaml = yaml.load(f, Loader=yaml.FullLoader)
        
        service_yaml['metadata']['name'] = c['name'] + '-nlb'
        service_yaml['spec']['selector']['app'] = c['name'] + '-label'

        with open(f".././k8s/service-{c['name']}.yaml", 'w') as file:
            yaml.dump(service_yaml, file, default_flow_style=False)


@api.route('/')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@api.route('/example/<string:name>')  # url pattern으로 name 설정
class Example(Resource):
    def get(self, name):  # 멤버 함수의 파라미터로 name 설정
        return {"message" : "Welcome, %s!" % name}

@api.route('/test',  methods=['POST']) 
class Execute(Resource):
    def post(self):
        response = Response('hello')

        @response.call_on_close
        def on_close():
            for i in range(10):
                time.sleep(1)
                print(i)

        return response


@api.route('/infra',  methods=['POST']) 
class Execute(Resource):
    def post(self): 
        ##Access_Key_ID = os.environ['Access_Key_ID']
        ##Secret_Access_Key = os.environ['Secret_Access_Key']
        response = Response(json.dumps("{'detail':'terraform apply command executed successfully.'}"), status=200, mimetype='application/json')

        params = request.get_json()
        Required_information = ["user_id"]
        # Required_information = ["user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps("{'detail':'no attribute in request BODY.'}"), status=400, mimetype='application/json') #400 오류 핸들링

        @response.call_on_close
        def on_close():
            os.system("./script.sh") # 쉘 스크립트 실행
            root = 'terraform.txt'
            bucket = 'kube-form'
            target = params['user_id'] + '/status/terraform_output.txt' 
            client.upload_file(root,bucket,target) # 유저의 S3 버킷에 터미널 출력내용 저장

        return response

@api.route('/cluster',  methods=['POST','GET']) 
class Execute(Resource):
    def post(self): 
        # params = {"user_id" : "newdeal", "node_group_num" : 2 , "container" : [{"dockerURL" : "pengbai/docker-supermario", "port" : 8080 , "name" : "mario" , "replicas" : 2 },{"dockerURL" : "alexwhen/docker-2048", "port" : 80 , "name" : "game" , "replicas" : 2 }]}
        params = request.get_json()
        Required_information = ["node_group_num","container","user_id"]
        Required_container = ["dockerURL","port","name","replicas"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps("{'detail':'no attribute in request BODY.'}"), status=400, mimetype='application/json') #400 오류 핸들링
            if(i == "container"):
                for j in Required_container:
                    for k in params['container']:
                        if(k.get(j) is None):
                            return Response(json.dumps("{'detail':'no attribute in request BODY container type.'}"), status=400, mimetype='application/json') #400 오류 핸들링
        #aws configure
        os.system("./cluster.sh") # 쉘 스크립트 실행
        print("sh script done")
        make_yaml(params)
        os.system("kubectl apply -f .././k8s/")

        root = 'terraform.txt'
        bucket = 'kube-form'
        target = params['user_id'] + '/status/cluster/' 
        path= "../k8s"

        for root,dirs,files in os.walk(path):
            for file in files:
                client.upload_file(os.path.join(root,file),bucket,target+file)

        #for f in os.listdir(path):
            #os.remove(os.path.join(path, f))

        time.sleep(10)

        stream = os.popen("kubectl get svc --no-headers | awk '{ print $4; }'")
        
        output = stream.read()
        client.put_object(Body=output,Bucket=bucket,Key=target+'service.txt')
        return Response(json.dumps("{'detail':'terraform apply command executed successfully.'}"), status=200, mimetype='application/json')

    def get(self): 
        ##Access_Key_ID = os.environ['Access_Key_ID']
        ##Secret_Access_Key = os.environ['Secret_Access_Key']

        params = request.get_json()
        Required_information = ["user_id"]
        # Required_information = ["user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key"]

        bucket = 'kube-form'
        target = params['user_id'] + '/status/cluster/' + 'service.txt'
        client.download_file(bucket,target,'service.txt')
        entry_points =[]

        f= open('service.txt','r')
        while True:
            line = f.readline()
            print(line[:6])
            if not line: break
            if line[:6] != '<none>': entry_points.append(line[:len(line)-1])
        f.close()
        
        return Response(json.dumps({'detail':'terraform apply command executed successfully.', 'entry_points' : entry_points}), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)