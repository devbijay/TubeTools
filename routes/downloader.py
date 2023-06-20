from flask import Blueprint, render_template, request, jsonify
from pytube import YouTube, Caption
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
            return jsonify(video_dict)

    return render_template("download_video.html")

@download.route("/captions", methods=["GET", "POST"])
def trim_audio():
    if request.method == "POST":
        payload = request.get_json()
        if video_id := payload.get("video_id"):
            yt = YouTube(url=f"https://youtube.com/watch?v={video_id}")
            yt.bypass_age_gate()
            video_streams_list = stream = yt.streams.get_highest_resolution()

            # Step 5: Generate the trimmed stream URL
            trimmed_stream_url = f"{stream.url}&begin={10}&end={20}"
            print("Trimmed Stream URL:", trimmed_stream_url)

    if video_id := request.args.get("video_id"):
        yt = YouTube(url=f"https://youtube.com/watch?v={video_id}")
        yt.bypass_age_gate()
        if captions := yt.captions.all():
            # Step 5: Select the first available caption track (assuming it's in English)
            caption = captions[0]  # 'a.en' represents English captions, you can modify it as needed

            # Step 6: Download the captions
            caption_text = caption.generate_srt_captions()
            print(caption_text)
            return caption_text

