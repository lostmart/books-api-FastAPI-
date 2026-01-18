from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    """Base schema with common book fields"""
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    publication_year: int = Field(..., ge=1000, le=2100)
    genre: str = Field(..., min_length=1, max_length=50)
    isbn: str | None = Field(None, description="ISBN-10 or ISBN-13 (without hyphens)")
    description: str | None = Field(None, max_length=1000)
    
    @field_validator('isbn', mode='before')
    @classmethod
    def normalize_isbn(cls, v: str | None) -> str | None:
        """
        Normalize ISBN by removing hyphens and spaces, then validate format.
        
        Accepts:
        - ISBN-10: 10 digits (e.g., "0451524935" or "0-451-52493-5")
        - ISBN-13: 13 digits (e.g., "9780451524935" or "978-0-451-52493-5")
        
        Returns the normalized ISBN (digits only) or None.
        """
        # If None or empty, return None
        if v is None or v == "":
            return None
        
        # Remove hyphens, spaces, and any other common separators
        normalized = v.replace('-', '').replace(' ', '').replace('.', '')
        
        # Validate it contains only digits
        if not normalized.isdigit():
            raise ValueError(
                f'ISBN must contain only digits (and optional hyphens/spaces). Got: {v}'
            )
        
        # Validate length (ISBN-10 or ISBN-13)
        if len(normalized) not in [10, 13]:
            raise ValueError(
                f'ISBN must be exactly 10 or 13 digits. Got {len(normalized)} digits: {normalized}'
            )
        
        return normalized


class BookCreate(BookBase):
    """Schema for creating a new book"""
    pass


class BookResponse(BookBase):
    """Schema for returning book data"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "1984",
                "author": "George Orwell",
                "publication_year": 1949,
                "genre": "Dystopian Fiction",
                "isbn": "9780451524935",  # Now without hyphens
                "description": "A dystopian social science fiction novel",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }
    }