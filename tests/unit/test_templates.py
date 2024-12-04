import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template import Template
from app.schemas.template import TemplateType, TemplateStatus

pytestmark = pytest.mark.asyncio

async def test_create_template(client: AsyncClient, override_get_session):
    """Test creating a new template"""
    response = await client.post(
        "/api/v1/templates/",
        json={
            "name": "New Template",
            "description": "A new test template",
            "html_content": "<html><body>Test</body></html>",
            "css_content": "body { color: black; }",
            "js_content": "console.log('test');",
            "config": {"test": True},
            "type": "DASHBOARD",
            "status": "DRAFT"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Template"

async def test_get_template(client: AsyncClient, sample_template: Template, override_get_session):
    """Test getting a specific template"""
    response = await client.get(f"/api/v1/templates/{sample_template.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_template.name

async def test_list_templates(client: AsyncClient, sample_template: Template, override_get_session):
    """Test listing all templates"""
    response = await client.get("/api/v1/templates/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

async def test_update_template(client: AsyncClient, sample_template: Template, override_get_session):
    """Test updating a template"""
    response = await client.put(
        f"/api/v1/templates/{sample_template.id}",
        json={
            "name": "Updated Template",
            "html_content": "<html><body>Updated</body></html>"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Template"

async def test_delete_template(client: AsyncClient, sample_template: Template, override_get_session):
    """Test deleting a template"""
    response = await client.delete(f"/api/v1/templates/{sample_template.id}")
    assert response.status_code == 200

async def test_create_template_invalid_data(client: AsyncClient, override_get_session):
    """Test creating a template with invalid data"""
    response = await client.post(
        "/api/v1/templates/",
        json={
            "name": "",  # Invalid: empty name
            "html_content": "<html><body>Test</body></html>"
        }
    )
    assert response.status_code == 422

async def test_update_nonexistent_template(client: AsyncClient, override_get_session):
    """Test updating a template that doesn't exist"""
    response = await client.put(
        "/api/v1/templates/999999",
        json={
            "name": "Updated Template",
            "html_content": "<html><body>Updated</body></html>"
        }
    )
    assert response.status_code == 404

async def test_template_name_unique_constraint(
    client: AsyncClient, sample_template: Template, override_get_session
):
    """Test that template names must be unique"""
    response = await client.post(
        "/api/v1/templates/",
        json={
            "name": sample_template.name,  # Using existing name
            "html_content": "<html><body>Test</body></html>",
            "type": "DASHBOARD",
            "status": "DRAFT"
        }
    )
    assert response.status_code == 400  # Bad request due to duplicate name