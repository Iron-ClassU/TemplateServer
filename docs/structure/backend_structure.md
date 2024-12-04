# AI Backend 시스템 구조

## Project structure

### Project source roots

``` shell
project
├── api     # AWS lambda function entry point
├── core    # Core logic, common utilities
├── server  # Server application, API routes
├── project # Project template boilerplate
├── tests   # Test code
├── pyproject.toml
└── .cursorrules
```

* "api", "core", "server" are the namespaces.
  * starts with "api", "core", "server" in the absolute package path.

### API

``` shell
api
├── __init__.py
├── {path_prefix}
│   ├── {path_prefix}_{path_name}_{http_method}.py
│   └── {path_prefix}_{path_name}_impl.py   # Implementation of the function(referenced in the api routes, too)
└── warmup
    ├── __init__.py
    └── warmup.py   # AWS lambda function wakeup handler
```

### core

``` shell
core
├── Makefile
├── __init__.py
├── config
│   ├── __init__.py
│   └── settings.py
├── factories
├── memory
│   └── __init__.py
├── models
│   ├── __init__.py
│   ├── auth.py
│   ├── base   # Database mapping classes
│   │   ├── __init__.py
│   │   ├── agents.py
│   │   ├── api_keys.py
│   │   ├── datasets.py
│   │   ├── project_members.py
│   │   ├── project_membership_requests.py
│   │   ├── projects.py
│   │   ├── users.py
│   │   └── workflows.py
│   ├── mongo
│   │   ├── agent_graph.py
│   │   ├── agent_graph_history.py
│   │   ├── agent_history.py
│   │   ├── data_model.py
│   │   ├── dataset_history.py
│   │   ├── knowledge_graph.py
│   │   ├── knowledge_graph_history.py
│   │   ├── llm_prompt.py
│   │   ├── llm_prompt_history.py
│   │   ├── project_history.py
│   │   ├── project_member_history.py
│   │   └── workflow_history.py
│   └── prompt
│       ├── prompt.py
│       └── prompt_history.py
├── schemas
├── services
│   └── {data_model_name:lower_snake_case}   # Dataclass for each data model
│       ├── __init__.py   # Module initialization
│       └── {module_name}.py   # Submodule contains data model, operator, any variables
└── utils
    ├── __init__.py
    ├── aws
    │   ├── __init__.py
    │   └── secrets.py
    ├── database.py
    ├── date_util.py
    ├── email.py
    ├── error_handling.py
    ├── exceptions.py
    ├── extractor.py
    ├── llm
    │   ├── __init__.py
    │   ├── llm_client.py
    │   ├── llm_config.py
    │   ├── llm_decorators.py
    │   └── llm_util.py
    ├── security.py
    ├── singleton.py
    └── slack_util.py
```

### server

``` shell
server
├── __init__.py
├── app.py
├── helper
│   ├── __init__.py
│   └── security.py
├── middleware
└── routes
    ├── __init__.py
    ├── auth
    │   └── __init__.py
    ├── health
    │   └── __init__.py
    ├── project
    ├── prompt
    │   └── __init__.py
    └── user
        └── __init__.py
```

### Project boilerplate

``` shell
project
├── README.md
├── agent
│   ├── __init__.py
│   ├── base_agent.py
│   └── llm_agent.py
├── config.py # 프로젝트 설정
├── dataset
│   └── __init__.py
├── project.py # 프로젝트 관리 핵심 클래스
├── pyproject.toml
└── workflow
    ├── __init__.py
    ├── agent_graph
    │   ├── __init__.py
    │   ├── examples
    │   │   ├── apple_workflow.py
    │   │   ├── function_workflow.py
    │   │   └── workflow_example.py
    │   ├── executor.py
    │   ├── graphs
    │   │   ├── __init__.py
    │   │   ├── builder.py
    │   │   ├── schema.py
    │   │   ├── state_manager.py
    │   │   └── state_types.py
    │   ├── machine
    │   │   └── __init__.py
    │   ├── node
    │   │   ├── __init__.py
    │   │   ├── base_node.py
    │   │   ├── data_node.py
    │   │   ├── llm_node.py
    │   │   ├── ml_node.py
    │   │   ├── prompt_node.py
    │   │   └── route_node.py
    │   └── tool
    │       ├── __init__.py
    │       ├── agent_interaction_tool.py
    │       ├── code_tool.py
    │       ├── data_processing_tool.py
    │       ├── db_tool.py
    │       ├── evaluation_tool.py
    │       ├── finance_tool.py
    │       ├── formatting_tool.py
    │       ├── image_tool.py
    │       ├── llm_tool.py
    │       ├── ml_tool.py
    │       ├── planning_tool.py
    │       ├── rag_tool.py
    │       ├── search_tool.py
    │       └── text_processing_tool.py
    ├── api
    │   └── workflow_api.py
    ├── executor.py # 워크플로우 실행 엔진
    ├── knowledge_graph
    │   └── __init__.py
    ├── prompts
    │   └── workflow_generator.py
    └── workflow.py
```

## 핵심 개념

## 1. Project (/project)
사용자가 생성하고 관리하는 최상위 단위입니다. 여러 사용자와 공유하여 협업이 가능하며, 멀티 에이전트 기반의 문제 해결 솔루션을 포함합니다.

### 1.2. Workflow (/project/workflow)
프로젝트 내의 문제 해결 프로세스를 구성하는 단위입니다.

#### 1.2.1 Agent Graph (/workflow/agent_graph)
단일 또는 멀티 에이전트로 구성된 실행 프로세스입니다.

##### 1.2.1.1 Node (/agent_graph/node)
AI 처리를 위한 함수 객체들입니다.
- LLM 노드: 언어 모델 기반 처리
- 데이터 노드: 데이터 처리 및 변환
- ML 노드: 머신러닝 모델 처리

##### 1.2.1.2 Graphs (/agent_graph/graphs)
- 노드 간 연결 관리
- StateGraph 상태 관리
- 데이터 포맷팅

##### 1.2.1.3 Tool (/agent_graph/tool)
노드가 사용하는 기능 컴포넌트들입니다.
- 검색 도구
- 웹크롤링 도구
- 문서 처리 도구
- 에이전트 평가 도구
- SQL 통신 도구
- RAG 시스템 도구

##### 1.2.1.4 Machine (/agent_graph/machine)
실행 환경을 관리합니다.
- ML 모델 실행
- 통계 모델 처리
- 실행 스케줄링
- 모니터링

#### 1.2.2 Knowledge Graph (/workflow/knowledge_graph)
- 전체 작업의 의미와 관계를 시각화
- 데이터베이스 연동
- 스키마 관리
- 데이터 포맷팅

### 1.3. Agent (/project/agent)
문제 해결을 위한 AI 에이전트들을 관리합니다.
- 기본 에이전트: 공통 기능 정의
- LLM 에이전트: 언어 모델 기반 처리
- ML 에이전트: 머신러닝 모델 기반 처리
- 하이브리드 에이전트: LLM과 ML의 조합
- 오케스트레이터: 에이전트 간 조율

### 1.4. Dataset (/project/dataset)
데이터 관리를 담당합니다.
- 데이터 로딩: Raw Data 입력
- 데이터 처리: 전처리 및 변환
- 데이터 검증: 유효성 검사
- 데이터 내보내기: 처리된 데이터 저장

## 2. Core 폴더
- **core/**: 시스템의 핵심 기능을 제공하는 파일들이 포함되어 있습니다. 이 폴더는 다음과 같은 하위 폴더로 구성되어 있습니다.

### 2.1 Config 폴더
- **config/**: 프로젝트의 설정 파일들이 위치합니다. 이곳에는 시스템 전반에 걸쳐 사용되는 설정 값들이 포함되어 있으며, `settings.py` 파일은 환경 설정을 관리합니다. 이 파일을 통해 데이터베이스 연결 정보, API 키, 기타 환경 변수 등을 설정할 수 있습니다.

### 2.2 DB 폴더
- **db/**: 데이터베이스와 관련된 파일들이 포함되어 있습니다.
  - **models.py**: 데이터베이스 모델을 정의하는 파일로, SQLAlchemy를 사용하여 데이터베이스 테이블과 매핑되는 클래스를 포함합니다. 각 모델은 데이터베이스의 엔티티를 표현하며, CRUD 작업을 수행하는 데 필요한 메서드를 정의합니다.
  - **operations.py**: 데이터베이스와의 상호작용을 위한 다양한 작업을 정의하는 파일입니다. 데이터 삽입, 조회, 업데이트, 삭제와 같은 기능을 포함합니다.

### 2.3 Memory 폴더
- **memory/**: 메모리 관리와 관련된 파일들이 포함되어 있습니다.
  - **memory_manager.py**: 시스템의 메모리 사용을 관리하는 기능을 제공하는 파일입니다. 메모리 최적화, 캐싱 전략 등을 구현하여 성능을 향상시키는 데 기여합니다.

### 2.4 Utils 폴더
- **utils/**: 다양한 유틸리티 함수들이 포함되어 있으며, 여러 모듈에서 공통적으로 사용되는 기능들을 제공합니다. 이 폴더는 코드의 재사용성을 높이고, 각 모듈 간의 의존성을 줄이는 데 기여합니다.

##### 2.4.1 AWS 폴더
- **aws/**: AWS와 관련된 유틸리티 함수들이 포함되어 있습니다. 이 폴더는 AWS 서비스와의 상호작용을 단순화하고, 비밀 정보 관리와 같은 기능을 제공합니다.

##### 2.4.2 LLM 폴더
- **llm/**: 대형 언어 모델(LLM)과 관련된 유틸리티 함수들이 포함되어 있습니다. 이 폴더는 LLM과의 상호작용을 위한 클라이언트 및 설정 관리 기능을 제공합니다.

##### 2.4.3 Date Util 파일
- **date_util.py**: 날짜 및 시간 관련 유틸리티 함수들이 포함되어 있습니다. 이 파일은 날짜 형식 변환 및 날짜 계산 기능을 제공하여, 날짜와 시간을 처리하는 데 필요한 공통 기능을 제공합니다.

##### 2.4.4 Error Handling 파일
- **error_handling.py**: 에러 처리와 관련된 기능을 제공하는 파일로, 시스템에서 발생하는 예외를 관리하고, 적절한 응답을 반환하는 데 사용됩니다.

##### 2.4.5 기타 유틸리티 파일
- **기타 유틸리티 파일들**: 이메일 전송, 로깅, 헬퍼 함수 등 다양한 기능을 제공하는 파일들이 포함되어 있습니다. 이 파일들은 시스템의 효율성을 높이고, 코드의 일관성을 유지하는데 기여합니다.

이렇게 `utils` 폴더는 전체 시스템의 효율성을 향상시키고, 코드의 재사용성을 높이는 데 중요한 역할을 합니다.

## 3. API 폴더
- **api/**: 외부와의 인터페이스를 정의하는 파일들이 포함되어 있습니다. 이 폴더는 사용자 인증, 사용자 관리, 미들웨어, 초기화 및 준비 작업을 위한 파일들이 위치합니다.

## 4. Server 폴더
- **server/**: 애플리케이션의 주요 실행 파일과 관련된 코드가 포함되어 있습니다. 이 폴더는 FastAPI 애플리케이션을 구성하고, 라우팅, 미들웨어, 보안 및 기타 서버 관련 기능을 정의합니다.

### 4.1 Init 파일
- **__init__.py**: 서버 모듈을 초기화하는 파일로, 이 폴더가 패키지로 인식되도록 합니다.

### 4.2 App 파일
- **app.py**: FastAPI 애플리케이션의 진입점으로, 서버의 초기화 및 설정을 담당합니다. 데이터베이스 초기화, 로깅 설정, 미들웨어 추가, 라우터 포함 등의 기능을 수행합니다.

### 4.3 Helper 폴더
- **helper/**: 보조 기능을 제공하는 파일들이 포함되어 있습니다. 이 폴더는 보안 관련 기능을 포함하여, 사용자 인증 및 권한 부여를 처리하는 데 필요한 기능을 제공합니다.

### 4.4 Routes 폴더
- **routes/**: API 엔드포인트를 정의하는 파일들이 포함되어 있습니다. 각 라우트는 특정 기능을 수행하며, 사용자 인증, 사용자 정보 관리, 건강 체크 등의 기능을 제공합니다. 이 폴더는 다음과 같은 하위 폴더로 구성되어 있습니다:
  - **auth/**: 사용자 인증 관련 API 엔드포인트를 포함합니다.
  - **health/**: 서버의 상태를 확인하는 건강 체크 API 엔드포인트를 포함합니다.
  - **user/**: 사용자 정보 관리와 관련된 API 엔드포인트를 포함합니다.

이렇게 `server` 폴더는 애플리케이션의 핵심 기능을 구성하고, API 요청을 처리하는 데 필요한 모든 요소를 포함하여, 전체 시스템의 구조를 명확하게 정의합니다.

## 5. Tests 폴더
- **tests/**: 각 모듈에 대한 테스트 코드가 포함되어 있습니다. 테스트는 프로젝트의 품질을 보장하는 데 중요한 역할을 합니다.
  - **test_project/**: 프로젝트 관련 기능에 대한 테스트를 포함합니다.
  - **test_workflow/**: 워크플로우 관련 기능에 대한 테스트를 포함합니다.
  - **test_agent/**: 에이전트 관련 기능에 대한 테스트를 포함합니다.
  - **test_dataset/**: 데이터셋 관련 기능에 대한 테스트를 포함합니다.

## 6. Docs 폴더
- **docs/**: 프로젝트 문서화와 관련된 파일들이 포함되어 있습니다. API 문서, 가이드, 예제 등이 위치합니다.
  - **api/**: API 문서화와 관련된 파일들이 포함됩니다.
  - **guides/**: 사용자를 위한 가이드 문서가 포함됩니다.
  - **examples/**: 코드 예제와 사용 사례가 포함됩니다.

## 7. 기타 파일
- **.env**: 환경 변수 설정 파일입니다.
- **requirements.txt**: 프로젝트의 의존성을 정의하는 파일입니다.
- **setup.py**: 패키지 설정 파일로, 프로젝트를 배포하는 데 사용됩니다.
- **README.md**: 프로젝트에 대한 설명과 사용법을 제공하는 파일입니다.
