# Database DDL
## MySQL Tables

### USERS
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '유저 고유번호',
    username VARCHAR(255) NOT NULL COMMENT '유저 이름',
    password VARCHAR(255) NOT NULL COMMENT '유저 비밀번호',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT '유저 이메일',
    activated BOOLEAN DEFAULT FALSE COMMENT '활성 여부 1: 활성, 0: 비활성',
    activation_code VARCHAR(255) COMMENT '유저 인증 해시 코드',
    activated_at DATETIME COMMENT '유저 인증 일시',
    last_login DATETIME COMMENT '마지막 로그인 일시',
    last_ip VARCHAR(45) COMMENT '마지막 로그인 IP',
    device_type VARCHAR(50) COMMENT '디바이스 종류',
    photo VARCHAR(255) COMMENT '프로필 사진 URL',
    social JSON COMMENT '소셜 로그인 정보',
    reset_code VARCHAR(255) COMMENT '비밀번호 찾기 코드',
    reset_code_expired_at DATETIME COMMENT '비밀번호 찾기 코드 만료일시',
    provider VARCHAR(20) DEFAULT 'local' COMMENT '인증 제공자',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
);
```

### API_KEY
```sql
CREATE TABLE api_key (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'API 키 고유번호',
    key_id VARCHAR(40) NOT NULL UNIQUE COMMENT 'API 키 ID (UUID)',
    user_id BIGINT NOT NULL COMMENT 'USERS.id',
    secret_key VARCHAR(255) NOT NULL COMMENT '해시된 API 키',
    name VARCHAR(255) NOT NULL COMMENT 'API 키 이름',
    type ENUM('session', 'restapi') NOT NULL DEFAULT 'session' COMMENT 'API 키 유형',
    status ENUM('ACTIVE', 'REVOKED', 'EXPIRED') DEFAULT 'ACTIVE' COMMENT 'API 키 상태',
    expired_at DATETIME COMMENT '만료일시',
    scopes TEXT DEFAULT '*' COMMENT '권한 범위 (콤마로 구분된 문자열)',
    provider VARCHAR(255) DEFAULT '' COMMENT '서비스 제공자',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시'
);
```

### PROJECTS
```sql
CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '프로젝트 고유 번호',
    key VARCHAR(255) UNIQUE NOT NULL COMMENT '프로젝트 키',
    user_id BIGINT NOT NULL COMMENT '생성자 ID',
    name VARCHAR(255) NOT NULL COMMENT '프로젝트명',
    goal TEXT COMMENT '프로젝트 목표',
    description TEXT COMMENT '프로젝트 설명',
    howto TEXT COMMENT '프로젝트 해결 방법',
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE' COMMENT '활성 여부',
    delete_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '삭제 여부',
    open_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '오픈 여부',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    deleted_at DATETIME COMMENT '삭제일시',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### PROJECT_MEMBERS
```sql
CREATE TABLE project_members (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '프로젝트 멤버 고유번호',
    project_id BIGINT NOT NULL COMMENT '프로젝트 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    role ENUM('VIEWER', 'COMMENTER', 'EDITOR', 'ADMIN') DEFAULT 'VIEWER' COMMENT '멤버 역할',
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE' COMMENT '상태',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### PROJECT_MEMBERSHIP_REQUESTS
```sql
CREATE TABLE project_membership_requests (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '프로젝트 요청 고유번호',
    project_id BIGINT NOT NULL COMMENT '프로젝트 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    request_type ENUM('JOIN_REQUEST', 'INVITE', 'ROLE_CHANGE', 'REMOVE') NOT NULL COMMENT '요청 타입',
    role ENUM('VIEWER', 'COMMENTER', 'EDITOR', 'ADMIN') NOT NULL COMMENT '요청 역할',
    status ENUM('PENDING', 'ACCEPTED', 'DECLINED', 'CANCELED') DEFAULT 'PENDING' COMMENT '요청 상태',
    message TEXT COMMENT '요청 메시지',
    requester_id BIGINT NOT NULL COMMENT '요청자 ID',
    responder_id BIGINT COMMENT '응답자 ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (requester_id) REFERENCES users(id),
    FOREIGN KEY (responder_id) REFERENCES users(id)
);
```

### WORKFLOWS
```sql
CREATE TABLE workflows (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '워크플로우 고유 아이디',
    project_id BIGINT NOT NULL COMMENT '프로젝트 ID',
    parent_id BIGINT COMMENT '상위 워크플로우 ID',
    user_id BIGINT NOT NULL COMMENT '생성자 ID',
    is_folder ENUM('Y', 'N') DEFAULT 'N' COMMENT '폴더 여부',
    is_main ENUM('Y', 'N') DEFAULT 'N' COMMENT '메인 워크플로우 여부',
    open_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '오픈 여부',
    agent_graph_id VARCHAR(24) COMMENT 'Mongo Agent Graph ID',
    knowledge_graph_id VARCHAR(24) COMMENT 'Mongo Knowledge Graph ID',
    name VARCHAR(255) NOT NULL COMMENT '워크플로우 이름',
    goal TEXT COMMENT '목표',
    description TEXT COMMENT '설명',
    delete_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '삭제 여부',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    deleted_at DATETIME COMMENT '삭제일시',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (parent_id) REFERENCES workflows(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### DATASETS
```sql
CREATE TABLE datasets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '데이터셋 고유번호',
    project_id BIGINT NOT NULL COMMENT '프로젝트 ID',
    parent_id BIGINT COMMENT '상위 데이터셋 ID',
    user_id BIGINT NOT NULL COMMENT '생성자 ID',
    data_type ENUM('RAW', 'MODEL') NOT NULL COMMENT '데이터 타입',
    file_type VARCHAR(50) COMMENT '파일 종류 (RAW 타입)',
    link VARCHAR(255) COMMENT '파일 링크 (RAW 타입)',
    mongodb_collection VARCHAR(255) COMMENT 'MongoDB 컬렉션명 (RAW 타입)',
    model_id VARCHAR(24) COMMENT 'Mongo Data Model ID (MODEL 타입)',
    delete_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '삭제 여부',
    is_folder ENUM('Y', 'N') DEFAULT 'N' COMMENT '폴더 여부',
    open_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '공개 여부',
    name VARCHAR(255) NOT NULL COMMENT '데이터셋 이름',
    description TEXT COMMENT '데이터셋 설명',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (parent_id) REFERENCES datasets(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### AGENTS
```sql
CREATE TABLE agents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '에이전트 고유 번호',
    project_id BIGINT NOT NULL COMMENT '프로젝트 ID',
    parent_id BIGINT COMMENT '상위 에이전트 ID',
    user_id BIGINT NOT NULL COMMENT '생성자 ID',
    delete_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '삭제 여부',
    is_folder ENUM('Y', 'N') DEFAULT 'N' COMMENT '폴더 여부',
    open_yn ENUM('Y', 'N') DEFAULT 'N' COMMENT '오픈 여부',
    name VARCHAR(255) NOT NULL COMMENT '에이전트 이름',
    description TEXT COMMENT '에이전트 설명',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    deleted_at DATETIME COMMENT '삭제일시',
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (parent_id) REFERENCES agents(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## MongoDB Collections

### agent_graph
```javascript
db.createCollection("agent_graph", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflow_id", "version", "created_at", "updated_by", "is_agent", "nodes", "edges"],
            properties: {
                workflow_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                is_agent: { bsonType: "bool" },
                agent_id: { bsonType: "number" },
                nodes: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "type", "data"],
                        properties: {
                            id: { bsonType: "string" },
                            type: { enum: ["llm", "tool", "machine", "data", "function"] },
                            data: { bsonType: "object" },
                            reference: {
                                bsonType: "object",
                                properties: {
                                    llm_prompt_id: { bsonType: "objectId" },
                                    tool_name: { bsonType: "string" },
                                    machine_id: { bsonType: "string" },
                                    data_id: { bsonType: "string" },
                                    function_name: { bsonType: "string" }
                                }
                            }
                        }
                    }
                },
                edges: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["source", "target"],
                        properties: {
                            source: { bsonType: "string" },
                            target: { bsonType: "string" },
                            data: { bsonType: "object" }
                        }
                    }
                }
            }
        }
    }
});
```

### knowledge_graph
```javascript
db.createCollection("knowledge_graph", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflow_id", "version", "created_at", "updated_by", "problem_definition", "nodes", "edges"],
            properties: {
                workflow_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                problem_definition: {
                    bsonType: "object",
                    required: ["context", "objectives", "resources", "problem_classification"],
                    properties: {
                        context: {
                            bsonType: "object",
                            properties: {
                                background: { bsonType: "string" },
                                current_situation: { bsonType: "string" },
                                pain_points: { bsonType: "array", items: { bsonType: "string" } }
                            }
                        },
                        objectives: {
                            bsonType: "object",
                            properties: {
                                primary_goal: { bsonType: "string" },
                                sub_goals: { bsonType: "array", items: { bsonType: "string" } },
                                success_criteria: { bsonType: "array", items: { bsonType: "string" } }
                            }
                        },
                        resources: {
                            bsonType: "object",
                            properties: {
                                available_data: { bsonType: "array", items: { bsonType: "string" } },
                                constraints: { bsonType: "array", items: { bsonType: "string" } },
                                requirements: { bsonType: "array", items: { bsonType: "string" } }
                            }
                        },
                        problem_classification: {
                            bsonType: "object",
                            properties: {
                                domain: { bsonType: "array", items: { bsonType: "string" } },
                                complexity: { bsonType: "string" },
                                difficulty: { bsonType: "string" },
                                project_type: { bsonType: "string" }
                            }
                        }
                    }
                },
                nodes: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "type", "data"],
                        properties: {
                            id: { bsonType: "string" },
                            type: { bsonType: "string" },
                            data: { bsonType: "object" }
                        }
                    }
                },
                edges: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["source", "target"],
                        properties: {
                            source: { bsonType: "string" },
                            target: { bsonType: "string" },
                            data: { bsonType: "object" }
                        }
                    }
                },
                note: { bsonType: "string" }
            }
        }
    }
});
```

### data_model
```javascript
db.createCollection("data_model", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "json_data", "created_at", "updated_at"],
            properties: {
                name: { bsonType: "string" },
                description: { bsonType: "string" },
                json_data: { bsonType: "object" },
                created_at: { bsonType: "date" },
                updated_at: { bsonType: "date" }
            }
        }
    }
});
```

### llm_prompt
```javascript
db.createCollection("llm_prompt", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflow_id", "version", "created_at", "updated_by", "name", "prompt_text"],
            properties: {
                workflow_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                name: { bsonType: "string" },
                description: { bsonType: "string" },
                prompt_text: { bsonType: "string" },
                variables: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["name", "type"],
                        properties: {
                            name: { bsonType: "string" },
                            type: { bsonType: "string" },
                            description: { bsonType: "string" }
                        }
                    }
                },
                tags: { bsonType: "array", items: { bsonType: "string" } },
                category: { bsonType: "string" },
                is_template: { bsonType: "bool" }
            }
        }
    }
});
```

### History Collections

각 히스토리 컬렉션(project_history, project_member_history, dataset_history, agent_history, workflow_history, agent_graph_history, knowledge_graph_history, llm_prompt_history)은 다음과 같은 기본 구조를 따릅니다:

```javascript
db.createCollection("<entity>_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["<entity>_id", "version", "created_at", "updated_by", "data", "action"],
            properties: {
                <entity>_id: { bsonType: "number" },  // ObjectId for MongoDB entities
                project_id: { bsonType: "number" },   // if applicable
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                data: { bsonType: "object" },         // entity-specific data structure
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

각 히스토리 컬렉션의 data 필드는 해당 엔터티의 구조를 따릅니다.

### project_history
```javascript
db.createCollection("project_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["project_id", "version", "created_at", "updated_by", "data", "action"],
            properties: {
                project_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                data: {
                    bsonType: "object",
                    required: ["name", "goal", "description", "howto", "open_yn", "status", "delete_yn"],
                    properties: {
                        name: { bsonType: "string" },
                        goal: { bsonType: "string" },
                        description: { bsonType: "string" },
                        howto: { bsonType: "string" },
                        open_yn: { bsonType: "string" },
                        status: { bsonType: "string" },
                        delete_yn: { bsonType: "string" }
                    }
                },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### project_member_history
```javascript
db.createCollection("project_member_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["project_member_id", "project_id", "version", "created_at", "updated_by", "data", "action"],
            properties: {
                project_member_id: { bsonType: "number" },
                project_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                data: {
                    bsonType: "object",
                    required: ["user_id", "role", "status"],
                    properties: {
                        user_id: { bsonType: "number" },
                        role: { bsonType: "string" },
                        status: { bsonType: "string" }
                    }
                },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### dataset_history
```javascript
db.createCollection("dataset_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["dataset_id", "project_id", "version", "created_at", "updated_by", "data", "action"],
            properties: {
                dataset_id: { bsonType: "number" },
                project_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                data: {
                    bsonType: "object",
                    required: ["name", "description", "data_type"],
                    properties: {
                        parent_id: { bsonType: "number" },
                        name: { bsonType: "string" },
                        description: { bsonType: "string" },
                        data_type: { bsonType: "string" },
                        file_type: { bsonType: "string" },
                        link: { bsonType: "string" },
                        mongodb_collection: { bsonType: "string" },
                        is_folder: { bsonType: "string" },
                        open_yn: { bsonType: "string" },
                        delete_yn: { bsonType: "string" }
                    }
                },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### agent_history
```javascript
db.createCollection("agent_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["agent_id", "project_id", "version", "created_at", "updated_by", "data", "action"],
            properties: {
                agent_id: { bsonType: "number" },
                project_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                data: {
                    bsonType: "object",
                    required: ["name", "description"],
                    properties: {
                        parent_id: { bsonType: "number" },
                        name: { bsonType: "string" },
                        description: { bsonType: "string" },
                        is_folder: { bsonType: "string" },
                        open_yn: { bsonType: "string" },
                        delete_yn: { bsonType: "string" }
                    }
                },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### workflow_history
```javascript
db.createCollection("workflow_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflow_history_id", "workflow_id", "version", "created_at", "updated_by", "action"],
            properties: {
                workflow_history_id: { bsonType: "number" },
                workflow_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                agent_graph_version_id: { bsonType: "string" },
                knowledge_graph_version_id: { bsonType: "string" },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### agent_graph_history
```javascript
db.createCollection("agent_graph_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflow_history_id", "version", "created_at", "updated_by", "nodes", "edges", "action"],
            properties: {
                workflow_history_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                agents: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "type", "config"],
                        properties: {
                            id: { bsonType: "string" },
                            type: { bsonType: "string" },
                            config: { bsonType: "object" }
                        }
                    }
                },
                nodes: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "type", "data"],
                        properties: {
                            id: { bsonType: "string" },
                            type: { enum: ["llm", "tool", "machine", "data", "function"] },
                            data: { bsonType: "object" },
                            reference: {
                                bsonType: "object",
                                properties: {
                                    llm_prompt_id: { bsonType: "objectId" },
                                    tool_name: { bsonType: "string" },
                                    machine_id: { bsonType: "string" },
                                    data_id: { bsonType: "string" },
                                    function_name: { bsonType: "string" }
                                }
                            }
                        }
                    }
                },
                edges: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["source", "target"],
                        properties: {
                            source: { bsonType: "string" },
                            target: { bsonType: "string" },
                            data: { bsonType: "object" }
                        }
                    }
                },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### knowledge_graph_history
```javascript
db.createCollection("knowledge_graph_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflow_history_id", "version", "created_at", "updated_by", "problem_definition", "nodes", "edges", "action"],
            properties: {
                workflow_history_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                problem_definition: {
                    bsonType: "object",
                    required: ["context", "objectives", "resources", "problem_classification"],
                    properties: {
                        context: {
                            bsonType: "object",
                            properties: {
                                background: { bsonType: "string" },
                                current_situation: { bsonType: "string" },
                                pain_points: { bsonType: "array", items: { bsonType: "string" } }
                            }
                        },
                        objectives: {
                            bsonType: "object",
                            properties: {
                                primary_goal: { bsonType: "string" },
                                sub_goals: { bsonType: "array", items: { bsonType: "string" } },
                                success_criteria: { bsonType: "array", items: { bsonType: "string" } }
                            }
                        },
                        resources: {
                            bsonType: "object",
                            properties: {
                                available_data: { bsonType: "array", items: { bsonType: "string" } },
                                constraints: { bsonType: "array", items: { bsonType: "string" } },
                                requirements: { bsonType: "array", items: { bsonType: "string" } }
                            }
                        },
                        problem_classification: {
                            bsonType: "object",
                            properties: {
                                domain: { bsonType: "array", items: { bsonType: "string" } },
                                complexity: { bsonType: "string" },
                                difficulty: { bsonType: "string" },
                                project_type: { bsonType: "string" }
                            }
                        }
                    }
                },
                nodes: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "type", "data"],
                        properties: {
                            id: { bsonType: "string" },
                            type: { bsonType: "string" },
                            data: { bsonType: "object" }
                        }
                    }
                },
                edges: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["source", "target"],
                        properties: {
                            source: { bsonType: "string" },
                            target: { bsonType: "string" },
                            data: { bsonType: "object" }
                        }
                    }
                },
                note: { bsonType: "string" },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```

### llm_prompt_history
```javascript
db.createCollection("llm_prompt_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["prompt_id", "workflow_id", "version", "created_at", "updated_by", "data", "action"],
            properties: {
                prompt_id: { bsonType: "objectId" },
                workflow_id: { bsonType: "number" },
                version: { bsonType: "number" },
                created_at: { bsonType: "date" },
                updated_by: { bsonType: "number" },
                data: {
                    bsonType: "object",
                    required: ["name", "prompt_text"],
                    properties: {
                        name: { bsonType: "string" },
                        description: { bsonType: "string" },
                        prompt_text: { bsonType: "string" },
                        variables: {
                            bsonType: "array",
                            items: {
                                bsonType: "object",
                                required: ["name", "type"],
                                properties: {
                                    name: { bsonType: "string" },
                                    type: { bsonType: "string" },
                                    description: { bsonType: "string" }
                                }
                            }
                        },
                        tags: { bsonType: "array", items: { bsonType: "string" } },
                        category: { bsonType: "string" },
                        is_template: { bsonType: "bool" }
                    }
                },
                action: { enum: ["CREATE", "UPDATE", "DELETE"] }
            }
        }
    }
});
```