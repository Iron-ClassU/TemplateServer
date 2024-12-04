from fastapi.templating import Jinja2Templates
from typing import Dict, Any
from src.core.config import settings

class TemplateService:
    def __init__(self):
        self.templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
    
    async def get_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """템플릿 렌더링"""
        try:
            # Jinja2Templates는 Request 객체를 필요로 함
            request = context.get('request')
            if not request:
                raise ValueError("Request object is required")
            
            # 템플릿 렌더링
            response = self.templates.TemplateResponse(
                name=template_name,
                context=context
            )
            return response.body.decode()
            
        except ValueError as ve:
            raise TemplateRenderError(f"Request error: {str(ve)}")
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template: {str(e)}")

class TemplateRenderError(Exception):
    """템플릿 렌더링 실패 예외"""
    pass