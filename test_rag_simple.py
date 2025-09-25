#!/usr/bin/env python3
"""
Test the current RAG system to see if blog posts are loaded and searchable
"""
import sys
import os
sys.path.insert(0, 'backend')

from backend.app.services.rag_service import FloxRAGService
import asyncio

async def test_rag():
    print("🧪 Testing Current RAG System")
    print("=" * 50)
    
    # Initialize RAG service
    rag = FloxRAGService()
    await rag.initialize()
    
    print(f"📚 Total documents loaded: {len(rag.documents)}")
    
    # Check for blog posts
    blog_docs = [doc for doc in rag.documents if 'blogs' in doc.get('path', '')]
    print(f"📰 Blog documents: {len(blog_docs)}")
    
    # Test search for "build and publish"
    print("\n🔍 Testing search for 'build and publish'...")
    results = await rag.search("build and publish")
    print(f"   Found {len(results)} results")
    
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['source']} (score: {result['relevance_score']:.2f})")
        print(f"      Type: {result['doc_type']}")
        print(f"      Content: {result['content'][:200]}...")
        print()
    
    # Test search for "flox build"
    print("\n🔍 Testing search for 'flox build'...")
    results2 = await rag.search("flox build")
    print(f"   Found {len(results2)} results")
    
    for i, result in enumerate(results2[:3], 1):
        print(f"   {i}. {result['source']} (score: {result['relevance_score']:.2f})")
        print(f"      Content: {result['content'][:150]}...")
        print()

if __name__ == "__main__":
    asyncio.run(test_rag())
