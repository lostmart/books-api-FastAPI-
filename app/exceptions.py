"""
Custom exceptions for the application.

These represent business-level errors, separate from HTTP concerns.
"""


class BookNotFoundError(Exception):
    """Raised when a book is not found in the database"""
    def __init__(self, book_id: int):
        self.book_id = book_id
        super().__init__(f"Book with id {book_id} not found")


class BookAlreadyExistsError(Exception):
    """Raised when attempting to create a book with a duplicate ISBN"""
    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Book with ISBN {isbn} already exists")


class ISBNAlreadyExistsError(Exception):
    """Raised when attempting to update a book to an ISBN that already exists"""
    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Another book with ISBN {isbn} already exists")