"""
FloxAI RAG Service - Flox-focused document search and retrieval
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

from app.services.vector_rag_service import FloxVectorRAGService

class FloxRAGService:
    """Flox-focused document search service with vector-based semantic search"""
    
    def __init__(self):
        self.vector_service = FloxVectorRAGService()
        self.is_ready = False
        self.flox_docs = []
        self.documents = []
    
    async def initialize(self):
        """Initialize the service"""
        await self.vector_service.initialize()
        if self.vector_service.is_ready:
            await self.load_documents()
            self.is_ready = True
        else:
            print("❌ Vector RAG service failed to initialize")
            self.is_ready = False
    
    async def load_documents(self):
        """Load Flox documentation into vector database"""
        from app.core.config import get_settings
        settings = get_settings()
        docs_path = Path(settings.docs_path)
        
        if not docs_path.exists():
            print("⚠️  Documentation path does not exist")
            return
        
        # Load documents into vector database
        stats = await self.vector_service.load_documents(docs_path)
        print(f"📚 Loaded {stats.get('chunks_processed', 0)} document chunks")
        
        # Add FloxAI-specific knowledge
        self._add_floxai_knowledge()
        
        # Add Flox best practices
        self._add_flox_best_practices()
    
    def _add_floxai_knowledge(self):
        """Add FloxAI-specific documentation"""
        floxai_docs = [
            {
                'content': """
# FloxAI - Your Flox Development Co-pilot

FloxAI demonstrates the power of Flox for creating reproducible, cross-platform development environments.

## Key Features:
- Cross-platform compatibility (macOS Intel/ARM, Linux x86_64/ARM64)
- Reproducible environments using manifest.toml
- Service orchestration with Flox services
- Environment variable management
- Multi-language development (Python + Node.js)

## Quick Commands:
- `flox activate` - Enter the FloxAI environment
- `floxybot` - Start FloxAI in production mode
- `floxybotdev` - Start FloxAI in development mode
- `floxai-setup` - Initialize documentation and database
- `floxstatus` - Show Flox environment status
                """,
                'source': 'floxai_overview.md',
                'path': 'floxai_overview.md',
                'type': 'floxai_knowledge'
            },
            {
                'content': """
# Flox Environment Management

## Creating Environments:
```bash
# Initialize a new Flox environment
flox init

# Activate an environment
flox activate

# Edit the manifest
flox edit
```

## Managing Packages:
```toml
[install]
python3.pkg-path = "python3"
nodejs.pkg-path = "nodejs" 
git.pkg-path = "git"
```

## Environment Variables:
```toml
[vars]
API_PORT = "8000"
DATABASE_URL = "sqlite:///app.db"
```

## Services:
```toml
[services.api]
command = "python app.py"
is-daemon = true
```
                """,
                'source': 'flox_basics.md',
                'path': 'flox_basics.md', 
                'type': 'flox_knowledge'
            }
        ]
        
        self.flox_docs.extend(floxai_docs)
        self.documents.extend(floxai_docs)
    
    def _add_flox_best_practices(self):
        """Add Flox best practices and common patterns"""
        best_practices = {
            'content': """
# Flox Best Practices

## Manifest Structure:
1. Always specify version = 1
2. Use descriptive package names with .pkg-path
3. Organize variables logically in [vars]
4. Use services for long-running processes
5. Leverage hooks for environment setup

## Cross-Platform Compatibility:
- Test on different architectures
- Use Flox-managed packages when possible
- Avoid hardcoded paths - use environment variables
- Specify systems when needed

## Development Workflow:
- Use `flox activate` to enter environments
- Edit manifest.toml for changes
- Use services for multi-process applications
- Leverage environment variables for configuration

## Common Patterns:
- Web apps: API service + frontend service
- Data science: Python + Jupyter + packages
- Full-stack: Database + API + frontend + tools
            """,
            'source': 'flox_best_practices.md',
            'path': 'flox_best_practices.md',
            'type': 'best_practices'
        }
        
        self.documents.append(best_practices)
    
    async def search(self, query: str) -> List[Dict]:
        """Enhanced search with Flox focus using vector similarity"""
        if not self.is_ready:
            return []
        
        # Use vector search for semantic similarity
        results = await self.vector_service.search_with_context(
            query=query,
            context="flox development environment package management",
            n_results=5
        )
        
        # Boost Flox-related content
        flox_keywords = ['flox', 'manifest', 'environment', 'package', 'service', 'activate']
        has_flox_context = any(word in query.lower() for word in flox_keywords)
        
        # Apply Flox-specific boosting
        for result in results:
            content_lower = result['content'].lower()
            
            # Boost Flox-specific documents
            if result.get('doc_type') in ['flox_docs', 'blog_post']:
                result['relevance_score'] *= 1.5
            
            # Further boost if query has Flox context
            if has_flox_context and 'flox' in content_lower:
                result['relevance_score'] *= 1.3
            
            # Ensure relevance score is between 0 and 1
            result['relevance_score'] = min(1.0, result['relevance_score'])
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results
    
    def _extract_snippet(self, content: str, query_words: List[str], max_length: int = 300) -> str:
        """Extract a relevant snippet from the content"""
        content_lower = content.lower()
        
        # Find the first occurrence of any query word
        best_pos = len(content)
        for word in query_words:
            pos = content_lower.find(word)
            if pos != -1 and pos < best_pos:
                best_pos = pos
        
        if best_pos == len(content):
            return content[:max_length] + "..." if len(content) > max_length else content
        
        # Extract snippet around the match
        start = max(0, best_pos - max_length // 2)
        end = min(len(content), start + max_length)
        
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet
    
    async def get_context_for_query(self, query: str) -> Tuple[str, List[Dict]]:
        """Get formatted context with Flox expertise"""
        results = await self.search(query)
        
        if not results:
            return "", []
        
        context_parts = []
        for result in results[:3]:
            doc_type = result.get('doc_type', 'general')
            type_label = {
                'flox_knowledge': 'FloxAI Knowledge',
                'flox_docs': 'Flox Documentation', 
                'best_practices': 'Flox Best Practices',
                'general': 'Documentation'
            }.get(doc_type, 'Documentation')
            
            context_parts.append(f"[{type_label}] {result['source']}\n{result['content']}")
        
        context = "\n\n---\n\n".join(context_parts)
        return context, results
    
    async def cleanup(self):
        """Cleanup resources"""
        pass
