from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.schemas.book import BookCreate, BookResponse
from app.models.book import Book

# Create the FastAPI application instance
app = FastAPI(
    title="Books API",
    description="A simple REST API for managing books with database persistence",
    version="0.3.0"
)


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Create all database tables when the application starts"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Books API",
        "docs": "/docs",
        "status": "running",
        "version": "0.3.0"
    }


@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """
    Get all books from the database.
    
    - **db**: Database session (injected automatically)
    """
    books = db.query(Book).all()
    return books


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a specific book by ID from the database.
    
    - **book_id**: The ID of the book to retrieve
    - **db**: Database session (injected automatically)
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    
    return book


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book in the database.
    
    - **book**: Book data to create
    - **db**: Database session (injected automatically)
    """
    # Check if ISBN already exists
    if book.isbn:
        existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ISBN {book.isbn} already exists"
            )
    
    # Create new book instance (SQLAlchemy model)
    db_book = Book(**book.model_dump())
    
    # Add to database session
    db.add(db_book)
    
    # Commit the transaction (save to database)
    db.commit()
    
    # Refresh to get the generated ID and timestamps
    db.refresh(db_book)
    
    return db_book