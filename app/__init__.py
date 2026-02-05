from flask import Flask, g
import logging
from app.config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from app.extensions import socketio, migrate, bcrypt, db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config.Config')

    # reverse proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Initialize extensions
    socketio.init_app(
        app,
        cors_allowed_origins=app.config["CORS_ORIGIN"],
        logger=Config.DEBUG,
        engineio_logger=Config.DEBUG,
    )
    
    bcrypt.init_app(app)

    # Import and register blueprints
    from app.core import core
    from app.chat import chat


    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(chat, url_prefix='/chat')
    
    migrate.init_app(app, db)

    return app


def create_logger():
    logs = logging.getLogger(__name__)

    return logs

