"""
Pytest configuration and fixtures.

Fixtures are reusable test setup code that pytest automatically
provides to test functions that request them.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

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
    
    # Override the get_db dependency to use our test database
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


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