from enum import Enum
from typing import Optional
import re

class classification(Enum):
    G           = (1, "G")
    PG          = (2, "PG")
    PG13        = (3, "PG-13")
    R           = (4, "R")
    NC17        = (5, "NC-17")
    Approved    = (6, "Approved")
    NotRated    = (7, "Not Rated")
    Passed      = (8, "Passed")
    TVPG        = (9, "TV-PG")
    Plus18      = (10, "18+")
    Unrated     = (11, "Unrated")
    X           = (12, "X")
    TVMA        = (13, "TV-MA")
    GP          = (14, "GP")

    def __init__(self, number, label):
        self._value_ = number
        self.label = label

    def __str__(self):
        return self.label
    
class StaffRole(Enum):
    Director   = 1
    Writer     = 2
    Cast       = 3
class Genre(Enum):
    Action     = (1, "Action")
    Adventure  = (2, "Adventure")
    Animation  = (3, "Animation")
    Biography  = (4, "Biography")
    Comedy     = (5, "Comedy")
    Crime      = (6, "Crime")
    Drama      = (7, "Drama")
    Family     = (8, "Family")
    Fantasy    = (9, "Fantasy")
    FilmNoir   = (10, "Film-Noir")
    History    = (11, "History")
    Horror     = (12, "Horror")
    Music      = (13, "Music")
    Musical    = (14, "Musical")
    Mystery    = (15, "Mystery")
    Romance    = (16, "Romance")
    SciFi      = (17, "Sci-Fi")
    Sport      = (18, "Sport")
    Thriller   = (19, "Thriller")
    War        = (20, "War")
    Western    = (21, "Western")

    def __init__(self, number, label):
        self._value_ = number
        self.label = label

    def __str__(self):
        return self.label
    
class movie:
    def __init__(
            self, 
            ranking : int, 
            title : str, 
            release_date : int,
            classification : Optional[classification],
            duration : Optional[int],
            tagline : str,
            rating : float,
            budget : Optional[int],
            box_office : Optional[int],
            genre : list[Genre], 
            director : list[str], 
            cast : list[str],
            writer : list[str]):
    
        self.ranking = ranking
        self.title = title
        self.release_date = release_date
        self.classification = classification
        self.duration = duration
        self.tagline = tagline
        self.rating = rating
        self.budget = budget
        self.box_office = box_office
        self.genre = genre
        self.director = director
        self.cast = cast
        self.writer = writer

def create_genre(genre_list: list[str]) -> list[Genre]:
    result = []
    for genre in genre_list:
        for g in Genre:
            if g.label.lower() == genre.lower():
                result.append(g)
                break
    return result

def create_classification(classification_str: str) -> classification | None:
    if not classification_str or classification_str == "Not Available":
        return None
    for cls in classification:
        if cls.label.lower() == classification_str.lower():
            return cls
    if classification_str == "13+":
        return classification.PG13
    raise ValueError(f"Unknown classification: {classification_str}")

def remove_char_from_budget_and_box_office(value: str) -> Optional[int]:
    if value == "Not Available":
        return None
    value = re.sub(r"\D", '', value)
    return int(value) 


def create_movie(row) -> movie:
    return movie(
        ranking=row[0],
        title=row[1],
        release_date=row[2],
        rating=row[3],
        genre= create_genre(row[4]),
        classification=create_classification(row[5]),
        duration=row[6],
        tagline=row[7][:255],
        budget=remove_char_from_budget_and_box_office(row[8]),
        box_office=remove_char_from_budget_and_box_office(row[9]),
        cast=row[10],
        director=row[11],
        writer=row[12]
    )


