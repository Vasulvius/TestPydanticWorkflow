# Installation

Cette page vous guide à travers l'installation et la configuration de Dynamic Agent Workflows.

## Prérequis

### Système
- **Python 3.12+** (recommandé 3.12 ou supérieur)
- **Git** pour cloner le projet
- **UV**

### Clés API
Vous aurez besoin d'au moins une clé API pour un modèle de langage :

- **OpenAI** (recommandé) : GPT-4o-mini pour les tests
- **Anthropic** : Claude pour une alternative
- **Local** : Ollama pour une solution locale

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-depot-interne>
```

### 2. Installation avec UV (recommandé)

[UV](https://github.com/astral-sh/uv) est l'outil de gestion de dépendances Python le plus rapide.

```bash
# Installer UV (si pas déjà fait)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installer les dépendances
uv install

# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

## Configuration

### 1. Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
# OpenAI (recommandé pour commencer)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (optionnel)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Configuration avancée (optionnel)
LOG_LEVEL=INFO
MAX_WORKFLOW_ITERATIONS=50
DEFAULT_MODEL=openai:gpt-4o-mini
```

### 2. Obtenir une clé OpenAI

1. Rendez-vous sur [platform.openai.com](https://platform.openai.com)
2. Créez un compte ou connectez-vous
3. Allez dans la section "API Keys"
4. Créez une nouvelle clé API
5. Copiez la clé dans votre fichier `.env`

!!! warning "Sécurité"
    Ne commitez jamais votre fichier `.env` ! Il est déjà dans le `.gitignore`.

### 3. Test de l'installation

Vérifiez que tout fonctionne :

```bash
# Test avec un workflow simple
uv run main.py --writer
```

Si tout se passe bien, vous devriez voir l'exécution du workflow Writer-Reviewer.

## Vérification de l'installation

### Structure des fichiers

Votre projet devrait ressembler à ceci :

```
dynamic-agent-workflows/
├── .env                    # Vos variables d'environnement
├── .venv/                  # Environnement virtuel (UV)
├── main.py                 # Point d'entrée pour les tests
├── pyproject.toml          # Configuration du projet
├── src/                    # Code source
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── ...
├── docs/                   # Documentation
└── examples/               # Exemples de workflows
```

## Problèmes courants

### Erreur d'import

```bash
ModuleNotFoundError: No module named 'src'
```

**Solution** : Assurez-vous d'être dans le bon répertoire et que l'environnement virtuel est activé.

### Erreur de clé API

```bash
openai.AuthenticationError: Incorrect API key provided
```

**Solution** : Vérifiez votre clé API dans le fichier `.env` et qu'elle est valide.

### Erreur de dépendances

```bash
ImportError: No module named 'pydantic_ai'
```

**Solution** : Réinstallez les dépendances :

```bash
uv install --reload
```

## Prochaines étapes

Une fois l'installation terminée :

1. 📖 [Créez votre premier workflow](first-workflow.md)
2. � [Explorez les exemples](../examples/writer-reviewer.md)
3. � [Découvrez la syntaxe des workflows](../workflow-definition/syntax.md)
