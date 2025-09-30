# FloxAI Build & Publish Strategy

## Overview
Enable FloxAI as a layerable and composable Flox environment while maintaining current functionality.

## Key Constraints Discovered
1. **Cannot build from FloxHub environments** - need local git repository
2. **Git requirements**: clean tracked files, remote defined, current revision pushed
3. **Layering works at runtime** - environments stack with upper layers overriding lower
4. **Composition works at build time** - declarative merging with conflict resolution

## Proposed Architecture

### 1. Modular Component Design
Split FloxAI into composable components:

#### Core Components:
- **floxai-base**: Essential Python/Node runtime, FastAPI, React build tools
- **floxai-rag**: RAG service, ChromaDB, embeddings, document processing
- **floxai-llm**: LLM service, Anthropic client, Claude integration
- **floxai-ui**: Frontend components, Vite dev server, production build
- **floxai-docs**: Documentation vectorization, Flox/Nix knowledge base

#### Usage Patterns:
- **Full FloxAI**: Compose all components for complete experience
- **Layering**: Users can layer individual components as needed
- **Development**: Compose base + specific components for focused work

### 2. Build Strategy

#### Phase 1: Local Environment Setup
1. Create clean local git repository (not FloxHub-linked)
2. Copy FloxAI source with modular manifest structure
3. Implement build scripts for each component

#### Phase 2: Component Manifests
Each component gets its own manifest with:
- `[build]` sections for packaging
- `[install]` for dependencies
- `[vars]` for configuration
- `[services]` for runtime services

#### Phase 3: Composition Manifest
Master manifest using `[include]` to compose components:
```toml
[include]
environments = [
    { remote = "8bittacosupreme/floxai-base" },
    { remote = "8bittacosupreme/floxai-rag" },
    { remote = "8bittacosupreme/floxai-llm" },
    { remote = "8bittacosupreme/floxai-ui" },
    { remote = "8bittacosupreme/floxai-docs" }
]
```

### 3. Layering Benefits
- **For Developers**: Layer `floxai-docs` on existing environments for AI assistance
- **For Teams**: Layer `floxai-rag` for knowledge base functionality
- **For Projects**: Layer complete FloxAI for full development co-pilot

### 4. Migration Path
1. **No Breaking Changes**: Current unified approach continues working
2. **Gradual Adoption**: Components available for layering
3. **User Choice**: Full install vs selective layering

## Implementation Steps

### Step 1: Create Build Environment
- Set up local git repo with clean state
- Implement modular build scripts
- Test simple component builds

### Step 2: Component Separation
- Extract RAG service as standalone buildable component
- Extract LLM service as standalone component
- Create UI build component
- Create docs vectorization component

### Step 3: Publishing
- Publish components to FloxHub
- Create composition manifests
- Test layering scenarios

### Step 4: Documentation & Examples
- Layer usage examples
- Composition patterns
- Migration guide

## Benefits
1. **Flexibility**: Users choose components they need
2. **Reusability**: Components useful in other projects
3. **Maintainability**: Cleaner separation of concerns
4. **Extensibility**: Easier to add new AI capabilities
5. **Performance**: Lighter environments for specific use cases

## Next Actions
1. Create local build environment
2. Implement first component build (likely floxai-base)
3. Test build/publish process
4. Iterate on remaining components