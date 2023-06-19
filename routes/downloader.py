from flask import Blueprint, render_template, request, jsonify
from pytube import YouTube
import re

download = Blueprint("download", __name__, url_prefix="/download")


@download.route("/audio", methods=["GET", "POST"])
def audio():
    if request.method == "POST":
        payload = request.get_json()
        if video_id := payload.get("video_id"):
            print(video_id)
            yt = YouTube(f"https://youtube.com/watch?v={video_id}")
            audio_stream = yt.streams.filter(only_audio=True).first()
            return jsonify({"url": audio_stream.url})

    return render_template("download.html")
