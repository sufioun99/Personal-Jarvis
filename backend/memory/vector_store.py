"""
Vector Database Memory System using ChromaDB
"""
import logging
from typing import List, Optional
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class VectorMemory:
    """
    Vector-based memory system for conversation history and context
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self._init_chroma()
    
    def _init_chroma(self):
        """Initialize ChromaDB client"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.client = chromadb.Client(Settings(
                persist_directory=self.persist_directory,
                anonymized_telemetry=False
            ))
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="jarvis_memory",
                metadata={"description": "Personal Jarvis conversation memory"}
            )
            
            logger.info("Vector memory initialized with ChromaDB")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            self.client = None
            self.collection = None
    
    async def store_interaction(
        self,
        text: str,
        role: str,
        metadata: Optional[dict] = None
    ):
        """
        Store an interaction in vector memory
        
        Args:
            text: The text content
            role: 'user' or 'assistant'
            metadata: Additional metadata
        """
        if not self.collection:
            logger.warning("ChromaDB not initialized, skipping storage")
            return
        
        try:
            doc_id = str(uuid.uuid4())
            
            meta = {
                "role": role,
                "timestamp": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            self.collection.add(
                documents=[text],
                metadatas=[meta],
                ids=[doc_id]
            )
            
            logger.debug(f"Stored interaction: {role} - {text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")
    
    async def get_relevant_context(
        self,
        query: str,
        n_results: int = 5
    ) -> List[str]:
        """
        Get relevant context from memory based on query
        
        Args:
            query: Query text
            n_results: Number of results to return
        
        Returns:
            List of relevant context strings
        """
        if not self.collection:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results and results['documents']:
                contexts = []
                for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                    role = meta.get('role', 'unknown')
                    contexts.append(f"{role}: {doc}")
                return contexts
            
            return []
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
    
    async def search_memory(
        self,
        query: str,
        role: Optional[str] = None,
        n_results: int = 10
    ) -> List[dict]:
        """
        Search memory with optional filtering
        
        Args:
            query: Search query
            role: Optional role filter ('user' or 'assistant')
            n_results: Number of results
        
        Returns:
            List of matching documents with metadata
        """
        if not self.collection:
            return []
        
        try:
            where = {"role": role} if role else None
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )
            
            if results and results['documents']:
                matches = []
                for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                    matches.append({
                        "text": doc,
                        "metadata": meta
                    })
                return matches
            
            return []
            
        except Exception as e:
            logger.error(f"Error searching memory: {str(e)}")
            return []
    
    async def clear_memory(self):
        """Clear all stored memory"""
        if not self.collection:
            return
        
        try:
            # Delete and recreate collection
            self.client.delete_collection(name="jarvis_memory")
            self.collection = self.client.get_or_create_collection(
                name="jarvis_memory",
                metadata={"description": "Personal Jarvis conversation memory"}
            )
            logger.info("Memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {str(e)}")
    
    def get_stats(self) -> dict:
        """Get memory statistics"""
        if not self.collection:
            return {"status": "not initialized"}
        
        try:
            count = self.collection.count()
            return {
                "status": "active",
                "total_interactions": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
