#!/usr/bin/env python3
"""
Migration script to process existing documents into vector database
"""
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, 'backend')

from backend.app.services.vector_rag_service import FloxVectorRAGService
from backend.app.core.config import get_settings

async def migrate_documents():
    """Migrate existing documents to vector database"""
    print("🚀 Starting Vector RAG Migration")
    print("=" * 50)
    
    # Initialize vector service
    vector_service = FloxVectorRAGService()
    await vector_service.initialize()
    
    if not vector_service.is_ready:
        print("❌ Failed to initialize vector service")
        return False
    
    # Get settings
    settings = get_settings()
    docs_path = Path(settings.docs_path)
    
    if not docs_path.exists():
        print(f"❌ Documentation path does not exist: {docs_path}")
        return False
    
    print(f"📁 Processing documents from: {docs_path}")
    
    # Clear existing collection
    print("🗑️  Clearing existing collection...")
    await vector_service.clear_collection()
    
    # Load documents
    print("📚 Loading documents into vector database...")
    stats = await vector_service.load_documents(docs_path)
    
    if stats.get('status') == 'success':
        print("✅ Migration completed successfully!")
        print(f"   📊 Chunks processed: {stats.get('chunks_processed', 0)}")
        print(f"   📊 Documents: {stats.get('total_documents', 0)}")
        print(f"   📊 Document types: {stats.get('doc_types', {})}")
        
        # Test search
        print("\n🧪 Testing semantic search...")
        test_results = await vector_service.search("build and publish", n_results=3)
        print(f"   Found {len(test_results)} results for 'build and publish'")
        
        for i, result in enumerate(test_results, 1):
            print(f"   {i}. {result['source']} (score: {result['relevance_score']:.3f})")
            print(f"      Type: {result['doc_type']}")
            print(f"      Content: {result['content'][:100]}...")
            print()
        
        return True
    else:
        print(f"❌ Migration failed: {stats}")
        return False

async def test_vector_search():
    """Test the vector search functionality"""
    print("\n🔍 Testing Vector Search Capabilities")
    print("=" * 50)
    
    vector_service = FloxVectorRAGService()
    await vector_service.initialize()
    
    if not vector_service.is_ready:
        print("❌ Vector service not ready")
        return
    
    # Test queries
    test_queries = [
        "build and publish",
        "flox environment management",
        "manifest.toml configuration",
        "package management",
        "cross-platform development"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = await vector_service.search(query, n_results=2)
        print(f"   Found {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['source']} (score: {result['relevance_score']:.3f})")
            print(f"      {result['content'][:80]}...")

if __name__ == "__main__":
    print("FloxAI Vector RAG Migration")
    print("This will process all documents into a vector database for semantic search")
    print()
    
    # Run migration
    success = asyncio.run(migrate_documents())
    
    if success:
        # Run tests
        asyncio.run(test_vector_search())
        print("\n🎉 Migration and testing completed successfully!")
    else:
        print("\n❌ Migration failed. Check the errors above.")
        sys.exit(1)
