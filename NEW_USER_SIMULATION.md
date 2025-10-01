# New User Simulation: Discovering FloxAI

## User Journey: Sarah, Python Developer

Sarah is working on a Python data analysis project and heard about AI coding assistants. She has Flox installed.

### 1. Discovery
```bash
$ flox search ai
# Results include:
# 8bittacosupreme/floxai-complete - Complete FloxAI development co-pilot system
# 8bittacosupreme/floxai-base     - Core runtime and dependencies for FloxAI
# 8bittacosupreme/floxai-llm      - Claude integration and AI services
```

### 2. Quick Start (Complete System)
```bash
$ flox activate -r 8bittacosupreme/floxai-complete
✅ You are now using the environment 'floxai-complete'.

FloxAI Complete System v1.0.3
All components: Base + RAG + LLM + Frontend + Documentation
Ready to use as development co-pilot
Run: floxai-setup to initialize

$ floxai-setup
🔑 Setting up Claude API key...
[Interactive key prompt and setup]
✅ FloxAI ready for use!

$ floxai
Starting FloxAI...
🚀 Backend running on port 8000
🌐 Frontend running on port 3000
💬 Chat at http://localhost:3000
```

### 3. Minimal Integration (Just AI Chat)
Sarah's colleague Bob just wants AI help in his existing project:

```bash
$ cd my-rust-project
$ flox activate  # His existing Rust environment

# Add AI capabilities on top
$ flox activate -r 8bittacosupreme/floxai-base
✅ You are now using the environment 'floxai-base'.

$ flox activate -r 8bittacosupreme/floxai-llm
✅ You are now using the environment 'floxai-llm'.

# Now Bob has: His Rust environment + Python runtime + Claude AI
$ floxai-llm
FloxAI LLM Component v1.0.3
Provides: Claude Sonnet 4, Anthropic API integration
Features: Secure API key management, LLM conversations
Usage: Layer on floxai-base for AI chat functionality
```

### 4. Project Integration (Composition)
Sarah's team wants AI built into their project environment:

```bash
$ cd team-project
$ cat > .flox/env/manifest.toml << 'EOF'
version = 1

[include]
environments = [
    { remote = "8bittacosupreme/floxai-base" },
    { remote = "8bittacosupreme/floxai-llm" }
]

[install]
# Team's project dependencies
pytest.pkg-path = "python313Packages.pytest"
pandas.pkg-path = "python313Packages.pandas"
jupyter.pkg-path = "python313Packages.jupyter"
EOF

$ flox activate
✅ You are now using the environment 'team-project'.
FloxAI Base Component v1.0.3
Provides: Python 3.13, FastAPI, Node.js, Git, Core utilities

# Team now has: Their project deps + AI capabilities
# Integrated, reproducible, shareable
```

### 5. Component Discovery
```bash
$ floxai-base
FloxAI Base Component v1.0.3
Provides: Python 3.13, FastAPI, Node.js, Git, Core utilities
Usage: Layer this environment for FloxAI development
Next: Add floxai-rag, floxai-llm, or other components as needed

$ ls /nix/store/*floxai-base*/share/floxai/
base-info.json  # Contains component metadata
```

## What Users Experience

### ✅ Immediate Value
- **30 seconds to AI assistance**: `flox activate -r 8bittacosupreme/floxai-complete`
- **No setup complexity**: Components handle dependencies
- **Works anywhere**: Layer on any existing environment

### ✅ Flexible Adoption
- **Start minimal**: Just base + LLM for simple AI chat
- **Grow complexity**: Add RAG when knowledge base needed
- **Full system**: Complete development co-pilot

### ✅ Team Integration
- **Shareable**: Commit manifest changes to git
- **Reproducible**: Same environment for whole team
- **Composable**: Mix with project-specific dependencies

### ✅ No Vendor Lock-in
- **Exit anytime**: Type `exit` to remove
- **Mix and match**: Use just the components you need
- **Standard Flox**: Uses normal Flox layering/composition

## User Testimonials (Simulated)

> "I just wanted AI code help and `flox activate -r 8bittacosupreme/floxai-llm` gave me Claude integration instantly. No Docker, no complex setup." - Bob (Rust Developer)

> "Our team uses the composition approach. FloxAI is just part of our project environment now. Everyone gets AI assistance automatically." - Sarah (Team Lead)

> "Started with just the LLM component, then added knowledge base when I needed doc search. Perfect gradual adoption." - Alice (Data Scientist)

## Success Metrics Achieved

✅ **Discovery**: Found via `flox search`
✅ **Quick Start**: Working AI in 30 seconds
✅ **Flexibility**: Minimal to full system options
✅ **Integration**: Works with existing projects
✅ **Team Adoption**: Shareable via git
✅ **No Lock-in**: Standard Flox patterns