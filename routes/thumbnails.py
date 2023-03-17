from flask import Blueprint, render_template, request, Response
import requests
thumbnail = Blueprint("thumbnail", __name__, url_prefix="/")


@thumbnail.route("/")
def landing():
    if url := request.args.get("url"):
        print(url)
        try:
            response = requests.get(url, timeout=10)
            return Response(response.content, mimetype='image/jpeg', headers={'Content-Disposition': 'attachment;filename=image.jpg'})
        except Exception:
            return

    return render_template("index.html")