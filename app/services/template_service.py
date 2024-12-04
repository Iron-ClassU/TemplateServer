from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.template import Template
from app.schemas.template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateType,
    TemplateStatus,
    TemplatePreview
)

class TemplateService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_template(self, template: TemplateCreate) -> Template:
        """Create a new template."""
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
        search: Optional[str] = None
    ) -> List[Template]:
        """Get all templates with filtering and search."""
        query = select(Template)

        if type:
            query = query.where(Template.type == type)
        if status:
            query = query.where(Template.status == status)
        if tag:
            # This assumes tags is a JSON array
            query = query.where(Template.tags.contains([tag]))
        if search:
            query = query.where(Template.name.ilike(f"%{search}%"))

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

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
        if template.html_content and not (
            "<html" in template.html_content.lower() and 
            "</html>" in template.html_content.lower()
        ):
            errors.append("Invalid HTML structure")
        
        # Check for basic Jinja2 syntax
        if template.html_content:
            try:
                from jinja2 import Environment
                env = Environment()
                env.parse(template.html_content)
            except Exception as e:
                errors.append(f"Invalid Jinja2 syntax: {str(e)}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    async def render_preview(
        self, template: Template, context: Dict[str, Any] = None
    ) -> str:
        """Generate a preview of the template with sample data."""
        from jinja2 import Template as Jinja2Template
        
        # Default context if none provided
        if context is None:
            context = {
                "title": "Preview Title",
                "content": "Sample Content",
                "items": [
                    {"name": "Item 1", "value": "Value 1"},
                    {"name": "Item 2", "value": "Value 2"}
                ]
            }
        
        try:
            # Create Jinja2 template
            jinja_template = Jinja2Template(template.html_content)
            
            # Render HTML
            html_content = jinja_template.render(**context)
            
            # Inject CSS if present
            if template.css_content:
                html_content = html_content.replace(
                    "</head>",
                    f"<style>{template.css_content}</style></head>"
                )
            
            # Inject JS if present
            if template.js_content:
                html_content = html_content.replace(
                    "</body>",
                    f"<script>{template.js_content}</script></body>"
                )
            
            return html_content
        except Exception as e:
            raise ValueError(f"Template rendering error: {str(e)}")

    async def clone_template(self, template_id: int, new_name: str) -> Optional[Template]:
        """Clone an existing template."""
        # Get existing template
        original = await self.get_template(template_id)
        if not original:
            return None
        
        # Create new template with copied content
        new_template = TemplateCreate(
            name=new_name,
            description=f"Clone of {original.name}",
            html_content=original.html_content,
            css_content=original.css_content,
            js_content=original.js_content,
            config=original.config,
            type=original.type,
            status=TemplateStatus.DRAFT,
            tags=original.tags
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
            "error_count": 0  # Mock data
        }

    async def get_all_tags(self) -> List[str]:
        """Get all unique tags used in templates."""
        result = await self.session.execute(
            select(Template.tags)
            .where(Template.tags.is_not(None))
            .distinct()
        )
        all_tags = result.scalars().all()
        # Flatten and deduplicate tags
        unique_tags = set()
        for tags in all_tags:
            if isinstance(tags, list):
                unique_tags.update(tags)
        return sorted(list(unique_tags))