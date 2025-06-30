# Roadmap - Dynamic Agent Workflows

Cette roadmap présente les fonctionnalités planifiées et les améliorations futures pour Dynamic Agent Workflows.

## 🎯 Vision

Devenir le framework de référence pour la création et l'exécution de workflows d'agents IA, offrant une flexibilité maximale tout en conservant une simplicité d'utilisation.

---

## 🚀 Version 1.0 (MVP) - ✅ Terminé

### Fonctionnalités de base
- [x] Définition de workflows via JSON
- [x] Support des agents Pydantic AI
- [x] Exécution de workflows avec transitions conditionnelles
- [x] Gestion des boucles avec limitation d'itérations
- [x] Historique complet des exécutions
- [x] Architecture Clean/Hexagonale
- [x] Évaluateur de conditions générique

### Types de nœuds
- [x] Nœuds de traitement (`process`)
- [x] Nœuds de décision (`decision`)
- [x] Nœuds de fin (`end`)

### Conditions supportées
- [x] Conditions booléennes simples (`approved`, `passed`, `hired`)
- [x] Conditions négatives (`rejected`, `failed`)
- [x] Conditions spéciales (`rejected_not_final`, `final_review`)

### Exemples fournis
- [x] Writer-Reviewer Workflow
- [x] Hiring Process Workflow
- [x] Development Workflow (partiellement)

---

## 🔧 Version 1.1 - Amélioration de la robustesse

### Nouvelles fonctionnalités
- [ ] Possibilité de créer des tools et de les donner à des agents

### Parsing et validation
- [ ] Amélioration du parsing JSON des réponses d'agents
- [ ] Support des blocs markdown dans les réponses
- [ ] Validation automatique des structures JSON
- [ ] Gestion robuste des erreurs de parsing

### Gestion d'erreurs
- [ ] Système d'exceptions personnalisées
- [ ] Retry automatique en cas d'erreur temporaire
- [ ] Logging structuré avec niveaux

### Monitoring et observabilité
- [ ] Extraction d'un diagramme mermaid d'un workflow
- [ ] Métriques de performance des workflows
- [ ] Temps d'exécution par nœud
- [ ] Taux de succès/échec
- [ ] Dashboard de monitoring basique

---

## 🚀 Version 1.2 - Extension des fonctionnalités

### Nouveaux types de nœuds
- [ ] **Nœud parallèle** (`parallel`) : Exécution simultanée de plusieurs agents
- [ ] **Nœud de synchronisation** (`sync`) : Attendre plusieurs branches parallèles
- [ ] **Nœud de transformation** (`transform`) : Transformation de données sans IA
- [ ] **Nœud de validation** (`validate`) : Validation de schémas Pydantic

### Conditions avancées
- [ ] **Conditions numériques** : `score > 80`, `confidence >= 0.8`
- [ ] **Conditions temporelles** : `timeout`, `max_duration`
- [ ] **Conditions complexes** : Combinaisons avec AND/OR
- [ ] **Conditions dynamiques** : Basées sur l'historique d'exécution

### Agents étendus
- [ ] Agents personnalisés avec hooks
- [ ] Agents de type "humain" pour intervention manuelle
- [ ] Cache intelligent des réponses d'agents

---

## 🌟 Version 1.3 - Écosystème et intégrations

### Interface utilisateur
- [ ] **Web UI** pour créer des workflows visuellement
- [ ] **Éditeur graphique** drag-and-drop
- [ ] **Visualiseur de workflows** en temps réel
- [ ] **Dashboard d'administration**

### Persistance et état
- [ ] **Base de données** pour sauvegarder les workflows
- [ ] **État persistant** des exécutions en cours
- [ ] **Reprise après crash** des workflows interrompus
- [ ] **Versioning** des workflows