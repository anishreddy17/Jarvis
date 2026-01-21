"""
Vector store management using Pinecone
"""
import logging
from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Manages vector storage and retrieval using Pinecone"""
    
    def __init__(self):
        """Initialize Pinecone and embedding model"""
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize or connect to index
        self._initialize_index()
    
    def _initialize_index(self):
        """Create index if it doesn't exist"""
        try:
            # Check if index exists
            if self.index_name not in self.pc.list_indexes().names():
                logger.info(f"Creating new index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
            
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error initializing index: {e}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text"""
        return self.embedding_model.encode(text).tolist()
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Add documents to the vector store
        
        Args:
            documents: List of dicts with 'id', 'text', and optional 'metadata'
        """
        try:
            vectors = []
            for doc in documents:
                embedding = self.embed_text(doc['text'])
                vector = {
                    'id': doc['id'],
                    'values': embedding,
                    'metadata': {
                        'text': doc['text'],
                        **(doc.get('metadata', {}))
                    }
                }
                vectors.append(vector)
            
            # Upsert in batches of 100
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            logger.info(f"Added {len(documents)} documents to vector store")
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            top_k: Number of results to return
        
        Returns:
            List of matching documents with scores
        """
        try:
            if top_k is None:
                top_k = settings.top_k_results
            
            query_embedding = self.embed_text(query)
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            documents = []
            for match in results['matches']:
                documents.append({
                    'id': match['id'],
                    'score': match['score'],
                    'text': match['metadata'].get('text', ''),
                    'metadata': {k: v for k, v in match['metadata'].items() if k != 'text'}
                })
            
            return documents
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def delete_all(self) -> bool:
        """Delete all vectors from the index"""
        try:
            self.index.delete(delete_all=True)
            logger.info("Deleted all documents from vector store")
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        try:
            return self.index.describe_index_stats()
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
