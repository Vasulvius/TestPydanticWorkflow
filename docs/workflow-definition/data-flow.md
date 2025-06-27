# Échange de données entre nœuds

Cette section explique comment les données circulent entre les nœuds d'un workflow et quels formats sont supportés.

## Principe général

Dans Dynamic Agent Workflows, **chaque nœud reçoit les données de sortie du nœud précédent** et les transforme selon sa logique métier. Les données circulent de façon linéaire, mais peuvent être enrichies ou transformées à chaque étape.

```mermaid
graph LR
    A[Données initiales] --> B[Nœud 1]
    B --> C[Données transformées] --> D[Nœud 2]
    D --> E[Données finales]
```

## Types de données supportés

### 1. Données simples

```python
# String
"Bonjour, je voudrais un article sur l'IA"

# Number  
42

# Boolean
True
```

### 2. Objets JSON

```json
{
  "topic": "Intelligence artificielle",
  "length": "500 mots",
  "audience": "développeurs",
  "urgent": true
}
```

### 3. Listes et tableaux

```json
{
  "requirements": [
    "Authentification JWT",
    "Base de données PostgreSQL", 
    "API REST"
  ],
  "priorities": [1, 2, 3]
}
```

### 4. Structures complexes

```json
{
  "candidate": {
    "name": "Marie Dupont",
    "skills": ["Python", "Docker", "AWS"],
    "experience": {
      "years": 5,
      "companies": ["TechCorp", "StartupXYZ"]
    }
  },
  "position": {
    "title": "Senior Developer",
    "salary_range": [60000, 80000]
  }
}
```

## Flux de données par type de nœud

### Nœuds de traitement (`process`)

Les nœuds de traitement **transforment** les données d'entrée :

```python
# Entrée
{
  "topic": "IA dans la santé",
  "length": "300 mots"
}

# ↓ Agent Writer transforme

# Sortie
"L'intelligence artificielle révolutionne le secteur de la santé..."
```

### Nœuds de décision (`decision`)

Les nœuds de décision **enrichissent** les données avec des métadonnées de décision :

```python
# Entrée
"Article sur l'IA dans la santé..."

# ↓ Agent Reviewer évalue

# Sortie
{
  "approved": True,
  "feedback": "Excellent article, bien structuré",
  "score": 85
}
```

### Nœuds de fin (`end`)

Les nœuds de fin **retournent** les données telles qu'elles les reçoivent.

## Cas spéciaux d'échange

### 1. Manager final avec contexte enrichi

Le nœud `manager_final` reçoit automatiquement un contexte enrichi :

```python
# Données enrichies automatiquement
{
  "content": "Données du nœud précédent",
  "original_request": "Demande initiale de l'utilisateur", 
  "iterations": {"writer": 2, "reviewer": 2},
  "history": [...]  # Historique complet
}
```

### 2. Boucles de rétroaction

Dans une boucle, les données précédentes sont passées avec le feedback :

```python
# Première itération
Input → Writer → "Article version 1"

# Reviewer évalue
"Article version 1" → Reviewer → {"approved": False, "feedback": "Manque d'exemples"}

# Deuxième itération (boucle)
{"approved": False, "feedback": "Manque d'exemples"} → Writer → "Article version 2 avec exemples"
```

## Transformation des données

### Par les agents

Les agents peuvent transformer les données de différentes façons :

```python
# Agent de synthèse
["Point 1", "Point 2", "Point 3"] → "Résumé des 3 points principaux..."

# Agent de validation
"Contenu à valider" → {"valid": True, "issues": []}

# Agent d'enrichissement  
{"name": "John"} → {"name": "John", "greeting": "Bonjour John!", "timestamp": "2025-06-27"}
```

### Par le workflow

Le framework peut automatiquement :

```python
# Ajouter des métadonnées
data → {
  "data": data,
  "node_id": "current_node",
  "iteration": 1,
  "timestamp": "2025-06-27T10:30:00"
}
```

## Formats de sortie des agents

### Agents de traitement

```python
# Retour simple (string, number, boolean)
return "Contenu généré par l'agent"

# Retour structuré  
return {
  "content": "Contenu principal",
  "metadata": {"word_count": 250, "language": "fr"}
}
```

### Agents de décision

**Format obligatoire** : Objet JSON avec champs de décision

```json
{
  "approved": true,           // Décision principale
  "feedback": "...",          // Commentaires
  "score": 85,               // Score optionnel
  "final_review": false      // Métadonnées de contrôle
}
```

!!! warning "Format des agents de décision"
    Les agents de décision DOIVENT retourner un objet JSON valide pour que les conditions fonctionnent correctement.

## Gestion des erreurs dans les données

### Données malformées

```python
# Si un agent retourne des données invalides
try:
    result = agent.execute(input_data)
except Exception as e:
    result = {
        "error": "agent_execution_failed",
        "message": str(e),
        "input": input_data
    }
```

### Parsing JSON échoué

```python
# Si le parsing JSON d'un agent de décision échoue
{
  "error": "parsing_failed",
  "raw_response": "Réponse brute de l'agent...",
  "fallback": True
}
```

## Exemples pratiques

### Workflow Writer-Reviewer

```python
# 1. Données initiales
{
  "topic": "IA en médecine",
  "length": "200 mots",
  "audience": "médecins"
}

# 2. Manager → Instructions détaillées
"Rédigez un article de 200 mots sur l'IA en médecine pour médecins..."

# 3. Writer → Article
"L'intelligence artificielle transforme la médecine moderne..."

# 4. Reviewer → Évaluation
{
  "approved": False,
  "feedback": "Manque de sources scientifiques",
  "final_review": False
}

# 5. Writer (itération 2) → Article amélioré
"L'intelligence artificielle transforme la médecine moderne. Selon une étude de Nature..."

# 6. Reviewer → Approbation
{
  "approved": True,
  "feedback": "Excellent article avec sources fiables"
}

# 7. Manager final → Présentation finale
"Voici votre article approuvé sur l'IA en médecine : [article complet]"
```

### Workflow de recrutement

```python
# 1. Données candidat
{
  "name": "Sophie Martin",
  "cv": "Développeuse Python 3 ans...",
  "position": "Senior Developer"
}

# 2. RH → Évaluation initiale
{
  "passed": True,
  "feedback": "Profil intéressant, expérience cohérente",
  "score": 75
}

# 3. Technique → Évaluation technique
{
  "passed": True,
  "score": 85,
  "technical_notes": "Bonnes connaissances Python et cloud"
}

# 4. Final → Décision finale
{
  "hired": True,
  "decision": "Candidature retenue, profil adapté",
  "salary_offer": 65000
}
```

## Débogage des données

### Historique complet

L'historique capture tous les échanges :

```python
result = workflow_service.execute_workflow(...)

for step in result['execution_history']:
    print(f"Nœud: {step['node_id']}")
    print(f"Entrée: {step['input']}")
    print(f"Sortie: {step['output']}")
    print(f"Timestamp: {step['timestamp']}")
    print("---")
```

### Mode détaillé

```bash
# Afficher tous les échanges
uv run main.py --writer --detailed
```

## Bonnes pratiques

### 1. Formats cohérents

```json
// ✅ Bon - Structure consistante
{
  "content": "...",
  "metadata": {"score": 85}
}

// ❌ Éviter - Formats incohérents
"Simple string" → {"complex": "object"} → 42
```

### 2. Validation des données

```python
# Dans vos agents personnalisés
def validate_input(self, data):
    if not isinstance(data, dict):
        raise ValueError("Expected dict input")
    
    required_fields = ["topic", "length"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field: {field}")
```

### 3. Documentation des formats

```json
{
  "nodes": [
    {
      "id": "analyzer",
      "description": "INPUT: {text: string} → OUTPUT: {sentiment: string, confidence: float}"
    }
  ]
}
```

## Prochaines étapes

- 🎯 [Conditions et transitions](conditions.md) - Logique conditionnelle basée sur les données
-  [Exemples pratiques](../examples/writer-reviewer.md) - Voir des cas concrets
- 🏗️ [Architecture](../architecture/overview.md) - Comprendre le fonctionnement interne
