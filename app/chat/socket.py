import logging
from datetime import datetime
from typing import Dict

from flask import session, request, flash
from app.extensions import socketio
from flask_socketio import emit, join_room
from app.config import Config
from app import create_logger

logger = create_logger()


active_users: Dict[str, dict] = {}


@socketio.event
def connect():
    username = session.get("username", "Guest")
    active_users[request.sid] = {   #type: ignore
        "username": username,
        "connected_at": datetime.now().isoformat(),
    }

    emit(
        "active_users",
        {"users": [u["username"] for u in active_users.values()]},
        broadcast=True,
    )

    logger.info("User connected: %s", username)


@socketio.event
def disconnect():
    user = active_users.pop(request.sid, None)      #type: ignore
    if user:
        emit(
            "active_users",
            {"users": [u["username"] for u in active_users.values()]},
            broadcast=True,
        )
        logger.info("User disconnected: %s", user["username"])


@socketio.on("join")
def join(data):
    room = data.get("room")
    username = session.get("username")

    if not room:
        return

    join_room(room)
    active_users[request.sid]["room"] = room    #type: ignore

    emit(
        "status",
        {
            "msg": f"{username} joined {room}",
            "type": "join",
            "timestamp": datetime.now().isoformat(),
        },
        to=room,
    )


@socketio.event
def handle_message(data: dict):
    try:
        username = session['username']
        room = data.get('room ', "General")
        msg_type = data.get('type', 'message')
        message = data.get('msg', "").strip()

        if not message:
            return
        
        timestamp = datetime.now().isoformat()

        if msg_type == 'private_message':
            target_user = data.get('target')
            
            if not target_user:
                return
            
            for sid, user_data in active_users.items():
                if user_data['username'] == target_user:
                    emit('private', {
                        'msg': message,
                        'from': username,
                        'to': target_user,
                        'timestamp': timestamp
                    }, to=sid)
        
        else:
            if room not in Config.CHAT_ROOMS:
                return
            
            emit('message', {
                'msg': message,
                'from': username,
                'timestamp': timestamp,
                'type': msg_type
            }, to=room)
            
    except Exception as e:
        logger.error("Error handling message: %s", str(e))