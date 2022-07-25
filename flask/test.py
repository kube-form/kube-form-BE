from copyreg import constructor
from sys import api_version
from flask import Flask,Response,request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api,Resource  # Api 구현을 위한 Api 객체 import
import os,subprocess,json,base64,boto3
from matplotlib import container
import yaml # pip install pyYAML
from Crypto.Cipher import AES
import make

client = boto3.client('kms')
key_id = os.environ['KMS_KEY_ID']
pad = lambda s: s + (32 - len(s) % 32) * ' '

# data key 생성
data_key = client.generate_data_key(KeyId=key_id, KeySpec='AES_256')
plaintext_key = data_key.get('Plaintext') # 평문 data key
ciphertext_blob = data_key.get('CiphertextBlob') # 암호화된 data key


# 암호화
def encrypt_data(self, plaintext_message):
  crypter = AES.new(self.plaintext_key) # 평문 data key를 이용하여 암호화 객체 생성
  encrypted_data = base64.b64encode(crypter.encrypt(self.pad(plaintext_message))) # 문자열을 암호화하고 base64로 인코딩

  return encrypted_data, self.ciphertext_blob # 암호화된 data key(복호화에 필요한 평문 Data Key를 얻기 위해 꼭 필요한 정보), 이미 생성된 암호화된 data key 반환 

# 복호화
def decrypt_data(self, encrypted_data, ciphertext_blob):
  decrypted_key = self.client.decrypt(ciphertext_blob).get('Plaintext') # 전달 받은 암호화된 문자열(encrypted_data)과 Data Key(ciphertext_blob)로 평문 Data Key를 반환
  crypter = AES.new(decrypted_key) # 암호화 역순으로 암호화된 문자열을 base64로 디코딩

  return crypter.decrypt(base64.b64decode(encrypted_data)).rstrip() # 복호화해서 반환
  
  
def lambda_handler(event, context):
    # TODO implement
    
    # IAM 유저 암호화해서 저장
    encrypt_data(self, "testestestest")
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }