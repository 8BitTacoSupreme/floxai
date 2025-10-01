# FloxAI Publishing Workflow

## Build Process (Local Environment Required)

Since builds cannot be performed from FloxHub environments, the publishing workflow requires a local git clone:

```bash
# 1. Clone to local directory
git clone https://github.com/8BitTacoSupreme/floxai.git
cd floxai

# 2. Remove any existing FloxHub environment
rm -rf .flox

# 3. Initialize local Flox environment
flox init

# 4. Install required build dependencies
flox install python313 nodejs git

# 5. Build components
flox build floxai-base      # Core runtime
flox build floxai-rag       # Knowledge base
flox build floxai-llm       # AI services
flox build floxai-complete  # Full system

# 6. Publish to FloxHub
flox publish floxai-base      # → 8bittacosupreme/floxai-base
flox publish floxai-rag       # → 8bittacosupreme/floxai-rag
flox publish floxai-llm       # → 8bittacosupreme/floxai-llm
flox publish floxai-complete  # → 8bittacosupreme/floxai-complete
```

## Expected Build Outputs

### floxai-base
- **Binary**: `/bin/floxai-base` - Component info display
- **Metadata**: `/share/floxai/base-info.json` - Component details
- **Provides**: Python 3.13, FastAPI, Node.js, Git, SQLite

### floxai-rag
- **Binary**: `/bin/floxai-rag` - RAG component info
- **Services**: Copied RAG service code to `/lib/python/floxai/`
- **Metadata**: `/share/floxai/rag-info.json`
- **Provides**: ChromaDB, Sentence Transformers, Document Processing

### floxai-llm
- **Binary**: `/bin/floxai-llm` - LLM component info
- **Services**: LLM service code and secure key setup
- **Metadata**: `/share/floxai/llm-info.json`
- **Provides**: Claude Sonnet 4, Anthropic API, Secure key management

### floxai-complete
- **Binary**: `/bin/floxai` - Full system entry point
- **Services**: Complete backend, frontend, scripts
- **Metadata**: `/share/floxai/complete-info.json`
- **Provides**: Everything integrated

## Publishing Benefits

1. **Components available in FloxHub catalog**
2. **Discoverable via `flox search floxai`**
3. **Layerable with `flox activate -r 8bittacosupreme/floxai-*`**
4. **Composable via `[include]` sections**
5. **Versioned and reproducible**

## Next: Test User Experience

Once published, users can:
- Layer individual components as needed
- Compose custom environments
- Use complete system out-of-the-box
- No need for local FloxAI repository