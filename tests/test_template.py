from fastapi import Request
from fastapi.testclient import TestClient
from services.template_service import TemplateService
from src.main import app

client = TestClient(app)

def test_template_render():
    response = client.get(
        "/api/v1/template/base.html",
        params={
            "context": {
                "title": "홈",
                "navigation": [{"url": "/", "title": "홈", "active": True}]
            }
        }
    )
    assert response.status_code == 200
    assert "홈" in response.text 


async def test_template_render1():
    # FastAPI TestClient를 사용하여 request 객체 생성
    client = TestClient(app)  # app은 FastAPI 인스턴스

    # 가짜 request 객체 생성
    with client:
        request = Request(scope=client.scope)

    # TemplateService 인스턴스 생성
    template_service = TemplateService()

    # 올바른 context와 template_name 설정
    context = {"request": request, "some_key": "some_value"}
    template_name = "valid_template.html"  # 실제 존재하는 템플릿 파일명

    # 비동기 함수 호출
    rendered_template = await template_service.get_template(template_name, context)
    assert "expected_content" in rendered_template  # 예상되는 내용 확인