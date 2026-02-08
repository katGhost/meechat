from datetime import datetime
from typing import Dict

from flask import session, request
from flask_socketio import emit, join_room, leave_room

from app.extensions import socketio
from app.config import Config
from app import create_logger

logger = create_logger()

active_users: Dict[str, dict] = {}


@socketio.event
def connect():
    username = session.get("username", "Guest")

    active_users[request.sid] = {
        "username": username,
        "room": None,
        "connected_at": datetime.utcnow().isoformat(),
    }

    emit_active_users()
    logger.info("User connected: %s", username)


@socketio.event
def disconnect():
    user = active_users.pop(request.sid, None)
    if user:
        emit_active_users()
        logger.info("User disconnected: %s", user["username"])


@socketio.on("join")
def handle_join(data):
    room = data.get("room")
    username = session.get("username", "Guest")

    if room not in Config.CHAT_ROOMS:
        return

    join_room(room)
    active_users[request.sid]["room"] = room

    emit(
        "status",
        {"msg": f"{username} joined {room}"},
        to=room,
    )


@socketio.on("leave")
def handle_leave(data):
    room = data.get("room")
    if room:
        leave_room(room)


@socketio.on("message")
def handle_message(data):
    username = session.get("username", "Guest")
    message = data.get("msg", "").strip()

    if not message:
        return

    timestamp = datetime.utcnow().isoformat()

    if data.get("type") == "private_message":
        target = data.get("target")
        for sid, user in active_users.items():
            if user["username"] == target:
                emit(
                    "private_message",
                    {
                        "msg": message,
                        "from": username,
                        "timestamp": timestamp,
                    },
                    to=sid,
                )
        return

    room = data.get("room")
    if room not in Config.CHAT_ROOMS:
        return

    emit(
        "message",
        {
            "msg": message,
            "from": username,
            "timestamp": timestamp,
        },
        to=room,
    )


def emit_active_users():
    emit(
        "active_users",
        {"users": [u["username"] for u in active_users.values()]},
        broadcast=True,
    )
