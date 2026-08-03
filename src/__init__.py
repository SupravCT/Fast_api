from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from .errors import (
    create_exception_handler,
    InvaildToken,
    RevokedToken,
    NoPermission
)


@asynccontextmanager
async def life_span(app):
    print(f"server is starting................")
    await init_db()
    yield
    print(f"server has been stopped")

version='v1'


app=FastAPI(
    #lifespan=life_span
)

app.add_exception_handler(
    InvaildToken,
    create_exception_handler(401,"Invalid or expired token")
)
app.add_exception_handler(
    RevokedToken,
    create_exception_handler(401,"Token has been revoked")
)
app.add_exception_handler(
    NoPermission,
    create_exception_handler(403,"You do not have permission to perform this action")
)

app.include_router(book_router,prefix='/api/{version}/books')

app.include_router(auth_router,prefix='/api/{version}/auth')