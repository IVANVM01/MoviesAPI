#  Dependences

#Python
import json
from typing import List

#Pydantic

#FastAPI
from fastapi import FastAPI
from fastapi import Depends, Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse

#Own
from jwt_manager import create_token

#Models
from models import User, JWTBearer, Movie


#  App Instance
app = FastAPI(
    title="Movie API",
    description="APP with FastAPI",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Iván Vergara",
        "url": "https://github.com/IVANVM01/MovieAPI",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
)


#  Paths - Endpoints: Los path operations son evaluados en orden

# Home
@app.get(path='/', tags=['Home'])   # Path Operator Decoratior
def home():                         # Path Operator Function
    #return "Hello world!"
    return HTMLResponse(
        content="""
            <h1>Hello World</h1>
            <p>API with a content</p>
        """,
        status_code=status.HTTP_200_OK
    )


# Login
@app.post(
    path="/login",
    tags=["Auth"],
    response_model=dict,
    status_code=status.HTTP_200_OK
)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)
    
    return JSONResponse(content={"message": "Usuario o contraseña incorrectos"}, status_code=status.HTTP_200_UNAUTHORIZED)


@app.get(
    path="/movies",
    tags=["Movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
)
def get_movies() -> List[Movie]:
    with open("movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)   # Devuelve un objeto JSON como un diccionario
        return JSONResponse(content=movies, status_code=status.HTTP_200_OK)


# Path Parameters & Validaciones
@app.get(
    path="/movies/{id}",
    tags=["Movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    with open("movies.json", "r", encoding="utf-8") as f:
        movies = json.loads(f.read()) #Convertir el string leido a lista de diccionarios, que es equivalente a un json
        for item in movies:
            if item['id'] == id:
                return JSONResponse(content=item, status_code=status.HTTP_200_OK)

        return JSONResponse(content={"message": "No se ha encontrado la película"}, status_code=status.HTTP_404_NOT_FOUND)


# Query Parameters & Validaciones
@app.get(
    path="/movies/",
    tags=["Movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK
)
def get_movies_by_category(
    category: str = Query(min_length=5,
                          max_length=15,
                          title="Categoria Movie",
                          description="This is the movie category")
                    ) -> List[Movie]:
    with open("movies.json", "r", encoding="utf-8") as f:
        movies = json.loads(f.read())
        data = [item for item in movies if item['category'] == category]
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@app.post(
    path="/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
def create_movie(movie: Movie) -> dict:
    with open("movies.json", "r+", encoding="utf-8") as f:
        movies = json.loads(f.read())
        movie_dict = movie.dict()
        movies.append(movie_dict)
        f.seek(0) #Principio del archivo
        f.write(json.dumps(movies)) #Convertir la lista de diccionarios a json y escribirla
        return JSONResponse(content={"message": "Se ha registrado la película"}, status_code=status.HTTP_201_CREATED)


@app.put(
    path="/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_200_OK
)
def update_movie(id: int, movie: Movie) -> dict:
    with open("movies.json", "r+", encoding="utf-8") as f:
        movies = json.load(f)
        for index, item in enumerate(movies):
            if item['id'] == id:
                movies[index]['title'] = movie.title
                movies[index]['overview'] = movie.overview
                movies[index]['year'] = movie.year
                movies[index]['rating'] = movie.rating
                movies[index]['category'] = movie.category
                break
        f.seek(0) #Principio del archivo
        json.dump(movies, f)
        return JSONResponse(content={"message": "Se ha actualizado la película"}, status_code=status.HTTP_200_OK)


@app.delete(
    path="/movies",
    tags=["Movies"],
    response_model=dict,
    status_code=status.HTTP_200_OK
)
def delete_movie(id: int) -> dict:
    with open("movies.json", "r+", encoding="utf-8") as f:
        movies = json.load(f)
        for item in movies:
            if item['id'] == id:
                movies.remove(item)
                break
        f.seek(0) #Principio del archivo
        json.dump(movies, f)
        return JSONResponse(content={"message": "Se ha eliminado la película"}, status_code=status.HTTP_200_OK)