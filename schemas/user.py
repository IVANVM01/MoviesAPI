#  Dependences
#Pydantic
from pydantic import BaseModel, Field

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