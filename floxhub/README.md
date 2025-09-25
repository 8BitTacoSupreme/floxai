# FloxAI - FloxHub Package

The ultimate Flox development co-pilot with ChromaDB vector RAG, packaged for FloxHub distribution.

## 🎯 Three Usage Modes

### 1. **Layer Mode** (Recommended)
Add FloxAI as a layer to any Flox environment for context-aware AI assistance.

```bash
# Install as layer
flox install floxai --layer

# Use in your environment
floxai chat "How do I add Redis to this environment?"
floxai analyze
floxai suggest
floxai layer    # Start full layer interface
```

**Perfect for**: Getting AI assistance while working in your own projects

### 2. **Standalone Mode**
Run FloxAI as a dedicated development environment with full knowledge base.

```bash
# Install standalone
flox install floxai

# Activate and use
flox activate floxai
floxybot        # General Flox/Nix AI
floxai-demo     # Capabilities showcase
```

**Perfect for**: Learning Flox, general troubleshooting, demonstrations

### 3. **Service Mode**
Run FloxAI as a service with full web interface.

```bash
# Install service mode
flox install floxai --service

# Start service
floxai serve
# Access at http://localhost:3000
```

**Perfect for**: Team environments, persistent AI assistance

## 🧠 Vector RAG System

FloxAI includes a sophisticated vector-based Retrieval Augmented Generation system:

- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: `all-MiniLM-L6-v2` embeddings
- **2,055 Document Chunks**: Flox blogs, docs, and processed content
- **Semantic Search**: Understands context and meaning, not just keywords
- **Flox-Focused**: Prioritizes Flox-specific content in responses

## 🚀 Installation

### Quick Install
```bash
# Layer mode (recommended)
./install.sh layer

# Standalone mode
./install.sh standalone

# Service mode
./install.sh service
```

### Manual Install
```bash
# Install packages
flox install python313 nodejs git curl sqlite jq tree
flox install python313Packages.chromadb python313Packages.sentence-transformers
flox install python313Packages.fastapi python313Packages.uvicorn
flox install python313Packages.anthropic python313Packages.requests
# ... (see install.sh for complete list)

# Set up environment
export CLAUDE_API_KEY="your-key-here"
floxai setup
```

## 📋 Commands

### Layer Mode Commands (L3 Resident Engineer)
- `floxai chat <message>` - Ask FloxAI questions
- `floxai analyze` - Analyze current environment
- `floxai suggest` - Get improvement suggestions
- `floxai layer` - Start full layer interface
- `floxai serve` - Start as service

### Standalone Mode Commands (L1/L2 Support)
- `floxybot` - General Flox/Nix AI assistant
- `floxai-setup` - Interactive setup
- `floxai-demo` - Run capabilities demo
- `flox-demo` - Interactive Flox learning journey

## 🎯 Use Cases

### **Layer Mode Examples**
```bash
# In a Node.js project
floxai chat "How do I add TypeScript to this environment?"
floxai analyze  # Shows Node.js project analysis
floxai suggest  # Gets TypeScript-specific suggestions

# In a Python project  
floxai chat "What's the best way to manage Python dependencies in Flox?"
floxai layer    # Full interface with Python context
```

### **Standalone Mode Examples**
```bash
# General Flox learning
floxybot  # Ask about Flox concepts, troubleshooting

# Demonstrations
floxai-demo  # Show Flox capabilities to others
```

## 🔧 Configuration

### Environment Variables
```bash
export CLAUDE_API_KEY="your-anthropic-api-key"
export FLOXAI_CONTEXT_MODE=true    # Enable context awareness
export FLOXAI_DEV_MODE=false       # Production mode
```

### Flox Environment
```toml
# In your manifest.toml
[vars]
CLAUDE_API_KEY = "your-key-here"
FLOXAI_CONTEXT_MODE = "true"
```

## 🌟 Features

- **AI-Powered Assistance**: Claude AI with Flox expertise
- **Vector RAG**: Semantic search across Flox documentation
- **Context Awareness**: Analyzes your specific environment
- **Cross-Platform**: macOS (Intel/ARM) and Linux support
- **Flox Integration**: Demonstrates Flox's core capabilities
- **Layer Composition**: Shows Flox's layer system
- **Service Management**: Flox services without Docker

## 📚 Documentation

- [FloxAI Main README](../README.md) - Complete documentation
- [Vector RAG Architecture](../README.md#-vector-rag-system-architecture) - Technical details
- [Flox Documentation](https://flox.dev/docs) - Flox platform docs
- [FloxHub Guide](https://flox.dev/docs/floxhub) - FloxHub distribution

## 🐛 Support

- **Issues**: [GitHub Issues](https://github.com/flox/floxai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/flox/floxai/discussions)
- **Flox Community**: [Flox Discord](https://discord.gg/flox)

## 🎉 Why FloxAI?

FloxAI demonstrates Flox's power for:
- **Reproducible Environments**: Same setup everywhere
- **Cross-Platform Development**: macOS and Linux compatibility
- **Layer Composition**: Add AI to any Flox environment
- **Service Management**: Run complex applications without Docker
- **Native Performance**: No virtualization overhead

Every aspect reinforces Flox's value proposition: development environments that "just work" everywhere.