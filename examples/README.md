# FloxAI Component Usage Examples

These examples demonstrate how to use FloxAI components in different combinations.

## Layering (Ad Hoc Usage)

### Basic Development with AI
```bash
# Start with base runtime
flox activate -r 8bittacosupreme/floxai-base

# Add AI capabilities when needed
flox activate -r 8bittacosupreme/floxai-llm
```

### Full Knowledge-Aware Development
```bash
# Layer all components for complete functionality
flox activate -r 8bittacosupreme/floxai-base -- \
flox activate -r 8bittacosupreme/floxai-rag -- \
flox activate -r 8bittacosupreme/floxai-llm
```

## Composition (Declarative Usage)

### floxai-minimal.toml
Use when you only need AI chat without knowledge base:
```bash
flox activate -f examples/floxai-minimal.toml
```

### floxai-knowledge.toml
Use when you need AI with document knowledge:
```bash
flox activate -f examples/floxai-knowledge.toml
```

### Custom Project Integration
```toml
# your-project/.flox/env/manifest.toml
[include]
environments = [
    { remote = "8bittacosupreme/floxai-base" },
    { remote = "8bittacosupreme/floxai-llm" }
]

[install]
# Your project-specific packages
rust.pkg-path = "rust"
```

## Component Overview

| Component | Provides | Use When |
|-----------|----------|----------|
| `floxai-base` | Python, FastAPI, Node.js, Git | Need foundation runtime |
| `floxai-rag` | ChromaDB, embeddings, search | Need knowledge base |
| `floxai-llm` | Claude API, secure keys | Need AI conversations |
| `floxai-complete` | Everything above + UI | Need full system |

## Migration Path

**Current Users**: No changes needed - your existing FloxAI continues working

**New Users**: Choose your approach:
- **Simple**: Use `floxai-complete` for everything
- **Modular**: Layer/compose components as needed
- **Project-specific**: Include relevant components in your manifest