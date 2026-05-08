from enum import Enum
from pydantic import BaseModel, Field, field_validator

class GenreEnum(str, Enum):
    fiction = "Fiction"
    nonfiction = "Non-Fiction"
    science_fiction = "Science Fiction"
    fantasy = "Fantasy"
    mystery = "Mystery"
    biography = "Biography"
    history = "History"
    romance = "Romance"

class BookCreate(BaseModel):
    title: str= Field(...,min_length=1, description= "Book Title")
    author: str= Field(...,min_length=1, description="Book Author")
    genre: GenreEnum=Field(...,description="Book Genre")
    price: float= Field(gt=0,description="Book price must be positive")
    available :bool= Field(default=True, description= "Availability status")

    @field_validator('title', 'author')
    @classmethod
    def title_must_not_be_blanks(cls,v:str)-> str:
        if not v.strip():
            raise ValueError('Field author or title cannot be blank')
        return v.strip()
    @field_validator('available')
    @classmethod
    def validate_available(cls, v):
        if v is not None and not isinstance(v, bool):
            raise ValueError(
                'Available must be a boolean value (true or false). '
                f'Received: {v} of type {type(v).__name__}'
            )
        return v
    class Config:
        json_schema_extra={
             "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "price": 15.99,
                "available": True
            }
        }
class BookUpdate(BaseModel):

    title: str | None = Field(None, min_length=1)
    author: str | None = Field(None, min_length=1)
    genre: GenreEnum | None = None
    price: float | None = Field(None, gt=0)
    available: bool | None = None

    @field_validator('title', 'author')
    @classmethod
    def title_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('Field author or title cannot be blank')
        return v.strip() if v else None
    
    @field_validator('available')
    @classmethod
    def validate_available(cls, v):
        if v is not None and not isinstance(v, bool):
            raise ValueError(
                'Available must be a boolean value (true or false). '
                f'Received: {v} of type {type(v).__name__}'
            )
        return v

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    genre: str
    price: float
    available: bool

    class Config:
        from_attributes=True
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "price": 15.99,
                "available": True
            }
        }