#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,Response,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api,Resource  # Api 구현을 위한 Api 객체 import
import os,subprocess,json,base64,boto3
client = boto3.client('s3')

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

@api.route('/execute',  methods=['POST']) 
class Execute(Resource):
    def post(self): 
        ##Access_Key_ID = os.environ['Access_Key_ID']
        ##Secret_Access_Key = os.environ['Secret_Access_Key']
        params = request.get_json()
        Required_information = ["user_id","Encrypted_Access_Key_ID","Encrypted_Secret_Access_Key"]
        for i in Required_information :
            if(params.get(i) is None):
                return Response(json.dumps("{'detail':'no '${i}' attribute in request BODY.'}"), status=400, mimetype='application/json') #400 오류 핸들링

        os.system("./script.sh") # 쉘 스크립트 실행
        
        root = 'terraform.txt'
        bucket = 'kube-form'
        target = 'status/' + params['user_id'] + '/plan.txt'

        client.upload_file(root,bucket,target) # 유저의 S3 버킷에 터미널 출력내용 저장

        return Response(json.dumps("{'detail':'terraform apply command executed successfully.'}"), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)