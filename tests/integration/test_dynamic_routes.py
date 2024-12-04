import pytest
from httpx import AsyncClient
from bs4 import BeautifulSoup

from app.models.template import Template
from app.models.route import Route

pytestmark = pytest.mark.asyncio

async def test_render_dynamic_route(
    client: AsyncClient,
    sample_template: Template,
    sample_route: Route
):
    """Test rendering a dynamic route with template"""
    response = await client.get("/test")
    assert response.status_code == 200
    
    # Parse HTML and check content
    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.h1.text == "Test Page"
    
    # Check if CSS and JS are injected
    assert "color: blue;" in response.text
    assert "console.log('Hello');" in response.text

async def test_nonexistent_route(client: AsyncClient):
    """Test accessing a route that doesn't exist"""
    response = await client.get("/nonexistent")
    assert response.status_code == 404

async def test_inactive_route(
    client: AsyncClient,
    db_session,
    sample_template: Template,
    sample_route: Route
):
    """Test accessing an inactive route"""
    # Deactivate the route
    sample_route.is_active = False
    db_session.add(sample_route)
    await db_session.commit()
    
    response = await client.get("/test")
    assert response.status_code == 404

async def test_inactive_template(
    client: AsyncClient,
    db_session,
    sample_template: Template,
    sample_route: Route
):
    """Test accessing a route with inactive template"""
    # Deactivate the template
    sample_template.is_active = False
    db_session.add(sample_template)
    await db_session.commit()
    
    response = await client.get("/test")
    assert response.status_code == 404

async def test_template_with_invalid_html(
    client: AsyncClient,
    db_session,
    sample_template: Template,
    sample_route: Route
):
    """Test rendering a template with invalid HTML"""
    # Update template with invalid Jinja2 syntax
    sample_template.html_content = "<html>{{ invalid syntax }}</html>"
    db_session.add(sample_template)
    await db_session.commit()
    
    response = await client.get("/test")
    assert response.status_code == 500
    assert "Template rendering error" in response.json()["detail"]

async def test_template_with_complex_data(
    client: AsyncClient,
    db_session,
    sample_template: Template,
    sample_route: Route
):
    """Test rendering a template with complex data structure"""
    # Update template and route with complex data
    sample_template.html_content = """
        <html>
            <body>
                <h1>{{ config.title }}</h1>
                <ul>
                {% for item in config.items %}
                    <li>{{ item.name }}: {{ item.value }}</li>
                {% endfor %}
                </ul>
            </body>
        </html>
    """
    sample_route.handler_config = {
        "title": "Complex Test",
        "items": [
            {"name": "Item 1", "value": "Value 1"},
            {"name": "Item 2", "value": "Value 2"}
        ]
    }
    db_session.add(sample_template)
    db_session.add(sample_route)
    await db_session.commit()
    
    response = await client.get("/test")
    assert response.status_code == 200
    
    # Parse and check complex HTML structure
    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.h1.text == "Complex Test"
    items = soup.find_all("li")
    assert len(items) == 2
    assert "Item 1: Value 1" in items[0].text
    assert "Item 2: Value 2" in items[1].text 