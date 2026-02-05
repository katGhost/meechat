import logging
from app import create_app
from app.extensions import socketio
from app.config import Config

app = create_app()


if __name__ == "__main__":
    socketio.run(app, debug=app.config[Config.DEBUG])