import os
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    os.system("python3 fogflock.py -l 2 -t 0.8 -u '"+request.args.get('text','')+"'")
    json_data=open("data.json").read()
    data = json.loads(json_data)
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',8080))
    app.run(host='0.0.0.0',port=port)
