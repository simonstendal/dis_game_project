import psycopg2
import os
import pandas as pd
from models.movie import create_movie, StaffRole 

user = os.getenv("PGPUSER")
password = os.getenv("PGPASSWORD")
host = os.getenv("DB_HOST")
dbname = os.getenv("DB_NAME")

connectionstring = f"dbname={dbname} user={user} password={password} host={host}"

timemap = {'h' : 60, 'm' : 1}

def get_connection():
    try:
        return psycopg2.connect(connectionstring)
    except Exception as e:
        print(f"Error connecting to the database: {e}")

def convert_time_to_minutes(time_str) -> int | None:
    if not time_str or time_str == "Not Available":
        return None
    time_parts = time_str.split()
    total_minutes = 0
    for part in time_parts:
        if part[-1] == 'h':
            total_minutes += int(part[:-1]) * timemap['h']
        elif part[-1] == 'm':
            total_minutes += int(part[:-1]) * timemap['m']
    return total_minutes

def read_data_and_create_movies():
    data = pd.read_csv("DB/IMDB Top 250 Movies.csv", delimiter=",")
    fields_movies = (f"ranking, title, release_year, rating, age_rating, run_time, "
                  f"tagline, budget, box_office")

    sql_select_movies = "SELECT id FROM movies WHERE title = %(title)s;"

    sql_inser_movies =  (f"INSERT INTO movies ({fields_movies}) "
            f"VALUES (%(ranking)s, %(title)s, %(release_year)s, %(rating)s," 
            f"%(age_rating)s, %(run_time)s, %(tagline)s, %(budget)s, %(box_office)s)"
            f"RETURNING id;")

    sql_genres = "INSERT INTO genres (movie_id, genre) VALUES (%(movie_id)s, %(genre)s) ON CONFLICT DO NOTHING;"

    sql_select_staff = "SELECT id FROM staff WHERE staff_name = %(name)s;"
    sql_insert_staff = "INSERT INTO staff (staff_name) VALUES (%(name)s) RETURNING id;"
    sql_insert_movie_staff = (f"INSERT INTO movie_staff (movie_id, staff_id, staff_role) "
                                "VALUES (%(Mid)s, %(Sid)s, %(role)s) ON CONFLICT DO NOTHING;")
    
    for _, row in data.iterrows():
        row['budget'] = row['budget']
        row['box_office'] = row['box_office']
        row['casts'] = row['casts'].split(",")
        row['directors'] = row['directors'].split(",")
        row['writers'] = row['writers'].split(",")
        row['genre'] = row['genre'].split(",")
        row['run_time'] = convert_time_to_minutes(row['run_time'])
        movie = create_movie(row)

        conn = get_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return
        
        values_movies = {
                    'ranking': movie.ranking,
                    'title': movie.title,
                    'tagline': movie.tagline,
                    'release_year': movie.release_date,
                    'age_rating': movie.classification.value if movie.classification else None,
                    'run_time': movie.duration,
                    'rating': movie.rating,
                    'budget': movie.budget,
                    'box_office': movie.box_office
                }

        with conn.cursor() as cur:
            try:
                cur.execute(sql_select_movies, {'title': movie.title})
                movie_id = cur.fetchone()
                movie_id = movie_id[0] if movie_id else None
                if movie_id is None:
                    cur.execute(sql_inser_movies, values_movies)
                    movie_id = cur.fetchone()
                    movie_id = movie_id[0] if movie_id else None
                for genre in movie.genre:
                    cur.execute(sql_genres, {'movie_id': movie_id, 'genre': genre.value})
                for director in movie.director:
                    cur.execute(sql_select_staff, {'name': director})
                    staff_id = cur.fetchone()
                    if staff_id is None:
                        cur.execute(sql_insert_staff, {'name': director})
                        staff_id = cur.fetchone()
                    cur.execute(sql_insert_movie_staff, 
                        {'Mid': movie_id, 'Sid': staff_id, 'role': StaffRole.Director.value}) 
                for cast in movie.cast:
                    cur.execute(sql_select_staff, {'name': cast})
                    staff_id = cur.fetchone()
                    if staff_id is None:
                        cur.execute(sql_insert_staff, {'name': cast})
                        staff_id = cur.fetchone()
                    cur.execute(sql_insert_movie_staff, 
                        {'Mid': movie_id, 'Sid': staff_id, 'role': StaffRole.Cast.value})
                for writer in movie.writer:
                    cur.execute(sql_select_staff, {'name': writer})
                    staff_id = cur.fetchone()
                    if staff_id is None:
                        cur.execute(sql_insert_staff, {'name': writer})
                        staff_id = cur.fetchone()
                    cur.execute(sql_insert_movie_staff, 
                        {'Mid': movie_id, 'Sid': staff_id, 'role': StaffRole.Writer.value})
                conn.commit()
            except Exception as e:
                print(f"Error inserting movie '{movie.title}' with ranking {movie.ranking}: {e}")
                conn.rollback()

    
