"""
Tests for API endpoints.

These tests focus on HTTP responses, status codes, and API behavior.
"""

import pytest


class TestBookAPI:
    """Tests for Book API endpoints"""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data
    
    def test_get_all_books_empty(self, client):
        """Test getting books when database is empty"""
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_book(self, client, sample_book_data):
        """Test creating a book via API"""
        response = client.post("/books", json=sample_book_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_book_data["title"]
        assert data["author"] == sample_book_data["author"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_book_with_invalid_data(self, client):
        """Test creating a book with invalid data"""
        invalid_data = {
            "title": "",  # Too short
            "author": "Test",
            "publication_year": 5000,  # Too high
            "genre": "Test"
        }
        
        response = client.post("/books", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_book_with_duplicate_isbn(self, client, sample_book_data):
        """Test creating books with duplicate ISBN"""
        # Create first book
        client.post("/books", json=sample_book_data)
        
        # Try to create duplicate
        response = client.post("/books", json=sample_book_data)
        assert response.status_code == 409  # Conflict
        assert "already exists" in response.json()["detail"]
    
    def test_get_all_books(self, client, sample_book_data):
        """Test getting all books"""
        # Create two books
        client.post("/books", json=sample_book_data)
        client.post("/books", json={**sample_book_data, "isbn": "9780987654321", "title": "Book 2"})
        
        response = client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 2
    
    def test_get_book_by_id(self, client, sample_book_data):
        """Test getting a specific book by ID"""
        # Create a book
        create_response = client.post("/books", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        # Get it by ID
        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == sample_book_data["title"]
    
    def test_get_nonexistent_book(self, client):
        """Test getting a book that doesn't exist"""
        response = client.get("/books/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_update_book(self, client, sample_book_data):
        """Test updating a book"""
        # Create a book
        create_response = client.post("/books", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        # Update it
        updated_data = {**sample_book_data, "title": "Updated Title"}
        response = client.put(f"/books/{book_id}", json=updated_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["id"] == book_id
    
    def test_update_nonexistent_book(self, client, sample_book_data):
        """Test updating a book that doesn't exist"""
        response = client.put("/books/999", json=sample_book_data)
        assert response.status_code == 404
    
    def test_delete_book(self, client, sample_book_data):
        """Test deleting a book"""
        # Create a book
        create_response = client.post("/books", json=sample_book_data)
        book_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_book(self, client):
        """Test deleting a book that doesn't exist"""
        response = client.delete("/books/999")
        assert response.status_code == 404
    
    def test_isbn_with_hyphens_normalized(self, client):
        """Test that ISBNs with hyphens are accepted and normalized"""
        book_data = {
            "title": "ISBN Test",
            "author": "Test Author",
            "publication_year": 2024,
            "genre": "Test",
            "isbn": "978-1-234-56789-0",
            "description": "Test"
        }
        
        response = client.post("/books", json=book_data)
        assert response.status_code == 201
        
        # ISBN should be normalized (no hyphens)
        data = response.json()
        assert data["isbn"] == "9781234567890"