            Node(
                name="summarize_text",
                type=NodeType.LLM,
                model_name="gpt-4",
                description="텍스트 요약 생성",
                config=LLMNodeConfig(
                    prompt_id="Mongo_LLM_Prompt._id",
                    variables={
                        "input_text": "previous.output",
                        "max_length": "300",
                        "style": "concise"
                    }
                ),
                front_metadata=FrontMetadata({
                    position={"x": 360, "y": 130},
                    size={"width": 200, "height": 50},
                    style={
                        "body": {
                            "fill": "#e6f3ff",
                            "stroke": "#0066cc"
                        },
                        "label": {
                            "text": "Vector Database",
                            "fill": "#000000"
                        }
                    }
                })
            ),

            # 데이터 노드 예시
            Node(
                name="fetch_documents",
                type=NodeType.DATA,
                type_id="vector_store",
                description="관련 문서 검색",
                config=DataNodeConfig(
                    dataset_id="customer_support_docs_v2"
                ),
                front_metadata=FrontMetadata({
                    position={"x": 360, "y": 130},
                    size={"width": 200, "height": 50},
                    style={
                        "body": {
                            "fill": "#e6f3ff",
                            "stroke": "#0066cc"
                        },
                        "label": {
                            "text": "Vector Database",
                            "fill": "#000000"
                        }
                    }
                })
            ),

            # ML 노드 예시
            Node(
                name="classify_intent",
                type=NodeType.ML,
                type_id="classification",
                description="사용자 의도 분류",
                config=MLNodeConfig(
                    model_id="intent_classifier_v1",
                    parameters={
                        "threshold": 0.7,
                        "top_k": 3
                    }
                ),
                front_metadata=FrontMetadata(...)
            ),

            # 라우터 노드 예시
            Node(
                name="confidence_router",
                type=NodeType.ROUTER,
                type_id="condition",
                description="신뢰도 기반 라우팅",
                config=RouterNodeConfig(
                    next_nodes=["human_review", "auto_reply", "escalate"],
                    conditions={
                        "confidence > 0.9": "auto_reply",
                        "confidence > 0.7": "human_review",
                        "default": "escalate"
                    }
                ),
                front_metadata=FrontMetadata(...)
            )

            Edge(
                id="edge1",
                source="fetch_context",
                target="generate_answer",
                type=EdgeType.DEFAULT,
                front_metadata={
                    "router": {"name": "manhattan"},
                    "connector": {"name": "rounded"}
                }
            ),
            Edge(
                id="edge2",
                source="generate_answer",
                target="quality_check",
                type=EdgeType.DEFAULT,
                front_metadata={
                    "router": {"name": "manhattan"},
                    "connector": {"name": "rounded"}
                }
            )
