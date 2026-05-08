from app.models.book import Book
from app.schemas.book_schemas import BookCreate, BookUpdate
from typing import Optional,List

class BookRepository:
    def __init__(self):
        self._books:dict[str,Book]={}
    def create (self,book_id:str,book_data:BookCreate)->Book:
        book=Book(
            id=book_id,
            title=book_data.title,
            author=book_data.author,
            genre=book_data.genre.value,
            price=book_data.price,
            available=book_data.available
        )
        self._books[book_id]=book
        return book
    
    def get_all(self,genre:Optional[str] = None, available: Optional[bool] = None)->List[Book]:
        books=list(self._books.values())
        if genre:
            books=[b for b in books if b.genre.lower()==genre.lower()]
        if available is not None:
            books=[b for b in books if b.available==available]
        return books
    
    def get_by_id(self,book_id:str)->Optional[Book]:
        return self._books.get(book_id)
    
    def update (self,book_id:str,book_data:BookUpdate)->Optional[Book]:
        book=self._books.get(book_id)
        if not book:
            return None
        
        if book_data.title is not None:
            book.title=book_data.title
        if book_data.author is not None:
            book.author = book_data.author
        if book_data.genre is not None:
            book.genre = book_data.genre.value
        if book_data.price is not None:
            book.price = book_data.price
        if book_data.available is not None:
            book.available = book_data.available
        return book
    
    def delete(self,book_id:str)->bool:
        if book_id in self._books:
            del self._books[book_id]
            return True
        return False
