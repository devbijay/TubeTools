from flask import Blueprint, render_template

thumbnail = Blueprint("thumbnail", __name__, url_prefix="/")


@thumbnail.route("/")
def landing():
    return render_template("index.html")