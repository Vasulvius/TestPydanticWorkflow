WRITER_REVIEWER_WORKFLOW = {
    "name": "Writer-Reviewer Workflow",
    "description": "Workflow d'écriture avec manager, révision et feedback",
    "start_node": "manager_initial",
    "nodes": [
        {
            "id": "manager_initial",
            "name": "Manager Initial",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Manager",
                "system_prompt": """You are a project manager. Take the user's request and reformulate it into clear, detailed instructions for a content writer.

                Transform the user request into specific writing instructions including:
                - The exact topic to cover
                - Target length and format
                - Key points to address
                - Writing style and tone
                - Any specific requirements

                Return your reformulated instructions as clear, actionable guidance for the writer.""",
            },
        },
        {
            "id": "writer",
            "name": "Content Writer",
            "type": "process",
            "max_iterations": 3,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Writer",
                "system_prompt": """You are a professional content writer. Follow the manager's instructions carefully to create high-quality content.

                If you receive feedback from a reviewer, incorporate it to improve your content while staying true to the original instructions.

                Create engaging, well-structured content that meets all the specified requirements.""",
            },
        },
        {
            "id": "reviewer",
            "name": "Content Reviewer",
            "type": "decision",
            "max_iterations": 3,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Reviewer",
                "node_type": "decision",  # Ajout pour identifier l'agent
                "system_prompt": """You are a content reviewer. Evaluate the content against the original manager instructions.

                You MUST respond with ONLY a JSON object in this EXACT format (no extra text):
                {"approved": true, "feedback": "your feedback here", "final_review": false}

                Guidelines:
                - Set "approved" to true only if the content fully meets requirements
                - Set "final_review" to true if this is the 3rd iteration
                - Keep feedback concise and actionable
                - DO NOT add any text before or after the JSON""",
            },
        },
        {
            "id": "manager_final",
            "name": "Manager Final",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Manager",
                "system_prompt": """You are a project manager providing the final response to the user.

                You will receive either:
                1. An approved article - present it professionally to the user
                2. A rejected article after maximum iterations - explain the situation and provide a summary

                Format your response appropriately based on whether the content was approved or not.""",
            },
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "manager_initial", "to_node": "writer"},
        {"from_node": "writer", "to_node": "reviewer"},
        {"from_node": "reviewer", "to_node": "writer", "condition": "rejected_not_final"},
        {"from_node": "reviewer", "to_node": "manager_final", "condition": "approved"},
        {"from_node": "reviewer", "to_node": "manager_final", "condition": "final_review"},
        {"from_node": "manager_final", "to_node": "end"},
    ],
}

DEVELOPMENT_WORKFLOW = {
    "name": "Software Development Workflow",
    "description": "Workflow de développement avec analyse, développement et tests",
    "start_node": "analyst",
    "nodes": [
        {
            "id": "analyst",
            "name": "Requirement Analyst",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Analyst",
                "system_prompt": "Analyze requirements and create detailed specifications.",
            },
        },
        {
            "id": "developer",
            "name": "Developer",
            "type": "process",
            "max_iterations": 3,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Developer",
                "system_prompt": "Write code based on specifications. Return {code: 'code', status: 'complete/incomplete'}.",
            },
        },
        {
            "id": "tester",
            "name": "Tester",
            "type": "decision",
            "max_iterations": 2,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Tester",
                "system_prompt": "Test the code and return {has_bugs: true/false, test_report: 'report'}.",
            },
        },
        {
            "id": "release_manager",
            "name": "Release Manager",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "ReleaseManager",
                "system_prompt": "Prepare the release and finalize deployment.",
            },
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "analyst", "to_node": "developer"},
        {"from_node": "developer", "to_node": "developer", "condition": "incomplete"},
        {"from_node": "developer", "to_node": "tester", "condition": "complete"},
        {"from_node": "tester", "to_node": "developer", "condition": "has_bugs"},
        {"from_node": "tester", "to_node": "release_manager", "condition": "no_bugs"},
        {"from_node": "release_manager", "to_node": "end"},
    ],
}

HIRING_WORKFLOW = {
    "name": "Hiring Process Workflow",
    "description": "Processus de recrutement avec plusieurs étapes",
    "start_node": "candidate",
    "nodes": [
        {
            "id": "candidate",
            "name": "Candidate",
            "type": "start",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Candidate",
                "system_prompt": "Process candidate application.",
            },
        },
        {
            "id": "hr_screening",
            "name": "HR Screening",
            "type": "decision",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "HRScreener",
                "system_prompt": "Screen candidate CV and return {passed: true/false, feedback: 'feedback'}.",
            },
        },
        {
            "id": "technical_interview",
            "name": "Technical Interview",
            "type": "decision",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "TechnicalInterviewer",
                "system_prompt": "Conduct technical interview and return {passed: true/false, score: number}.",
            },
        },
        {
            "id": "final_interview",
            "name": "Final Interview",
            "type": "decision",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "FinalInterviewer",
                "system_prompt": "Conduct final interview and return {hired: true/false, decision: 'reason'}.",
            },
        },
        {"id": "employee", "name": "Employee", "type": "end", "agent_config": {}},
        {"id": "rejected", "name": "Rejected", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "candidate", "to_node": "hr_screening"},
        {"from_node": "hr_screening", "to_node": "rejected", "condition": "rejected"},
        {"from_node": "hr_screening", "to_node": "technical_interview", "condition": "passed"},
        {"from_node": "technical_interview", "to_node": "rejected", "condition": "failed"},
        {"from_node": "technical_interview", "to_node": "final_interview", "condition": "passed"},
        {"from_node": "final_interview", "to_node": "employee", "condition": "hired"},
        {"from_node": "final_interview", "to_node": "rejected", "condition": "rejected"},
    ],
}
