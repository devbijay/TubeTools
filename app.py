from flask import Flask

from routes.downloader import download
from routes.thumbnails import thumbnail


def create_app():
    app = Flask(__name__)
    app.register_blueprint(thumbnail)
    app.register_blueprint(download)

    return app
