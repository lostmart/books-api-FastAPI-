from typing import Optional
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate
from app.models.book import Book
from app.exceptions import (
    BookNotFoundError,
    BookAlreadyExistsError,
    ISBNAlreadyExistsError
)


class BookService:
    """
    Service layer for book business logic.
    
    Handles business rules, validation, and orchestrates
    repository operations. Sits between endpoints and repositories.
    """
    
    def __init__(self, repository: BookRepository):
        """
        Initialize service with a repository.
        
        Args:
            repository: BookRepository instance for data access
        """
        self.repository = repository
    
    def get_all_books(self) -> list[Book]:
        """
        Get all books.
        
        Returns:
            List of all books
        """
        return self.repository.get_all()
    
    def get_book_by_id(self, book_id: int) -> Book:
        """
        Get a book by ID.
        
        Args:
            book_id: ID of the book to retrieve
            
        Returns:
            Book object
            
        Raises:
            BookNotFoundError: If book doesn't exist
        """
        book = self.repository.get_by_id(book_id)
        
        if book is None:
            raise BookNotFoundError(book_id)
        
        return book
    
    def create_book(self, book_data: BookCreate) -> Book:
        """
        Create a new book.
        
        Business rules:
        - ISBN must be unique (if provided)
        
        Args:
            book_data: Book data to create
            
        Returns:
            Created book
            
        Raises:
            BookAlreadyExistsError: If ISBN already exists
        """
        # Business rule: Check for duplicate ISBN
        if book_data.isbn:
            existing_book = self.repository.get_by_isbn(book_data.isbn)
            if existing_book:
                raise BookAlreadyExistsError(book_data.isbn)
        
        # Delegate to repository for data access
        return self.repository.create(book_data)
    
    def update_book(self, book_id: int, book_data: BookCreate) -> Book:
        """
        Update an existing book.
        
        Business rules:
        - Book must exist
        - ISBN must be unique (if changed)
        
        Args:
            book_id: ID of book to update
            book_data: New book data
            
        Returns:
            Updated book
            
        Raises:
            BookNotFoundError: If book doesn't exist
            ISBNAlreadyExistsError: If new ISBN already exists
        """
    # Business rule: Ensure book exists
        existing_book = self.repository.get_by_id(book_id)
        if existing_book is None:
            raise BookNotFoundError(book_id)
        
        # Business rule: Check if new ISBN conflicts with another book
        if book_data.isbn:
            book_with_isbn = self.repository.get_by_isbn(book_data.isbn)
            if book_with_isbn and book_with_isbn.id != book_id:
                raise ISBNAlreadyExistsError(book_data.isbn)
        
        # Delegate to repository for data access
        updated_book = self.repository.update(book_id, book_data)
        
        # This shouldn't happen since we checked existence above,
        # but handle it for type safety
        if updated_book is None:
            raise BookNotFoundError(book_id)
        
        return updated_book
    
    def delete_book(self, book_id: int) -> None:
        """
        Delete a book.
        
        Business rules:
        - Book must exist
        
        Args:
            book_id: ID of book to delete
            
        Raises:
            BookNotFoundError: If book doesn't exist
        """
        # Business rule: Ensure book exists before deleting
        success = self.repository.delete(book_id)
        
        if not success:
            raise BookNotFoundError(book_id)