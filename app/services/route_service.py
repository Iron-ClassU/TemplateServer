from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from app.models.route import Route
from app.models.template import Template

class RouteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_route(
        self,
        path: str,
        template_id: int,
        method: str = "GET",
        handler_config: Dict[str, Any] = None
    ) -> Route:
        """Create a new route."""
        try:
            # Verify template exists
            template_result = await self.session.execute(
                select(Template).where(Template.id == template_id)
            )
            template = template_result.scalar_one_or_none()
            if not template:
                raise ValueError("Template not found")

            # Create route
            route = Route(
                path=path,
                template_id=template_id,
                method=method,
                handler_config=handler_config or {}
            )
            self.session.add(route)
            await self.session.commit()
            await self.session.refresh(route)
            return route
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Route with this path already exists")

    async def get_route(self, route_id: int) -> Optional[Route]:
        """Get a route by ID."""
        result = await self.session.execute(
            select(Route).where(Route.id == route_id)
        )
        return result.scalar_one_or_none()

    async def get_route_by_path(self, path: str) -> Optional[Route]:
        """Get a route by path."""
        result = await self.session.execute(
            select(Route).where(Route.path == path, Route.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_routes(self, skip: int = 0, limit: int = 100) -> List[Route]:
        """Get all routes with pagination."""
        result = await self.session.execute(
            select(Route)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update_route(
        self,
        route_id: int,
        path: Optional[str] = None,
        template_id: Optional[int] = None,
        method: Optional[str] = None,
        handler_config: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None
    ) -> Optional[Route]:
        """Update a route."""
        # Get existing route
        route = await self.get_route(route_id)
        if not route:
            return None

        # Build update data
        update_data = {}
        if path is not None:
            update_data["path"] = path
        if template_id is not None:
            # Verify template exists
            template_result = await self.session.execute(
                select(Template).where(Template.id == template_id)
            )
            if not template_result.scalar_one():
                raise ValueError("Template not found")
            update_data["template_id"] = template_id
        if method is not None:
            update_data["method"] = method
        if handler_config is not None:
            update_data["handler_config"] = handler_config
        if is_active is not None:
            update_data["is_active"] = is_active

        if not update_data:
            return route

        try:
            # Update route
            await self.session.execute(
                update(Route)
                .where(Route.id == route_id)
                .values(**update_data)
            )
            await self.session.commit()

            # Get updated route
            result = await self.session.execute(
                select(Route).where(Route.id == route_id)
            )
            return result.scalar_one_or_none()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Route with this path already exists")

    async def delete_route(self, route_id: int) -> bool:
        """Delete a route."""
        result = await self.session.execute(
            delete(Route).where(Route.id == route_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def validate_route(self, route: Route) -> Dict[str, Any]:
        """Validate route configuration."""
        errors = []
        
        # Check path format
        if not route.path.startswith("/"):
            errors.append("Path must start with '/'")
        
        # Check method
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        if route.method not in valid_methods:
            errors.append(f"Invalid method. Must be one of: {', '.join(valid_methods)}")
        
        # Verify template exists and is active
        template_result = await self.session.execute(
            select(Template).where(
                Template.id == route.template_id,
                Template.is_active == True
            )
        )
        if not template_result.scalar_one_or_none():
            errors.append("Template not found or inactive")
        
        # Validate handler config
        if route.handler_config:
            if not isinstance(route.handler_config, dict):
                errors.append("Handler config must be a dictionary")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    async def get_template_routes(self, template_id: int) -> List[Route]:
        """Get all routes associated with a template."""
        result = await self.session.execute(
            select(Route).where(Route.template_id == template_id)
        )
        return result.scalars().all()

    async def bulk_update_template_routes(
        self,
        template_id: int,
        is_active: bool
    ) -> int:
        """Update all routes associated with a template."""
        result = await self.session.execute(
            update(Route)
            .where(Route.template_id == template_id)
            .values(is_active=is_active)
        )
        await self.session.commit()
        return result.rowcount 