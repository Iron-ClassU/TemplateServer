import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.base import Base, get_session
from app.models.template import Template
from app.models.route import Route
from app.schemas.template import TemplateType

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for testing
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """Create tables for testing and drop them when done."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for testing."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture
async def client() -> AsyncClient:
    """Get async test client."""
    return AsyncClient(app=app, base_url="http://test")

@pytest.fixture
def sync_client() -> Generator[TestClient, None, None]:
    """Get sync test client."""
    with TestClient(app) as client:
        yield client

# Override the get_session dependency
@pytest.fixture
async def override_get_session(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Override the get_session dependency for testing."""
    async def get_session_override():
        yield db_session

    app.dependency_overrides[get_session] = get_session_override
    yield db_session
    app.dependency_overrides.pop(get_session, None)

@pytest.fixture
async def sample_template(db_session: AsyncSession) -> Template:
    """Create a sample template for testing."""
    template = Template(
        name="Test Template",
        description="A test template",
        html_content="<html><body><h1>{{ title }}</h1></body></html>",
        css_content="h1 { color: blue; }",
        js_content="console.log('Hello');",
        config={"test": True},
        type=TemplateType.DASHBOARD,
        status=TemplateStatus.DRAFT
    )
    db_session.add(template)
    await db_session.commit()
    await db_session.refresh(template)
    return template

@pytest.fixture
async def sample_route(db_session: AsyncSession, sample_template: Template) -> Route:
    """Create a sample route for testing."""
    route = Route(
        path="/test",
        template_id=sample_template.id,
        method="GET",
        handler_config={"title": "Test Page"}
    )
    db_session.add(route)
    await db_session.commit()
    await db_session.refresh(route)
    return route 