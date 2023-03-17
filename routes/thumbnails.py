from flask import Blueprint, render_template, request, Response
import requests
thumbnail = Blueprint("thumbnail", __name__, url_prefix="/")


@thumbnail.route("/")
def landing():
    if request.method == "POST":
        if url := request.form.get("url"):
            response = requests.get(url)
            return Response(response.content, mimetype='image/jpeg', headers={'Content-Disposition': 'attachment;filename=image.jpg'})

    return render_template("index.html")