from flask import send_file
from flask import Flask
import os, sys
import winreg as reg
import json, uuid, pickle, pyperclip, requests

app = Flask(__name__)
PORT = 8080
HOST = "0.0.0.0"
KEYS = r'D:\GITHUB\flask_test\keys.json'
def get_keys():
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

def add_menu_option():
    """
    Must be run as admin.
    """
    # Get path of current working directory and python.exe
    cwd = os.getcwd()
    python_exe = sys.executable

    # optional hide python terminal in windows
    hidden_terminal = '\\'.join(python_exe.split('\\')[:-1])+"\\pythonw.exe"


    # Set the path of the context menu (right-click menu)
    key_path = r'*\\shell\\ShareLink\\' # Change 'Organiser' to the name of your project

    # Create outer key
    key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path)
    reg.SetValue(key, '', reg.REG_SZ, '&Share Link')  # Change 'Organise folder' to the function of your script

    # create inner key
    key1 = reg.CreateKey(key, r"command")
    reg.SetValue(key1, '', reg.REG_SZ, hidden_terminal + f' {cwd}\\add_key.py "%1"')  # use hidden_terminal to to hide terminal

def start_flask():
    app.run(host = HOST, port = PORT, threaded = True, debug = False)

if __name__ == '__main__':
    start_flask()