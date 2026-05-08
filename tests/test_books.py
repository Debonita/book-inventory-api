import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Valid API Key for tests
VALID_API_KEY = "secret-api-key-12345"
INVALID_API_KEY = "wrong-key"


# Test 1: Create a book successfully
def test_create_book_success():
    """Test creating a book with valid data and API key"""
    response = client.post(
        "/books/",
        json={
            "title": "1984",
            "author": "George Orwell",
            "genre": "Fiction",
            "price": 12.99,
            "available": True
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"] == "George Orwell"
    assert data["genre"] == "Fiction"
    assert data["price"] == 12.99
    assert data["available"] == True
    assert "id" in data


# Test 2: List books with genre filter
def test_list_books_with_genre_filter():
    """Test filtering books by genre"""
    # Create test books
    client.post(
        "/books/",
        json={
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "genre": "Fantasy",
            "price": 15.99,
            "available": True
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    client.post(
        "/books/",
        json={
            "title": "Dune",
            "author": "Frank Herbert",
            "genre": "Science Fiction",
            "price": 18.99,
            "available": True
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    # Filter by Fantasy
    response = client.get(
        "/books/?genre=Fantasy",
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(book["genre"] == "Fantasy" for book in data)


# Test 3: Fetch a missing book — expect 404
def test_get_nonexistent_book():
    """Test fetching a book that doesn't exist"""
    response = client.get(
        "/books/99999",
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Book with id 99999 not found"


# Test 4: Submit invalid price — expect 422
def test_create_book_invalid_price():
    """Test creating a book with negative price"""
    response = client.post(
        "/books/",
        json={
            "title": "Invalid Book",
            "author": "Test Author",
            "genre": "Fiction",
            "price": -5.99,  # Invalid: negative price
            "available": True
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# Test 5: Missing X-API-Key header — expect 401
def test_missing_api_key():
    """Test accessing endpoint without API key"""
    response = client.get("/books/")
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any(
        error["loc"] == ["header", "x-api-key"] and error["type"] == "missing" for error in data["detail"]
    )


# Bonus Test 6: Invalid API key — expect 403
def test_invalid_api_key():
    """Test accessing endpoint with wrong API key"""
    response = client.get(
        "/books/",
        headers={"X-API-Key": INVALID_API_KEY}
    )
    
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid API Key"


# Bonus Test 7: Update book
def test_update_book():
    """Test updating an existing book"""
    # Create book
    create_response = client.post(
        "/books/",
        json={
            "title": "Original Title",
            "author": "Original Author",
            "genre": "Fiction",
            "price": 10.99,
            "available": True
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    book_id = create_response.json()["id"]
    
    # Update book
    update_response = client.put(
        f"/books/{book_id}",
        json={
            "title": "Updated Title",
            "author": "Updated Author",
            "genre": "Non-Fiction",
            "price": 20.99,
            "available": False
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"
    assert data["price"] == 20.99
    assert data["available"] == False


# Bonus Test 8: Delete book
def test_delete_book():
    """Test deleting a book"""
    # Create book
    create_response = client.post(
        "/books/",
        json={
            "title": "Book to Delete",
            "author": "Test Author",
            "genre": "Fiction",
            "price": 9.99,
            "available": True
        },
        headers={"X-API-Key": VALID_API_KEY}
    )
    book_id = create_response.json()["id"]
    
    # Delete book
    delete_response = client.delete(
        f"/books/{book_id}",
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert delete_response.status_code == 204
    
    # Verify book is deleted
    get_response = client.get(
        f"/books/{book_id}",
        headers={"X-API-Key": VALID_API_KEY}
    )
    assert get_response.status_code == 404