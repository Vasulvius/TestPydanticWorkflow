# Guide des outils

Les outils permettent aux agents d'interagir avec le monde extérieur et d'effectuer des actions spécifiques.

## 🎯 Concepts clés

### Qu'est-ce qu'un outil ?
Un outil est une fonction Python que les agents peuvent appeler pour :
- Accéder à des données externes
- Effectuer des calculs
- Interagir avec des APIs
- Manipuler des fichiers
- Valider des informations

### Types d'outils

#### Outils système
- `file_read` / `file_write` : Manipulation de fichiers
- `http_request` : Requêtes HTTP
- `current_time` : Date et heure

#### Outils métier
- `word_count` : Analyse de texte
- `validate_email` : Validation d'email
- `seo_analyze` : Analyse SEO

#### Outils personnalisés
Créés selon vos besoins spécifiques.

## 🚀 Utilisation dans les workflows

### Attribution d'outils
```json
{
  "id": "content_writer",
  "type": "process",
  "agent_config": {
    "system_prompt": "Utilise les outils pour améliorer ton contenu"
  },
  "tools": ["word_count", "seo_analyze", "grammar_check"]
}
```

### Prompts efficaces
```json
{
  "system_prompt": "Tu es un rédacteur expert. UTILISE OBLIGATOIREMENT l'outil word_count pour vérifier la longueur de ton texte avant de répondre."
}
```

## 🔧 Créer des outils personnalisés

### Structure de base
```python
@registry.register_tool("nom_outil", "Description de l'outil")
async def mon_outil(param1: str, param2: int = 10) -> str:
    """Documentation de l'outil"""
    # Logique de l'outil
    return "Résultat"
```

### Exemple complet
```python
@registry.register_tool("translate_text", "Traduit un texte via API")
async def translate_text(text: str, target_lang: str = "en") -> str:
    """Traduit un texte vers la langue cible"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.translate.com/v1/translate",
            json={"text": text, "target": target_lang}
        )
        return response.json()["translated_text"]
```

## 📋 Bonnes pratiques

### 1. Nommage clair
```python
# ✅ Bon
validate_email()
analyze_sentiment()
fetch_weather_data()

# ❌ Éviter
check()
process()
do_thing()
```

### 2. Gestion d'erreurs
```python
@registry.register_tool("safe_api_call", "Appel API avec gestion d'erreurs")
async def safe_api_call(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except Exception as e:
        return f"Erreur: {e}"
```

### 3. Documentation complète
```python
@registry.register_tool("complex_calculation", "Calcul complexe avec paramètres")
async def complex_calculation(
    data: str,
    algorithm: str = "default",
    precision: int = 2
) -> str:
    """
    Effectue un calcul complexe sur les données.
    
    Args:
        data: Données JSON à analyser
        algorithm: Algorithme à utiliser (default, advanced, experimental)
        precision: Nombre de décimales (0-10)
    
    Returns:
        Résultat du calcul formaté
    
    Examples:
        >>> await complex_calculation('{"values": [1,2,3]}')
        "Moyenne: 2.00"
    """
    # Implementation
```

## 🔍 Débogage des outils

### Logs d'utilisation
```python
@registry.register_tool("debug_tool", "Outil avec logs")
async def debug_tool(input_data: str) -> str:
    print(f"🔧 Outil debug_tool appelé avec: {input_data}")
    result = process_data(input_data)
    print(f"🔧 Outil debug_tool retourne: {result}")
    return result
```

## Prochaines étapes

-  [Exemples pratiques](../examples/writer-reviewer.md) - Voir des cas concrets
- 🏗️ [Architecture](../architecture/overview.md) - Comprendre le fonctionnement interne