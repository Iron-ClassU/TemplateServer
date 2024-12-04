``` json
{
    _id: ObjectId(),
    workflow_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    is_agent: Boolean,
    agent_id: Number,
    nodes: [{
        id: String,
        type: enum("llm", "tool", "machine", "data", "function"),
        data: Object,
        reference: {
            llm_prompt_id: ObjectId,
            tool_name: String,
            machine_id: String,
            data_id: String,
            function_name: String
        }
    }],
    edges: [{
        source: String,
        target: String,
        data: Object
    }]
}
```

// knowledge_graph 컬렉션
``` json
{
    _id: ObjectId(),
    workflow_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    problem_definition: {
        context: {
            background: String,
            current_situation: String,
            pain_points: [String]
        },
        objectives: {
            primary_goal: String,
            sub_goals: [String],
            success_criteria: [String]
        },
        resources: {
            available_data: [String],
            constraints: [String],
            requirements: [String]
        },
        problem_classification: {
            domain: [String],
            complexity: String,
            difficulty: String,
            project_type: String
        }
    },
    nodes: [{
        id: String,
        type: String,
        data: Object
    }],
    edges: [{
        source: String,
        target: String,
        data: Object
    }],
    note: String
}
```

// data_model 컬렉션
``` json
{
    _id: ObjectId(),
    name: String,
    description: String,
    json_data: Object,
    created_at: Timestamp,
    updated_at: Timestamp
}
```

// workflow_history 컬렉션
``` json
{
    _id: ObjectId(),
    workflow_history_id: Number,
    workflow_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    agent_graph_version_id: String,
    knowledge_graph_version_id: String,
    action: enum("CREATE", "UPDATE", "DELETE")
}
```

// agent_graph_history 컬렉션
``` json
{
    _id: ObjectId(),
    workflow_history_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    nodes: [{
        id: String,
        type: enum("llm", "tool", "machine", "data", "function"),
        data: Object,
        reference: {
            llm_prompt_id: ObjectId,
            tool_name: String,
            machine_id: String,
            data_id: String,
            function_name: String
        }
    }],
    edges: [{
        source: String,
        target: String,
        data: Object
    }],
    action: enum("CREATE", "UPDATE", "DELETE")
}
```

// llm_prompt 컬렉션
``` json
{
    _id: ObjectId(),
    workflow_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    name: String,
    description: String,
    prompt_text: String,
    variables: [{
        name: String,
        type: String,
        description: String
    }],
    tags: [String],
    category: String,
    is_template: Boolean
}
```

// project_history 컬렉션
``` json
{
    _id: ObjectId(),
    project_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    data: {
        name: String,
        goal: String,
        description: String,
        howto: String,
        open_yn: String,
        status: String,
        delete_yn: String
    },
    action: enum("CREATE", "UPDATE", "DELETE")
}
```

// project_member_history 컬렉션
``` json
{
    _id: ObjectId(),
    project_member_id: Number,
    project_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    data: {
        user_id: Number,
        role: String,
        status: String
    },
    action: enum("CREATE", "UPDATE", "DELETE")
}
```

// dataset_history 컬렉션
``` json
{
    _id: ObjectId(),
    dataset_id: Number,
    project_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    data: {
        parent_id: Number,
        name: String,
        description: String,
        data_type: String,
        file_type: String,
        link: String,
        mongodb_collection: String,
        is_folder: String,
        open_yn: String,
        delete_yn: String
    },
    action: enum("CREATE", "UPDATE", "DELETE")
}
```

// agent_history 컬렉션
``` json
{
    _id: ObjectId(),
    agent_id: Number,
    project_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    data: {
        parent_id: Number,
        name: String,
        description: String,
        graph_db_id: String,
        is_folder: String,
        open_yn: String,
        delete_yn: String
    },
    action: enum("CREATE", "UPDATE", "DELETE")
}
```

// llm_prompt_history 컬렉션
``` json
{
    _id: ObjectId(),
    prompt_id: ObjectId,
    workflow_id: Number,
    version: Number,
    created_at: Timestamp,
    updated_by: Number,
    data: {
        name: String,
        description: String,
        prompt_text: String,
        variables: [{
            name: String,
            type: String,
            description: String
        }],
        tags: [String],
        category: String,
        is_template: Boolean
    },
    action: enum("CREATE", "UPDATE", "DELETE")
}
```