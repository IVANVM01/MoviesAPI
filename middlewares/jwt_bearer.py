#FastAPI
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

#Own
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Las credenciales son incorrectas.")