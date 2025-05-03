# Ollama RAG Analysis Agent

Un agent intelligent qui combine recherche web, RAG (Retrieval-Augmented Generation) et analyse LLM pour fournir des réponses enrichies avec évaluation automatique de qualité.

## Fonctionnalités clés

- 🔍 **Recherche web avancée** avec extraction des contenus pertinents
- 📚 **Intégration RAG** pour contextualiser les réponses
- 🤖 **Analyse automatique** des réponses par LLM (Ollama)
- ✅ **Évaluation de qualité** : pertinence, cohérence, biais, clarté
- ✨ **Résumé automatique** des points clés
- 📝 **Gestion transparente des sources** avec tracking complet

## Prérequis

- Python 3.9+
- Ollama installé et configuré (serveur local ou distant)
- Modèle LLM compatible (par défaut: `mistral`)

## Installation

0. Ollama
```bash
# Charger les modeles
ollama pull mistral
# Lancer le serveur
ollama serve
```

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-repo/ollama-rag-agent.git
cd ollama-rag-agent
```

2. Creer l'environnement et installer les packages python 
```bash
uv venv .venv
.venv\scripts\activate # Windows
source .venv\scripts\activate # Unix

uv pip install -r requirements.txt
```

3. Lancer le serveur mcp
```bash
cd app
uv run mcp_server.py
```
##   Utiliser l'agent en CLI :

```bash
python agent.py "Votre question ici"
```
ou 

```bash
uv run agent.py "Votre question ici"
```