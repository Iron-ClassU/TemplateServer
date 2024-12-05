from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class TemplateVersionBase(BaseModel):
    html_content: str
    css_content: Optional[str] = None
    js_content: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None


class TemplateVersionCreate(TemplateVersionBase):
    pass


class TemplateVersionInDB(TemplateVersionBase):
    id: int
    template_id: int
    version_number: int
    created_at: datetime
    created_by: Optional[int] = None

    class Config:
        from_attributes = True


class VersionComparisonResult(BaseModel):
    version1: int
    version2: int
    differences: Dict[str, Any]
    created_at_diff: Any
    has_changes: bool
