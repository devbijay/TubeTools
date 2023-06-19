from flask import Blueprint, render_template, request, jsonify
from pytube import YouTube
import re

download = Blueprint("download", __name__, url_prefix="/download")


@download.route("/audio", methods=["GET", "POST"])
def audio():
    if request.method == "POST":
        payload = request.get_json()
        if video_id := payload.get("video_id"):
            yt = YouTube(url=f"https://youtube.com/watch?v={video_id}", use_oauth=False, allow_oauth_cache=True)
            yt.bypass_age_gate()
            audio_stream = yt.streams.filter(only_audio=True).first()
            return jsonify({"url": audio_stream.url, "size": audio_stream.filesize_mb})
    return render_template("download.html")


@download.route("/video", methods=["GET", "POST"])
def video():
    if request.method == "POST":
        payload = request.get_json()
        if video_id := payload.get("video_id"):
            yt = YouTube(url=f"https://youtube.com/watch?v={video_id}", use_oauth=False, allow_oauth_cache=True)
            yt.bypass_age_gate()
            video_streams = yt.streams
            video_streams = [streams for streams in video_streams
                             if (streams.includes_video_track and streams.includes_audio_track)]
            video_streams = video_streams[::-1]  # Reversing To Get Highest To The Lowest resolution
            video_dict = []
            for stream in video_streams:
                video_data = {"res": stream.resolution,
                              "size": f"{stream.filesize / (1024 * 1024):.2f} MB",
                              "url": stream.url}
                video_dict.append(video_data)
            return jsonify(video_dict)

    return render_template("download_video.html")
