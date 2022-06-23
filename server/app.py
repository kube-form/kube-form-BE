import json,os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    stream = os.popen('ls -al')
    output = stream.read()
    return jsonify(output)

app.run(debug=True)