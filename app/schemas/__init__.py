"""
Pydantic schemas for Dashboard Generator.
"""

from .route import RouteBase, RouteCreate, RouteInDB, RouteUpdate
from .template import (
    TemplateBase,
    TemplateConfig,
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
from .version import (
    TemplateVersionBase,
    TemplateVersionCreate,
    TemplateVersionInDB,
    VersionComparisonResult,
)

__all__ = [
    # Template schemas
    "TemplateBase",
    "TemplateCreate",
    "TemplateUpdate",
    "TemplateInDB",
    "TemplatePreview",
    "TemplateStats",
    "TemplateType",
    "TemplateStatus",
    "TemplateConfig",
    "TemplateValidationResult",
    "TemplateRenderRequest",
    "TemplateRenderResult",
    # Route schemas
    "RouteBase",
    "RouteCreate",
    "RouteUpdate",
    "RouteInDB",
    # Version schemas
    "TemplateVersionBase",
    "TemplateVersionCreate",
    "TemplateVersionInDB",
    "VersionComparisonResult",
]
