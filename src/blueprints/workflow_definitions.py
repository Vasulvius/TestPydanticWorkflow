MONO_AGENT_WITH_TOOLS = {
    "name": "Mono Agent with Tools",
    "description": "Un seul agent avec des outils pour traiter les messages utilisateur",
    "start_node": "assistant",
    "nodes": [
        {
            "id": "assistant",
            "name": "Assistant with Tools",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "AssistantAgent",
                "system_prompt": """Tu es un assistant intelligent avec accès à plusieurs outils.

INSTRUCTIONS:
1. Analyse la demande de l'utilisateur
2. Utilise les outils appropriés pour enrichir ta réponse
3. Fournis une réponse complète et utile

OUTILS DISPONIBLES:
- word_count: Pour analyser la longueur des textes
- current_time: Pour obtenir la date/heure actuelle
- grammar_check: Pour vérifier la grammaire

Utilise ces outils quand ils sont pertinents pour répondre à la demande.""",
            },
            "tools": ["word_count", "current_time", "grammar_check"],
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [{"from_node": "assistant", "to_node": "end"}],
}

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
                "node_type": "decision",
                "system_prompt": """You are a content reviewer. Evaluate the content against the original manager instructions.

                You MUST respond with ONLY a JSON object in this EXACT format:
                {"approved": true, "feedback": "your feedback here", "final_review": false}

                Guidelines:
                - Set "approved" to true only if the content fully meets requirements
                - Set "final_review" to true if this is the 3rd iteration
                - Keep feedback concise and actionable""",
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

ADVANCED_CONTENT_WORKFLOW = {
    "name": "Advanced Content Creation with Review",
    "description": "Workflow complet avec recherche, rédaction et révision",
    "start_node": "researcher",
    "nodes": [
        {
            "id": "researcher",
            "name": "Content Researcher",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Researcher",
                "system_prompt": """Tu es un chercheur expert. Effectue une recherche approfondie sur le sujet donné.

INSTRUCTIONS:
1. Analyse le sujet et l'audience cible
2. Identifie 5-7 points clés à couvrir
3. Trouve des exemples concrets et actuels
4. Propose une structure logique pour l'article

RÉPONSE:
- **Sujet analysé**: [résumé du sujet]
- **Points clés**: [liste des points principaux]
- **Exemples**: [exemples concrets à inclure]
- **Structure proposée**: [plan de l'article]
- **Angle d'approche**: [perspective à adopter]""",
            },
            "tools": ["current_time", "http_request"],
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
                "system_prompt": """Tu es un rédacteur expert. Crée un article de qualité basé sur les recherches.

INSTRUCTIONS:
1. Suis la structure proposée par le chercheur
2. Écris un titre accrocheur (H1)
3. Rédige une introduction engageante
4. Développe chaque section avec des sous-titres (H2, H3)
5. Inclus les exemples fournis par le chercheur
6. Termine par une conclusion avec appel à l'action
7. Utilise les outils pour vérifier la qualité

FORMAT:
# Titre Principal
## Introduction
[contenu introduction]

## Section 1
[contenu avec exemples]

## Section 2
[contenu avec exemples]

## Conclusion
[résumé et appel à l'action]""",
            },
            "tools": ["word_count", "grammar_check"],
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
                "node_type": "decision",
                "system_prompt": """Tu es un réviseur expert. Évalue la qualité de l'article.

CRITÈRES D'ÉVALUATION:
- Structure claire avec titres et sous-titres
- Contenu informatif et pertinent
- Exemples concrets et utiles
- Respect du ton et de l'audience
- Longueur appropriée
- Qualité rédactionnelle

RÉPONSE JSON OBLIGATOIRE:
{
  "approved": true/false,
  "feedback": "commentaires détaillés sur les améliorations",
  "score": 0-100,
  "missing_elements": ["liste des éléments manquants"],
  "final_review": false
}""",
            },
            "tools": ["word_count"],
        },
        {
            "id": "finalizer",
            "name": "Content Finalizer",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Finalizer",
                "system_prompt": """Tu es responsable de présenter l'article final.

INSTRUCTIONS:
Tu recevras soit :
1. Un article approuvé par le reviewer
2. Un article après le nombre maximum d'itérations

Dans les deux cas, extrais et présente UNIQUEMENT l'article final, sans commentaires ni métadonnées.

Si tu reçois un objet JSON avec des métadonnées, trouve l'article dans les données d'historique et présente-le proprement.

RÉPONSE ATTENDUE: L'article complet, bien formaté, prêt à être publié.""",
            },
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "researcher", "to_node": "writer"},
        {"from_node": "writer", "to_node": "reviewer"},
        {"from_node": "reviewer", "to_node": "writer", "condition": "rejected_not_final"},
        {"from_node": "reviewer", "to_node": "finalizer", "condition": "approved"},
        {"from_node": "reviewer", "to_node": "finalizer", "condition": "final_review"},
        {"from_node": "finalizer", "to_node": "end"},
    ],
}

TOOLS_TEST_WORKFLOW = {
    "name": "Tools Testing Workflow",
    "description": "Workflow pour tester l'utilisation des outils et les itérations",
    "start_node": "researcher",
    "nodes": [
        {
            "id": "researcher",
            "name": "Research Agent",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Researcher",
                "system_prompt": """Tu es un chercheur qui DOIT utiliser ses outils.

INSTRUCTIONS OBLIGATOIRES:
1. Utilise l'outil 'current_time' pour obtenir la date
2. Utilise l'outil 'word_count' pour analyser ton texte de sortie
3. Mentionne explicitement dans ta réponse quand tu utilises chaque outil

RÉPONSE ATTENDUE:
Un rapport de recherche incluant :
- La date actuelle obtenue via l'outil
- Le nombre de mots de ton rapport via l'outil
- Des informations pertinentes sur le sujet""",
            },
            "tools": ["current_time", "word_count"],
        },
        {
            "id": "strict_reviewer",
            "name": "Strict Reviewer",
            "type": "decision",
            "max_iterations": 3,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "StrictReviewer",
                "node_type": "decision",
                "system_prompt": """Tu es un réviseur TRÈS STRICT qui teste les itérations.

STRATÉGIE DE TEST:
- Itération 1: TOUJOURS rejeter (approved: false)
- Itération 2: Approuver si qualité correcte (approved: true)
- Itération 3+: Forcer l'approbation (final_review: true)

UTILISE L'OUTIL word_count pour analyser le contenu.

RÉPONSE JSON OBLIGATOIRE:
{
  "approved": true/false,
  "feedback": "commentaires spécifiques",
  "iteration_number": <numéro_actuel>,
  "word_analysis": "résultat de word_count",
  "final_review": false
}""",
            },
            "tools": ["word_count"],
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
                "system_prompt": """Tu es un rédacteur qui s'améliore à chaque itération.

INSTRUCTIONS:
1. Utilise l'outil 'word_count' pour vérifier la longueur
2. Si tu reçois du feedback, améliore le contenu
3. Mentionne le numéro d'itération dans ton article
4. Intègre les suggestions de façon visible

OBJECTIF: Créer un article qui s'améliore à chaque révision.""",
            },
            "tools": ["word_count", "grammar_check"],
        },
        {
            "id": "finalizer",
            "name": "Final Processor",
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Finalizer",
                "system_prompt": """Tu présentes le résultat final avec statistiques.

Utilise l'outil word_count pour donner les métriques finales.""",
            },
            "tools": ["word_count"],
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "researcher", "to_node": "writer"},
        {"from_node": "writer", "to_node": "strict_reviewer"},
        {"from_node": "strict_reviewer", "to_node": "writer", "condition": "rejected_not_final"},
        {"from_node": "strict_reviewer", "to_node": "finalizer", "condition": "approved"},
        {"from_node": "strict_reviewer", "to_node": "finalizer", "condition": "final_review"},
        {"from_node": "finalizer", "to_node": "end"},
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
                "system_prompt": """You are a requirement analyst. Analyze the user requirements and create detailed technical specifications.

                Transform the requirements into clear development specifications including:
                - Functional requirements
                - Technical constraints
                - Architecture guidelines
                - Success criteria

                Provide clear, actionable specifications for the developer.""",
            },
        },
        {
            "id": "developer",
            "name": "Developer",
            "type": "decision",
            "max_iterations": 3,
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Developer",
                "node_type": "decision",
                "system_prompt": """You are a software developer. Write code based on the analyst specifications.

                You MUST respond with ONLY a JSON object:
                {"complete": true, "code": "your code here", "description": "what you implemented"}

                Set "complete" to:
                - true if you have fully implemented all requirements
                - false if you need more iterations to finish""",
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
                "node_type": "decision",
                "system_prompt": """You are a software tester. Test the provided code for bugs and issues.

                You MUST respond with ONLY a JSON object:
                {"has_bugs": false, "test_report": "detailed test report", "severity": "low"}

                Set "has_bugs" to:
                - true if you find any bugs or issues
                - false if the code passes all tests""",
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
                "system_prompt": """You are a release manager. Prepare the final release package and deployment instructions.""",
            },
        },
        {"id": "end", "name": "End", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "analyst", "to_node": "developer"},
        {"from_node": "developer", "to_node": "developer", "condition": "incomplete"},
        {"from_node": "developer", "to_node": "tester", "condition": "complete"},
        {"from_node": "tester", "to_node": "developer", "condition": "has_issues"},
        {"from_node": "tester", "to_node": "release_manager", "condition": "no_issues"},
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
            "type": "process",
            "agent_config": {
                "type": "pydantic",
                "model": "openai:gpt-4o-mini",
                "name": "Candidate",
                "system_prompt": """You are processing a job candidate application.

                Prepare the candidate profile for the hiring process.""",
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
                "node_type": "decision",
                "system_prompt": """You are an HR recruiter conducting initial screening.

                Respond with JSON: {"passed": true, "feedback": "detailed feedback", "score": 85}

                Set "passed" to true if candidate should proceed, false otherwise.""",
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
                "node_type": "decision",
                "system_prompt": """You are a technical interviewer assessing candidate's technical skills.

                Respond with JSON: {"passed": true, "score": 85, "technical_notes": "assessment"}""",
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
                "node_type": "decision",
                "system_prompt": """You are conducting the final interview to make the hiring decision.

                Respond with JSON: {"hired": true, "decision": "detailed decision", "salary_offer": 75000}""",
            },
        },
        {"id": "employee", "name": "Employee", "type": "end", "agent_config": {}},
        {"id": "rejected", "name": "Rejected", "type": "end", "agent_config": {}},
    ],
    "edges": [
        {"from_node": "candidate", "to_node": "hr_screening"},
        {"from_node": "hr_screening", "to_node": "rejected", "condition": "failed"},
        {"from_node": "hr_screening", "to_node": "technical_interview", "condition": "passed"},
        {"from_node": "technical_interview", "to_node": "rejected", "condition": "failed"},
        {"from_node": "technical_interview", "to_node": "final_interview", "condition": "passed"},
        {"from_node": "final_interview", "to_node": "employee", "condition": "hired"},
        {"from_node": "final_interview", "to_node": "rejected", "condition": "rejected"},
    ],
}
