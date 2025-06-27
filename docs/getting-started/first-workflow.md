# Premier workflow

Ce guide vous accompagne dans la création et l'exécution de votre premier workflow d'agents.

## Workflow simple : Echo Bot

Commençons par un workflow minimal qui transforme une entrée utilisateur.

### 1. Définition JSON

Créez un fichier `my_first_workflow.json` :

```json
{
  "name": "Echo Workflow",
  "description": "Mon premier workflow qui reformule l'entrée utilisateur",
  "start_node": "echo_agent",
  "nodes": [
    {
      "id": "echo_agent",
      "name": "Echo Agent",
      "type": "process",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "EchoBot",
        "system_prompt": "You are a friendly assistant. Rephrase the user's message in a more formal and structured way."
      }
    },
    {
      "id": "end",
      "name": "End",
      "type": "end",
      "agent_config": {}
    }
  ],
  "edges": [
    {"from_node": "echo_agent", "to_node": "end"}
  ]
}
```

### 2. Code d'exécution

Créez un fichier `run_my_workflow.py` :

```python
import asyncio
import json
from src.application.services import WorkflowService

async def main():
    # Charger le workflow
    with open("my_first_workflow.json", "r") as f:
        workflow_json = json.load(f)
    
    # Créer le service
    workflow_service = WorkflowService()
    
    # Données d'entrée
    input_data = "salut, comment ça va ?"
    
    # Exécuter le workflow
    result = await workflow_service.execute_workflow_from_json(
        workflow_json,
        input_data
    )
    
    print("🏁 Résultat :")
    print(result['final_result'])
    
    print(f"\n📊 Statistiques :")
    print(f"Étapes : {len(result['execution_history'])}")
    print(f"Itérations : {result['total_iterations']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Exécution

```bash
uv run run_my_workflow.py
```

**Résultat attendu :**
```
🏁 Résultat :
Bonjour ! Je me porte bien, merci de vous en enquérir. Comment puis-je vous assister aujourd'hui ?

📊 Statistiques :
Étapes : 2
Itérations : 2
```

## Workflow avec décision : Sentiment Analyzer

Créons maintenant un workflow qui prend des décisions.

### 1. Définition JSON

```json
{
  "name": "Sentiment Analysis Workflow",
  "description": "Analyse le sentiment et route vers la réponse appropriée",
  "start_node": "sentiment_analyzer",
  "nodes": [
    {
      "id": "sentiment_analyzer",
      "name": "Sentiment Analyzer",
      "type": "decision",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "SentimentAnalyzer",
        "node_type": "decision",
        "system_prompt": "Analyze the sentiment of the text and return JSON: {\"positive\": true/false, \"confidence\": 0.0-1.0, \"emotion\": \"joy|anger|sadness|neutral\"}"
      }
    },
    {
      "id": "positive_responder",
      "name": "Positive Responder",
      "type": "process",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "PositiveResponder",
        "system_prompt": "Generate an enthusiastic and supportive response to positive sentiment."
      }
    },
    {
      "id": "negative_responder",
      "name": "Negative Responder", 
      "type": "process",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "NegativeResponder",
        "system_prompt": "Generate an empathetic and helpful response to negative sentiment."
      }
    },
    {
      "id": "end",
      "name": "End",
      "type": "end",
      "agent_config": {}
    }
  ],
  "edges": [
    {"from_node": "sentiment_analyzer", "to_node": "positive_responder", "condition": "positive"},
    {"from_node": "sentiment_analyzer", "to_node": "negative_responder", "condition": "negative"},
    {"from_node": "positive_responder", "to_node": "end"},
    {"from_node": "negative_responder", "to_node": "end"}
  ]
}
```

### 2. Mise à jour de l'évaluateur

Ajoutez la condition `negative` dans `ConditionEvaluator` :

```python
# Dans src/core/condition_evaluator.py
def _evaluate_generic_condition(self, condition: str, result: Dict[str, Any], context: Dict[str, Any]) -> bool:
    # ... code existant ...
    
    # Conditions négatives
    negative_mappings = {
        "rejected": "approved",
        "failed": "passed", 
        "not_hired": "hired",
        "incomplete": "complete",
        "negative": "positive"  # Nouvelle condition
    }
```

### 3. Test du workflow

```python
import asyncio
import json
from src.application.services import WorkflowService

async def test_sentiment_workflow():
    with open("sentiment_workflow.json", "r") as f:
        workflow_json = json.load(f)
    
    workflow_service = WorkflowService()
    
    test_cases = [
        "Je suis tellement heureux aujourd'hui !",
        "Je me sens vraiment déprimé...",
        "C'est une journée normale."
    ]
    
    for text in test_cases:
        print(f"\n🧪 Test: '{text}'")
        result = await workflow_service.execute_workflow_from_json(workflow_json, text)
        print(f"➡️ Réponse: {result['final_result']}")

if __name__ == "__main__":
    asyncio.run(test_sentiment_workflow())
```

## Workflow avec boucle : Auto-amélioration

Créons un workflow qui s'améliore en boucle.

### 1. Définition JSON

```json
{
  "name": "Self-Improving Content",
  "description": "Génère et améliore du contenu en boucle",
  "start_node": "content_generator",
  "nodes": [
    {
      "id": "content_generator",
      "name": "Content Generator",
      "type": "process",
      "max_iterations": 3,
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "ContentGenerator",
        "system_prompt": "Generate or improve content based on input. If you receive feedback, incorporate it to make the content better."
      }
    },
    {
      "id": "quality_checker",
      "name": "Quality Checker",
      "type": "decision",
      "max_iterations": 3,
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "QualityChecker",
        "node_type": "decision",
        "system_prompt": "Evaluate content quality and return JSON: {\"approved\": true/false, \"score\": 0-100, \"feedback\": \"specific improvements needed\", \"final_review\": false}"
      }
    },
    {
      "id": "end",
      "name": "End",
      "type": "end",
      "agent_config": {}
    }
  ],
  "edges": [
    {"from_node": "content_generator", "to_node": "quality_checker"},
    {"from_node": "quality_checker", "to_node": "content_generator", "condition": "rejected_not_final"},
    {"from_node": "quality_checker", "to_node": "end", "condition": "approved"},
    {"from_node": "quality_checker", "to_node": "end", "condition": "final_review"}
  ]
}
```

## Bonnes pratiques pour débuter

### 1. Commencez simple

```json
// ✅ Bon premier workflow
{
  "nodes": [
    {"id": "single_agent", "type": "process", ...},
    {"id": "end", "type": "end", ...}
  ],
  "edges": [
    {"from_node": "single_agent", "to_node": "end"}
  ]
}

// ❌ Évitez la complexité initiale
{
  "nodes": [...10 agents avec boucles complexes...]
}
```

### 2. Testez chaque étape

```python
# Test d'un agent isolé
async def test_single_agent():
    agent_config = {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "system_prompt": "..."
    }
    
    agent = PydanticAgent(agent_config)
    result = await agent.execute("test input", {})
    print(f"Agent result: {result}")
```

### 3. Vérifiez les formats JSON

```python
# Pour les agents de décision
def validate_decision_output(result):
    if not isinstance(result, dict):
        raise ValueError("Decision agents must return dict")
    
    required_fields = ["approved"]  # ou "passed", "valid", etc.
    for field in required_fields:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")
```

### 4. Utilisez des prompts clairs

```json
// ✅ Bon prompt
{
  "system_prompt": "You are a content reviewer. Evaluate the content for clarity (40%), accuracy (30%), and engagement (30%). Return JSON: {\"approved\": true/false, \"score\": 0-100, \"feedback\": \"specific feedback\"}. Approve only if score >= 80."
}

// ❌ Prompt vague
{
  "system_prompt": "Review this content."
}
```

## Débogage courant

### Agent ne répond pas

```bash
# Vérifiez les variables d'environnement
echo $OPENAI_API_KEY

# Testez la connexion API
python -c "from openai import OpenAI; client = OpenAI(); print('API OK')"
```

### JSON invalide

```python
# Validez votre JSON
import json

try:
    with open("workflow.json") as f:
        workflow = json.load(f)
    print("JSON valide ✅")
except json.JSONDecodeError as e:
    print(f"JSON invalide ❌: {e}")
```

### Conditions ne fonctionnent pas

```python
# Vérifiez le format de sortie des agents de décision
result = await agent.execute(input_data, context)
print(f"Agent output type: {type(result)}")
print(f"Agent output: {result}")

# Doit être un dict pour les agents de décision
assert isinstance(result, dict), "Decision agents must return dict"
```

## Prochaines étapes

Une fois ces premiers workflows maîtrisés :

1. 🔄 [Explorez les workflows complexes](../examples/writer-reviewer.md)
2. 🎯 [Apprenez les conditions avancées](../workflow-definition/conditions.md)
3. 📊 [Comprenez l'échange de données](../workflow-definition/data-flow.md)
4. 🏗️ [Découvrez l'architecture](../architecture/overview.md)
