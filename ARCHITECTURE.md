# 🏗️ Jarvis AI Assistant - System Architecture

## Overview

This document provides a detailed technical overview of the Jarvis AI Assistant architecture, explaining how all components work together to create a fully functional RAG-based AI assistant.

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                         │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Streamlit Frontend                      │   │
│  │  - Chat Interface                                    │   │
│  │  - Knowledge Management                              │   │
│  │  - Settings & Configuration                          │   │
│  └──────────────────┬───────────────────────────────────┘   │
└────────────────────┬┴───────────────────────────────────────┘
                     │ HTTP/REST
                     │
┌────────────────────┴───────────────────────────────────────┐
│                     API LAYER (FastAPI)                     │
│                                                             │
│  Endpoints:                                                 │
│  - POST /query           - Query with RAG                  │
│  - POST /knowledge/add   - Add documents                   │
│  - POST /knowledge/upload - Upload files                   │
│  - DELETE /knowledge/clear - Clear knowledge base          │
│  - GET /health           - System health check             │
│  - GET /stats            - System statistics               │
└────────────────────┬───────────────────────────────────────┘
                     │
┌────────────────────┴───────────────────────────────────────┐
│                   RAG ENGINE (Orchestrator)                 │
│                                                             │
│  Core Functions:                                            │
│  1. Query Processing                                        │
│  2. Context Retrieval                                       │
│  3. Response Generation                                     │
│  4. Knowledge Management                                    │
└──────────┬─────────────────────────┬────────────────────────┘
           │                         │
           │                         │
    ┌──────┴──────┐          ┌──────┴──────────┐
    │             │          │                  │
┌───┴─────────────┴───┐  ┌──┴──────────────────┴──┐
│   LLM INTERFACE     │  │   VECTOR STORE          │
│   (Ollama)          │  │   (Pinecone)            │
│                     │  │                         │
│ - Model: LLaMA      │  │ - Embeddings Storage    │
│ - Generation        │  │ - Similarity Search     │
│ - Conversation Mem. │  │ - Metadata Management   │
└─────────────────────┘  └─────────────────────────┘
```

## Component Details

### 1. Frontend Layer (Streamlit)

**File:** `streamlit_app.py`

**Responsibilities:**
- User interface for chat interactions
- Knowledge base management UI
- System configuration and settings
- Visual display of retrieved context
- Real-time streaming responses (future enhancement)

**Key Features:**
- Clean, intuitive chat interface
- Sidebar for configuration
- Context transparency (shows which documents were used)
- Conversation history management
- File upload support

**Technology:**
- Streamlit for rapid UI development
- asyncio for async API calls
- httpx for HTTP requests

### 2. API Layer (FastAPI)

**File:** `api.py`

**Responsibilities:**
- RESTful API endpoints
- Request validation
- Error handling
- CORS configuration
- API documentation (auto-generated)

**Endpoints:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/query` | Query with RAG |
| POST | `/knowledge/add` | Add text knowledge |
| POST | `/knowledge/add-documents` | Batch add documents |
| POST | `/knowledge/upload` | Upload file |
| DELETE | `/knowledge/clear` | Clear all knowledge |
| POST | `/conversation/clear` | Clear conversation |
| GET | `/stats` | System statistics |

**Request/Response Models:**
- Pydantic models for type safety
- Automatic validation
- JSON serialization

### 3. RAG Engine

**File:** `rag_engine.py`

**Responsibilities:**
- Orchestrate the entire RAG pipeline
- Coordinate between vector store and LLM
- Manage knowledge base operations
- Handle query processing flow

**RAG Flow:**

```
User Query
    │
    ▼
┌─────────────────┐
│ Embed Query     │ (Convert to vector)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Search Vectors  │ (Find similar chunks)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieve Top-K  │ (Get most relevant)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Context   │ (Prepare prompt)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate LLM    │ (Get response)
│ Response        │
└────────┬────────┘
         │
         ▼
    Final Answer
```

**Key Methods:**
- `query()`: Process user query with RAG
- `add_knowledge()`: Add documents to knowledge base
- `clear_knowledge()`: Remove all documents
- `check_health()`: Verify system components

### 4. Vector Store (Pinecone)

**File:** `vector_store.py`

**Responsibilities:**
- Vector embedding storage
- Similarity search
- Metadata management
- Index operations

**Operations:**

1. **Initialization:**
   - Connect to Pinecone
   - Create or load index
   - Configure dimensions and metrics

2. **Embedding:**
   - Use sentence-transformers
   - Model: `all-MiniLM-L6-v2`
   - Dimension: 384

3. **Storage:**
   - Upsert vectors with metadata
   - Batch operations for efficiency
   - Automatic deduplication by ID

4. **Retrieval:**
   - Cosine similarity search
   - Top-K results
   - Include metadata in results

**Why Pinecone?**
- Managed service (no infrastructure)
- Fast similarity search
- Scales automatically
- Free tier available

### 5. LLM Interface (Ollama)

**File:** `llm_interface.py`

**Responsibilities:**
- Communication with Ollama API
- Prompt engineering
- Conversation history management
- Response generation

**Prompt Structure:**

```
[System Prompt]
You are Jarvis, a helpful AI assistant...

[Context from Vector Store]
Context information:
1. [Relevant chunk 1]
2. [Relevant chunk 2]
...

[Conversation History]
User: Previous question
Assistant: Previous answer
...

[Current Query]
User: Current question
Assistant:
```

**Why Ollama?**
- Self-hosted (privacy)
- Easy model management
- Good performance
- Active community

### 6. Document Processor

**File:** `document_processor.py`

**Responsibilities:**
- Text chunking
- Overlap management
- Metadata attachment
- Batch processing

**Chunking Strategy:**

```
Original Document (2000 chars)
        │
        ▼
┌──────────────────┐
│ Chunk 1 (0-500)  │
└──────────────────┘
      │ overlap 50
      ▼
┌──────────────────┐
│ Chunk 2 (450-950)│
└──────────────────┘
      │ overlap 50
      ▼
┌──────────────────┐
│ Chunk 3 (900-1400)│
└──────────────────┘
```

**Why Chunking?**
- LLMs have context limits
- Better semantic matching
- Improved retrieval accuracy
- More targeted responses

### 7. Configuration Management

**File:** `config.py`

**Responsibilities:**
- Environment variable loading
- Settings validation
- Default values
- Type safety

**Configuration Options:**
- API endpoints
- Model parameters
- Chunking settings
- Database credentials

## Data Flow

### Adding Knowledge

```
1. User submits document via UI
        │
        ▼
2. API receives document
        │
        ▼
3. Document Processor chunks text
   - Splits into ~500 char chunks
   - Adds overlap
   - Attaches metadata
        │
        ▼
4. Vector Store generates embeddings
   - Uses sentence-transformer
   - Creates 384-dim vectors
        │
        ▼
5. Pinecone stores vectors
   - Upserts with metadata
   - Indexed for fast search
        │
        ▼
6. Success response to user
```

### Query Processing

```
1. User asks question via UI
        │
        ▼
2. API receives query
        │
        ▼
3. RAG Engine processes:
   a. Embed query text
        │
        ▼
   b. Search Pinecone for similar vectors
        │
        ▼
   c. Retrieve top-3 matching chunks
        │
        ▼
   d. Build prompt with context
        │
        ▼
   e. Send to Ollama LLM
        │
        ▼
   f. Get generated response
        │
        ▼
4. Return answer + context to UI
        │
        ▼
5. Display to user with sources
```

## Security Considerations

### Current Implementation:
- Environment variables for secrets
- No authentication (local use only)
- CORS enabled for development

### Production Recommendations:
1. **Authentication:**
   - JWT tokens
   - API keys
   - OAuth integration

2. **Authorization:**
   - Role-based access
   - Resource-level permissions

3. **Data Security:**
   - Encrypt sensitive data
   - Secure vector storage
   - Audit logging

4. **Network Security:**
   - HTTPS only
   - Rate limiting
   - DDoS protection

## Performance Optimization

### Current Optimizations:
- Batch vector operations
- Async I/O throughout
- Efficient chunking
- Connection pooling

### Future Improvements:
1. **Caching:**
   - Redis for frequent queries
   - Embedding cache
   - Response cache

2. **Parallel Processing:**
   - Multi-threaded embedding
   - Concurrent Pinecone queries
   - Streaming responses

3. **Model Optimization:**
   - Quantized models
   - GPU acceleration
   - Model compression

## Scalability

### Current Scale:
- Single instance
- ~1000 documents
- ~10 concurrent users

### Scaling Strategies:

1. **Horizontal Scaling:**
   - Load balancer
   - Multiple API instances
   - Distributed Ollama

2. **Vertical Scaling:**
   - More RAM for embeddings
   - GPU for faster inference
   - SSD for faster I/O

3. **Database Scaling:**
   - Pinecone auto-scales
   - Sharding for large datasets
   - Regional replicas

## Monitoring & Observability

### Recommended Metrics:
- Query latency
- Retrieval accuracy
- Model response time
- API error rates
- Vector store operations

### Logging:
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARN, ERROR)
- Query audit trail
- System health checks

## Future Enhancements

### Phase 1:
- [ ] PDF/DOCX support
- [ ] Web scraping
- [ ] Advanced filters
- [ ] Export conversations

### Phase 2:
- [ ] Multi-user support
- [ ] User authentication
- [ ] Fine-tuning interface
- [ ] Analytics dashboard

### Phase 3:
- [ ] Voice interface
- [ ] Mobile app
- [ ] Enterprise features
- [ ] Advanced RAG techniques

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Streamlit | Interactive UI |
| Backend API | FastAPI | REST endpoints |
| LLM Runtime | Ollama | Model hosting |
| Vector DB | Pinecone | Similarity search |
| Embeddings | Sentence Transformers | Text vectorization |
| Language | Python 3.9+ | Core implementation |
| Async | asyncio | Async operations |
| HTTP Client | httpx | API communication |
| Config | python-dotenv | Environment management |

## Conclusion

This architecture provides a solid foundation for a production-ready AI assistant with:
- ✅ Clean separation of concerns
- ✅ Scalable components
- ✅ Maintainable codebase
- ✅ Extensible design
- ✅ Production-ready patterns

The modular design allows easy replacement or enhancement of any component without affecting the rest of the system.
