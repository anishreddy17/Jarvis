"""
RAG (Retrieval-Augmented Generation) Engine
Orchestrates the entire RAG pipeline
"""
import logging
from typing import List, Dict, Any, Optional
from vector_store import VectorStore
from llm_interface import LLMInterface
from document_processor import DocumentProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGEngine:
    """Main RAG engine that orchestrates retrieval and generation"""
    
    def __init__(self):
        """Initialize RAG components"""
        self.vector_store = VectorStore()
        self.llm = LLMInterface()
        self.doc_processor = DocumentProcessor()
        logger.info("RAG Engine initialized")
    
    async def query(
        self,
        question: str,
        use_context: bool = True,
        top_k: int = None
    ) -> Dict[str, Any]:
        """
        Process a query using RAG
        
        Args:
            question: User's question
            use_context: Whether to retrieve and use context
            top_k: Number of context documents to retrieve
        
        Returns:
            Dict with answer, context, and metadata
        """
        try:
            context_docs = []
            context_texts = []
            
            # Retrieve relevant context if enabled
            if use_context:
                context_docs = self.vector_store.search(question, top_k)
                context_texts = [doc['text'] for doc in context_docs]
                logger.info(f"Retrieved {len(context_docs)} context documents")
            
            # Generate response using LLM
            answer = await self.llm.generate_response(
                query=question,
                context=context_texts if context_texts else None
            )
            
            return {
                'question': question,
                'answer': answer,
                'context': context_docs,
                'used_context': use_context and len(context_docs) > 0
            }
        
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'question': question,
                'answer': "I encountered an error processing your question.",
                'context': [],
                'used_context': False,
                'error': str(e)
            }
    
    def add_knowledge(self, text: str, doc_name: str = None, doc_type: str = None) -> bool:
        """
        Add knowledge to the system
        
        Args:
            text: Text content to add
            doc_name: Name of the document
            doc_type: Type of document
        
        Returns:
            Success status
        """
        try:
            # Process document into chunks
            chunks = self.doc_processor.process_document(
                text=text,
                doc_name=doc_name,
                doc_type=doc_type
            )
            
            if not chunks:
                logger.warning("No chunks created from document")
                return False
            
            # Add to vector store
            success = self.vector_store.add_documents(chunks)
            
            if success:
                logger.info(f"Successfully added knowledge: {doc_name}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            return False
    
    def add_knowledge_from_file(self, file_path: str) -> bool:
        """Add knowledge from a text file"""
        try:
            text = self.doc_processor.load_text_file(file_path)
            if text:
                return self.add_knowledge(
                    text=text,
                    doc_name=file_path.split('/')[-1],
                    doc_type='text_file'
                )
            return False
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            return False
    
    def add_multiple_documents(self, documents: List[Dict[str, str]]) -> bool:
        """
        Add multiple documents at once
        
        Args:
            documents: List of dicts with 'text' and optional 'name', 'type'
        """
        try:
            chunks = self.doc_processor.process_multiple_documents(documents)
            return self.vector_store.add_documents(chunks)
        except Exception as e:
            logger.error(f"Error adding multiple documents: {e}")
            return False
    
    def clear_knowledge(self) -> bool:
        """Clear all knowledge from vector store"""
        return self.vector_store.delete_all()
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.llm.clear_history()
        logger.info("Cleared conversation history")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'vector_store': self.vector_store.get_stats(),
            'conversation_length': len(self.llm.conversation_history)
        }
    
    async def check_health(self) -> Dict[str, bool]:
        """Check health of all components"""
        llm_connected = await self.llm.check_connection()
        
        return {
            'llm': llm_connected,
            'vector_store': True,  # If initialized, it's working
            'overall': llm_connected
        }
