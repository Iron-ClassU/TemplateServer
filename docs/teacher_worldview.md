```mermaid
flowchart TB
    Check{일반/파트너 선생님 여부} --> Input

    subgraph Input
        S1[System1]:::system
        S2[System2]:::system
        I[Interview data]
    end

    subgraph Process
        A1[LLM Agent]:::agent
    end

    subgraph Output
        DB[(teacher_worldview)]
    end
    
    Check -->|파트너| I
    I -->|파트너 인터뷰 데이터| A1
    
    S1 -->|클래스 데이터| S1_collect[클래스 데이터 수집]
    S1_collect -->|"클래스명
    커리큘럼
    상세페이지
    해시태그
    선생님 프로필"| A1
    
    S2 -->|영상 데이터| S2_collect[첫 번째 영상 대본 추출]
    S2_collect -->|"Whisper AI 
    대본 데이터"| A1
    
    A1 -->|세계관 추출| DB:::output
    
    Output[["teacher_worldview.txt
    1. educational_philosophy
    2. life_goal
    3. life_experience
    4. interest
    5. recent_thinking
    6. effective_methods
    7. tip"]]

    style Input fill:000000,stroke:#01579b
    style Process fill:000000,stroke:#e65100
    style Output fill:000000,stroke:#1b5e20
    style Check fill:#f3e5f5,stroke:#4a148c,color:#333
    style Output rectangle
    classDef system fill:#FFA500,stroke:#000,color:#333
    classDef agent fill:#9370DB,stroke:#000
    classDef output fill:#FFFFFF,stroke:#000,color:#333
```

## input 값 정리
1. LLM input_data
    - 시스템1이 수집한 클래스 txt 데이터
    - 시스템2가 수집한 첫 번째 영상 대본
    - (파트너의 경우) 파트너 인터뷰 데이터 -> 삽입 공간 필요.

## 업데이트 이벤트 (트리거)
- 시스템2에서 뱉는 첫 번째 영상 대본이 update 될 경우, 에이전트 실행
    - 영상이 변경되는 순간이 트리거.