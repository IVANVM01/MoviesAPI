#  Dependences

#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

#Own
from jwt_manager import validate_token


#  Models
# Request Body & Validaciones
# Utiliza la clase Field, la cual utiliza los mismos atributos tal como las clases Path, Query, Body

class User(BaseModel):
    email: str = Field(min_length=5,
                       max_length=100,
                       title="Email",
                       description="This is the email"
                )
    password: str = Field(min_length=5,
                          max_length=15,
                          title="Password",
                          description="This is the password"
                )


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            return HTTPException(status_code=403, detail="Las credenciales son incorrectas.")


class Movie(BaseModel):
    id: Optional[int] = None    #None indica que es opcional
    title: str = Field(min_length=5,
                       max_length=15,
                       title="Movie ID",
                       description="This is the movie"
                )
    overview: str = Field(min_length=15,
                          max_length=50,
                          title="Movie Overview",
                          description="This is the movie overview"
                )
    year: int = Field(ge=1900, le=2023)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=5, max_length=15)

    class Config:           # Subclase para automatizar el llenado del request body y optimizar la experiencia de desarrollo
        schema_extra = {    # Este atributo sirve para definir la informacion por defecto para la documentacion interactiva
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de mi pelicula ...",
                "year": 2020,
                "rating": 5.0,
                "category": "Accion"
            }
        }