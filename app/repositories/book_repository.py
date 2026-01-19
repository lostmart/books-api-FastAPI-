from typing import Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate


class BookRepository:
    """
    Repository for Book database operations.
    
    Encapsulates all database queries related to books,
    providing a clean interface for data access.
    """
    
    def __init__(self, db: Session):
        """
        Initialize repository with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_all(self) -> list[Book]:
        """
        Get all books from the database.
        
        Returns:
            List of all Book objects
        """
        return self.db.query(Book).all()
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """
        Get a single book by its ID.
        
        Args:
            book_id: The ID of the book to retrieve
            
        Returns:
            Book object if found, None otherwise
        """
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        Get a book by its ISBN.
        
        Args:
            isbn: The ISBN to search for
            
        Returns:
            Book object if found, None otherwise
        """
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def create(self, book_data: BookCreate) -> Book:
        """
        Create a new book in the database.
        
        Args:
            book_data: Pydantic model with book data
            
        Returns:
            The created Book object with generated ID and timestamps
        """
        # Convert Pydantic model to dict and create SQLAlchemy model
        db_book = Book(**book_data.model_dump())
        
        # Add to session and commit
        self.db.add(db_book)
        self.db.commit()
        
        # Refresh to get generated values (id, timestamps)
        self.db.refresh(db_book)
        
        return db_book
    
    def update(self, book_id: int, book_data: BookCreate) -> Optional[Book]:
        """
        Update an existing book.
        
        Args:
            book_id: ID of the book to update
            book_data: New book data
            
        Returns:
            Updated Book object if found, None otherwise
        """
        # Get existing book
        db_book = self.get_by_id(book_id)
        
        if db_book is None:
            return None
        
        # Update fields from Pydantic model
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        # Commit changes
        self.db.commit()
        self.db.refresh(db_book)
        
        return db_book
    
    def delete(self, book_id: int) -> bool:
        """
        Delete a book from the database.
        
        Args:
            book_id: ID of the book to delete
            
        Returns:
            True if book was deleted, False if not found
        """
        db_book = self.get_by_id(book_id)
        
        if db_book is None:
            return False
        
        self.db.delete(db_book)
        self.db.commit()
        
        return True