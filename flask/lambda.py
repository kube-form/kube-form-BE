import requests,json
url = "http://3.39.156.140:3000/cluster"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {"user_id" : "newdeal3", "instance_type" : "t3.medium", "Encrypted_Access_Key_ID" : "AKIASPQZDTUHSGANU2FN" , "Encrypted_Secret_Access_Key":"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"}
flask_response = requests.get(url=url, json=data, headers=headers).json()
print(flask_response)