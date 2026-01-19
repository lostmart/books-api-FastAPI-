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

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/books-api.git
cd books-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows (Git Bash):**

```bash
source venv/Scripts/activate
```

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -e .
```

### 5. (Optional) Install test dependencies

```bash
pip install -e ".[test]"
```

## 🏃 Running the Application

### Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- **API**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

### Seed the database (optional)

Populate the database with sample books:

```bash
python -m app.seed
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run with coverage report
pytest --cov=app --cov-report=html
```

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

## 🔌 API Endpoints

### Books

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/`           | Health check        |
| GET    | `/books`      | Get all books       |
| GET    | `/books/{id}` | Get a specific book |
| POST   | `/books`      | Create a new book   |
| PUT    | `/books/{id}` | Update a book       |
| DELETE | `/books/{id}` | Delete a book       |

## 🏗️ Architecture

This project follows a **three-layer architecture**:

### 1. **Router Layer** (`main.py`)

- Handles HTTP requests and responses
- Converts between HTTP and domain objects
- Manages status codes and error responses

### 2. **Service Layer** (`services/`)

- Contains business logic and validation rules
- Enforces domain rules (e.g., unique ISBNs)
- Raises domain-specific exceptions

### 3. **Repository Layer** (`repositories/`)

- Manages data access and persistence
- Abstracts database operations
- Provides a clean interface for data manipulation

### Design Patterns Used

- **Repository Pattern** - Abstracts data access
- **Dependency Injection** - Manages object dependencies
- **Service Layer Pattern** - Encapsulates business logic
- **DTO Pattern** - Pydantic schemas as Data Transfer Objects

## 📚 Book Schema

### Request Body (Create/Update)

```json
{
	"title": "string (required, 1-200 chars)",
	"author": "string (required, 1-100 chars)",
	"publication_year": "integer (required, 1000-2100)",
	"genre": "string (required, 1-50 chars)",
	"isbn": "string (optional, 10 or 13 digits)",
	"description": "string (optional, max 1000 chars)"
}
```

### Response Body

```json
{
	"id": "integer",
	"title": "string",
	"author": "string",
	"publication_year": "integer",
	"genre": "string",
	"isbn": "string or null",
	"description": "string or null",
	"created_at": "datetime",
	"updated_at": "datetime"
}
```

## 🔍 Key Features Explained

### ISBN Normalization

ISBNs can be submitted with or without hyphens:

- Input: `978-0-451-52493-5`
- Stored as: `9780451524935`

This is handled automatically by a Pydantic field validator.

### Automatic Validation

Pydantic automatically validates:

- Required fields are present
- Data types are correct
- Values are within specified ranges
- Custom validation rules (e.g., ISBN format)

### Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET/PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Duplicate ISBN
- `422 Unprocessable Entity` - Validation error

## 🧩 Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[SQLite](https://www.sqlite.org/)** - Lightweight database (easily switchable to PostgreSQL/MySQL)
- **[pytest](https://pytest.org/)** - Testing framework
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server

## 🚧 Future Enhancements

- [ ] Add pagination for GET `/books`
- [ ] Add filtering (by author, genre, year)
- [ ] Add authentication (JWT tokens)
- [ ] Add user management
- [ ] Implement PATCH for partial updates
- [ ] Add database migrations (Alembic)
- [ ] Add caching (Redis)
- [ ] Add rate limiting
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**

- GitHub: [@lostmart](https://github.com/lostmart)
- LinkedIn: [Martin P](https://www.linkedin.com/in/martin-pedraza-dev)

## 🙏 Acknowledgments

- Built following clean architecture principles
- Inspired by best practices in REST API design
- FastAPI documentation and community

---

**⭐ If you found this project helpful, please give it a star!**
