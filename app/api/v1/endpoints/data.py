from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from app.models.base import get_session
from app.services.data_service import DataService
from app.schemas.data import (
    DataSourceCreate,
    DataSourceUpdate,
    DataSourceInDB,
    DataQueryParams,
    DataQueryResult,
    DataValidationResult,
    DataSourceType
)

router = APIRouter()

@router.post("/sources", response_model=DataSourceInDB)
async def create_data_source(
    data_source: DataSourceCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new data source."""
    data_service = DataService(session)
    try:
        return await data_service.create_data_source(data_source)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sources", response_model=List[DataSourceInDB])
async def list_data_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    type: Optional[DataSourceType] = None,
    is_active: Optional[bool] = None,
    session: AsyncSession = Depends(get_session)
):
    """List all data sources with optional filtering."""
    data_service = DataService(session)
    filter_params = {}
    if type is not None:
        filter_params['type'] = type
    if is_active is not None:
        filter_params['is_active'] = is_active
    return await data_service.get_data_sources(skip, limit, filter_params)

@router.get("/sources/{data_source_id}", response_model=DataSourceInDB)
async def get_data_source(
    data_source_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get a specific data source."""
    data_service = DataService(session)
    data_source = await data_service.get_data_source(data_source_id)
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return data_source

@router.put("/sources/{data_source_id}", response_model=DataSourceInDB)
async def update_data_source(
    data_source_id: int,
    data_source: DataSourceUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update a data source."""
    data_service = DataService(session)
    try:
        updated = await data_service.update_data_source(data_source_id, data_source)
        if not updated:
            raise HTTPException(status_code=404, detail="Data source not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/sources/{data_source_id}")
async def delete_data_source(
    data_source_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a data source."""
    data_service = DataService(session)
    if not await data_service.delete_data_source(data_source_id):
        raise HTTPException(status_code=404, detail="Data source not found")
    return {"message": "Data source deleted successfully"}

@router.post("/sources/{data_source_id}/validate", response_model=DataValidationResult)
async def validate_data_source(
    data_source_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Validate a data source configuration."""
    data_service = DataService(session)
    data_source = await data_service.get_data_source(data_source_id)
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return await data_service.validate_data_source(data_source)

@router.post("/sources/{data_source_id}/query", response_model=DataQueryResult)
async def query_data_source(
    data_source_id: int,
    query_params: DataQueryParams = Body(...),
    session: AsyncSession = Depends(get_session)
):
    """Query data from a data source."""
    data_service = DataService(session)
    try:
        return await data_service.query_data(data_source_id, query_params)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sources/{data_source_id}/sync")
async def sync_data_source(
    data_source_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Manually trigger data source synchronization."""
    data_service = DataService(session)
    try:
        await data_service.sync_data_source(data_source_id)
        return {"message": "Data source sync initiated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sources/{data_source_id}/status")
async def get_sync_status(
    data_source_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get the current sync status of a data source."""
    data_service = DataService(session)
    data_source = await data_service.get_data_source(data_source_id)
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return {
        "status": data_source.sync_status,
        "last_sync": data_source.last_sync,
        "is_active": data_source.is_active
    } 