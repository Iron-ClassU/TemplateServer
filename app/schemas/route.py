from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class RouteBase(BaseModel):
    path: str = Field(..., min_length=1, max_length=200)
    template_id: int
    method: str = Field(default="GET", pattern="^(GET|POST|PUT|DELETE|PATCH)$")
    handler_config: Optional[Dict[str, Any]] = None


class RouteCreate(RouteBase):
    pass


class RouteUpdate(BaseModel):
    path: Optional[str] = Field(None, min_length=1, max_length=200)
    template_id: Optional[int] = None
    method: Optional[str] = Field(None, pattern="^(GET|POST|PUT|DELETE|PATCH)$")
    handler_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class RouteInDB(RouteBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
