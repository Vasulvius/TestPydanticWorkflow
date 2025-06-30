# Syntaxe JSON des workflows

Cette section détaille la syntaxe complète pour définir des workflows d'agents via des fichiers JSON.

## Structure de base

Un workflow est défini par un objet JSON avec la structure suivante :

```json
{
  "name": "Nom du workflow",
  "description": "Description optionnelle",
  "start_node": "id_du_noeud_de_depart",
  "nodes": [...],
  "edges": [...]
}
```

## Propriétés du workflow

### Propriétés obligatoires

| Propriété    | Type     | Description                       |
| ------------ | -------- | --------------------------------- |
| `name`       | `string` | Nom unique du workflow            |
| `start_node` | `string` | ID du nœud de démarrage           |
| `nodes`      | `array`  | Liste des nœuds du workflow       |
| `edges`      | `array`  | Liste des transitions entre nœuds |

### Propriétés optionnelles

| Propriété     | Type     | Description             |
| ------------- | -------- | ----------------------- |
| `description` | `string` | Description du workflow |
| `version`     | `string` | Version du workflow     |
| `author`      | `string` | Auteur du workflow      |
| `tags`        | `array`  | Tags pour catégoriser   |

## Définition des nœuds

### Structure d'un nœud

```json
{
  "id": "identifiant_unique",
  "name": "Nom lisible",
  "type": "process|decision|start|end",
  "max_iterations": 3,
  "agent_config": {...}
}
```

### Propriétés des nœuds

| Propriété        | Type     | Obligatoire | Description                                         |
| ---------------- | -------- | ----------- | --------------------------------------------------- |
| `id`             | `string` | ✅           | Identifiant unique du nœud                          |
| `name`           | `string` | ✅           | Nom lisible pour les logs                           |
| `type`           | `string` | ✅           | Type de nœud (voir [Types de nœuds](node-types.md)) |
| `max_iterations` | `number` | ❌           | Limite d'itérations pour ce nœud                    |
| `agent_config`   | `object` | ✅*          | Configuration de l'agent (*sauf pour `end`)         |

### Configuration d'agent

```json
{
  "agent_config": {
    "type": "pydantic",
    "model": "openai:gpt-4o-mini",
    "name": "Agent Name",
    "node_type": "decision",
    "system_prompt": "Instructions pour l'agent...",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

#### Propriétés de `agent_config`

| Propriété       | Type     | Obligatoire | Description                  |
| --------------- | -------- | ----------- | ---------------------------- |
| `type`          | `string` | ✅           | Type d'agent (`pydantic`)    |
| `model`         | `string` | ✅           | Modèle à utiliser            |
| `name`          | `string` | ✅           | Nom de l'agent               |
| `system_prompt` | `string` | ✅           | Instructions système         |
| `node_type`     | `string` | ❌           | `decision` pour parsing JSON |
| `temperature`   | `number` | ❌           | Créativité (0.0-1.0)         |
| `max_tokens`    | `number` | ❌           | Limite de tokens             |

## Définition des transitions (edges)

### Structure d'une transition

```json
{
  "from_node": "noeud_source",
  "to_node": "noeud_destination", 
  "condition": "condition_optionnelle"
}
```

### Propriétés des transitions

| Propriété   | Type     | Obligatoire | Description                     |
| ----------- | -------- | ----------- | ------------------------------- |
| `from_node` | `string` | ✅           | ID du nœud source               |
| `to_node`   | `string` | ✅           | ID du nœud destination          |
| `condition` | `string` | ❌           | Condition pour cette transition |

## Exemple complet

Voici un exemple de workflow complet avec tous les éléments :

```json
{
  "name": "Content Creation Workflow",
  "description": "Workflow de création de contenu avec révision",
  "version": "1.0",
  "author": "Dynamic Workflows Team",
  "start_node": "manager_initial",
  "nodes": [
    {
      "id": "manager_initial",
      "name": "Project Manager", 
      "type": "process",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini",
        "name": "Manager",
        "system_prompt": "Transform user requests into clear writing instructions.",
        "temperature": 0.3
      }
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
        "system_prompt": "Write high-quality content based on instructions.",
        "temperature": 0.7,
        "max_tokens": 2000
      }
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
        "system_prompt": "Review content and return JSON: {\"approved\": true/false, \"feedback\": \"...\"}",
        "temperature": 0.2
      }
    },
    {
      "id": "manager_final",
      "name": "Final Manager",
      "type": "process",
      "agent_config": {
        "type": "pydantic",
        "model": "openai:gpt-4o-mini", 
        "name": "Manager",
        "system_prompt": "Present final results to the user."
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
    {"from_node": "manager_initial", "to_node": "writer"},
    {"from_node": "writer", "to_node": "reviewer"},
    {"from_node": "reviewer", "to_node": "writer", "condition": "rejected_not_final"},
    {"from_node": "reviewer", "to_node": "manager_final", "condition": "approved"},
    {"from_node": "reviewer", "to_node": "manager_final", "condition": "final_review"},
    {"from_node": "manager_final", "to_node": "end"}
  ]
}
```

## Bonnes pratiques

### Nommage

```json
// ✅ Bon - IDs clairs et cohérents
{
  "id": "content_writer",
  "name": "Content Writer"
}

// ❌ Éviter - IDs cryptiques
{
  "id": "n1", 
  "name": "Node 1"
}
```

### Organisation

```json
// ✅ Bon - Groupement logique des nœuds
{
  "nodes": [
    // Nœuds de traitement
    {"id": "manager_initial", "type": "process", ...},
    {"id": "writer", "type": "process", ...},
    
    // Nœuds de décision
    {"id": "reviewer", "type": "decision", ...},
    
    // Nœuds de fin
    {"id": "end", "type": "end", ...}
  ]
}
```

### Prompts système

```json
// ✅ Bon - Instructions claires et spécifiques
{
  "system_prompt": "You are a content reviewer. Evaluate the content and return JSON: {\"approved\": true/false, \"feedback\": \"specific feedback\"}. Approve only if content meets all requirements."
}

// ❌ Éviter - Instructions vagues
{
  "system_prompt": "Review this content."
}
```

## Validation automatique

Le framework valide automatiquement :

- ✅ **IDs uniques** : Tous les nœuds ont des IDs différents
- ✅ **Références valides** : Toutes les transitions pointent vers des nœuds existants  
- ✅ **Nœud de départ** : Le `start_node` existe dans les nœuds
- ✅ **Structure JSON** : Syntaxe JSON valide
- ✅ **Propriétés obligatoires** : Toutes les propriétés requises sont présentes

## Prochaines étapes

- 🎯 [Conditions et transitions](conditions.md) - Logique conditionnelle
- 📊 [Échange de données](data-flow.md) - Comment les données circulent
- 🔧[Guide des outils](tools-guide.md) - Comment donner des outils aux agents
- � [Exemples pratiques](../examples/writer-reviewer.md) - Workflows complets
- 🏗️ [Architecture](../architecture/overview.md) - Comprendre le fonctionnement interne
