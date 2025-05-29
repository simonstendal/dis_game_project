from flask import Blueprint, render_template, session

bp = Blueprint('win', __name__, url_prefix='/')

@bp.route("/win")
def win():
    return render_template("win.html", counter = session['counter'])