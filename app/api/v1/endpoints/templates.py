from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import get_session
from app.schemas.template import (
    TemplateCreate,
    TemplateInDB,
    TemplatePreview,
    TemplateRenderRequest,
    TemplateRenderResult,
    TemplateStats,
    TemplateStatus,
    TemplateType,
    TemplateUpdate,
    TemplateValidationResult,
)
from app.services.template_service import TemplateService

router = APIRouter()


@router.post("/", response_model=TemplateInDB)
async def create_template(
    template: TemplateCreate, session: AsyncSession = Depends(get_session)
):
    """Create a new template."""
    template_service = TemplateService(session)
    try:
        return await template_service.create_template(template)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TemplatePreview])
async def list_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    type: Optional[TemplateType] = None,
    status: Optional[TemplateStatus] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    """List all templates with filtering and search."""
    template_service = TemplateService(session)
    return await template_service.get_templates(
        skip=skip, limit=limit, type=type, status=status, tag=tag, search=search
    )


@router.get("/{template_id}", response_model=TemplateInDB)
async def get_template(
    template_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)
):
    """Get a specific template by ID."""
    template_service = TemplateService(session)
    template = await template_service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put("/{template_id}", response_model=TemplateInDB)
async def update_template(
    template_id: int = Path(..., gt=0),
    template: TemplateUpdate = Body(...),
    session: AsyncSession = Depends(get_session),
):
    """Update a template."""
    template_service = TemplateService(session)
    try:
        updated = await template_service.update_template(template_id, template)
        if not updated:
            raise HTTPException(status_code=404, detail="Template not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{template_id}")
async def delete_template(
    template_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)
):
    """Delete a template."""
    template_service = TemplateService(session)
    if not await template_service.delete_template(template_id):
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted successfully"}


@router.post("/{template_id}/validate", response_model=TemplateValidationResult)
async def validate_template(
    template_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)
):
    """Validate a template."""
    template_service = TemplateService(session)
    template = await template_service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return await template_service.validate_template(template)


@router.post("/{template_id}/render", response_model=TemplateRenderResult)
async def render_template(
    template_id: int = Path(..., gt=0),
    render_request: TemplateRenderRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    """Render a template with provided context."""
    template_service = TemplateService(session)
    try:
        return await template_service.render_template(
            template_id, render_request.context
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{template_id}/stats", response_model=TemplateStats)
async def get_template_stats(
    template_id: int = Path(..., gt=0), session: AsyncSession = Depends(get_session)
):
    """Get usage statistics for a template."""
    template_service = TemplateService(session)
    template = await template_service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return await template_service.get_template_stats(template_id)


@router.put("/{template_id}/status")
async def update_template_status(
    template_id: int = Path(..., gt=0),
    status: TemplateStatus = Body(...),
    session: AsyncSession = Depends(get_session),
):
    """Update template status (draft/published/archived)."""
    template_service = TemplateService(session)
    try:
        updated = await template_service.update_template(
            template_id, TemplateUpdate(status=status)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Template not found")
        return {"message": f"Template status updated to {status}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/types", response_model=List[str])
async def list_template_types():
    """List all available template types."""
    return [t.value for t in TemplateType]


@router.get("/tags", response_model=List[str])
async def list_template_tags(session: AsyncSession = Depends(get_session)):
    """List all used template tags."""
    template_service = TemplateService(session)
    return await template_service.get_all_tags()
