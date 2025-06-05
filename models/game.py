from database import get_connection
import models.movie as mov
import re
import random as rnd

class Game:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
def get_all_movies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, box_office, ranking, tagline, release_year FROM movies')
    all_movies = cur.fetchall()
	
    movies = []
    for row in all_movies:
        movies.append({'id': row[0],
            		   'title': row[1],
                       'box_office': row[2],
                       'ranking': row[3],
                       'tagline': row[4],
                       'release_year': row[5]})  # or {'title': row[0]}
    movies.sort(key=lambda m: m['title'].lower()) 
    return movies

def get_genres(movie_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM genres WHERE movie_id = %s', (movie_id,))
    genres = cur.fetchall()
    return genres

def movie_hint(movie:mov.movie, amount, rand_int: int):
    genres = get_genres(movie['id'])
    rnd_genre = rnd.randint(0,len(genres))
    genre = mov.Genre(genres[rnd_genre][1])
    hint1 = f"It is a {genre}-movie"
    hint2 = f"The year the movie was made is {movie['release_year']}:"
    hint3 = f"The movie had a budget of ${movie['box_office']}"
    hint4 = f"The movie is ranked top {movie['ranking']}/250 on IMDB's all time movies"
    hint5 = f"The tagline of the movie is: {movie['tagline']}"
    hint6 = analyse_title(movie['title'], rand_int)
    solution = f"The title of the movie was {movie['title']}. Better luck next time!"
    hint_array = [hint1,hint2,hint3,hint4,hint5,hint6,solution]
    return hint_array[0:amount]

def analyse_title(moive_title: str, rand_int: int):
    analyse_1 = re.search('[^e]*e[^e]*e[^e]*e', moive_title)
    analyse_2 = re.search('[theThe]', moive_title)
    analyse_3 = re.search('^[0-9a-zA-Z]', moive_title)
    analyse_4 = re.search('^/w*$', moive_title)
    analyse_5 = re.search('Forrest Gump$', moive_title)
    length_check = len(moive_title)
    regex = [analyse_1,analyse_2,analyse_3, analyse_4, analyse_5]
    chosen_hint = regex[rand_int]
    if chosen_hint:
        insert = ""
    else:
        insert = "not"
    string_array = [f"The movie does {insert} have 3 or more e's",
                    f"The movie does {insert} contain \"the\"",
                    f"The movie does {insert} contain special characters",
                    f"The movie is {insert} only one word",
                    f"The movie is {insert} \"Forrest Gump\"."]
    return string_array[rand_int]

    


# "ranking=row[0],
#         title=row[1],
#         release_date=row[2],
#         rating=row[3],
#         genre= create_genre(row[4]),
#         classification=create_classification(row[5]),
#         duration=row[6],
#         tagline=row[7],
#         budget=row[8] if row[8] != "Not Available" else None,
#         box_office=row[9] if row[9] != "Not Available" else None,
#         cast=row[10],
#         director=row[11],
#         writer=row[12]"
#def list_categories():
#    conn = db_connection()
#    cur = conn.cursor()
#    cur.execute('SELECT id, category_name FROM categories')
#    db_categories = cur.fetchall()

#    categories = []
#    for db_category in db_categories:
#        categories.append(Category(db_category[0], db_category[1]))
#    conn.close()
#    return categories

#def insert_category(category_name):
#    conn = db_connection()
#    cur = conn.cursor()
#    cur.execute('INSERT INTO categories (category_name) VALUES (%s) ON CONFLICT DO NOTHING', (category_name,))
#    conn.commit()
#    cur.close()
#    conn.close()
