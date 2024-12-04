"""
Pydantic schemas for Dashboard Generator.
"""

from .template import (
    TemplateBase,
    TemplateCreate,
    TemplateUpdate,
    TemplateInDB,
    TemplatePreview,
    TemplateStats,
    TemplateType,
    TemplateStatus,
    TemplateConfig,
    TemplateValidationResult,
    TemplateRenderRequest,
    TemplateRenderResult
)
from .route import RouteBase, RouteCreate, RouteUpdate, RouteInDB
from .version import (
    TemplateVersionBase,
    TemplateVersionCreate,
    TemplateVersionInDB,
    VersionComparisonResult
)
from .data import (
    DataSourceType,
    DataSourceConfig,
    DataSourceBase,
    DataSourceCreate,
    DataSourceUpdate,
    DataSourceInDB,
    DataQueryParams,
    DataQueryResult,
    DataValidationResult
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
    # Data schemas
    "DataSourceType",
    "DataSourceConfig",
    "DataSourceBase",
    "DataSourceCreate",
    "DataSourceUpdate",
    "DataSourceInDB",
    "DataQueryParams",
    "DataQueryResult",
    "DataValidationResult"
] 