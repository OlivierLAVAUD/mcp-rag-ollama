# MCP-RAG-AI-AGENT
## MCP SEARCH ANALYSIS & GENERATIVE AGENT
## Search 🔍,Analysis 📊 and Generate ✍️ on listed web sources

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un agent conversationnel intelligent implémentant le protocole Model Context Protocol (MCP) avec capacités RAG (Retrieval-Augmented Generation) utilisant Ollama comme backend LLM.


## Présentation de l'application

Cette application est un agent conversationnel intelligent qui combine plusieurs technologies avancées :

1. **Conformité avec le Protocole MCP(Model Context Protocol )** : Le Model Context Protocol (MCP) est un cadre standardisé permettant de définir et de gérer le contexte des agents IA, garantissant une meilleure interopérabilité, traçabilité et explicabilité. Dans ce système multi-agents, le MCP permet d’uniformiser la communication entre agents en encapsulant leurs métadonnées, leurs capacités et leurs contraintes.

2. **Architecture RAG & Modeles LLM avec Ollama** : 
   - Utilisation de modèles LLM locaux via Ollama
   - Pipeline complet de traitement des documents (extraction, découpage, embedding)
   - Recherche vectorielle avec FAISS (CPU/GPU)

3. **Architecture multi-agents** :
   - Agent de recherche (combine recherche web et RAG)
   - Agent d'analyse (analyse sémantique et statistique)
   - Agent de génération (création de contenu)

4. **Fonctionnalités avancées** :
   - Logging structuré pour le débogage
   - Configuration centralisée
   - Support multi-fournisseurs de recherche (Exa, Firecrawl)
   - Gestion automatique des erreurs

L'application est particulièrement adaptée pour :
- Les assistants virtuels intelligents
- Les systèmes de recherche d'information augmentée
- Les outils d'analyse de contenu
- Les générateurs de contenu automatisés

Le système est conçu pour être extensible avec de nouveaux agents et capacités tout en maintenant une architecture propre et modulaire.

## Fonctionnalités clés

- 📚**Recherche augmentée** : Combinaison de recherche web et RAG pour des réponses précises
- 🤖 **Multi-agents** : Architecture modulaire avec agents spécialisés
- ✅**Protocole MCP** : Implémentation du standard de conversation machine-to-machine
- ✨**Intégration Ollama** : Utilisation des modèles LLM locaux via Ollama
- 📝**Traitement avancé** : Extraction, nettoyage et analyse de contenu web

## Architecture technique

```markdown
NEXUS-MCP-LLM-RAG/
│
├── app/
│   ├── agent.py                 # Main agents (research, analysis, generation)
│   ├── agent_orchestrator.py    # Agent coordination logic
│   ├── config.py                # Central configuration
│   ├── mcp_server.py            # FastAPI MCP implementation
│   ├── rag.py                   # RAG processing
│   ├── search.py                # Advanced web search
│   │
│   └── utils/
│       └── logging_service.py   # Structured logging service
│
├── pyproject.toml               # Project configuration
├── requirements.txt             # Python dependencies
└── .env.sample                  # Environment template
```

## Prérequis

- Python 3.10+
- Ollama installé localement avec au moins un modèle (ex: `llama3`) (https://ollama.com/)
- Clé API pour un fournisseur de recherche (Exa ou Firecrawl)


## Installation

- Cloner le dépôt :
```bash
git clone https://github.com/OlivierLAVAUD/mcp-rag-ollama
cd ollama-rag-agent
```

- Charger les modèles LLM à partir d'ollama et lancer le serveur ollama

```bash
# Exemple: Chargement du modele "mistral"
ollama pull mistral

# Lancement du serveur sur une session terminal indépendante.
ollama serve
```

- Créez & modifiez votre fichier de configuration/paramètrage .env :
```bash
# Creez le fichier .env sur le template .env sample fournit et modifiez le. (voir Configuration)
```bash
    cp .env.sample .env 
    edit .env           
```

## Utilisation

### Lancer le serveur MCP
```bash
    uv run app/mcp_server.py
```

### Lancer une requête à l'Agent

```bash
    uv run app/agent.py "Donne moi les dernières actualités à propos des Agents IA"
```

## Configuration

Les paramètres principaux sont configurables via le fichier .env :
```bash
# Modèle Ollama
# === Génération Configuration du Modèle LLM via Ollama ===
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=llama3.2

OLLAMA_MODEL_TEMPERATURE=0.7  # Contrôle la créativité (0-1)
OLLAMA_MODEL_MAX_TOKENS=1024  # Nombre maximum de tokens générés
OLLAMA_MODEL_TOP_P=0.75       # Filtrage par noyau (0-1)

# === Paramètres RAG ===
RAG_CHUNK_SIZE=4096
RAG_CHUNK_OVERLAP=512
RAG_RESULTS=5

# Fournisseur de recherche
SEARCH_PROVIDER=exa  # ou firecrawl
EXA_API_KEY=votre_cle_api
...

```

## Licence

Ce projet est sous licence MIT - voir le fichier LICENCE.md pour plus de détails.

## Auteur

Olivier Lavaud - 2025


# Technical Documentation
## System Purpose

MCP-RAG-Ollama serves as a versatile query answering system that combines the power of large language models with real-time information retrieval. It enables users to:

    Get answers to questions using contextual knowledge from web searches
    Implement RAG workflows with Ollama models
    Access the system via both API endpoints and command-line interface



## Architecture Overview
The system follows a layered architecture pattern, separating client interactions, server operations, core processing, and external service integrations.
<p align="center"><img src="img/i1.png" alt="[Architecture Overview" width="600" height="400"></p>

## Core Components
The system consists of four main components that work together to provide RAG capabilities:
<p align="center"><img src="img/i2.png" alt="[Core Components" width="600" height="400">
</p>

```bash
    - MCP Server: The FastAPI server that exposes endpoints for client interactions.
    - OllamaAgent: The orchestrator that processes queries by combining web search and RAG.
    - RAG Processor: Handles document processing, embedding generation, and similarity search.
    - Web Searcher: Performs web searches and content extraction from relevant pages.
```

## Query Processing Flow
The following diagram illustrates how a user query flows through the system:

<p align="center"><img src="img/i3.png" alt="[Core Components" width="600" height="400"></p>

## Technology Stack

The MCP-RAG-Ollama system leverages multiple technologies and libraries:

<p align="center"><img src="img/i5.png" alt="[Technology Stack" width="500" height="300"></p>

## Deployment Architecture
The system can be deployed as follows:*

<p align="center"><img src="img/i4.png" alt="Deployment Architecture" width="600" height="400"></p>
