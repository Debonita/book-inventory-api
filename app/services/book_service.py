from app.repositories.book_repository import BookRepository
from app.schemas.book_schemas import BookCreate,BookUpdate,BookResponse
import uuid
from typing import Optional,List

class BookService:
    def __init__(self, repository:BookRepository):
        self.repository=repository

    def create_book(self,book_data:BookCreate)-> BookResponse:
        book_id=str(uuid.uuid4())
        book=self.repository.create(book_id,book_data)
        return BookResponse(**book.to_dict())
    
    def get_all_books(self, genre:Optional[str]=None, available:Optional[bool]=None)->List[BookResponse]:
        books=self.repository.get_all(genre=genre, available=available)
        return [BookResponse(**book.to_dict()) for book in books]
    
    def get_book_by_id(self,book_id:str)-> Optional[BookResponse]:
        book=self.repository.get_by_id(book_id)
        if book:
            return BookResponse(**book.to_dict)
        return None
    
    def update_book(self,book_id:str,book_data:BookUpdate)->Optional[BookResponse]:
        book=self.repository.update(book_id,book_data,)
        if book:
            return BookResponse(**book.to_dict())
        return None
    def delete_book(self,book_id:str) ->bool:
        return self.repository.delete(book_id)
        
    
