from schemas.movie import Movie                 #Esquema de Pydantic
from models.movie import Movie as MovieModel    #Modelo de SQLAlchemy


class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id: int, movie: Movie):
        db_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        db_movie.title = movie.title
        db_movie.overview = movie.overview
        db_movie.year = movie.year
        db_movie.rating = movie.rating
        db_movie.category = movie.category
        self.db.commit()
        return
    
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        #db_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        #self.db.delete(db_movie)
        self.db.commit()
        return