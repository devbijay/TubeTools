from flask import Flask
from routes.thumbnails import thumbnail


def create_app():
    app = Flask(__name__)
    app.register_blueprint(thumbnail)
    return app
