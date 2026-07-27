from fastapi import Header,status,APIRouter

from fastapi.exceptions import HTTPException
from src.books.book_data import books
from fastapi import Depends
from src.books.schemas import Book,BookUpdateModel,BookCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer
from uuid import UUID

book_router=APIRouter()
Book_service=BookService()
access_token_bearer=AccessTokenBearer()

@book_router.get("/",response_model=list[Book])
async def get_books(session:AsyncSession=Depends(get_session),
                    user_details=Depends(access_token_bearer)):
    books=await Book_service.get_all_books(session)
    return books

@book_router.post("/",status_code=201)
async def create_book(book_data:BookCreateModel,
                      session:AsyncSession=Depends(get_session),
                      user_details=Depends(access_token_bearer)):

    new_book=await Book_service.create_book(book_data,session)

    return new_book

@book_router.get("/{book_uid}")
async def get_book(book_uid: UUID,session:AsyncSession=Depends(get_session),
                   user_details=Depends(access_token_bearer)):
    book=await Book_service.get_book(book_uid,session)

    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.patch("/{book_uid}")
async def update_book(book_uid:UUID,book_update:BookUpdateModel,session:AsyncSession=Depends(get_session),
                      user_details=Depends(access_token_bearer)):
    updated_book=await Book_service.update_book(book_uid,book_update,session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@book_router.delete("/{book_uid}")
async def delete_book(book_uid:UUID,session:AsyncSession=Depends(get_session),
                      user_details=Depends(access_token_bearer)):
        book_to_delete=await Book_service.delete_book(book_uid,session)
        if book_to_delete:
            return book_to_delete
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)