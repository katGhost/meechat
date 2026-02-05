from app import create_logger
import random
from datetime import datetime

from flask import request, render_template, redirect, url_for, session, jsonify, flash
from app.config import Config
from app.chat import chat


logger = create_logger()

@chat.route('/chat-rooms')
def chat_rooms():
    session.clear()
    return render_template('chat/rooms.html', rooms=Config.CHAT_ROOMS)
