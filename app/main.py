from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.endpoints import routes
from app.api.v1.endpoints import templates as template_routes
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}


# Include routers
app.include_router(
    routes.router, prefix=f"{settings.API_V1_STR}/routes", tags=["routes"]
)
app.include_router(
    template_routes.router,
    prefix=f"{settings.API_V1_STR}/templates",
    tags=["templates"],
)

# Run the application if executed directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
