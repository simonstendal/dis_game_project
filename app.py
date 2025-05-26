from flask import Flask
from database import init_db
from controllers import game, startpage

init_db()

app = Flask(__name__)

app.register_blueprint(startpage.bp)
app.register_blueprint(game.bp)
