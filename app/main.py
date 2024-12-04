from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.core.config import settings
from app.api.v1.endpoints import routes, templates as template_routes, data

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Mount static files
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Setup Jinja2 templates
template_engine = Jinja2Templates(directory=settings.TEMPLATE_DIR)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# Include routers
app.include_router(routes.router, prefix=f"{settings.API_V1_STR}/routes", tags=["routes"])
app.include_router(template_routes.router, prefix=f"{settings.API_V1_STR}/templates", tags=["templates"])
app.include_router(data.router, prefix=f"{settings.API_V1_STR}/data", tags=["data"]) 