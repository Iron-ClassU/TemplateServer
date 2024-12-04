# AGI 솔루션 노드 컨셉

AGI 솔루션의 노드 시스템은 모듈화된 기능 단위로 구성되며, 각 노드는 특정 작업을 수행하는 독립적인 컴포넌트입니다. 이 문서는 AGI 솔루션에서 사용되는 다양한 노드 타입과 그 특성을 정의합니다.

## 노드 공통 속성

모든 노드는 다음과 같은 공통 속성을 가집니다:

```json
{
    "node_id": "unique_identifier",
    "node_type": "node_category",
    "version": "1.0.0",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "metadata": {},
    "input_schema": {},
    "output_schema": {},
    "dependencies": []
}
```

## 1. LLM 노드 타입
### 기본 LLM 노드
| 노드명 | 주요 속성 | 설명 |
|--------|-----------|------|
| BaseLLMNode | - model_type<br>- temperature<br>- max_tokens<br>- system_prompt<br>- memory_type | 기본 LLM 기능을 수행하는 노드 |
| AnalystNode | - analysis_type<br>- statistical_methods<br>- insight_format | 데이터 분석 및 통계적 추론 |
| StrategyNode | - strategy_type<br>- decision_criteria<br>- risk_metrics | 전략 수립 및 의사결정 지원 |
| CreativeNode | - content_type<br>- style_guide<br>- generation_rules | 콘텐츠 생성 및 창의적 작업 |

## 2. 데이터 노드 타입
### 데이터 소스 및 처리
| 노드명 | 주요 속성 | 설명 |
|--------|-----------|------|
| DatabaseNode | - connection_info<br>- query_type<br>- schema | 데이터베이스 연결 및 쿼리 |
| DataSourceAPINode | - endpoint<br>- auth_type<br>- request_format<br>- data_schema<br>- polling_interval | 데이터 수집 API 연동 |
| SpreadsheetNode | - sheet_id<br>- range<br>- update_interval | 스프레드시트 데이터 처리 |
| DocumentNode | - file_type<br>- extraction_method | 문서 데이터 추출 |
| MediaNode | - media_type<br>- processing_type | 미디어 파일 처리 |
| PreprocessNode | - cleaning_rules<br>- transformation_logic | 데이터 전처리 |
| ValidationNode | - validation_rules<br>- error_handling | 데이터 검증 |

## 3. 툴 노드 타입
### 외부 서비스 및 기능
| 노드명 | 주요 속성 | 설명 |
|--------|-----------|------|
| SearchNode | - search_engine<br>- query_builder<br>- result_filter | 외부 검색 수행 |
| IntegrationAPINode | - service_type<br>- integration_method<br>- response_handler<br>- action_mapping | 외부 서비스 기능 통합 |
| CalculationNode | - operation_type<br>- input_format<br>- output_format | 수치 계산 처리 |
| TransformationNode | - conversion_type<br>- format_rules | 데이터 형식 변환 |

## 4. 라우터 노드 타입
### 흐름 제어
| 노드명 | 주요 속성 | 설명 |
|--------|-----------|------|
| ConditionalNode | - conditions<br>- branches<br>- default_path | 조건부 분기 처리 |
| LoopNode | - iteration_type<br>- exit_condition<br>- loop_variables | 반복 작업 수행 |
| ParallelNode | - parallel_tasks<br>- sync_points<br>- resource_limits | 병렬 처리 관리 |
| ErrorHandlerNode | - error_patterns<br>- recovery_actions<br>- fallback_logic | 오류 처리 및 복구 |

## 5. ML 노드 타입
### 머신러닝 작업
| 노드명 | 주요 속성 | 설명 |
|--------|-----------|------|
| PredictionNode | - model_type<br>- features<br>- hyperparameters | 예측 모델 실행 |
| ClassificationNode | - classifier_type<br>- classes<br>- threshold | 분류 작업 수행 |
| EvaluationNode | - metrics<br>- validation_method<br>- benchmark | 모델 성능 평가 |

## 6. 통합 노드 타입
### 워크플로우 관리
| 노드명 | 주요 속성 | 설명 |
|--------|-----------|------|
| WorkflowControllerNode | - workflow_steps<br>- transition_rules<br>- state_management | 워크플로우 제어 |
| MonitoringNode | - monitoring_targets<br>- alert_conditions<br>- logging_rules | 시스템 모니터링 |

## 노드 간 연결 규칙

1. **데이터 흐름**
   - 노드 간 데이터는 정의된 스키마에 따라 전달
   - 입/출력 데이터 타입 호환성 검증 필수

2. **의존성 관리**
   - 순환 의존성 금지
   - 명시적 의존성 선언 필요

3. **버전 관리**
   - 노드 버전 호환성 보장
   - 하위 호환성 유지

## 노드 개발 가이드라인

1. **단일 책임 원칙**
   - 각 노드는 하나의 명확한 책임만 가짐
   - 기능 확장은 새로운 노드로 구현

2. **인터페이스 설계**
   - 명확한 입/출력 스키마 정의
   - 표준화된 에러 처리 구현

3. **성능 최적화**
   - 리소스 사용량 모니터링
   - 비동기 처리 권장

4. **테스트 요구사항**
   - 단위 테스트 필수
   - 통합 테스트 시나리오 구현

## 보안 고려사항

1. **데이터 보안**
   - 민감 정보 암호화
   - 접근 권한 관리

2. **실행 보안**
   - 리소스 사용 제한
   - 실행 환경 격리

## 모니터링 및 로깅

1. **성능 메트릭**
   - 실행 시간
   - 리소스 사용량
   - 오류 발생률

2. **로그 수준**
   - DEBUG: 개발 디버깅용
   - INFO: 일반 실행 정보
   - WARNING: 잠재적 문제
   - ERROR: 실행 실패



### **복잡한노드의 하나의 노드에서 처리하는 경우**
``` mermaid
sequenceDiagram
    actor User
    participant App
    participant LLM API
    participant Weather API
    participant Places API
    participant Restaurant API

    User->>App: "내일 서울에서 야외 데이트 계획 추천해줘"
    App->>LLM API: 사용자 질문 전송

    Note over LLM API: 계획을 위해<br/>날씨 확인 필요 판단
    LLM API->>App: get_weather 함수 호출 요청
    App->>Weather API: 내일 날씨 요청
    Weather API->>App: 날씨 데이터 응답
    App->>LLM API: 날씨 데이터 전달

    Note over LLM API: 맑은 날씨 확인,<br/>야외 명소 검색 결정
    LLM API->>App: search_outdoor_places 함수 호출 요청
    App->>Places API: 서울 야외 명소 검색
    Places API->>App: 명소 목록 응답
    App->>LLM API: 명소 데이터 전달

    Note over LLM API: 명소 근처<br/>식당 검색 필요 판단
    LLM API->>App: find_restaurants 함수 호출 요청
    App->>Restaurant API: 주변 맛집 검색
    Restaurant API->>App: 식당 목록 응답
    App->>LLM API: 식당 데이터 전달

    Note over LLM API: 모든 정보를 종합하여<br/>데이트 코스 계획 수립
    LLM API->>App: 최종 데이트 코스 추천
    App->>User: 종합 데이트 코스 추천 전달

```
### 실제 코드 예시
``` python
from openai import OpenAI
import json
from datetime import datetime, timedelta

client = OpenAI()

def process_date_recommendation():
    messages = [
        {"role": "user", "content": "내일 서울에서 야외 데이트를 계획하고 싶어. 추천해줘"}
    ]

    # 1. 첫 번째 LLM 호출 - 날씨 확인 필요성 판단
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=[
            {
                "name": "get_weather",
                "description": "Gets weather forecast for tomorrow",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "date": {"type": "string"}
                    }
                }
            }
        ],
        function_call="auto"
    )

    # 날씨 정보 가져오기
    weather_data = get_weather_data("서울", "tomorrow")
    messages.append(response.choices[0].message)
    messages.append({
        "role": "function",
        "name": "get_weather",
        "content": json.dumps(weather_data)
    })

    # 2. 두 번째 LLM 호출 - 야외 명소 검색
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=[
            {
                "name": "search_outdoor_places",
                "description": "Searches for outdoor attractions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "weather_condition": {"type": "string"}
                    }
                }
            }
        ],
        function_call="auto"
    )

    # 명소 정보 가져오기
    places_data = search_places("서울", weather_data["condition"])
    messages.append(response.choices[0].message)
    messages.append({
        "role": "function",
        "name": "search_outdoor_places",
        "content": json.dumps(places_data)
    })

    # 3. 세 번째 LLM 호출 - 주변 맛집 검색
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=[
            {
                "name": "find_restaurants",
                "description": "Finds restaurants near locations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "near_location": {"type": "string"},
                        "cuisine_type": {"type": "string"}
                    }
                }
            }
        ],
        function_call="auto"
    )

    # 레스토랑 정보 가져오기
    restaurant_data = find_restaurants(places_data["location"], "all")
    messages.append(response.choices[0].message)
    messages.append({
        "role": "function",
        "name": "find_restaurants",
        "content": json.dumps(restaurant_data)
    })

    # 4. 최종 LLM 호출 - 종합 계획 수립
    final_response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    return final_response.choices[0].message.content

# 실제 구현이 필요한 함수들
def get_weather_data(location, date):
    # 날씨 API 호출
    return {
        "condition": "맑음",
        "temperature": 23,
        "precipitation": 0
    }

def search_places(location, weather):
    # 장소 API 호출
    return {
        "places": [
            {
                "name": "서울숲",
                "type": "공원",
                "location": "성동구"
            },
            {
                "name": "북촌한옥마을",
                "type": "문화관광",
                "location": "종로구"
            }
        ]
    }

def find_restaurants(location, cuisine):
    # 맛집 API 호출
    return {
        "restaurants": [
            {
                "name": "맛있는 식당",
                "cuisine": "한식",
                "rating": 4.5
            },
            {
                "name": "로맨틱 레스토랑",
                "cuisine": "양식",
                "rating": 4.8
            }
        ]
    }

# 실행 예시
recommendation = process_date_recommendation()
print(recommendation)
```
