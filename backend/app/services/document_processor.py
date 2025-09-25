"""
FloxAI Document Processor - Process and chunk documents for vector storage
"""
import os
import re
import uuid
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import hashlib

from app.core.config import get_settings
from app.services.embedding_service import FloxEmbeddingService

class FloxDocumentProcessor:
    """Process documents for vector storage and retrieval"""
    
    def __init__(self):
        self.settings = get_settings()
        self.embedding_service = FloxEmbeddingService()
        self.is_ready = False
        
    async def initialize(self):
        """Initialize the document processor"""
        await self.embedding_service.initialize()
        self.is_ready = self.embedding_service.is_ready
    
    def process_document(self, file_path: Path, content: str, doc_type: str = "general") -> List[Dict]:
        """Process a single document into chunks with metadata"""
        if not self.is_ready:
            raise RuntimeError("Document processor not initialized")
        
        # Extract metadata
        metadata = self._extract_metadata(file_path, content, doc_type)
        
        # Chunk the content
        chunks = self.embedding_service.chunk_text(content)
        
        # Create chunk documents
        chunk_docs = []
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
                
            chunk_doc = {
                'id': self._generate_chunk_id(file_path, i),
                'content': chunk,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'source_file': str(file_path),
                'source_name': file_path.name,
                'doc_type': doc_type,
                'metadata': metadata,
                'created_at': datetime.now().isoformat(),
                'token_count': self.embedding_service.get_token_count(chunk)
            }
            chunk_docs.append(chunk_doc)
        
        return chunk_docs
    
    def process_markdown_file(self, file_path: Path) -> List[Dict]:
        """Process a markdown file specifically"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine document type based on path
            doc_type = self._determine_doc_type(file_path)
            
            return self.process_document(file_path, content, doc_type)
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return []
    
    def process_directory(self, directory_path: Path, pattern: str = "*.md") -> List[Dict]:
        """Process all files in a directory matching the pattern"""
        if not directory_path.exists():
            return []
        
        all_chunks = []
        for file_path in directory_path.rglob(pattern):
            if file_path.is_file():
                chunks = self.process_markdown_file(file_path)
                all_chunks.extend(chunks)
        
        return all_chunks
    
    def _extract_metadata(self, file_path: Path, content: str, doc_type: str) -> Dict:
        """Extract metadata from document"""
        metadata = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'file_size': len(content),
            'doc_type': doc_type,
            'created_at': datetime.now().isoformat()
        }
        
        # Extract title from content
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Extract tags/categories from path
        if 'blogs' in str(file_path):
            metadata['category'] = 'blog'
            # Extract date from filename if possible
            date_match = re.search(r'(\d{1,2})-([A-Za-z]+)-(\d{4})', file_path.name)
            if date_match:
                metadata['publish_date'] = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}"
        elif 'flox' in str(file_path):
            metadata['category'] = 'flox_docs'
        elif 'nix' in str(file_path):
            metadata['category'] = 'nix_docs'
        else:
            metadata['category'] = 'general'
        
        # Extract word count
        metadata['word_count'] = len(content.split())
        
        return metadata
    
    def _determine_doc_type(self, file_path: Path) -> str:
        """Determine document type based on file path"""
        path_str = str(file_path).lower()
        
        if 'blogs' in path_str:
            return 'blog_post'
        elif 'flox' in path_str:
            return 'flox_docs'
        elif 'nix' in path_str:
            return 'nix_docs'
        elif 'processed' in path_str:
            return 'processed_docs'
        else:
            return 'general'
    
    def _generate_chunk_id(self, file_path: Path, chunk_index: int) -> str:
        """Generate unique ID for a chunk"""
        # Use UUID for guaranteed uniqueness
        return str(uuid.uuid4())
    
    def get_document_stats(self, chunks: List[Dict]) -> Dict:
        """Get statistics about processed documents"""
        if not chunks:
            return {
                'total_chunks': 0,
                'total_documents': 0,
                'total_tokens': 0,
                'avg_chunk_size': 0,
                'doc_types': {}
            }
        
        doc_types = {}
        total_tokens = 0
        
        for chunk in chunks:
            doc_type = chunk.get('doc_type', 'unknown')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            total_tokens += chunk.get('token_count', 0)
        
        unique_docs = len(set(chunk['source_file'] for chunk in chunks))
        avg_chunk_size = total_tokens / len(chunks) if chunks else 0
        
        return {
            'total_chunks': len(chunks),
            'total_documents': unique_docs,
            'total_tokens': total_tokens,
            'avg_chunk_size': avg_chunk_size,
            'doc_types': doc_types
        }
