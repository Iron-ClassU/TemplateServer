# Node and Edge Prompt Guide

## Purpose
사용자 요구사항을 기반으로 Node와 Edge를 생성하기 위한 프롬프트 작성 가이드

## Node Generation

### 1. Node Type Analysis
프롬프트를 통해 필요한 노드 타입을 결정:

```python
# Node Types
LLM = "llm"      # LLM 기반 처리가 필요한 경우
DATA = "data"    # 데이터 접근/처리가 필요한 경우
ML = "ml"        # 머신러닝 모델 추론이 필요한 경우
ROUTER = "router" # 조건부 분기가 필요한 경우
```

### 2. Node Configuration Template

```python
{
    "name": str,          # 노드의 고유 식별자
    "type": NodeType,     # 노드 타입 (llm, data, ml, router)
    "type_id": str,       # 구체적인 구현 타입 (예: "gpt-4", "qa_dataset")
    "description": str,   # 노드의 목적과 기능 설명
    "config": {
        # LLM Node
        "prompt_id": str,           # 프롬프트 템플릿 ID
        "variables": Dict[str, str], # 변수 매핑

        # Data Node
        "dataset_id": str,          # 데이터셋 ID
        "data_type": str,           # 데이터 타입
        "filters": Dict[str, Any],  # 필터 조건

        # Router Node
        "next_nodes": List[str],    # 가능한 다음 노드들
        "conditions": Dict[str, str], # 조건별 다음 노드 매핑
        "default_node": str         # 기본 다음 노드
    },
    "execution": {
        "mode": str,      # "sync" 또는 "async"
        "timeout": int,   # 실행 제한 시간 (초)
        "requires": List[str]  # 의존하는 노드들
    }
}
```

### 3. Node Generation Process

1. **요구사항 분석**
   - 입력: 사용자의 자연어 요구사항
   - 출력: 필요한 처리 단계들의 목록

2. **노드 식별**
   - 각 처리 단계를 적절한 노드 타입으로 매핑
   - 노드 간의 의존성 파악

3. **설정 생성**
   - 각 노드의 구체적인 설정 정의
   - 변수 및 참조 관계 설정

## Edge Generation

### 1. Edge Configuration Template

```python
{
    "id": str,            # 엣지의 고유 식별자
    "source": str,        # 시작 노드의 name
    "target": str         # 도착 노드의 name
}
```

### 2. Edge Generation Process

1. **노드 관계 분석**
   - 노드 간의 데이터 흐름 파악
   - 실행 순서 결정

2. **엣지 생성**
   - 각 노드 쌍에 대해 적절한 엣지 생성
   - 엣지 ID 부여

## Example

입력 요구사항:
"사과를 어디서 살 수 있는지 알려주세요."

생성된 워크플로우:
```python
{
    "nodes": [
        {
            "name": "understand_request",
            "type": "llm",
            "type_id": "gpt-4",
            "description": "사용자 요청 이해 및 분석",
            "config": {
                "prompt_id": "request_analysis",
                "variables": {
                    "user_input": "input.question"
                }
            },
            "execution": {
                "mode": "sync",
                "timeout": 30
            }
        },
        # ... 추가 노드들
    ],
    "edges": [
        {
            "id": "edge1",
            "source": "understand_request",
            "target": "fetch_store_data"
        },
        # ... 추가 엣지들
    ]
}
```

## Best Practices

1. **명확한 명명 규칙**
   - 노드 이름은 기능을 명확히 표현
   - 엣지 ID는 연결을 쉽게 식별할 수 있게 지정

2. **모듈화**
   - 각 노드는 단일 책임 원칙 준수
   - 재사용 가능한 단위로 설계

3. **의존성 관리**
   - 명시적인 의존성 선언
   - 순환 의존성 방지

4. **에러 처리**
   - 각 노드의 실패 케이스 고려
   - 적절한 에러 처리 방식 설정 