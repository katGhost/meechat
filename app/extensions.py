from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


db = SQLAlchemy()
socketio = SocketIO()
bcrypt = Bcrypt()
migrate = Migrate()
