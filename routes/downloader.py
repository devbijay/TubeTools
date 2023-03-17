from flask import Blueprint, render_template
from pytube import YouTube
download = Blueprint("download", __name__, url_prefix="/download")


@download.route("/")
def landing():
    return render_template("download.html")