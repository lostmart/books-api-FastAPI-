from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from app.schemas.book import BookCreate, BookResponse

# Create the FastAPI application instance
app = FastAPI(
    title="Books API",
    description="A simple REST API for managing books",
    version="0.2.0"
)

# Hardcoded data - now with timestamps and more fields
BOOKS = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "publication_year": 1949,
        "genre": "Dystopian Fiction",
        "isbn": "978-0451524935",
        "description": "A dystopian social science fiction novel and cautionary tale",
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
        "updated_at": datetime(2024, 1, 1, 12, 0, 0)
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publication_year": 1960,
        "genre": "Southern Gothic",
        "isbn": "978-0061120084",
        "description": "A novel about racial injustice in the American South",
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
        "updated_at": datetime(2024, 1, 1, 12, 0, 0)
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publication_year": 1925,
        "genre": "Literary Fiction",
        "isbn": "978-0743273565",
        "description": "A tragic story of Jay Gatsby and his unrequited love",
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
        "updated_at": datetime(2024, 1, 1, 12, 0, 0)
    }
]

# Counter for generating IDs
next_id = 4


@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Books API",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/books", response_model=list[BookResponse])
def get_books():
    """
    Get all books
    
    Returns a list of all books in the system.
    """
    return BOOKS


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    """
    Get a specific book by ID
    
    - **book_id**: The ID of the book to retrieve
    """
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    
    # Proper error response with 404 status
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {book_id} not found"
    )


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    """
    Create a new book
    
    - **title**: Book title (required)
    - **author**: Book author (required)
    - **publication_year**: Year published (required, 1000-2100)
    - **genre**: Book genre (required)
    - **isbn**: ISBN number (optional)
    - **description**: Book description (optional)
    """
    global next_id
    
    # Check if ISBN already exists
    if book.isbn:
        for existing_book in BOOKS:
            if existing_book.get("isbn") == book.isbn:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Book with ISBN {book.isbn} already exists"
                )
    
    # Create new book with generated ID and timestamps
    now = datetime.now()
    new_book = {
        "id": next_id,
        **book.model_dump(),  # Convert Pydantic model to dict
        "created_at": now,
        "updated_at": now
    }
    
    BOOKS.append(new_book)
    next_id += 1
    
    return new_book