from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.models.base import get_session
from app.services.route_service import RouteService
from app.schemas.route import RouteCreate, RouteUpdate, RouteInDB

router = APIRouter()

@router.get("/", response_model=List[RouteInDB])
async def list_routes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    template_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session)
):
    """Get all routes with optional filtering by template_id."""
    route_service = RouteService(session)
    if template_id:
        routes = await route_service.get_template_routes(template_id)
    else:
        routes = await route_service.get_routes(skip=skip, limit=limit)
    return routes

@router.post("/", response_model=RouteInDB)
async def create_route(
    route: RouteCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new route."""
    route_service = RouteService(session)
    try:
        db_route = await route_service.create_route(
            path=route.path,
            template_id=route.template_id,
            method=route.method,
            handler_config=route.handler_config
        )
        return db_route
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{route_id}", response_model=RouteInDB)
async def get_route(
    route_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get a specific route by ID."""
    route_service = RouteService(session)
    route = await route_service.get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.put("/{route_id}", response_model=RouteInDB)
async def update_route(
    route_id: int,
    route_update: RouteUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update a route."""
    route_service = RouteService(session)
    try:
        updated_route = await route_service.update_route(
            route_id=route_id,
            path=route_update.path,
            template_id=route_update.template_id,
            method=route_update.method,
            handler_config=route_update.handler_config,
            is_active=route_update.is_active
        )
        if not updated_route:
            raise HTTPException(status_code=404, detail="Route not found")
        return updated_route
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{route_id}")
async def delete_route(
    route_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a route."""
    route_service = RouteService(session)
    if not await route_service.delete_route(route_id):
        raise HTTPException(status_code=404, detail="Route not found")
    return {"message": "Route deleted successfully"}

@router.post("/{route_id}/validate")
async def validate_route(
    route_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Validate a route configuration."""
    route_service = RouteService(session)
    route = await route_service.get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    validation_result = await route_service.validate_route(route)
    if not validation_result["is_valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Route validation failed",
                "errors": validation_result["errors"]
            }
        )
    return {"message": "Route configuration is valid"}

@router.put("/{route_id}/status")
async def update_route_status(
    route_id: int,
    is_active: bool,
    session: AsyncSession = Depends(get_session)
):
    """Update route active status."""
    route_service = RouteService(session)
    try:
        updated_route = await route_service.update_route(
            route_id=route_id,
            is_active=is_active
        )
        if not updated_route:
            raise HTTPException(status_code=404, detail="Route not found")
        return {"message": f"Route status updated to {'active' if is_active else 'inactive'}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/template/{template_id}/status")
async def update_template_routes_status(
    template_id: int,
    is_active: bool,
    session: AsyncSession = Depends(get_session)
):
    """Update status of all routes associated with a template."""
    route_service = RouteService(session)
    updated_count = await route_service.bulk_update_template_routes(
        template_id=template_id,
        is_active=is_active
    )
    return {
        "message": f"Updated {updated_count} routes",
        "updated_count": updated_count
    } 