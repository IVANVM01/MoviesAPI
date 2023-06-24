#  Dependences
#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel, Field

#  Models
# Request Body & Validaciones
# Utiliza la clase Field, la cual utiliza los mismos atributos tal como las clases Path, Query, Body
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