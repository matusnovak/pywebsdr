from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static', static_url_path='')
socketio = SocketIO(app, binary=True, async_mode='eventlet', host='0.0.0.0')

import pywebsdr.listen

@app.route('/js/<path:path>')
def send_js(path):
    print('FUCK', path)
    return app.send_static_file('js/' + path)

@app.route('/css/<path:path>')
def send_css(path):
    return app.send_static_file('css/' + path)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/favicon.ico')
def send_favicon():
    return app.send_static_file('favicon.ico')
