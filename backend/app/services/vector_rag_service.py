"""
FloxAI Vector RAG Service - ChromaDB-powered semantic search
"""
import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import chromadb
from chromadb.config import Settings
import numpy as np

from app.core.config import get_settings
from app.services.embedding_service import FloxEmbeddingService
from app.services.document_processor import FloxDocumentProcessor

class FloxVectorRAGService:
    """Vector-based RAG service using ChromaDB for semantic search"""
    
    def __init__(self):
        self.settings = get_settings()
        self.embedding_service = FloxEmbeddingService()
        self.document_processor = FloxDocumentProcessor()
        self.client = None
        self.collection = None
        self.is_ready = False
        
        # ChromaDB configuration
        self.collection_name = "floxai_documents"
        self.vector_db_path = Path(self.settings.vector_db_path)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """Initialize the vector RAG service"""
        try:
            print("🔄 Initializing Vector RAG Service...")
            
            # Initialize embedding service
            await self.embedding_service.initialize()
            if not self.embedding_service.is_ready:
                raise RuntimeError("Embedding service failed to initialize")
            
            # Initialize document processor
            await self.document_processor.initialize()
            if not self.document_processor.is_ready:
                raise RuntimeError("Document processor failed to initialize")
            
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(
                path=str(self.vector_db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(self.collection_name)
                print(f"✅ Connected to existing collection: {self.collection_name}")
            except Exception:
                # Collection doesn't exist, create it
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "FloxAI document embeddings"}
                )
                print(f"✅ Created new collection: {self.collection_name}")
            
            self.is_ready = True
            print("✅ Vector RAG Service initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Vector RAG Service: {e}")
            self.is_ready = False
    
    async def load_documents(self, docs_path: Optional[Path] = None) -> Dict:
        """Load and process documents into the vector database"""
        if not self.is_ready:
            raise RuntimeError("Vector RAG service not initialized")
        
        if docs_path is None:
            docs_path = Path(self.settings.docs_path)
        
        print(f"📚 Loading documents from: {docs_path}")
        
        # Process all markdown files
        chunks = self.document_processor.process_directory(docs_path, "*.md")
        
        if not chunks:
            print("⚠️  No documents found to process")
            return {"status": "no_documents", "chunks_processed": 0}
        
        print(f"📄 Processed {len(chunks)} chunks from documents")
        
        # Generate embeddings for all chunks
        print("🔄 Generating embeddings...")
        texts = [chunk['content'] for chunk in chunks]
        embeddings = self.embedding_service.generate_embeddings(texts)
        
        # Prepare data for ChromaDB
        ids = [chunk['id'] for chunk in chunks]
        metadatas = []
        documents = []
        
        for chunk in chunks:
            metadata = {
                'source_file': chunk['source_file'],
                'source_name': chunk['source_name'],
                'doc_type': chunk['doc_type'],
                'chunk_index': chunk['chunk_index'],
                'total_chunks': chunk['total_chunks'],
                'category': chunk['metadata'].get('category', 'general'),
                'title': chunk['metadata'].get('title', ''),
                'created_at': chunk['created_at'],
                'token_count': chunk['token_count']
            }
            metadatas.append(metadata)
            documents.append(chunk['content'])
        
        # Add to ChromaDB
        print("💾 Storing in ChromaDB...")
        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            documents=documents
        )
        
        # Get statistics
        stats = self.document_processor.get_document_stats(chunks)
        stats['status'] = 'success'
        stats['chunks_processed'] = len(chunks)
        
        print(f"✅ Successfully loaded {len(chunks)} chunks into vector database")
        print(f"   📊 Documents: {stats['total_documents']}")
        print(f"   📊 Document types: {stats['doc_types']}")
        
        return stats
    
    async def search(self, query: str, n_results: int = 5, doc_types: Optional[List[str]] = None) -> List[Dict]:
        """Search for relevant documents using semantic similarity"""
        if not self.is_ready:
            return []
        
        if not query.strip():
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.generate_embedding(query)
            
            # Prepare where clause for filtering
            where_clause = {}
            if doc_types:
                where_clause['doc_type'] = {"$in": doc_types}
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            # Process results
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    # Convert distance to similarity score (ChromaDB uses cosine distance)
                    similarity_score = 1 - distance
                    
                    search_results.append({
                        'content': doc,
                        'source': metadata.get('source_name', 'Unknown'),
                        'relevance_score': similarity_score,
                        'doc_type': metadata.get('doc_type', 'general'),
                        'category': metadata.get('category', 'general'),
                        'title': metadata.get('title', ''),
                        'chunk_index': metadata.get('chunk_index', 0),
                        'total_chunks': metadata.get('total_chunks', 1),
                        'metadata': metadata
                    })
            
            return search_results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    async def search_with_context(self, query: str, context: str = "", n_results: int = 5) -> List[Dict]:
        """Search with additional context for better results"""
        if not self.is_ready:
            return []
        
        # Combine query with context
        enhanced_query = f"{query} {context}".strip()
        
        # Search for Flox-related content first
        flox_results = await self.search(enhanced_query, n_results, ['flox_docs', 'blog_post'])
        
        # If we have enough Flox results, return them
        if len(flox_results) >= n_results:
            return flox_results
        
        # Otherwise, search more broadly
        general_results = await self.search(enhanced_query, n_results - len(flox_results))
        
        # Combine and deduplicate
        all_results = flox_results + general_results
        seen_sources = set()
        unique_results = []
        
        for result in all_results:
            source_key = f"{result['source']}_{result.get('chunk_index', 0)}"
            if source_key not in seen_sources:
                seen_sources.add(source_key)
                unique_results.append(result)
        
        return unique_results[:n_results]
    
    async def get_collection_stats(self) -> Dict:
        """Get statistics about the vector collection"""
        if not self.is_ready or not self.collection:
            return {"error": "Service not initialized"}
        
        try:
            count = self.collection.count()
            
            # Get sample metadata to analyze document types
            sample_results = self.collection.get(limit=100)
            doc_types = {}
            categories = {}
            
            if sample_results['metadatas']:
                for metadata in sample_results['metadatas']:
                    doc_type = metadata.get('doc_type', 'unknown')
                    category = metadata.get('category', 'unknown')
                    doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
                    categories[category] = categories.get(category, 0) + 1
            
            return {
                'total_chunks': count,
                'doc_types': doc_types,
                'categories': categories,
                'collection_name': self.collection_name
            }
            
        except Exception as e:
            return {"error": f"Failed to get stats: {e}"}
    
    async def clear_collection(self):
        """Clear all documents from the collection"""
        if not self.is_ready or not self.collection:
            return False
        
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "FloxAI document embeddings"}
            )
            print("✅ Collection cleared successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to clear collection: {e}")
            return False
