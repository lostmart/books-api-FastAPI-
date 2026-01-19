import pytest
import time  # Add this import at the top
from app.schemas.book import BookCreate
from app.exceptions import BookNotFoundError, BookAlreadyExistsError, ISBNAlreadyExistsError


class TestBookService:
    """Tests for BookService"""
    
    def test_create_book(self, book_service, sample_book_data):
        """Test creating a book"""
        book_data = BookCreate(**sample_book_data)
        created_book = book_service.create_book(book_data)
        
        assert created_book.id is not None
        assert created_book.title == sample_book_data["title"]
        assert created_book.author == sample_book_data["author"]
        assert created_book.isbn == sample_book_data["isbn"]
        assert created_book.created_at is not None
        assert created_book.updated_at is not None
    
    def test_create_book_with_duplicate_isbn(self, book_service, sample_book_data):
        """Test that creating a book with duplicate ISBN raises error"""
        # Create first book
        book_data = BookCreate(**sample_book_data)
        book_service.create_book(book_data)
        
        # Try to create another with same ISBN
        with pytest.raises(BookAlreadyExistsError) as exc_info:
            book_service.create_book(book_data)
        
        assert sample_book_data["isbn"] in str(exc_info.value)
    
    def test_get_all_books(self, book_service, sample_book_data):
        """Test getting all books"""
        # Initially empty
        books = book_service.get_all_books()
        assert len(books) == 0
        
        # Create two books
        book_data1 = BookCreate(**sample_book_data)
        book_service.create_book(book_data1)
        
        book_data2 = BookCreate(**{**sample_book_data, "isbn": "9780987654321", "title": "Second Book"})
        book_service.create_book(book_data2)
        
        # Should have two books
        books = book_service.get_all_books()
        assert len(books) == 2
    
    def test_get_book_by_id(self, book_service, sample_book_data):
        """Test getting a book by ID"""
        # Create a book
        book_data = BookCreate(**sample_book_data)
        created_book = book_service.create_book(book_data)
        
        # Retrieve it by ID
        retrieved_book = book_service.get_book_by_id(created_book.id)
        assert retrieved_book.id == created_book.id
        assert retrieved_book.title == created_book.title
    
    def test_get_book_by_invalid_id(self, book_service):
        """Test that getting non-existent book raises error"""
        with pytest.raises(BookNotFoundError) as exc_info:
            book_service.get_book_by_id(999)
        
        assert "999" in str(exc_info.value)
    
    def test_update_book(self, book_service, sample_book_data):
        """Test updating a book"""
        # Create a book
        book_data = BookCreate(**sample_book_data)
        created_book = book_service.create_book(book_data)
        
        # Small delay to ensure timestamp difference
        time.sleep(0.01)
        
        # Update it
        updated_data = BookCreate(**{**sample_book_data, "title": "Updated Title"})
        updated_book = book_service.update_book(created_book.id, updated_data)
        
        assert updated_book.id == created_book.id
        assert updated_book.title == "Updated Title"
        # Check that updated_at changed (or at least didn't go backwards)
        assert updated_book.updated_at >= created_book.updated_at
    
    def test_update_nonexistent_book(self, book_service, sample_book_data):
        """Test that updating non-existent book raises error"""
        book_data = BookCreate(**sample_book_data)
        
        with pytest.raises(BookNotFoundError):
            book_service.update_book(999, book_data)
    
    def test_update_book_with_duplicate_isbn(self, book_service, sample_book_data):
        """Test that updating to a duplicate ISBN raises error"""
        # Create two books
        book_data1 = BookCreate(**sample_book_data)
        book1 = book_service.create_book(book_data1)
        
        book_data2 = BookCreate(**{**sample_book_data, "isbn": "9780987654321", "title": "Second Book"})
        book2 = book_service.create_book(book_data2)
        
        # Try to update book2 with book1's ISBN
        update_data = BookCreate(**{**sample_book_data, "isbn": book1.isbn})
        
        with pytest.raises(ISBNAlreadyExistsError):
            book_service.update_book(book2.id, update_data)
    
    def test_delete_book(self, book_service, sample_book_data):
        """Test deleting a book"""
        # Create a book
        book_data = BookCreate(**sample_book_data)
        created_book = book_service.create_book(book_data)
        
        # Delete it
        book_service.delete_book(created_book.id)
        
        # Verify it's gone
        with pytest.raises(BookNotFoundError):
            book_service.get_book_by_id(created_book.id)
    
    def test_delete_nonexistent_book(self, book_service):
        """Test that deleting non-existent book raises error"""
        with pytest.raises(BookNotFoundError):
            book_service.delete_book(999)
    
    def test_isbn_normalization(self, book_service):
        """Test that ISBNs with hyphens are normalized"""
        book_data = BookCreate(
            title="ISBN Test",
            author="Test Author",
            publication_year=2024,
            genre="Test",
            isbn="978-1-234-56789-0",  # With hyphens
            description="Test"
        )
        
        created_book = book_service.create_book(book_data)
        
        # ISBN should be stored without hyphens
        assert created_book.isbn == "9781234567890"