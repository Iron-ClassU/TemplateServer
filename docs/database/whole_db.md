# 주의사항
- 모델 생성시, 클래스화를 먼저 진행해주세요.
- 팩토리 형태로 관리를 할 수 있게 생성해주세요.
- 팩토리 형태의 목표는 비즈니스 단에서 모델핸들링으로 최소한의 코드레벨을 구현하는 것이 목표입니다.

``` mermaid
erDiagram
    USERS ||--o{ PROJECTS : creates
    USERS ||--o{ PROJECT_MEMBERS : "is member of"
    USERS ||--o{ PROJECT_MEMBERSHIP_REQUESTS : "requests/is requested"
    PROJECTS ||--o{ WORKFLOWS : contains
    PROJECTS ||--o{ DATASETS : contains
    PROJECTS ||--o{ AGENTS : contains
    PROJECTS ||--o{ PROJECT_MEMBERS : "has members"
    PROJECTS ||--o{ PROJECT_MEMBERSHIP_REQUESTS : "has requests"
    WORKFLOWS ||--|| Mongo_Agent_Graph : "has graph"
    WORKFLOWS ||--|| Mongo_Knowledge_Graph : "has knowledge"
    DATASETS ||--o{ DATASETS : "is parent of"
    AGENTS ||--o{ AGENTS : "is parent of"
    PROJECTS ||--|| Mongo_Project_History : "has history"
    PROJECT_MEMBERS ||--|| Mongo_Project_Member_History : "has history"
    DATASETS ||--|| Mongo_Dataset_History : "has history"
    AGENTS ||--|| Mongo_Agent_History : "has history"
    Mongo_LLM_Prompt ||--|| Mongo_LLM_Prompt_History : "has history"
    DATASETS ||--o{ Mongo_Data_Model : "references when data_type=MODEL"
    WORKFLOWS ||--o{ WORKFLOWS: "is parent of"
    AGENTS ||--o{ Mongo_Agent_Graph : "is referenced by"


    USERS {
        bigint id PK "유저 고유번호"
        string username "유저 이름"
        string password "유저 비밀번호"
        string email "유저 이메일"
        boolean activated "활성 여부 1: 활성, 0: 비활성"
        string activation_code
        datetime activated_at
        datetime last_login "마지막 로그인 일시"
        string last_ip "마지막 로그인 IP"
        string device_type "디바이스 종류"
        string photo ""
        string social ""
        string reset_code ""
        datetime reset_code_expired_at ""
        datetime created_at "생성일시 | default: CURRENT_TIMESTAMP"
        timestamp updated_at "수정일시 | default: CURRENT_TIMESTAMP"
        string provider ""
    }

    API_KEY {
        bigint id PK "API 키 고유번호"
        string key_id UK "API 키 ID (UUID)"
        int user_id FK "USERS.id"
        string secret_key "해시된 API 키"
        string name "API 키 이름"
        enum type "API 키 유형 (SESSION, RESTAPI) | default: SESSION"
        enum status "API 키 상태 (ACTIVE, REVOKED, EXPIRED) | default: ACTIVE"
        datetime expired_at "만료일시"
        string scopes "권한 범위 (콤마로 구분된 문자열) | default: *"
        string provider "서비스 제공자"
        timestamp created_at "생성일시 | default: CURRENT_TIMESTAMP"
        timestamp updated_at "수정일시 | default: CURRENT_TIMESTAMP"
    }

    PROJECTS {
        bigint id PK "프로젝트 고유 번호"
        string key UK "프로젝트 키"
        int user_id FK "USERS.id"
        string name "프로젝트명"
        text goal "프로젝트 목표"
        text description "프로젝트 설명"
        text howto "프로젝트 해결 방법"
        enum status "활성 여부(ACTIVE, INACTIVE)"
        enum delete_yn "삭제 여부 (Y,N)"
        enum open_yn "오픈 여부(Y,N)"
        timestamp created_at "생성일시 | default: CURRENT_TIMESTAMP"
        timestamp updated_at "수정일시 | default: CURRENT_TIMESTAMP"
        timestamp deleted_at "삭제일시 | default: CURRENT_TIMESTAMP"
    }

    PROJECT_MEMBERS {
        bigint id PK "프로젝트 멤버 고유번호"
        int project_id FK "PROJECTS.id"
        int user_id FK "USERS.id"
        enum role "멤버 역할 (VIEWER, COMMENTER, EDITOR, ADMIN) | default: VIEWER"
        enum status "상태 (ACTIVE, INACTIVE)"
        timestamp created_at "생성일시 | default: CURRENT_TIMESTAMP"
        timestamp updated_at "수정일시 | default: CURRENT_TIMESTAMP"
    }

    PROJECT_MEMBERSHIP_REQUESTS {
        bigint id PK "프로젝트 요청 고유번호"
        int project_id FK "PROJECTS.id"
        int user_id FK "USERS.id"
        enum request_type "요청 타입 (INVITAION, JOIN)"
        enum role "요청 역할 (VIEWER, COMMENTER, EDITOR, ADMIN)"
        enum status "요청 상태 (PENDING, ACCEPTED, DECLINED, CANCELED)"
        text message "요청 메세지"
        int requester_id FK "요청자 USERS.id"
        int responder_id FK "응답자 USERS.id"
        timestamp created_at "생성일시 | default: CURRENT_TIMESTAMP"
        timestamp updated_at "수정일시 | default: CURRENT_TIMESTAMP"
    }

    WORKFLOWS {
        bigint id PK "워크플로우 고유 아이디"
        int project_id FK "PROJECTS.id"
        int parent_id FK
        int user_id FK "USERS.id"
        enum is_folder
        enum is_main
        enum open_yn "오픈 여부"
        text agent_graph_id "Mongo_Agent_Graph._id"
        text knowledge_graph_id "Mongo_Knowledge_Graph"
        text name "워크플로우 이름"
        text goal
        text description
        enum delete_yn "삭제여부"
        timestamp created_at "생성일시"
        timestamp updated_at "수정일시"
        timestamp deleted_at "삭제일시"
    }

    Mongo_Agent_Graph {
        ObjectId _id PK "에이전트 그래프 고유 id"
        Number workflow_id FK "WORKFLOWS.id"
        Number version "에이전트 그래프 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        Boolean is_agent "이 그래프가 에이전트인지 여부"
        Number agent_id FK "AGENTS.id | 이 그래프가 에이전트인 경우 연결된 에이전트 ID"
        Object[] nodes "Array of node objects with type enum(llm|tool|machine|data|function)"
        Object[] edges "Array of edge objects"
    }

    Mongo_Knowledge_Graph {
        ObjectId _id PK "지식 그래프 고유 id"
        Number workflow_id FK "WORKFLOWS.id"
        Number version "지식 그래프 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        Object problem_definition "Problem context"
        Object[] nodes "Array of node objects"
        Object[] edges "Array of edge objects"
        string note "문제 요구 정의서"
    }

    DATASETS {
        bigint id PK "데이터셋 고유번호"
        int project_id FK "PROJECTS.id"
        int parent_id FK
        int user_id FK "USERS.id"
        enum data_type "데이터 타입 (RAW, MODEL)"
        string file_type "파일 종류 (data_type=RAW일 때)"
        string link "파일 링크 (data_type=RAW일 때)"
        string mongodb_collection "MongoDB 컬렉션명 (data_type=RAW일 때)"
        string model_id "Mongo_Data_Model._id (data_type=MODEL일 때)"
        enum delete_yn "삭제 여부"
        enum is_folder "폴더 여부"
        enum open_yn "공개 여부"
        string name "데이터셋 이름"
        text description "데이터셋 설명"
        timestamp created_at "생성일시"
        timestamp updated_at "수정일시"
    }

    AGENTS {
        bigint id PK "에이전트 고유 번호"
        int project_id FK "PROJECTS.id"
        int parent_id FK
        int user_id FK "USERS.id"
        enum delete_yn "삭제 여부"
        enum is_folder
        enum open_yn "오픈 여부"
        string name "에이전트 이름"
        text description "에이전트 설명"
        timestamp created_at "생성일시 | default: CURRENT_TIMESTAMP"
        timestamp updated_at "수정일시 | default: CURRENT_TIMESTAMP"
        timestamp deleted_at "삭제일시 | default: NULL"
    }

    Mongo_Data_Model {
        ObjectId _id PK "데이터 모델 고유 id"
        text name "데이터 모델명"
        text description "데이터 모델 설명"
        json json_data "JSON 형식의 데이터"
        timestamp created_at "생성일시"
        timestamp updated_at "수정일시"
    }

    Mongo_Project_History {
        ObjectId _id PK "히스토리 고유 id"
        Number project_id FK "PROJECTS.id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        Object data "변경된 프로젝트 데이터"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_Project_Member_History {
        ObjectId _id PK "히스토리 고유 id"
        Number project_member_id FK "PROJECT_MEMBERS.id"
        Number project_id FK "PROJECTS.id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        Object data "변경된 멤버 데이터"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_Dataset_History {
        ObjectId _id PK "히스토리 고유 id"
        Number dataset_id FK "DATASETS.id"
        Number project_id FK "PROJECTS.id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        Object data "변경된 데이터셋 데이터"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_Agent_History {
        ObjectId _id PK "히스토리 고유 id"
        Number agent_id FK "AGENTS.id"
        Number project_id FK "PROJECTS.id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        Object data "변경된 에이전트 데이터 {
            parent_id: Number,
            name: String,
            description: String,
            is_folder: String,
            open_yn: String,
            delete_yn: String
        }"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_Workflow_History {
        ObjectId _id PK "히스토리 고유 id"
        Number workflow_history_id FK "WORKFLOWS.id"
        Number workflow_id FK "WORKFLOWS.id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Number updated_by "수정한 User (USERS.id)"
        String agent_graph_version_id FK "Mongo_Agent_Graph_History._id"
        String knowledge_graph_version_id FK "Mongo_Knowledge_Graph_History._id"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_Agent_Graph_History {
        ObjectId _id PK "히스토리 고유 id"
        Number workflow_history_id FK "Mongo_Workflow_History.workflow_history_id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Timestamp updated_at "수정일시"
        Number updated_by "수정한 User (USERS.id)"
        Object[] nodes "노드 배열"
        Object[] edges "엣지 배열"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_Knowledge_Graph_History {
        ObjectId _id PK "히스토리 고유 id"
        Number workflow_history_id FK "Mongo_Workflow_History.workflow_history_id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Timestamp updated_at "수정일시"
        Number updated_by "수정한 User (USERS.id)"
        Object problem_definition "문제 의"
        Object[] nodes "노드 배열"
        Object[] edges "엣지 배열"
        String note "메모"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    Mongo_LLM_Prompt {
        ObjectId _id PK "프롬프트 고유 id"
        Number workflow_id FK "WORKFLOWS.id"
        Number version "프롬프트 버전"
        Timestamp created_at "생성일시"
        Timestamp updated_at "수정일시"
        Number updated_by "수정한 User (USERS.id)"
        String name "프롬프트 이름"
        String description "프롬프트 설명"
        String prompt_text "프롬프트 텍스트"
        Object[] variables "변수 배열"
        String[] tags "태그 배열"
        String category "카테고리"
        Boolean is_template "템플릿 여부"
    }

    Mongo_LLM_Prompt_History {
        ObjectId _id PK "히스토리 고유 id"
        Number prompt_id FK "Mongo_LLM_Prompt._id"
        Number workflow_id FK "WORKFLOWS.id"
        Number version "히스토리 버전"
        Timestamp created_at "생성일시"
        Timestamp updated_at "수정일시"
        Number updated_by "수정한 User (USERS.id)"
        Object data "변경된 프롬프트 데이터 {
            name: String,
            description: String,
            prompt_text: String,
            variables: [{name, type, description}],
            tags: [String],
            category: String,
            is_template: Boolean
        }"
        String action "변경 타입 (CREATE, UPDATE, DELETE)"
    }

    WORKFLOWS ||--o{ Mongo_Workflow_History : "has workflow history"
    Mongo_Workflow_History ||--o{ Mongo_Agent_Graph_History : "has agent graph history"
    Mongo_Workflow_History ||--o{ Mongo_Knowledge_Graph_History : "has knowledge graph history"
    Mongo_Agent_Graph ||--o{ Mongo_LLM_Prompt : "references"
    Mongo_Agent_Graph_History ||--o{ Mongo_LLM_Prompt : "references"
    Mongo_Agent_Graph ||--|| Mongo_Agent_Graph_History : "has history"
    Mongo_Knowledge_Graph ||--|| Mongo_Knowledge_Graph_History : "has history"
