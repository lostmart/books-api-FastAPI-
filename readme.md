# Books REST API

A production-ready REST API for managing books, built with **FastAPI** and following clean architecture principles.

## 🚀 Features

- **Full CRUD Operations** - Create, Read, Update, and Delete books
- **Clean Architecture** - Three-layer architecture (Router → Service → Repository)
- **Data Validation** - Automatic validation with Pydantic
- **Type Safety** - Full type hints throughout the codebase
- **Database ORM** - SQLAlchemy for database operations
- **Comprehensive Testing** - Unit and integration tests with pytest
- **Auto-generated Docs** - Interactive API documentation with Swagger UI
- **ISBN Normalization** - Automatically handles ISBNs with or without hyphens

## 📋 Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Key Patterns

1. Dependency Injection: FastAPI's Depends() for clean service/repository instantiation
2. Repository Pattern: Abstract database operations behind an interface
3. DTO Pattern: Separate schemas for requests, responses, and database models
4. Error Handling: Custom exceptions that map to HTTP status codes

## folder

```text
books-api/
├── app/
│ ├── **init**.py
│ ├── main.py # FastAPI app initialization
│ ├── config.py # Configuration management
│ ├── models/
│ │ ├── **init**.py
│ │ └── book.py # SQLAlchemy models
│ ├── schemas/
│ │ ├── **init**.py
│ │ └── book.py # Pydantic schemas
│ ├── repositories/
│ │ ├── **init**.py
│ │ └── book_repository.py
│ ├── services/
│ │ ├── **init**.py
│ │ └── book_service.py
│ └── routers/
│ ├── **init**.py
│ └── books.py # API endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_services.py
├── requirements.txt
└── README.md
```
