from datetime import datetime
from typing import Any, Dict, List, Optional, cast

from fastapi.templating import Jinja2Templates
from jinja2 import Template as Jinja2Template
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.template import Template
from app.schemas.template import (
    TemplateConfig,
    TemplateCreate,
    TemplateStatus,
    TemplateType,
    TemplateUpdate,
)


class TemplateRenderError(Exception):
    """Template rendering error"""

    pass


class TemplateService:
    def __init__(self, session: Optional[AsyncSession] = None):
        if session is None:
            raise ValueError("Database session is required")
        self.session = session
        self.templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

    async def get_template_content(
        self, template_name: str, context: Dict[str, Any]
    ) -> str:
        """Render a template file from the templates directory."""
        try:
            request = context.get("request")
            if not request:
                raise ValueError("Request object is required")

            response = self.templates.TemplateResponse(
                name=template_name, context=context
            )
            return response.body.decode()
        except ValueError as ve:
            raise TemplateRenderError(f"Request error: {str(ve)}")
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template: {str(e)}")

    async def create_template(self, template: TemplateCreate) -> Template:
        """Create a new template."""
        if not self.session:
            raise ValueError("Database session required for this operation")

        try:
            db_template = Template(**template.model_dump())
            self.session.add(db_template)
            await self.session.commit()
            await self.session.refresh(db_template)
            return db_template
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Template with this name already exists")

    async def get_template(self, template_id: int) -> Optional[Template]:
        """Get a template by ID."""
        if not self.session:
            raise ValueError("Database session required for this operation")

        result = await self.session.execute(
            select(Template).where(Template.id == template_id)
        )
        return result.scalar_one_or_none()

    async def get_templates(
        self,
        skip: int = 0,
        limit: int = 100,
        type: Optional[TemplateType] = None,
        status: Optional[TemplateStatus] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Template]:
        """Get all templates with filtering and search."""
        query = select(Template)

        if type:
            query = query.where(Template.type == type)
        if status:
            query = query.where(Template.status == status)
        if tag:
            query = query.where(Template.tags.contains([tag]))
        if search:
            query = query.where(Template.name.ilike(f"%{search}%"))

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_template(
        self, template_id: int, template_update: TemplateUpdate
    ) -> Optional[Template]:
        """Update a template."""
        update_data = template_update.model_dump(exclude_unset=True)
        if not update_data:
            return None

        try:
            # Update the template
            await self.session.execute(
                update(Template)
                .where(Template.id == template_id)
                .values(**update_data, updated_at=datetime.utcnow())
            )
            await self.session.commit()

            # Get the updated template
            result = await self.session.execute(
                select(Template).where(Template.id == template_id)
            )
            return result.scalar_one_or_none()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Template name already exists")

    async def delete_template(self, template_id: int) -> bool:
        """Delete a template."""
        result = await self.session.execute(
            delete(Template).where(Template.id == template_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def validate_template(self, template: Template) -> Dict[str, Any]:
        """Validate template content and structure."""
        errors = []

        # Check HTML content
        if not template.html_content:
            errors.append("HTML content is required")

        # Basic HTML structure validation
        html_content = str(template.html_content) if template.html_content else ""
        if html_content and not (
            "<html" in html_content.lower() and "</html>" in html_content.lower()
        ):
            errors.append("Invalid HTML structure")

        # Check for basic Jinja2 syntax
        if html_content:
            try:
                from jinja2 import Environment

                env = Environment()
                # Convert SQLAlchemy Column to str explicitly
                template_str = str(html_content)
                env.parse(template_str)
            except Exception as e:
                errors.append(f"Invalid Jinja2 syntax: {str(e)}")

        return {"is_valid": len(errors) == 0, "errors": errors}

    async def render_preview(
        self, template: Template, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a preview of the template with sample data."""
        if context is None:
            context = {}

        try:
            # Convert SQLAlchemy Column to string
            html_content = str(template.html_content)
            jinja_template = Jinja2Template(html_content)
            return jinja_template.render(**context)
        except Exception as e:
            raise TemplateRenderError(f"Template rendering error: {str(e)}")

    async def clone_template(
        self, template_id: int, new_name: str
    ) -> Optional[Template]:
        """Clone an existing template."""
        original = await self.get_template(template_id)
        if not original:
            return None

        # Convert SQLAlchemy model attributes to appropriate types
        new_template = TemplateCreate(
            name=new_name,
            description=f"Clone of {str(original.name)}",
            html_content=str(original.html_content),
            css_content=str(original.css_content) if original.css_content else None,
            js_content=str(original.js_content) if original.js_content else None,
            config=cast(TemplateConfig, original.config) if original.config else None,
            tags=list(original.tags) if original.tags else None,
            status=TemplateStatus.DRAFT,
        )

        return await self.create_template(new_template)

    async def get_template_stats(self, template_id: int) -> Dict[str, Any]:
        """Get usage statistics for a template."""
        template = await self.get_template(template_id)
        if not template:
            raise ValueError("Template not found")

        # In a real implementation, this would query usage data
        return {
            "total_routes": len(template.routes),
            "active_routes": len([r for r in template.routes if r.is_active]),
            "last_used": datetime.utcnow(),  # Mock data
            "usage_count": 0,  # Mock data
            "avg_render_time": 0.1,  # Mock data
            "error_count": 0,  # Mock data
        }

    async def get_all_tags(self) -> List[str]:
        """Get all unique tags used in templates."""
        result = await self.session.execute(
            select(Template.tags).where(Template.tags.is_not(None)).distinct()
        )
        all_tags = result.scalars().all()
        # Flatten and deduplicate tags
        unique_tags = set()
        for tags in all_tags:
            if isinstance(tags, list):
                unique_tags.update(tags)
        return sorted(list(unique_tags))

    async def render_template(
        self,
        template_id: int,
        context: Dict[str, Any] | None = None,  # Use union type instead of Optional
    ) -> str:
        """Render a database template with the given context"""
        try:
            from jinja2 import Template as Jinja2Template

            # Default context if none provided
            if context is None:
                context = {}

            template = await self.get_template(template_id)
            if not template:
                raise ValueError("Template not found")

            # Convert SQLAlchemy Column to string before creating template
            template_str = str(template.html_content) if template.html_content else ""
            jinja_template = Jinja2Template(template_str)

            # Render HTML
            html_content = jinja_template.render(**context)

            # Inject CSS if present
            if template.css_content:
                css_content = str(template.css_content)
                html_content = html_content.replace(
                    "</head>", f"<style>{css_content}</style></head>"
                )

            # Inject JS if present
            if template.js_content:
                js_content = str(template.js_content)
                html_content = html_content.replace(
                    "</body>", f"<script>{js_content}</script></body>"
                )

            return html_content
        except Exception as e:
            raise TemplateRenderError(f"Template rendering error: {str(e)}")
