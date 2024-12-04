```mermaid
flowchart TD
    %% Input Data
    A[수강생 대화 raw_data] --> C[LLM Agent 1]
    A --> D[LLM Agent 2]
    A --> E[LLM Agent 3]
    B[user_log_event_data] --> F[LLM Agent 4]
    G[설문조사 출력값]

    %% LLM Agents Processing
    C --> H[recent_conversation_summary]
    D --> I[life_event_summary]

    E --> J[interest]
    F --> K[log_event_summary]
    G --> L[goal_setting]

    %% Final Output
    H --> M[history]
    I --> M
    J --> M
    K --> M
    L --> M

    %% Styling
    style A fill:#FFA500,stroke:#333,color:#333
    style B fill:#FFA500,stroke:#333,color:#333
    style C fill:#9370DB,stroke:#333
    style D fill:#9370DB,stroke:#333
    style E fill:#9370DB,stroke:#333
    style F fill:#9370DB,stroke:#333
    style G fill:#FFA500,stroke:#333,color:#333
    style M fill:#FFFFFF,stroke:#333,color:#333

```

## input 값 정리
1. LLM agent1, 2, 3 input_data
    - 수강생 대화 raw_data
2. LLM agent4 input_data
    - user_log_event_data 

## 업데이트 이벤트 (트리거)
- agent 1, 2, 3
    - raw_data가 10,000토큰 쌓였을 경우.
- agent 4 update
    - 다른 프롬프트에서 history 참조 필요 시, update 진행.