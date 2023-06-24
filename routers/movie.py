#  Dependences
#Python
from typing import List
#FastAPI
from fastapi import APIRouter
from fastapi import Depends, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
#Own
from config.database import Session
from schemas.movie import Movie                 #Esquema de Pydantic
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()


@movie_router.get(
    path="/movies",
    tags=["Movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


# Path Parameters & Validaciones
@movie_router.get(
    path="/movies/{id}",
    tags=["Movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message": "No se ha encontrado la película"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


# Query Parameters & Validaciones
@movie_router.get(
    path="/movies/",
    tags=["Movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK
)
def get_movies_by_category(
    category: str = Query(min_length=5,
                          max_length=15,
                          title="Categoria Movie",
                          description="This is the movie category"
                         )
                    ) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(content={"message": "No se encontraron películas"}, status_code=status.HTTP_404_NOT_FOUND)
    
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)


@movie_router.post(
    path="/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Se ha registrado la película"}, status_code=status.HTTP_201_CREATED)


@movie_router.put(
    path="/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_200_OK
)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message": "No se ha encontrado la película"}, status_code=status.HTTP_404_NOT_FOUND)
    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "Se ha actualizado la película"}, status_code=status.HTTP_200_OK)


@movie_router.delete(
    path="/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_200_OK
)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message": "No se ha encontrado la película"}, status_code=status.HTTP_404_NOT_FOUND)
    
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "Se ha eliminado la película"}, status_code=status.HTTP_200_OK)