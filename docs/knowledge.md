```mermaid
flowchart TD
    A[강의 영상] -->|Whisper AI| B[lecture_transcript <br> = raw_data]--> C[LLM Agent]
    C -->|추출| D[lecture_summary / 내용개요]
    C -->|추출| E[lecture_goal / 학습목표]
    C -->|추출| F[lecture_effect / 기대효과]
    C -->|추출| G[tip_summary / 팁 요약]
    D --> H[(knowledge DB)]
    E --> H
    F --> H
    G --> H
    
    %% Styling
    style B fill:#FFA500,stroke:#333,color:#333
    style C fill:#9370DB,stroke:#000
    style H fill:#FFFFFF,stroke:#333,color:#333
```

## input 값 정리
1. LLM agent input_data
    - 각 강의영상 별 lecture_transcript

## 업데이트 이벤트
- 새로운 강의가 추가되었을 시

## knowledge DB 구성
- class_id
- class_name
- lecture_id
- lecture_title
- mission
- lecutre_materials
- lecture_summary
- lecture_goal
- lecture_effect
- tip_summary