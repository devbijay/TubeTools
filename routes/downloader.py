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
            yt = YouTube(url=f"https://youtube.com/watch?v={video_id}")
            yt.bypass_age_gate()
            video_streams_list = yt.streams

            #Process Streams With Audio
            av_streams = [streams for streams in video_streams_list
                             if (streams.includes_video_track and streams.includes_audio_track)]
            av_streams = av_streams[::-1]  # Reversing To Get Highest To The Lowest resolution

            # Process Streams Without Audio
            only_vid_streams = [streams for streams in video_streams_list
                                if streams.includes_video_track and not streams.includes_audio_track]

            with_audio, no_audio= [], []
            for stream in av_streams:
                video_data = {"res": stream.resolution,
                              "size": f"{stream.filesize / (1024 * 1024):.2f} MB",
                              "url": stream.url}
                with_audio.append(video_data)

            for stream in only_vid_streams:
                video_data = {"res": stream.resolution,
                              "size": f"{stream.filesize / (1024 * 1024):.2f} MB",
                              "url": stream.url}
                no_audio.append(video_data)
            video_dict = {"av": with_audio, "ov": no_audio}
            print(video_dict)
            return jsonify(video_dict)

    return render_template("download_video.html")
