# MCP RAG Agent avec Ollama

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un agent conversationnel intelligent implémentant le protocole MCP (Machine Conversation Protocol) avec capacités RAG (Retrieval-Augmented Generation) utilisant Ollama comme backend LLM.

## Fonctionnalités clés

- 📚**Recherche augmentée** : Combinaison de recherche web et RAG pour des réponses précises
- 🤖 **Multi-agents** : Architecture modulaire avec agents spécialisés
- ✅**Protocole MCP** : Implémentation du standard de conversation machine-to-machine
- ✨**Intégration Ollama** : Utilisation des modèles LLM locaux via Ollama
- 📝**Traitement avancé** : Extraction, nettoyage et analyse de contenu web

## Architecture technique
```bash
.
├── app/
│ ├── agent.py # Agents principaux (recherche, analyse, génération)
│ ├── agent_orchestrator.py # Orchestration des agents
│ ├── config.py # Configuration centrale
│ ├── mcp_server.py # Serveur FastAPI implémentant MCP
│ ├── rag.py # Traitement RAG
│ ├── search.py # Recherche web avancée
│ └── utils/
│ └── logging_service.py # Service de logging structuré
├── pyproject.toml # Configuration du projet
├── requirements.txt # Dépendances Python
└── .env.sample # Configuration d'environnement
```
## Prérequis

- Python 3.10+
- Ollama installé localement avec au moins un modèle (ex: `llama3`)
- Clé API pour un fournisseur de recherche (Exa ou Firecrawl)


## Installation

0. Ollama
->  Installation sur votre systeme (Unix ou Windows) (https://ollama.com/)
->  Charger les modeles LLMs
```bash
# Exemple: Chargement du modele "mistral"
ollama pull mistral

# Lancement du serveur sur une session terminal indépendante.
ollama serve
```

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-repo/ollama-rag-agent.git
cd ollama-rag-agent
```

2. Installer les dépendances :
->  Creer l'environnement avec uv (plus rapide et fiable)
```bash
uv venv .venv
.venv\scripts\activate # Windows
#ou 
source .venv\scripts\activate # Unix
#puis
uv pip install -r requirements.txt
```

3. Configurer l'environnement de l'application et ses paramètres :
```bash
# Éditer le fichier .env puis ajoutez vos configurations (basée sur  .env sample)
cp .env.sample .env #Unix
edit .env           #Windows

```

4. Lancer le serveur mcp
```bash
cd app
uv run mcp_server.py
```
5. Utiliser l'agent en CLI :

```bash
python agent.py "Votre question ici"
```
ou 

```bash
uv run agent.py "Votre question ici"
```


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
