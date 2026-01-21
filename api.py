"""
FastAPI Backend for Jarvis AI Assistant
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

from config import settings
from rag_engine import RAGEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Jarvis AI Assistant API",
    description="API for personal AI assistant with RAG capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = RAGEngine()

# Pydantic models
class QueryRequest(BaseModel):
    question: str
    use_context: bool = True
    top_k: Optional[int] = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    context: List[Dict[str, Any]]
    used_context: bool

class AddKnowledgeRequest(BaseModel):
    text: str
    doc_name: Optional[str] = None
    doc_type: Optional[str] = None

class AddDocumentsRequest(BaseModel):
    documents: List[Dict[str, str]]

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, bool]

# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Jarvis AI Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health"""
    health = await rag_engine.check_health()
    
    return {
        "status": "healthy" if health['overall'] else "unhealthy",
        "components": health
    }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a query using RAG
    """
    try:
        result = await rag_engine.query(
            question=request.question,
            use_context=request.use_context,
            top_k=request.top_k
        )
        
        return result
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge/add")
async def add_knowledge(request: AddKnowledgeRequest):
    """
    Add knowledge to the system
    """
    try:
        success = rag_engine.add_knowledge(
            text=request.text,
            doc_name=request.doc_name,
            doc_type=request.doc_type
        )
        
        if success:
            return {"status": "success", "message": "Knowledge added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to add knowledge")
    
    except Exception as e:
        logger.error(f"Error adding knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge/add-documents")
async def add_documents(request: AddDocumentsRequest):
    """
    Add multiple documents
    """
    try:
        success = rag_engine.add_multiple_documents(request.documents)
        
        if success:
            return {
                "status": "success",
                "message": f"Added {len(request.documents)} documents"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add documents")
    
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a text file to add to knowledge base
    """
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        success = rag_engine.add_knowledge(
            text=text,
            doc_name=file.filename,
            doc_type='uploaded_file'
        )
        
        if success:
            return {
                "status": "success",
                "message": f"File '{file.filename}' processed and added"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to process file")
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/knowledge/clear")
async def clear_knowledge():
    """
    Clear all knowledge from vector store
    """
    try:
        success = rag_engine.clear_knowledge()
        
        if success:
            return {"status": "success", "message": "Knowledge cleared"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear knowledge")
    
    except Exception as e:
        logger.error(f"Error clearing knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/conversation/clear")
async def clear_conversation():
    """
    Clear conversation history
    """
    try:
        rag_engine.clear_conversation()
        return {"status": "success", "message": "Conversation cleared"}
    
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """
    Get system statistics
    """
    try:
        stats = rag_engine.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info"
    )
