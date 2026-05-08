from app.dependencies import get_book_service, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.book_schemas import BookResponse, BookCreate, BookUpdate
from app.services.book_service import BookService
from typing import List, Optional

router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    return service.create_book(book)


@router.get("/", response_model=List[BookResponse])
def get_books(
    genre: Optional[str] = Query(None, description="Filter by genre"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    service: BookService = Depends(get_book_service)
):
    return service.get_all_books(genre=genre, available=available)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    book = service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: str,
    book_data: BookUpdate,
    service: BookService = Depends(get_book_service)
):
    book = service.update_book(book_id, book_data)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    deleted = service.delete_book(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return None