WRITER_REVIEWER_WORKFLOW = {
    "name": "Writer-Reviewer Workflow",
    "description": "Workflow d'écriture avec révision et feedback",
    "start_node": "writer",
    "nodes": [
        {
            "id": "writer",
            "name": "Content Writer",
            "type": "process",
            "max_iterations": 5,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Writer",
                "system_prompt": "You are a professional content writer. Create high-quality content based on the requirements.",
            },
        },
        {
            "id": "reviewer",
            "name": "Content Reviewer",
            "type": "decision",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Reviewer",
                "system_prompt": "You are a content reviewer. Evaluate the content and return {approved: true/false, feedback: 'your feedback'}.",
            },
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "writer", "to_node": "reviewer"},
        {"from_node": "reviewer", "to_node": "end", "condition": "approved"},
        {"from_node": "reviewer", "to_node": "writer", "condition": "rejected"},
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
