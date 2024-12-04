# Edge Design

## Edge Structure

### Basic Edge Properties
```python
{
    "id": str,        # 엣지 고유 식별자
    "source": str,    # 시작 노드 이름
    "target": str,    # 도착 노드 이름
    "config": {       # 선택적 설정
        "condition": str,     # 조건식
        "data_mapping": dict  # 데이터 매핑 규칙
    }
}
```

## Edge Requirements

### 1. Uniqueness
- 각 엣지의 `id`는 워크플로우 내에서 고유해야 함
- 동일한 `source`와 `target`을 가진 중복 엣지는 불가

### 2. Node References
- `source`와 `target`은 실제 존재하는 노드의 name이어야 함
- 존재하지 않는 노드를 참조할 수 없음

### 3. Direction
- 모든 엣지는 방향성을 가짐
- 순환 참조는 허용되지 않음

## Edge Validation Rules

### 1. Basic Edge Validation
```python
def validate_edge(edge: Dict, nodes: List[Dict]):
    # 필수 필드 검증
    required_fields = ["id", "source", "target"]
    for field in required_fields:
        if field not in edge:
            raise ValueError(f"Missing required field: {field}")

    # 노드 참조 검증
    node_names = {node["name"] for node in nodes}
    if edge["source"] not in node_names:
        raise ValueError(f"Invalid source node: {edge['source']}")
    if edge["target"] not in node_names:
        raise ValueError(f"Invalid target node: {edge['target']}")
```

### 2. Edge Uniqueness Validation
```python
def validate_edge_uniqueness(edges: List[Dict]):
    edge_ids = set()
    edge_pairs = set()

    for edge in edges:
        # ID 중복 검사
        if edge["id"] in edge_ids:
            raise ValueError(f"Duplicate edge id: {edge['id']}")
        edge_ids.add(edge["id"])

        # source-target 쌍 중복 검사
        pair = (edge["source"], edge["target"])
        if pair in edge_pairs:
            raise ValueError(f"Duplicate edge: {edge['source']} -> {edge['target']}")
        edge_pairs.add(pair)
```

### 3. Router Edge Validation
```python
def validate_router_edges(edges: List[Dict], nodes: List[Dict]):
    router_nodes = [n for n in nodes if n["type"] == "router"]

    for router in router_nodes:
        next_nodes = router["config"]["next_nodes"]
        edge_targets = {e["target"] for e in edges
                       if e["source"] == router["name"]}

        # 모든 next_nodes가 edge로 연결되어 있는지 확인
        for next_node in next_nodes:
            if next_node not in edge_targets:
                raise ValueError(
                    f"Missing edge for router {router['name']} -> {next_node}"
                )
```

## Node-Edge Relationship Examples

### 1. Basic Connection
```python
{
    "nodes": [
        {"name": "node1", "type": "llm", ...},
        {"name": "node2", "type": "data", ...}
    ],
    "edges": [
        {"id": "edge1", "source": "node1", "target": "node2"}
    ]
}
```

### 2. Router Connection
```python
{
    "nodes": [
        {
            "name": "router1",
            "type": "router",
            "config": {
                "next_nodes": ["node2", "node3"]
            }
        }
    ],
    "edges": [
        {"id": "edge1", "source": "router1", "target": "node2"},
        {"id": "edge2", "source": "router1", "target": "node3"}
    ]
}
```

### 3. Dependency Connection
```python
{
    "nodes": [
        {
            "name": "node3",
            "execution": {
                "requires": ["node1", "node2"]
            }
        }
    ],
    "edges": [
        {"id": "edge1", "source": "node1", "target": "node3"},
        {"id": "edge2", "source": "node2", "target": "node3"}
    ]
}
