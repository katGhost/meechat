#import asyncio
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit, send
#import websockets

app = Flask(__name__)

app.secret_key = "dev_secret_key"
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
# init
socket = SocketIO(app, cors_allowed_origins="*")


@socket.on('/chat', namespace='chatApp')
def custom_handler(message):
    print(f'Received: {message}')
    if message != 'User is connected':
        send(message, broadcast=True)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socket.run(app, debug=True, host='0.0.0.0')

