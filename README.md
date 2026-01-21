# 🤖 Jarvis AI Assistant

A personal AI assistant powered by a self-hosted Large Language Model (LLM) with Retrieval-Augmented Generation (RAG) capabilities. This project implements a complete enterprise-grade AI assistant with knowledge base storage, contextual understanding, and a beautiful chatbot interface.

## 🎯 Features

- **Self-Hosted LLM**: Uses Ollama to run models like LLaMA locally
- **RAG Pipeline**: Retrieval-Augmented Generation for contextually relevant responses
- **Vector Database**: Pinecone for efficient similarity search
- **Chatbot UI**: Beautiful Streamlit interface for easy interaction
- **REST API**: FastAPI backend for programmatic access
- **Document Processing**: Automatic chunking and embedding of documents
- **Conversation Memory**: Maintains context across the conversation
- **Knowledge Management**: Add, update, and manage your knowledge base

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   (Backend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RAG Engine    │
│   (Orchestrator)│
└─────┬─────┬─────┘
      │     │
      ▼     ▼
  ┌───────┐  ┌──────────┐
  │ LLM   │  │ Pinecone │
  │(Ollama)│ │ (Vector) │
  └───────┘  └──────────┘
```

## 📋 Prerequisites

1. **Python 3.9+**
2. **Ollama** - Self-hosted LLM runtime
3. **Pinecone Account** - Vector database (free tier available)
4. **Git** (for cloning the repository)

## 🚀 Installation

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com](https://ollama.com)

### Step 2: Pull an LLM Model

```bash
# Start Ollama (if not already running)
ollama serve

# In a new terminal, pull a model
ollama pull llama2

# Or try other models:
# ollama pull mistral
# ollama pull codellama
```

### Step 3: Set Up Pinecone

1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Get your API key and environment from the dashboard

### Step 4: Clone and Install

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Update these values in `.env`:
```env
PINECONE_API_KEY=your_actual_api_key
PINECONE_ENVIRONMENT=your_environment
OLLAMA_MODEL=llama2
```

## 🎮 Usage

### Quick Start

1. **Test the system:**
```bash
python setup_and_test.py
```

This will:
- Check connectivity to Ollama and Pinecone
- Add sample documents to the knowledge base
- Run test queries
- Verify everything is working

2. **Start the API backend:**
```bash
python api.py
```

The API will be available at `http://localhost:8000`

3. **Start the Streamlit UI** (in a new terminal):
```bash
streamlit run streamlit_app.py
```

The UI will open automatically in your browser at `http://localhost:8501`

### Using the Chatbot UI

1. **Add Knowledge:**
   - Use the sidebar to add documents to your knowledge base
   - Paste text directly or upload files
   - Give documents meaningful names for organization

2. **Ask Questions:**
   - Type your question in the chat input
   - Enable/disable context retrieval in settings
   - View retrieved context for transparency

3. **Manage Conversation:**
   - Clear conversation history when starting new topics
   - Check system health from the sidebar

## 🔧 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are your products?",
    "use_context": true
  }'
```

### Add Knowledge
```bash
curl -X POST http://localhost:8000/knowledge/add \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your document text here",
    "doc_name": "Document Title"
  }'
```

### Upload File
```bash
curl -X POST http://localhost:8000/knowledge/upload \
  -F "file=@document.txt"
```

## 📁 Project Structure

```
jarvis-ai-assistant/
├── api.py                  # FastAPI backend
├── streamlit_app.py        # Streamlit UI
├── rag_engine.py          # RAG orchestration
├── vector_store.py        # Pinecone integration
├── llm_interface.py       # Ollama/LLM integration
├── document_processor.py  # Document chunking
├── config.py              # Configuration management
├── sample_data.py         # Sample documents for testing
├── setup_and_test.py      # Setup and testing script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PINECONE_API_KEY` | Pinecone API key | Required |
| `PINECONE_ENVIRONMENT` | Pinecone environment | Required |
| `PINECONE_INDEX_NAME` | Vector index name | jarvis-knowledge-base |
| `OLLAMA_BASE_URL` | Ollama API URL | http://localhost:11434 |
| `OLLAMA_MODEL` | Model to use | llama2 |
| `EMBEDDING_MODEL` | Sentence transformer model | all-MiniLM-L6-v2 |
| `CHUNK_SIZE` | Document chunk size | 500 |
| `CHUNK_OVERLAP` | Chunk overlap | 50 |
| `TOP_K_RESULTS` | Context documents to retrieve | 3 |

### Customizing the LLM

You can use different Ollama models:

```bash
# List available models
ollama list

# Pull a different model
ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral
```

## 🧪 Testing

### Quick Test
```bash
python setup_and_test.py quick
```

### Full Test Suite
```bash
python setup_and_test.py
```

### Manual Testing

1. Start the API: `python api.py`
2. In another terminal:

```python
import asyncio
from rag_engine import RAGEngine

async def test():
    rag = RAGEngine()
    
    # Add knowledge
    rag.add_knowledge(
        text="Python is a programming language.",
        doc_name="Python Basics"
    )
    
    # Query
    result = await rag.query("What is Python?")
    print(result['answer'])

asyncio.run(test())
```

## 🚨 Troubleshooting

### "Cannot connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check if a model is installed: `ollama list`
- Verify the URL in `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

### "Pinecone API error"
- Verify your API key in `.env`
- Check your Pinecone dashboard for quota limits
- Ensure the index name doesn't conflict

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Port already in use
Change ports in `.env`:
```env
API_PORT=8001
```

And run Streamlit on different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 🎓 How It Works

### RAG Pipeline

1. **Document Ingestion:**
   - Documents are split into chunks (~500 characters)
   - Each chunk is converted to embeddings using sentence transformers
   - Embeddings are stored in Pinecone with metadata

2. **Query Processing:**
   - User query is converted to embedding
   - Pinecone finds similar chunks (cosine similarity)
   - Top K most relevant chunks are retrieved

3. **Response Generation:**
   - Retrieved context + query are sent to LLM
   - LLM generates contextually relevant response
   - Response is returned to user

### Why This Approach?

- **Self-hosted**: Full control over your data and models
- **Efficient**: Vector search is much faster than full-text search
- **Contextual**: RAG provides relevant information to the LLM
- **Scalable**: Can handle large knowledge bases
- **Private**: No data sent to external APIs (except Pinecone)

## 🔒 Security Considerations

- Keep your `.env` file secure and never commit it
- Use environment variables for all sensitive data
- Consider using local vector databases for fully private deployments
- Implement authentication for production deployments
- Rate limit API endpoints in production

## 🚀 Next Steps & Enhancements

- [ ] Add support for PDF and DOCX files
- [ ] Implement user authentication
- [ ] Add conversation export functionality
- [ ] Support for multiple knowledge bases
- [ ] Fine-tuning capabilities
- [ ] Web scraping for knowledge ingestion
- [ ] Advanced analytics and usage tracking
- [ ] Multi-user support
- [ ] Voice interface integration

## 📚 Resources

- [Ollama Documentation](https://ollama.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is provided as-is for educational purposes.

## 🙏 Acknowledgments

Built with:
- Ollama for local LLM hosting
- Pinecone for vector storage
- FastAPI for the backend
- Streamlit for the UI
- Sentence Transformers for embeddings

---

**Happy Building! 🚀**

If you have questions or run into issues, please check the troubleshooting section or create an issue.
