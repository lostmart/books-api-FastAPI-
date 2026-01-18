
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
├── requirements.txt
└── README.md
```
