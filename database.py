import psycopg2
import os
import pandas as pd
from models.movie import create_movie

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
    for _, row in data.iterrows():
        row['budget'] = row['budget'].replace("$", "").replace(",", "")
        row['box_office'] = row['box_office'].replace("$", "").replace(",", "")
        row['casts'] = row['casts'].split(",")
        row['directors'] = row['directors'].split(",")
        row['writers'] = row['writers'].split(",")
        row['genre'] = row['genre'].split(",")
        row['run_time'] = convert_time_to_minutes(row['run_time'])
        movie = create_movie(row)

        fields = (f"ranking, title, release_year, rating, age_rating, run_time, "
                  f"tagline, budget, box_office")

        sql =  (f"INSERT INTO movies ({fields}) "
                f"VALUES (%(ranking)s, %(title)s, %(release_year)s, %(rating)s, %(age_rating)s, %(run_time)s, %(tagline)s, %(budget)s, %(box_office)s);")

        values = {
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

        conn = get_connection()
        if conn is None:
            print("Failed to connect to the database.")
            return
        
        with conn.cursor() as cur:
            try:
                cur.execute(sql, values)
                conn.commit()
            except Exception as e:
                print(f"Error inserting movie: {e}")
                conn.rollback()

    
