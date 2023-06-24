#  Dependences
#FastAPI
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
#Own
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.user import user_router
from routers.movie import movie_router


#  App Instance
app = FastAPI(
    title="Movie API",
    description="APP with FastAPI",
    version="0.0.2",
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
app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(movie_router)


Base.metadata.create_all(bind=engine)


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