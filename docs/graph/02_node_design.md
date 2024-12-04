# Node Design

## Node Categories
1. **LLM Nodes**
   - 목적: 자연어 처리, 텍스트 생성, 분석
   - 예시: understand_request, generate_response

2. **Data Nodes**
   - 목적: 데이터 접근, 저장, 조회
   - 예시: fetch_store_data, save_result

3. **ML Nodes**
   - 목적: 머신러닝 모델 추론
   - 예시: classify_intent, predict_price

4. **Router Nodes**
   - 목적: 조건부 분기, 병렬 처리
   - 예시: price_range_router, category_router

## Node Structure

### Common Node Properties
```python
{
    "name": str,          # 고유 식별자
    "type": NodeType,     # 노드 타입
    "type_id": str,       # 구체적 구현 타입
    "description": str,   # 노드 설명
    "config": dict,       # 노드 설정
    "execution": {
        "mode": str,      # "sync" or "async"
        "timeout": int,   # 제한 시간 (초)
        "requires": List[str]  # 의존하는 노드들
    }
}
```

### Node Type Specifications

1. **LLM Node**
```python
{
    "type": "llm",
    "type_id": str,  # 사용할 LLM 모델
    "config": {
        "prompt_id": str,           # 프롬프트 템플릿 ID
        "variables": Dict[str, str]  # 변수 매핑
    }
}
```

2. **Data Node**
```python
{
    "type": "data",
    "type_id": str,  # 데이터셋 타입
    "config": {
        "dataset_id": str,          # DATASETS 테이블 ID
        "data_type": str,           # RAW or MODEL
        "filters": Dict[str, Any],  # 선택적 필터
        "columns": List[str]        # 선택적 컬럼
    }
}
```

3. **ML Node**
```python
{
    "type": "ml",
    "type_id": str,  # ML 모델 타입
    "config": {
        "model_id": str,            # 모델 ID
        "input_columns": List[str],  # 입력 특성
        "output_column": str         # 출력 컬럼
    }
}
```

4. **Router Node**
```python
{
    "type": "router",
    "type_id": str,  # 라우터 타입
    "config": {
        "next_nodes": List[str],     # 가능한 다음 노드들
        "conditions": Dict[str, str], # 조건별 매핑
        "default_node": str          # 기본 노드
    }
}
```

## Node Requirements

### Validation Rules

1. **Node Validation**
```python
def validate_node(node: Dict):
    required_fields = ["name", "type", "type_id"]
    for field in required_fields:
        if field not in node:
            raise ValueError(f"Missing required field: {field}")

    if node["type"] not in NodeType.__members__:
        raise ValueError(f"Invalid node type: {node['type']}")
```

2. **Config Validation**
```python
def validate_node_config(node: Dict):
    if "config" not in node:
        raise ValueError("Missing config field")

    config_validators = {
        "llm": validate_llm_config,
        "data": validate_data_config,
        "ml": validate_ml_config,
        "router": validate_router_config
    }

    validator = config_validators.get(node["type"])
    if validator:
        validator(node["config"])
```

### Execution Modes
1. **Synchronous (sync)**
   - 순차적 실행이 필요한 경우
   - 이전 노드의 결과가 즉시 필요한 경우

2. **Asynchronous (async)**
   - 독립적으로 실행 가능한 경우
   - 병렬 처리가 가능한 경우

### Variable Reference Patterns
- 노드 출력 참조: `"node_name.output_field"`
- 입력 데이터 참조: `"input.field_name"`
- 이전 노드 참조: `"previous.field_name"`
