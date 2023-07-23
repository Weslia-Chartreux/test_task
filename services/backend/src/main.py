from fastapi import FastAPI

from uvicorn import run
from src.routers import auth, post, like

app = FastAPI()

app.include_router(auth.router, tags=['Auth'], prefix='/api')
app.include_router(like.router, tags=['Like'], prefix='/api')
app.include_router(post.router, tags=['Posts'], prefix='/api')

if __name__ == "__main__":
    run(app)
