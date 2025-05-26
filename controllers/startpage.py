from flask import Blueprint, render_template

bp = Blueprint('startpage', __name__, url_prefix='/')

@bp.route("/")
def startpage():
    return render_template("startpage.html")