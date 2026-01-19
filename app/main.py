from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.schemas.book import BookCreate, BookResponse
from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService
from app.exceptions import (
    BookNotFoundError,
    BookAlreadyExistsError,
    ISBNAlreadyExistsError
)

# Create the FastAPI application instance
app = FastAPI(
    title="Books API",
    description="A simple REST API for managing books with clean architecture",
    version="0.5.0"
)


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Create all database tables when the application starts"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


# Dependency to get book service
def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """
    Dependency that provides a BookService instance.
    
    Creates the full dependency chain:
    Session → Repository → Service
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        BookService instance
    """
    repository = BookRepository(db)
    return BookService(repository)


@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Books API",
        "docs": "/docs",
        "status": "running",
        "version": "0.5.0"
    }


@app.get("/books", response_model=list[BookResponse])
def get_books(service: BookService = Depends(get_book_service)):
    """
    Get all books from the database.
    
    - **service**: Book service (injected automatically)
    """
    return service.get_all_books()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, service: BookService = Depends(get_book_service)):
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


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
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


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookCreate,
    service: BookService = Depends(get_book_service)
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


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
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