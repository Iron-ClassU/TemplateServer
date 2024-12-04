from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum

class DataSourceType(str, Enum):
    REST_API = "rest_api"
    DATABASE = "database"
    FILE = "file"
    STATIC = "static"

class DataSourceConfig(BaseModel):
    type: DataSourceType
    connection_details: Dict[str, Any]
    parameters: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    auth_config: Optional[Dict[str, Any]] = None
    cache_ttl: Optional[int] = Field(None, ge=0)  # Time to live in seconds
    retry_config: Optional[Dict[str, Any]] = None

class DataSourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    config: DataSourceConfig
    transform_config: Optional[Dict[str, Any]] = None
    schedule: Optional[str] = None  # Cron expression for scheduled updates

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    config: Optional[DataSourceConfig] = None
    transform_config: Optional[Dict[str, Any]] = None
    schedule: Optional[str] = None
    is_active: Optional[bool] = None

class DataSourceInDB(DataSourceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_sync: Optional[datetime] = None
    sync_status: Optional[str] = None

    class Config:
        from_attributes = True

class DataQueryParams(BaseModel):
    filters: Optional[Dict[str, Any]] = None
    sort: Optional[List[str]] = None
    page: Optional[int] = Field(1, ge=1)
    page_size: Optional[int] = Field(50, ge=1, le=1000)
    fields: Optional[List[str]] = None

class DataQueryResult(BaseModel):
    data: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int

class DataValidationResult(BaseModel):
    is_valid: bool
    errors: Optional[List[Dict[str, Any]]] = None
    warnings: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None 