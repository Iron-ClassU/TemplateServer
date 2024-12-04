from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class TemplateType(str, Enum):
    DASHBOARD = "dashboard"
    REPORT = "report"
    WIDGET = "widget"
    LAYOUT = "layout"

class TemplateStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class TemplateConfig(BaseModel):
    type: TemplateType
    layout: Optional[Dict[str, Any]] = None
    theme: Optional[Dict[str, Any]] = None
    components: Optional[List[Dict[str, Any]]] = None
    data_bindings: Optional[Dict[str, Any]] = None
    permissions: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None

class TemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    html_content: str
    css_content: Optional[str] = None
    js_content: Optional[str] = None
    config: Optional[TemplateConfig] = None
    status: TemplateStatus = Field(default=TemplateStatus.DRAFT)
    tags: Optional[List[str]] = None
    parent_id: Optional[int] = None  # For template inheritance
    version_notes: Optional[str] = None

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    html_content: Optional[str] = None
    css_content: Optional[str] = None
    js_content: Optional[str] = None
    config: Optional[TemplateConfig] = None
    status: Optional[TemplateStatus] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None
    version_notes: Optional[str] = None

class TemplateInDB(TemplateBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int = Field(default=1)

    class Config:
        from_attributes = True

class TemplatePreview(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: TemplateType
    status: TemplateStatus
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]
    version: int

class TemplateStats(BaseModel):
    total_routes: int
    active_routes: int
    last_used: Optional[datetime]
    usage_count: int
    avg_render_time: Optional[float]
    error_count: int

class TemplateDependency(BaseModel):
    template_id: int
    name: str
    type: str
    is_required: bool
    default_value: Optional[Any] = None

class TemplateValidationResult(BaseModel):
    is_valid: bool
    errors: Optional[List[Dict[str, Any]]] = None
    warnings: Optional[List[Dict[str, Any]]] = None
    dependencies: Optional[List[TemplateDependency]] = None
    metadata: Optional[Dict[str, Any]] = None

class TemplateRenderRequest(BaseModel):
    template_id: int
    context: Dict[str, Any]
    preview: bool = False
    validate: bool = True

class TemplateRenderResult(BaseModel):
    html: str
    css: Optional[str] = None
    js: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    render_time: float 