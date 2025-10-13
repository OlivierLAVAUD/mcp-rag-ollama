# MCP-RAG-AI-AGENT
## A MCP Rag AI Agent for Search 🔍,Analysis 📊 and Generative ✍️ tasks on listed web sources.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent conversational agent implementing the Model Context Protocol (MCP) with RAG (Retrieval-Augmented Generation) capabilities using Ollama as the LLM backend.
Application Overview

This application is an intelligent conversational agent that combines several advanced technologies:

    Compliance with the MCP (Model Context Protocol): The Model Context Protocol (MCP) is a standardized framework for defining and managing the context of AI agents, ensuring better interoperability, traceability, and explainability. In this multi-agent system, the MCP standardizes communication between agents by encapsulating their metadata, capabilities, and constraints.

    RAG Architecture & LLM Models with Ollama:

        Use of local LLM models via Ollama
        Complete document processing pipeline (extraction, chunking, embedding)
        Vector search with FAISS (CPU/GPU)

    Multi-Agent Architecture:

        Search Agent (combines web search and RAG)
        Analysis Agent (semantic and statistical analysis)
        Generation Agent (content creation)

    Advanced Features:

        Structured logging for debugging
        Centralized configuration
        Support for multiple search providers (Exa, Firecrawl)
        Automatic error handling

The application is particularly suited for:

    Intelligent virtual assistants
    Augmented information retrieval systems
    Content analysis tools
    Automated content generators

The system is designed to be extensible with new agents and capabilities while maintaining a clean, modular architecture.
Key Features

    📚 Augmented Search: Combination of web search and RAG for precise answers
    🤖 Multi-Agent: Modular architecture with specialized agents
    ✅ MCP Protocol: Implementation of the machine-to-machine conversation standard
    ✨ Ollama Integration: Use of local LLM models via Ollama
    📝 Advanced Processing: Web content extraction, cleaning, and analysis

Technical Architecture

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

## Prerequisite

- curl (https://curl.se/)
```bash
        sudo apt update
        sudo apt install curl
```

- uv (https://docs.astral.sh/uv/getting-started/installation/)
```bash
        sudo apt update
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.local/bin/env 
```

- Python 3.10+

- ollama (https://ollama.com/download)
```bash
        sudo apt update
        curl -fsSL https://ollama.com/install.sh | sh
        source $HOME/.local/bin/env 
``` 
- EXA Api key (https://dashboard.exa.ai/api-keys)

- Firecrawl Api Key (https://www.firecrawl.dev/)

- tmux (terminal multi-session)
```bash
        sudo apt update
        sudo apt install tmux
``` 

## Install with sources

- clone and access the repo :
```bash
    git clone https://github.com/OlivierLAVAUD/mcp-rag-ollama
    cd ollama-rag-agent
```

- create python env and activate
```bash
    uv venv --python 3.10
    source .venv/bin/activate
```
- install the python packages
```bash
    uv sync
```
- download ollama llm models:  llama3.2, mistral (https://ollama.com/search)
```bash
    ollama  pull llama3.2
    ollama  pull mistral
    # Launch ollama server
    ollama serve
```

- create your own env configuration file for modyfing parameters
```bash
    cp .env.sample .env 
    nano .env
    # specify SEARCH_PROVIDER exa or firecrawl
    # add exa or firecrawl api keys 
    # save the file
```

- create a terminal session with tmux
```bash
    tmux new-session -d -s mcp-server
    tmux attach-session -t mcp-server
    # note for detach: Ctrl + B puis D
```

- launch the mcp server

```bash
    uv run app/mcp_server.py
```

- create a  nother terminal session with tmux
- prompt for asking 

```bash
    uv run app/agent.py "Donne moi les dernières actualités à propos des Agents IA"
```

## Sample execution
<p align="center"><img src="img/image.png" alt="[Core Components" width="1200" height="600"></p>


## Licence

The MIT License (MIT) 
Copyright (c) 2025 Olivier Lavaud

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
