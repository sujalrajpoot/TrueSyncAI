from flask import Flask
from app.config import Config
from app.routes import api_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints (modular routes)
    app.register_blueprint(api_blueprint)

    return app
