from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from src.services.template_service import TemplateService
from src.core.config import settings
from typing import Dict, Any

router = APIRouter()

@router.get("/template/{template_name}", response_class=HTMLResponse)
async def render_template(
    request: Request,
    template_name: str,
    context: Dict[str, Any] = {},
    template_service: TemplateService = Depends()
):
    try:
        rendered = await template_service.get_template(
            template_name=template_name,
            context={**context, "request": request}
        )
        return HTMLResponse(content=rendered)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 