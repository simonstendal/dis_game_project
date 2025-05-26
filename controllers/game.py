from flask import Blueprint, render_template

bp = Blueprint('game', __name__, url_prefix='/')

@bp.route('/game')
def game():
    return render_template('game.html')
