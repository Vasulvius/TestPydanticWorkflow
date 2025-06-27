# Dynamic Agent Workflows

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic AI](https://img.shields.io/badge/pydantic--ai-0.3.4+-green.svg)](https://github.com/pydantic/pydantic-ai)

Framework Python interne pour créer et exécuter des workflows d'agents IA dynamiques basés sur JSON.

## 🎯 Présentation

Dynamic Agent Workflows permet de définir des workflows complexes d'agents IA via des fichiers JSON simples. Le framework gère automatiquement l'exécution, les transitions conditionnelles, les boucles de rétroaction et fournit un historique complet des exécutions.

### Exemple de workflow simple

```json
{
  "name": "Writer-Reviewer Workflow",
  "start_node": "writer",
  "nodes": [
    {
      "id": "writer",
      "name": "Content Writer",
      "type": "process",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "system_prompt": "You are a professional writer..."
      }
    },
    {
      "id": "reviewer", 
      "name": "Content Reviewer",
      "type": "decision",
      "agent_config": {
        "type": "pydantic",
        "system_prompt": "Review content and return JSON: {\"approved\": true/false}"
      }
    }
  ],
  "edges": [
    {"from_node": "writer", "to_node": "reviewer"},
    {"from_node": "reviewer", "to_node": "writer", "condition": "rejected"},
    {"from_node": "reviewer", "to_node": "end", "condition": "approved"}
  ]
}
```

## 🚀 Installation

### Prérequis

- Python 3.12+
- Variables d'environnement pour l'API OpenAI (ou autre modèle)

### Installation des dépendances

```bash
# Avec UV (recommandé)
uv install
```

### Configuration

Créez un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎮 Utilisation

### Exécution des exemples

```bash
# Lancer tous les workflows de test
uv run main.py --all

# Lancer seulement le workflow Writer-Reviewer
uv run main.py --writer

# Lancer les workflows de recrutement
uv run main.py --hiring

# Afficher l'aide
uv run main.py --help
```

### Utilisation programmatique

```python
import asyncio
from src.application.services import WorkflowService

async def main():
    workflow_service = WorkflowService()
    
    # Définir votre workflow JSON
    workflow_json = {
        "name": "Mon Workflow",
        "start_node": "start",
        # ... définition complète
    }
    
    # Données d'entrée
    input_data = {"message": "Hello World"}
    
    # Exécuter le workflow
    result = await workflow_service.execute_workflow_from_json(
        workflow_json, 
        input_data
    )
    
    print(f"Résultat: {result['final_result']}")
    print(f"Historique: {len(result['execution_history'])} étapes")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📋 Exemples de workflows

### 1. Writer-Reviewer (Création de contenu)
```
Manager → Writer ⟷ Reviewer → Manager → End
```
- **Usage** : Création de contenu avec révision automatisée
- **Boucles** : Writer ↔ Reviewer (max 3 itérations)
- **Conditions** : `approved`, `rejected_not_final`, `final_review`

### 2. Hiring Process (Recrutement)
```
Candidat → RH → Technique → Final → Embauché/Rejeté
```
- **Usage** : Processus de recrutement multi-étapes
- **Branchements** : Plusieurs sorties possibles (embauché/rejeté)
- **Conditions** : `passed`, `failed`, `hired`, `rejected`

### 3. Development Workflow (Développement logiciel)
```
Analyste → Développeur ⟷ Testeur → Release Manager → End
```
- **Usage** : Cycle de développement avec tests
- **Boucles** : Développeur ↔ Testeur si bugs détectés
- **Conditions** : `complete`, `incomplete`, `has_issues`, `no_issues`

## 🏗️ Architecture

Le projet suit une architecture hexagonale (Clean Architecture) :

```
src/
├── domain/              # Entités métier et interfaces
│   ├── entities/        # WorkflowDefinition, WorkflowNode, etc.
│   └── interfaces/      # IAgent, IWorkflowExecutor, etc.
├── application/         # Services et cas d'usage
│   └── services/        # WorkflowService
├── infrastructure/      # Implémentations concrètes
│   ├── agents/          # PydanticAgent
│   ├── executors/       # WorkflowExecutor
│   └── factories/       # AgentFactory
├── core/               # Logique métier centrale
│   └── condition_evaluator.py
└── blueprints/         # Définitions des workflows
    └── workflow_definitions.py
```

## 📖 Documentation

La documentation complète est disponible avec MkDocs :

```bash
# Installer les dépendances de documentation
uv sync

# Servir la documentation en local
mkdocs serve

# Générer la documentation statique
mkdocs build
```

Accédez à la documentation sur : `http://localhost:8000`

## 🔧 Définition des workflows

### Structure JSON de base

```json
{
  "name": "Nom du workflow",
  "description": "Description du workflow",
  "start_node": "id_du_nœud_de_départ",
  "nodes": [...],
  "edges": [...]
}
```

### Types de nœuds

- **`process`** : Nœud de traitement (agent qui transforme les données)
- **`decision`** : Nœud de décision (agent qui retourne des conditions)
- **`start`** : Nœud de démarrage (optionnel)
- **`end`** : Nœud de fin

### Conditions supportées

- **Conditions booléennes** : `approved`, `passed`, `hired`, `complete`
- **Conditions négatives** : `rejected`, `failed`, `incomplete`
- **Conditions spéciales** : `rejected_not_final`, `final_review`, `has_issues`, `no_issues`

### Gestion des itérations

```json
{
  "id": "reviewer",
  "max_iterations": 3,  // Limite le nombre d'itérations
  "agent_config": {...}
}
```

## 🛣️ Roadmap

Voir [ROADMAP.md](ROADMAP.md) pour les fonctionnalités planifiées et l'évolution du framework.