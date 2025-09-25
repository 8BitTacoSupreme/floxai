"""
FloxAI Embedding Service - Vector embeddings for semantic search
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import tiktoken

from app.core.config import get_settings

class FloxEmbeddingService:
    """Service for generating and managing text embeddings"""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self.encoding = None
        self.is_ready = False
        
        # Embedding model configuration
        self.model_name = "all-MiniLM-L6-v2"  # Fast, good quality, small size
        self.max_chunk_size = 500
        self.chunk_overlap = 50
        
    async def initialize(self):
        """Initialize the embedding model"""
        try:
            print("🔄 Loading embedding model...")
            self.model = SentenceTransformer(self.model_name)
            self.encoding = tiktoken.get_encoding("cl100k_base")
            self.is_ready = True
            print(f"✅ Embedding model loaded: {self.model_name}")
        except Exception as e:
            print(f"❌ Failed to load embedding model: {e}")
            self.is_ready = False
    
    def chunk_text(self, text: str, max_size: Optional[int] = None) -> List[str]:
        """Split text into overlapping chunks for embedding"""
        if max_size is None:
            max_size = self.max_chunk_size
            
        # Clean and normalize text
        text = self._clean_text(text)
        
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check if adding this sentence would exceed max size
            if len(current_chunk) + len(sentence) + 1 > max_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        if not self.is_ready:
            raise RuntimeError("Embedding service not initialized")
        
        if not texts:
            return np.array([])
        
        # Generate embeddings
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text"""
        return self.generate_embeddings([text])[0]
    
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        # Normalize embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        return float(similarity)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for embedding"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        # Remove markdown formatting
        text = re.sub(r'#{1,6}\s+', '', text)  # Headers
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)  # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)  # Code
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Links
        
        return text.strip()
    
    def get_token_count(self, text: str) -> int:
        """Get token count for text (useful for chunking)"""
        if not self.encoding:
            return len(text.split())  # Fallback to word count
        
        return len(self.encoding.encode(text))
    
    def is_text_too_long(self, text: str, max_tokens: int = 512) -> bool:
        """Check if text is too long for embedding"""
        return self.get_token_count(text) > max_tokens
