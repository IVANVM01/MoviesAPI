#Starlette
from starlette.middleware.base import BaseHTTPMiddleware

#FastAPI
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    #Método que se ejecuta para detectar errores en la aplicación
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(content={"error":str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)