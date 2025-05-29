from flask import Flask
from database import read_data_and_create_movies
from controllers import game, startpage, win

read_data_and_create_movies()

app = Flask(__name__)
app.secret_key = "secret"
app.register_blueprint(startpage.bp)
app.register_blueprint(game.bp)
app.register_blueprint(win.bp)