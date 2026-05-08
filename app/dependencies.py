from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService
from fastapi import Header, HTTPException, status

_book_repository=BookRepository()

def get_book_repository()->BookRepository:
    return _book_repository

def get_book_service()->BookService:
    repository = get_book_repository()
    return BookService(repository=repository)

def get_current_user(x_api_key: str = Header(...)) -> dict:
    VALID_API_KEY = "secret-api-key-12345"
    
    if x_api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    # Return a mock user object
    return {"username": "api_user", "api_key": x_api_key}
