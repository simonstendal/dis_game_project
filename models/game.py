from database import get_connection
import models.movie as mov

class Game:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
def get_all_movies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT title, box_office, ranking, tagline FROM movies')
    all_movies = cur.fetchall()

    movies = []
    for row in all_movies:
        movies.append({'title': row[0],
                       'box_office': row[1],
                       'ranking': row[2],
                       'tagline': row[3]})  # or {'title': row[0]}
    return movies

def movie_hint(movie:mov.movie, amount):
    hint1 = f"The genre of the movie is"
    hint2 = f"The year the movie was made is:"
    hint3 = f"The movie had a budget of  {movie['box_office']}"
    hint4 = f"The movie is ranked top {movie['ranking']}/250 on IMDB's all time movies"
    hint5 = f"The tagline of the movie is: {movie['tagline']}"
    solution = f"The title of the movie was {movie['title']}. Better luck next time!"
    hint_array = [hint1,hint2,hint3,hint4,hint5, solution]
    return hint_array[0:amount]


    

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
