# Development Guide

## Environment Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- git

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd dashboard_generator
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Development Workflow

### Code Organization

The project follows a modular structure:

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
```

### Adding New Features

1. Create new models in `app/models/`
2. Define schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/api/v1/endpoints/`
5. Add tests in `tests/`

### Database Management

#### Creating Migrations

When you make changes to models:

```bash
alembic revision --autogenerate -m "description"
```

Review the generated migration in `alembic/versions/` before applying.

#### Applying Migrations

```bash
alembic upgrade head  # Apply all migrations
alembic upgrade +1    # Apply next migration
alembic downgrade -1  # Rollback last migration
```

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_templates.py

# Run with coverage
pytest --cov=app tests/
```

#### Writing Tests

1. Unit Tests (`tests/unit/`):
   - Test individual components
   - Mock external dependencies
   - Focus on business logic

2. Integration Tests (`tests/integration/`):
   - Test component interactions
   - Use test database
   - Test API endpoints

Example test:
```python
import pytest
from app.services.template_service import TemplateService

async def test_create_template(db_session):
    service = TemplateService(db_session)
    template = await service.create_template(
        name="Test Template",
        html_content="<h1>Test</h1>"
    )
    assert template.name == "Test Template"
```

### Code Style

#### Python Style Guide

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use type hints
- Write docstrings for classes and functions

Example:
```python
from typing import Optional

def calculate_total(x: int, y: int, z: Optional[int] = None) -> int:
    """Calculate the sum of two or three numbers.

    Args:
        x: First number
        y: Second number
        z: Optional third number

    Returns:
        The sum of the input numbers
    """
    return x + y + (z or 0)
```

#### Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

Example:
```python
import os
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.template_service import TemplateService
```

### Documentation

#### Code Documentation

- Use docstrings for modules, classes, and functions
- Include type hints
- Document exceptions and return values
- Add comments for complex logic

#### API Documentation

- Document all API endpoints
- Include request/response examples
- Document error responses
- Keep OpenAPI schema up to date

### Error Handling

- Use custom exceptions for business logic
- Handle expected errors gracefully
- Log unexpected errors
- Return appropriate HTTP status codes

Example:
```python
from fastapi import HTTPException

async def get_template(template_id: int):
    template = await db.get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Template {template_id} not found"
        )
    return template
```

## Deployment

### Building for Production

1. Install production dependencies:
```bash
pip install -r requirements.txt
```

2. Set production environment variables:
```bash
export ENVIRONMENT=production
export DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

3. Apply database migrations:
```bash
alembic upgrade head
```

### Running in Production

Using uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Using gunicorn with uvicorn workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
``` 