#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,Response  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
import os,subprocess,json,base64,boto3


app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


@api.route('/')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@api.route('/example/<string:name>')  # url pattern으로 name 설정
class Hello(Resource):
    def get(self, name):  # 멤버 함수의 파라미터로 name 설정
        return {"message" : "Welcome, %s!" % name}

@api.route('/execute') 
class Hello(Resource):
    def get(self): 
        ##Access_Key_ID = os.environ['Access_Key_ID']
        ##Secret_Access_Key = os.environ['Secret_Access_Key']

        os.system("./script.sh")
        
        return Response("{'detail':'terraform apply command executed successfully.'}", status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)