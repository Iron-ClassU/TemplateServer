```mermaid
flowchart TD
    Start([시작]) --> SystemA[시스템1: 클래스 데이터 수집]:::system
    SystemA --> |수집| ClassData[클래스명/커리큘럼/상세페이지/해시태그/선생님 프로필/준비물링크]
    
    SystemB[시스템2: 첫 영상 대본 추출]:::system --> |Whisper AI| Script[영상 대본]
    
    Partner{파트너 선생님?} --> |Yes| Interview[인터뷰 내용 추가]
    
    ClassData --> |input_data 업데이트시| Agent1[LLM Agent 1]:::agent
    Agent1 --> Output1[class_summary/class_goal/teacher_summary]:::output
    
    Script --> |input_data 업데이트시| Agent2[LLM Agent 2]:::agent
    Output1 --> Agent2
    Partner --> |Yes| Marketing[마케팅쪽 출력값]
    Marketing --> Agent2
    Agent2 --> Output2[appeal_point/learner_summary]:::output
    
    ReviewDB[(리뷰 DB)] --> |input_data 업데이트시| Agent3[LLM Agent 3]:::agent
    Agent3 --> Output3[learner_review]:::output
    
    Output1 --> Final[데이터 통합]
    Output2 --> Final
    Output3 --> Final
    
    Final --> Save[class_info]:::output2
    Save --> End([종료])

    classDef system fill:#FFA500,stroke:#000,color:#333
    classDef agent fill:#9370DB
    classDef output fill:#D3D3D3,stroke:#000,color:#333
    classDef output2 fill:#FFFFFF,stroke:#000,color:#333
```

## input 값 정리
1. LLM agent1 input_data
    - 클래스명 / 커리큘럼 / 상세페이지 / 해시태그 / 선생님 프로필
2. LLM agent2 input_data
    - LLM 에이전트 1 출력값(class_summary/class_goal/teacher_summary) + 영상 대본
    - (파트너의 경우) 인터뷰 내용 / 마케팅 출력값 추가 
3. LLM agent3 input_data
    - 리뷰 DB

## 업데이트 이벤트 (트리거)
- input_data 업데이트 시 에이전트 실행
- LLM 에이전트3의 경우, 리뷰 데이터 업데이를 기준으로 갈지, 주기로 갈지 고민지점임.




