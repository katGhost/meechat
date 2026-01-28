import os
import random
import logging
from typing import Dict
from datetime import datetime
from string import ascii_uppercase, ascii_lowercase

from flask import Flask, flash, jsonify, redirect, render_template, request  
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from werkzeug.middleware.proxy_fix import ProxyFix



basedir = os.path.abspath(os.path.dirname(__file__))
# config class
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")
    DEBUG = True

    # Rooms
    chat_rooms = [
        "General",
        "Software Development",
        "Showoff WIP",
        "Funny Stuff"
    ]


# Configure flask app
app = Flask(__name__)
app.config.from_object(Config)

# handle reserve proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# socket setup
socket = SocketIO(
    app,
    cors_allowed_origins=app.config["CORS_ORIGIN"],
    logger=True,
    engineio_logger=True
)

# dictionary to hold users
active_users: Dict[str, dict] = {}


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socket.run(app, debug=app.config["DEBUG"])

