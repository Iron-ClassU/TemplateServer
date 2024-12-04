"""
API v1 endpoints for Dashboard Generator.
"""

from .routes import router as routes_router
from .templates import router as templates_router
from .data import router as data_router

__all__ = [
    "routes_router",
    "templates_router",
    "data_router"
] 