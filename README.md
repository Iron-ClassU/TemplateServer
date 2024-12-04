# Dashboard Generator

A FastAPI-based dynamic dashboard generator with template management system, providing a flexible and powerful way to create, manage, and serve dynamic dashboards.

## Features

### Template Management
- Create and manage dashboard templates
- Support for HTML, CSS, and JavaScript content
- Template versioning and inheritance
- Template validation and preview
- Template status management (draft/published/archived)

### Dynamic Routing
- Dynamic route creation and management
- Route-template binding
- Route validation and status management
- Bulk route operations

### Data Integration
- Multiple data source types support:
  - REST API
  - Database
  - File
  - Static data
- Data transformation capabilities
- Scheduled data synchronization
- Data source validation

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite (with async support)
- **ORM**: SQLAlchemy (async)
- **Migration**: Alembic
- **Template Engine**: Jinja2
- **Data Validation**: Pydantic
- **Testing**: Pytest

## Project Structure

```
app/
├── api/                 # API endpoints
│   └── v1/
│       └── endpoints/   # API v1 endpoints
├── core/               # Core configuration
├── models/             # SQLAlchemy models
├── schemas/            # Pydantic schemas
├── services/           # Business logic
├── templates/          # Jinja2 templates
└── static/            # Static files

tests/
├── unit/              # Unit tests
└── integration/       # Integration tests
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
alembic upgrade head
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### Templates
- `POST /api/v1/templates/` - Create template
- `GET /api/v1/templates/` - List templates
- `GET /api/v1/templates/{id}` - Get template
- `PUT /api/v1/templates/{id}` - Update template
- `DELETE /api/v1/templates/{id}` - Delete template
- `POST /api/v1/templates/{id}/validate` - Validate template
- `POST /api/v1/templates/{id}/render` - Render template

#### Routes
- `POST /api/v1/routes/` - Create route
- `GET /api/v1/routes/` - List routes
- `GET /api/v1/routes/{id}` - Get route
- `PUT /api/v1/routes/{id}` - Update route
- `DELETE /api/v1/routes/{id}` - Delete route
- `POST /api/v1/routes/{id}/validate` - Validate route

#### Data Sources
- `POST /api/v1/data/sources/` - Create data source
- `GET /api/v1/data/sources/` - List data sources
- `GET /api/v1/data/sources/{id}` - Get data source
- `PUT /api/v1/data/sources/{id}` - Update data source
- `DELETE /api/v1/data/sources/{id}` - Delete data source
- `POST /api/v1/data/sources/{id}/validate` - Validate data source
- `POST /api/v1/data/sources/{id}/query` - Query data source
- `POST /api/v1/data/sources/{id}/sync` - Sync data source

## Development

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test category:
```bash
pytest tests/unit/  # Run unit tests
pytest tests/integration/  # Run integration tests
```

### Code Style

This project follows PEP 8 style guide. Key points:
- Use 4 spaces for indentation
- Maximum line length of 88 characters
- Use type hints for function arguments and return values
- Document classes and functions using docstrings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 