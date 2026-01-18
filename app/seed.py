"""
Database seeding script to populate initial data.

Run this script to add sample books to the database:
    python -m app.seed
"""

from datetime import datetime
from app.database import SessionLocal, engine, Base
from app.models.book import Book


def seed_books():
    """Add sample books to the database"""
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if books already exist
        existing_count = db.query(Book).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} books. Skipping seed.")
            return
        
        # Sample books to add
        sample_books = [
            Book(
                title="1984",
                author="George Orwell",
                publication_year=1949,
                genre="Dystopian Fiction",
                isbn="9780451524935",
                description="A dystopian social science fiction novel and cautionary tale"
            ),
            Book(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                publication_year=1960,
                genre="Southern Gothic",
                isbn="9780061120084",
                description="A novel about racial injustice in the American South"
            ),
            Book(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                publication_year=1925,
                genre="Literary Fiction",
                isbn="9780743273565",
                description="A tragic story of Jay Gatsby and his unrequited love"
            ),
            Book(
                title="The Hobbit",
                author="J.R.R. Tolkien",
                publication_year=1937,
                genre="Fantasy",
                isbn="9780547928227",
                description="A fantasy novel about Bilbo Baggins' adventure"
            ),
            Book(
                title="Harry Potter and the Philosopher's Stone",
                author="J.K. Rowling",
                publication_year=1997,
                genre="Fantasy",
                isbn="9780439708180",
                description="A young wizard's journey begins at Hogwarts"
            )
        ]
        
        # Add all books to the session
        db.add_all(sample_books)
        
        # Commit the transaction
        db.commit()
        
        print(f"✅ Successfully seeded {len(sample_books)} books!")
        
        # Display what was added
        for book in sample_books:
            print(f"  - {book.title} by {book.author}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding database...")
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    # Seed the data
    seed_books()