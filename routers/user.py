#  Dependences
#FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
#Own
from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()


# Login
@user_router.post(
    path="/login",
    tags=["Auth"],
    response_model=dict,
    status_code=status.HTTP_200_OK
)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Usuario o contraseña incorrectos"}, status_code=status.HTTP_401_UNAUTHORIZED)