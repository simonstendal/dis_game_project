To run the project, first use "docker compose build", followed by "docker compose up -d".
You may need to run the commands as superuser with "sudo" if running on linux.
This should start the project on local host port 5000, ie. type in localhost:5000 into your browser.

As for the regex, we use it for a random hint, see the method "analyse_title" in models/game.py.
Our ER diagram has also been attatched to the project, see ER_diagram.png.

Our project both creates and queries a database with info on the top-rated 250 movies on IMDB.
To play the game press the button on the startpage and write in movies in the searchbar, each
time you fail you will gain another hint. Starting a new game chooses a new random movie to guess.
