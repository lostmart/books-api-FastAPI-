from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI(
    title="Books API",
    description="A simple REST API for managing books",
    version="0.1.0"
)

# Hardcoded data - our "database" for now
BOOKS = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "publication_year": 1949,
        "genre": "Dystopian Fiction"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publication_year": 1960,
        "genre": "Southern Gothic"
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publication_year": 1925,
        "genre": "Literary Fiction"
    }
]


@app.get("/")
def read_root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Books API",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/books")
def get_books():
    """Get all books"""
    return BOOKS


@app.get("/books/{book_id}")
def get_book(book_id: int):
    """Get a specific book by ID"""
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    
    # If not found, return a simple error
    return {"error": "Book not found"}