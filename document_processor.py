"""
Document processing and chunking utilities
"""
import logging
import uuid
from typing import List, Dict, Any
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document processing and chunking for RAG"""
    
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to chunks
        
        Returns:
            List of document chunks with IDs and metadata
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            
            # Try to find a natural break point (sentence end)
            if end < text_length:
                # Look for period, question mark, or exclamation mark
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?\n':
                        end = i + 1
                        break
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk = {
                    'id': str(uuid.uuid4()),
                    'text': chunk_text,
                    'metadata': {
                        'chunk_index': len(chunks),
                        **(metadata or {})
                    }
                }
                chunks.append(chunk)
            
            # Move to next chunk with overlap
            start = end - self.chunk_overlap
            
            # Ensure we make progress
            if start <= end - self.chunk_size:
                start = end
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def process_document(
        self,
        text: str,
        doc_id: str = None,
        doc_name: str = None,
        doc_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Process a complete document into chunks
        
        Args:
            text: Document text
            doc_id: Document identifier
            doc_name: Document name/title
            doc_type: Document type (e.g., 'pdf', 'txt', 'web')
        
        Returns:
            List of processed chunks ready for vector store
        """
        if doc_id is None:
            doc_id = str(uuid.uuid4())
        
        metadata = {
            'doc_id': doc_id,
            'doc_name': doc_name or 'Unknown',
            'doc_type': doc_type or 'text'
        }
        
        chunks = self.chunk_text(text, metadata)
        logger.info(f"Processed document '{doc_name}' into {len(chunks)} chunks")
        
        return chunks
    
    def process_multiple_documents(
        self,
        documents: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple documents
        
        Args:
            documents: List of dicts with 'text' and optional 'name', 'type'
        
        Returns:
            Combined list of all chunks
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.process_document(
                text=doc.get('text', ''),
                doc_name=doc.get('name'),
                doc_type=doc.get('type')
            )
            all_chunks.extend(chunks)
        
        logger.info(f"Processed {len(documents)} documents into {len(all_chunks)} total chunks")
        return all_chunks
    
    @staticmethod
    def load_text_file(file_path: str) -> str:
        """Load text from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return ""
    
    def process_text_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a text file into chunks"""
        text = self.load_text_file(file_path)
        if text:
            return self.process_document(
                text=text,
                doc_name=file_path.split('/')[-1],
                doc_type='text_file'
            )
        return []
