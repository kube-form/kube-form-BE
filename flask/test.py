from copyreg import constructor
from sys import api_version
from flask import Flask,Response,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api,Resource  # Api 구현을 위한 Api 객체 import
import os,subprocess,json,base64,boto3
from matplotlib import container
import yaml # pip install pyYAML
client = boto3.client('s3')

root = 'terraform.txt'
bucket = 'kube-form'
target = 'status/cluster/' + "newdeal"
path= "../k8s"

for root,dirs,files in os.walk(path):
    for file in files:
        print(os.path.join(root,file))
        client.upload_file(os.path.join(root,file),bucket,target+'.yaml')
