# FloxAI - The Flox Development Co-pilot 🤖

FloxAI is both a powerful Flox development assistant and a comprehensive demonstration of Flox's capabilities for creating reproducible, cross-platform development environments. **Latest update**: Now powered by Claude Sonnet 4 with improved service initialization!

## 🎯 Dual Purpose

**1. Production-Ready Flox Co-pilot**
- Intelligent assistance for Flox environments and Nix ecosystem
- Context-aware development guidance
- Manifest analysis and optimization suggestions

**2. Flox Technology Showcase**
- Demonstrates Flox's power for multi-language development stacks
- Shows cross-platform reproducibility without Docker
- Exhibits environment isolation and dependency management

### Core Features

#### 1. **AI-Powered Flox Assistance** ⚡
- Answers questions about Flox environments, manifest.toml files, and best practices
- **NEW**: Powered by Claude Sonnet 4 (latest model) for superior responses
- Includes RAG (Retrieval Augmented Generation) for searching Flox documentation
- **FIXED**: Resolved service initialization issues for reliable AI functionality

#### 2. **Full-Stack Architecture**
- **Backend**: Python FastAPI with async support
  - REST API endpoints for chat, feedback, and health monitoring
  - SQLite database for conversation history and feedback tracking
  - **ChromaDB vector store** for semantic document search with embeddings
  - **Vector RAG Service** with semantic similarity search
  - **Document Processor** for intelligent chunking and embedding generation
- **Frontend**: React TypeScript with Vite
  - Real-time chat interface with markdown rendering
  - Syntax highlighting for code blocks
  - Feedback mechanism for response quality tracking
  - Responsive design with Flox branding

#### 3. **Flox Environment Integration**
- Runs entirely within a Flox environment
- Uses Flox-managed packages: Python 3.13, Node.js 22, SQLite, Git, and more
- Environment variables managed through manifest.toml
- Demonstrates cross-platform compatibility (macOS ARM/Intel, Linux)

### Current Status - MVP Complete ✅

1. **Vector RAG System**: ✅ ChromaDB-powered semantic search with 2,055 document chunks
2. **Documentation**: ✅ Full Flox documentation ingested and searchable
3. **Context Awareness**: ✅ Detects Flox environment and project context
4. **Learning**: ✅ Feedback system implemented with continuous improvement
5. **Flox Integration**: ✅ Complete Flox environment with all dependencies
6. **Claude AI**: ✅ Working Claude integration with correct model

## 🧠 Vector RAG System Architecture

FloxAI uses a sophisticated vector-based Retrieval Augmented Generation (RAG) system powered by ChromaDB for semantic document search.

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Documents     │───▶│  Document        │───▶│   ChromaDB      │
│   (Markdown)    │    │  Processor       │    │   Vector Store  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Embedding       │    │   Vector RAG    │
                       │  Service         │    │   Service       │
                       └──────────────────┘    └─────────────────┘
```

### Key Features

- **Semantic Search**: Uses `all-MiniLM-L6-v2` embeddings for understanding context and meaning
- **Intelligent Chunking**: 500-character chunks with 50-character overlap for optimal retrieval
- **Document Processing**: 2,055 chunks from 117 documents including:
  - 1,645 blog post chunks (including "Introducing Flox Build and Publish")
  - 410 Flox documentation chunks
- **Flox-Focused Boosting**: Prioritizes Flox-specific content in search results
- **Persistent Storage**: ChromaDB ensures fast retrieval across sessions

### Search Capabilities

- **Semantic Understanding**: Finds relevant content even with different wording
- **Context-Aware**: Boosts Flox-related content for development queries
- **Multi-Document Search**: Searches across blogs, docs, and processed content
- **Relevance Scoring**: Returns results ranked by semantic similarity

### Vector RAG Services

#### 1. **FloxVectorRAGService** (`vector_rag_service.py`)
- ChromaDB collection management
- Semantic search with cosine similarity
- Document loading and processing
- Flox-focused content boosting

#### 2. **FloxEmbeddingService** (`embedding_service.py`)
- Text embedding generation using `all-MiniLM-L6-v2`
- Intelligent text chunking (500 chars with 50 char overlap)
- Cosine similarity calculations
- Text cleaning and normalization

#### 3. **FloxDocumentProcessor** (`document_processor.py`)
- Markdown document processing
- Metadata extraction (title, category, date)
- Chunk generation with unique IDs
- Document type classification

#### 4. **FloxRAGService** (`rag_service.py`)
- Main RAG interface
- Integrates vector search with Flox-specific boosting
- Context-aware search enhancement
- Legacy keyword search fallback

## 🚀 Usage Modes

FloxAI offers three distinct usage modes to demonstrate Flox's versatility:

### Prerequisites
- Flox installed (version 1.7.3+)
- Claude API key from Anthropic (optional, but recommended)

### Quick Start
```bash
# Clone and enter the project
cd floxai

# Activate Flox environment
flox activate

# One-time setup (prompts for Claude API key)
./floxai-setup
```

### Usage Modes

#### 1. **Standalone Mode** - General Flox/Nix AI
```bash
./floxybot
```
- **Purpose**: General-purpose Flox and Nix knowledge base
- **Use Case**: Learning Flox, troubleshooting, best practices
- **Features**: Cross-platform guidance, manifest help, ecosystem knowledge
- **Access**: http://localhost:4173 (production build)

#### 2. **Layer Mode** - L3 Resident Engineer
```bash
floxai --layer
```
- **Purpose**: Hands-on environment work and analysis
- **Use Case**: Add FloxAI as a layer to any Flox environment for context-aware assistance
- **Features**: Environment analysis, manifest optimization, project-specific suggestions
- **Access**: Full web interface with environment context

#### 3. **Demo Mode** - Flox Capabilities Showcase
```bash
./floxai-demo
```

#### 4. **Interactive Learning** - Complete Flox Learning Journey
```bash
./flox-demo
```
- **Purpose**: Interactive Flox learning with hands-on project building
- **Use Case**: Learning Flox concepts, building real projects, understanding workflows
- **Features**: 
  - Enhance existing projects with FloxAI layer
  - Build hello world projects from scratch
  - Learn: init → develop → build → publish → deploy
  - Interactive guidance through Flox features

### Available Commands
- `floxai-setup` - Interactive setup with Claude API key configuration
- `floxybot` - L1/L2 support (general questions, troubleshooting) **← Default for production use**
- `floxai --layer` - L3 resident engineer (hands-on environment work)
- `flox-demo` - Interactive Flox learning journey (walkthrough all features)
- `update_docs.sh` - Update documentation and vector database (Flox docs, Nix docs, Flox blogs, ChromaDB)

### API Endpoints
- `GET /health` - Health check with service status
- `GET /docs` - Interactive API documentation
- `POST /api/chat/query` - Main chat endpoint
- `POST /api/chat/feedback` - Submit feedback
- `GET /api/chat/flox-stats` - Usage statistics

## Project Structure
```
floxai/
├── .flox/env/manifest.toml  # Flox environment definition
├── backend/                 # Python FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── db/             # Database layer
│   │   └── services/       # LLM and RAG services
│   │       ├── rag_service.py           # Main RAG service
│   │       ├── vector_rag_service.py    # ChromaDB vector search
│   │       ├── embedding_service.py     # Text embeddings
│   │       ├── document_processor.py    # Document chunking
│   │       ├── llm_service.py           # Claude AI integration
│   │       └── learning_service.py      # Feedback learning
│   └── requirements.txt
├── frontend/               # React TypeScript application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── services/       # API client
│   └── package.json
├── scripts/                # Utility scripts
├── data/                   # Runtime data (created on setup)
│   ├── floxai.db          # SQLite database
│   ├── vector_db/         # ChromaDB vector storage
│   └── flox_docs/         # Documentation
└── venv/                   # Python virtual environment

```

## Technology Stack
- **Backend**: Python 3.13, FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS
- **AI/ML**: Anthropic Claude API, ChromaDB, Sentence Transformers, Tiktoken
- **Vector RAG**: ChromaDB vector store, all-MiniLM-L6-v2 embeddings
- **Infrastructure**: Flox package management, SQLite, Node.js 22

## Feedback System
Users can mark responses as helpful, which:
- Records success metrics in the database
- Tracks which responses work for users
- Calculates success rates for monitoring
- Provides data for future improvements

## 📦 FloxHub Integration (Planned)

FloxAI is designed for easy distribution via FloxHub:

### As a Layer
```bash
# In any Flox environment
flox install floxai --layer
floxai chat "How do I add Redis to this environment?"
floxai analyze  # Analyzes current manifest
floxai suggest  # Provides improvement suggestions
```

### As a Standalone Package
```bash
flox install floxai
flox activate floxai-env
floxybot  # General Flox/Nix AI assistant
```

### As a Service
```bash
flox run floxai --service --port 8080
# Provides HTTP API for integration with other tools
```

## 🎯 Flox-First Philosophy

FloxAI embodies the "Flox-first" approach to development:

### Instead of Docker
- **Before**: Complex Dockerfiles, image builds, container orchestration
- **After**: Simple `manifest.toml`, native performance, instant startup

### Instead of Language-Specific Managers
- **Before**: pyenv + nvm + rbenv + different versions across projects
- **After**: One Flox environment per project, all languages managed consistently

### Instead of Manual Setup
- **Before**: "Works on my machine" - complex setup docs
- **After**: `flox activate` - identical environment everywhere

## Current Statistics Tracked
- Total messages processed
- Unique sessions  
- Successful interactions
- Success rate percentage
- Environment information
- Context-aware vs standalone usage patterns
