from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Book(Base):
    """
    SQLAlchemy model representing the books table in the database.
    
    This is different from the Pydantic schemas:
    - This defines the database table structure
    - Pydantic schemas define API request/response structure
    """
    __tablename__ = "books"
    
    # Primary key - auto-incrementing
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Book information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # ISBN - unique constraint ensures no duplicates
    # nullable=True means it's optional
    isbn: Mapped[str | None] = mapped_column(String(13), unique=True, nullable=True)
    
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Timestamps - automatically managed
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now, 
        onupdate=datetime.now,
        nullable=False
    )
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"