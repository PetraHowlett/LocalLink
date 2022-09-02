from flask import send_file
from flask import Flask
import json, uuid, pickle, pyperclip, requests

app = Flask(__name__)
PORT = 8080
HOST = "0.0.0.0"
KEYS = r'D:\GITHUB\flask_test\keys.json'
def get_keys():
    print("keys = ", KEYS)
    with open(KEYS) as f:
        data = f.read()
        keys = json.loads(data)
        return keys
        
def generate_key():
    return str(uuid.uuid4())


@app.route('/<path:key>',methods = ['GET','POST'])
def get_files(key):
    keys = get_keys()
    if keys.get(key):
        file = keys[key]
        try:
            return send_file(file, as_attachment=True)
        except Exception as e:
            return str(e)
    else: print("Key not found")

def add_key(file):
    ip = str(requests.get('https://api.ipify.org').content.decode('utf8'))
    keys = get_keys()
    key = generate_key()
    keys[key] = file
    with open(KEYS, 'w') as fp:
        json.dump(keys, fp, indent = 4)
    pyperclip.copy("http://{ip}:{port}/{key}".format(ip = ip, port = PORT, key = key))   

def start_flask():
    app.run(host = HOST, port = PORT, threaded = True, debug = False)

if __name__ == '__main__':
    start_flask()