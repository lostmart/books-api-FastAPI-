from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.schemas.book import BookCreate, BookResponse
from app.repositories.book_repository import BookRepository

# Create the FastAPI application instance
app = FastAPI(
    title="Books API",
    description="A simple REST API for managing books with repository pattern",
    version="0.4.0"
)


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Create all database tables when the application starts"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


# Dependency to get book repository
def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    """
    Dependency that provides a BookRepository instance.
    
    Args:
        db: Database session (injected by FastAPI)
        
    Returns:
        BookRepository instance
    """
    return BookRepository(db)


@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Books API",
        "docs": "/docs",
        "status": "running",
        "version": "0.4.0"
    }


@app.get("/books", response_model=list[BookResponse])
def get_books(repo: BookRepository = Depends(get_book_repository)):
    """
    Get all books from the database.
    
    - **repo**: Book repository (injected automatically)
    """
    return repo.get_all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, repo: BookRepository = Depends(get_book_repository)):
    """
    Get a specific book by ID.
    
    - **book_id**: The ID of the book to retrieve
    - **repo**: Book repository (injected automatically)
    """
    book = repo.get_by_id(book_id)
    
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    return book


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, repo: BookRepository = Depends(get_book_repository)):
    """
    Create a new book in the database.
    
    - **book**: Book data to create
    - **repo**: Book repository (injected automatically)
    """
    # Check if ISBN already exists
    if book.isbn:
        existing_book = repo.get_by_isbn(book.isbn)
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ISBN {book.isbn} already exists"
            )
    
    return repo.create(book)


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookCreate,
    repo: BookRepository = Depends(get_book_repository)
):
    """
    Update an existing book.
    
    - **book_id**: ID of the book to update
    - **book**: New book data
    - **repo**: Book repository (injected automatically)
    """
    # Check if updating ISBN to one that already exists
    if book.isbn:
        existing_book = repo.get_by_isbn(book.isbn)
        # If ISBN exists and belongs to a different book
        if existing_book and existing_book.id != book_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ISBN {book.isbn} already exists"
            )
    
    updated_book = repo.update(book_id, book)
    
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    return updated_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, repo: BookRepository = Depends(get_book_repository)):
    """
    Delete a book from the database.
    
    - **book_id**: ID of the book to delete
    - **repo**: Book repository (injected automatically)
    """
    success = repo.delete(book_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    # 204 No Content - successful deletion returns nothing
    return None