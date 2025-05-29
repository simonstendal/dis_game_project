from flask import Blueprint, render_template, request, session, redirect, url_for
from models.game import get_all_movies, movie_hint
import random 

bp = Blueprint('game', __name__, url_prefix='/')

@bp.route('/game', methods=['GET', 'POST'])
def game():
    random_num = random.randint(1,250)
    movies = get_all_movies()
    if 'random_movie' not in session:
        session['random_movie'] = movies[random_num]
        session['counter'] = 1
    result = False
    if request.method == "POST":
        user_guess = request.form['movie_guess']
        if user_guess.strip().lower() == session['random_movie']['title'].strip().lower():
            result = True
            return redirect(url_for("win.win"))
        else:
            session['counter'] += 1
    return render_template('game.html', movies = movies, random_movie = session['random_movie'], result = result, counter = session['counter'], hints = movie_hint(session['random_movie'], session['counter']))
