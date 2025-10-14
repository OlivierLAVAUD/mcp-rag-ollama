# MCP-RAG-AI-AGENT
## A MCP Rag AI Agent for Search 🔍, Analysis 📊 and Generative tasks ✍️ on listed web sources.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is a sophisticated Multi-Agent RAG (Retrieval-Augmented Generation) system built around the Model Context Protocol (MCP) with Ollama as the LLM backend. The system combines web search, document analysis, and content generation capabilities in a modular architecture.
#
The system is particularly suited for:
- Intelligent virtual assistants
- Augmented information retrieval systems  
- Content analysis tools
- Automated content generators

## Key Features

🔍 Augmented Search
-    Real-time web search combined with contextual RAG
-    Multiple search providers with fallback options
-    Automatic content extraction and cleaning
-    Relevant source identification and citation

🤖 Multi-Agent Architecture
-    Specialized agents for different task types
-    Centralized orchestration with lazy initialization
-    Extensible agent registry for easy expansion
-    Consistent interface across all agents

📊 Advanced Processing
-    Semantic search with vector embeddings
-    Text analysis (length, word count, lexical density)
-    Intelligent summarization with configurable parameters
-    Content normalization and filtering

🛠 Production Ready
-    Structured JSON logging with rotation
-    Comprehensive error handling and recovery
-    Health monitoring endpoints
-    Configuration validation at startup

## Technical Architecture

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

## Installation
### Clone and Setup
```bash
    git clone https://github.com/OlivierLAVAUD/mcp-rag-ollama
    cd ollama-rag-agent
```
### Create Python Environment
```bash
    uv venv --python 3.10
    source .venv/bin/activate
```
### Install Dependencies
```bash
    uv sync
```
### Download Ollama Models (https://ollama.com/search)
```bash
    ollama  pull llama3.2
    ollama  pull mistral
    # Launch ollama server
    ollama serve
```

### Configure Environment
```bash
    cp .env.sample .env 
    nano .env
    # specify SEARCH_PROVIDER exa or firecrawl
    # add exa or firecrawl api keys 
    # save the file
```


## Usage

### Start MCP Server
```bash
# Create a terminal session with tmux
tmux new-session -d -s mcp-server
tmux attach-session -t mcp-server
# Note: to detach use Ctrl + B then D

# Launch the MCP server
uv run app/mcp_server.py
```

### Execute Queries
```bash
    # Create another terminal session
    tmux new-session -d -s mcp-client
    tmux attach-session -t mcp-client

    # Run queries
    uv run app/agent.py "Donne moi les dernières actualités à propos des Agents IA"
```

<p align="center"><img src="img/image.png" alt="[Core Components" width="1200" height="600"></p>

## API Endpoints
The server provides the following REST endpoints:

-    POST /search - Enhanced search with RAG capabilities
-    POST /analyze - Text analysis and statistics
-    POST /generate - Content generation
-    GET /health - Server health check
-    GET /tools - List available MCP tools

## Configuration

The system is highly configurable through environment variables. Key configuration options include:

-    Ollama Settings: Model selection, temperature, token limits
-    RAG Parameters: Chunk size, overlap, results count
-    Search Providers: Exa or Firecrawl with API keys
-    Server Configuration: Host, port, logging levels
-    FAISS Settings: CPU/GPU mode, index path

See .env.sample for all available configuration options.

## Core Components
### Agent System

-    OllamaAgent: Main agent combining search + RAG + summarization
-    AnalysisAgent: Text analysis and statistics
-    GenerationAgent: Content creation using LLMs
-    AgentOrchestrator: Central coordination and routing

### RAG Pipeline

-    FAISS Vector Store: Efficient similarity search
-    Ollama Embeddings: Text embedding generation
-    Document Processing: Chunking and text splitting
-    Similarity Search: Configurable result retrieval

### Search Engine

-    Multiple Providers: Exa and Firecrawl support
-    Content Extraction: Web scraping and cleaning
-    Text Normalization: HTML parsing and filtering

### Technology Stack

-    Framework: FastAPI, FastMCP
-    LLM: Ollama (llama3.2, mistral)
-    Vector Database: FAISS
-    Search: Exa, Firecrawl
-    Document Processing: LangChain, BeautifulSoup
-    Configuration: Python-dotenv
-    Logging: Structured JSON logging

## Licence

The MIT License (MIT) 
Copyright (c) 2025 Olivier Lavaud

# Technical Documentation
## System Purpose

MCP-RAG-Ollama serves as a versatile query answering system that combines the power of large language models with real-time information retrieval. It enables users to:

-    Get answers to questions using contextual knowledge from web searches
-    Implement RAG workflows with Ollama models
-    Access the system via both API endpoints and command-line interface



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
