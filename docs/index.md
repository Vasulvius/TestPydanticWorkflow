# Dynamic Agent Workflows

Bienvenue dans **Dynamic Agent Workflows**, un framework Python pour créer et exécuter des workflows d'agents IA dynamiques basés sur JSON.

## 🎯 Qu'est-ce que c'est ?

Dynamic Agent Workflows vous permet de définir des workflows complexes d'agents IA via des fichiers JSON simples et de les exécuter avec des transitions conditionnelles, des boucles de rétroaction et une gestion avancée des itérations.

## ✨ Fonctionnalités principales

- **🔧 Configuration JSON** : Définissez vos workflows via des fichiers JSON simples
- **🤖 Agents IA intégrés** : Support natif de Pydantic AI et extensible à d'autres frameworks
- **🔄 Boucles conditionnelles** : Créez des workflows avec feedback et itérations limitées
- **📊 Historique complet** : Traçabilité complète de l'exécution avec métriques
- **🏗️ Architecture propre** : Basé sur les principes SOLID et Clean Architecture
- **🚀 Extensible** : Facilement extensible pour de nouveaux types d'agents et conditions

## 🚀 Démarrage rapide

```bash
# Installation
pip install -r requirements.txt

# Exécution d'un workflow de test
python main.py --writer

# Voir toutes les options
python main.py --help
```

## 📋 Exemples de workflows supportés

### Writer-Reviewer Workflow
```
Manager → Writer ⟷ Reviewer → Manager → End
```
Un workflow de création de contenu avec révision itérative.

### Processus de recrutement
```
Candidat → RH → Technique → Final → Embauché/Rejeté
```
Un processus de recrutement multi-étapes avec branchements conditionnels.

### Développement logiciel
```
Analyste → Développeur ⟷ Testeur → Release Manager → End
```
Un cycle de développement avec tests et corrections itératives.

## 🎯 Cas d'usage

- **Création de contenu** : Workflows d'écriture avec révision automatisée
- **Processus métier** : Automatisation de processus complexes avec décisions
- **Validation en cascade** : Systèmes de validation multi-niveaux
- **Pipelines de traitement** : Chaînes de traitement avec conditions de sortie
- **Systèmes d'approbation** : Workflows d'approbation avec boucles de feedback

## 🏗️ Architecture

Le framework est basé sur une architecture hexagonale avec :

- **Domain Layer** : Entités métier et interfaces
- **Application Layer** : Services et cas d'usage
- **Infrastructure Layer** : Implémentations concrètes
- **Core Layer** : Logique métier centrale

## 📚 Documentation

- [Guide de démarrage](getting-started/installation.md) - Installation et premier workflow
- [Définition des workflows](workflow-definition/syntax.md) - Syntaxe JSON complète
- [Exemples pratiques](examples/writer-reviewer.md) - Workflows prêts à l'emploi
- [Architecture](architecture/overview.md) - Détails techniques
- [API Reference](api/interfaces.md) - Documentation des interfaces

## 🛣️ Roadmap

Consultez notre [roadmap](roadmap.md) pour voir les fonctionnalités à venir et contribuer au projet.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez nos guidelines de contribution pour commencer.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
