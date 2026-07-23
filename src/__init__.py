from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router


@asynccontextmanager
async def life_span(app):
    print(f"server is starting................")
    await init_db()
    yield
    print(f"server has been stopped")

version='v1'


app=FastAPI(
    lifespan=life_span
)

app.include_router(book_router,prefix='/api/{version}/books')

app.include_router(auth_router,prefix='/api/{version}/auth')