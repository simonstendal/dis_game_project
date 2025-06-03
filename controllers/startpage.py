from flask import Blueprint, render_template, session
from models.game import get_all_movies
import random 

bp = Blueprint('startpage', __name__, url_prefix='/')

@bp.route("/")
def startpage():
    random_num = random.randint(1,250)
    movies = get_all_movies()
    session['random_movie'] = movies[random_num]
    session['counter'] = 1
    session['rand_int'] = random.randint(0,4)
    return render_template("startpage.html")