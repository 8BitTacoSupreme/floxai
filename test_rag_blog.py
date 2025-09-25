#!/usr/bin/env python3
"""
Test script to check if blog posts are loaded into the RAG system
"""
import sys
import os
sys.path.insert(0, 'backend')

from backend.app.services.rag_service import FloxRAGService
from backend.app.core.config import get_settings
import asyncio

async def test_rag_blog_loading():
    """Test if blog posts are loaded into RAG system"""
    print("🧪 Testing RAG Blog Post Loading")
    print("=" * 50)
    
    # Initialize RAG service
    rag_service = FloxRAGService()
    await rag_service.initialize()
    
    print(f"📚 Total documents loaded: {len(rag_service.documents)}")
    
    # Check for blog posts specifically
    blog_docs = [doc for doc in rag_service.documents if 'blogs' in doc.get('path', '')]
    print(f"📰 Blog documents found: {len(blog_docs)}")
    
    for doc in blog_docs:
        print(f"   - {doc['source']} ({doc.get('type', 'unknown')})")
        if 'build' in doc['content'].lower() and 'publish' in doc['content'].lower():
            print(f"     ✅ Contains 'build and publish' content")
    
    # Test search for "build and publish"
    print("\n🔍 Testing search for 'build and publish'...")
    results = await rag_service.search("build and publish")
    print(f"   Found {len(results)} results")
    
    for i, result in enumerate(results[:3], 1):
        print(f"   {i}. {result['source']} (score: {result['relevance_score']:.2f})")
        print(f"      {result['content'][:100]}...")
        print()

if __name__ == "__main__":
    asyncio.run(test_rag_blog_loading())
