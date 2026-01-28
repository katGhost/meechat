import os
import random
import logging
from typing import Dict
from datetime import datetime
from string import ascii_uppercase, ascii_lowercase

from flask import Flask, flash, jsonify, redirect, render_template, request  
from flask_socketio import SocketIO, emit, send, join_room, leave_room



app = Flask(__name__)

app.secret_key = "M0jsib73-009naIne-8nwTjm3"
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
# socket
socket = SocketIO(app, cors_allowed_origins="*")


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socket.run(app, debug=True, host='0.0.0.0')

