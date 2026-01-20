"""
Pytest configuration and fixtures.

Fixtures are reusable test setup code that pytest automatically
provides to test functions that request them.
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends, HTTPException, status

from app.database import Base, get_db
from app.main import app
from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService


# Set testing environment variable
os.environ["TESTING"] = "1"


# Create in-memory SQLite database for testing
import tempfile
import os

# Create a temporary file for the test database to ensure shared state
temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
temp_db.close()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{temp_db.name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """
    Provides a clean database session for each test.
    
    Creates all tables before the test, drops them after.
    Each test gets a fresh, isolated database.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def book_repository(db_session):
    """
    Provides a BookRepository instance with a test database session.
    """
    return BookRepository(db_session)


@pytest.fixture
def book_service(book_repository):
    """
    Provides a BookService instance with a test repository.
    """
    return BookService(book_repository)


@pytest.fixture
def client():
    """
    Provides a FastAPI TestClient with a test database.
    
    This allows testing HTTP endpoints without running a server.
    """
    # Create tables before client is used
    Base.metadata.create_all(bind=engine)
    
    # Create a test app without lifespan handler to avoid conflicts
    test_app = FastAPI(
        title="Books API",
        description="A simple REST API for managing books with clean architecture",
        version="0.5.0"
    )
    
    # Create test-specific dependency that yields a session
    def get_test_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def get_test_book_service(db = Depends(get_test_db)):
        repository = BookRepository(db)
        return BookService(repository)
    
    # Copy routes from main app
    from app.schemas.book import BookCreate, BookResponse
    from app.exceptions import BookNotFoundError, BookAlreadyExistsError, ISBNAlreadyExistsError
    
    @test_app.get("/")
    def read_root():
        """Root endpoint - health check"""
        return {
            "message": "Welcome to Books API",
            "docs": "/docs",
            "status": "running",
            "version": "0.5.0"
        }

    @test_app.get("/books", response_model=list[BookResponse])
    def get_books(service = Depends(get_test_book_service)):
        """
        Get all books from the database.
        
        - **service**: Book service (injected automatically)
        """
        return service.get_all_books()

    @test_app.get("/books/{book_id}", response_model=BookResponse)
    def get_book(book_id: int, service = Depends(get_test_book_service)):
        """
        Get a specific book by ID.
        
        - **book_id**: The ID of the book to retrieve
        - **service**: Book service (injected automatically)
        """
        try:
            return service.get_book_by_id(book_id)
        except BookNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

    @test_app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
    def create_book(book: BookCreate, service = Depends(get_test_book_service)):
        """
        Create a new book in the database.
        
        - **book**: Book data to create
        - **service**: Book service (injected automatically)
        """
        try:
            return service.create_book(book)
        except BookAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )

    @test_app.put("/books/{book_id}", response_model=BookResponse)
    def update_book(
        book_id: int,
        book: BookCreate,
        service = Depends(get_test_book_service)
    ):
        """
        Update an existing book.
        
        - **book_id**: ID of the book to update
        - **book**: New book data
        - **service**: Book service (injected automatically)
        """
        try:
            return service.update_book(book_id, book)
        except BookNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        except ISBNAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )

    @test_app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_book(book_id: int, service = Depends(get_test_book_service)):
        """
        Delete a book from the database.
        
        - **book_id**: ID of the book to delete
        - **service**: Book service (injected automatically)
        """
        try:
            service.delete_book(book_id)
            return None
        except BookNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
    
    with TestClient(test_app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    # Clean up the temporary database file
    try:
        os.unlink(temp_db.name)
    except:
        pass


@pytest.fixture
def sample_book_data():
    """
    Provides sample book data for testing.
    """
    return {
        "title": "Test Book",
        "author": "Test Author",
        "publication_year": 2024,
        "genre": "Test Genre",
        "isbn": "9781234567890",
        "description": "A test book description"
    }