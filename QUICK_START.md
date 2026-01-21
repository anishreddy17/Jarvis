# 🚀 Quick Start Guide

Get Jarvis AI Assistant running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Ollama installed ([ollama.com](https://ollama.com))
- [ ] Pinecone account created ([pinecone.io](https://pinecone.io))
- [ ] Git (optional, for cloning)

## 5-Minute Setup

### Step 1: Install Ollama (2 minutes)

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Start Ollama and pull a model:**
```bash
# Start Ollama
ollama serve &

# Pull LLaMA 2 (in new terminal)
ollama pull llama2
```

### Step 2: Configure Environment (1 minute)

1. Get your Pinecone API key from [pinecone.io](https://app.pinecone.io)

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Edit `.env` with your details:
```env
PINECONE_API_KEY=your-key-here
PINECONE_ENVIRONMENT=us-east-1-aws
OLLAMA_MODEL=llama2
```

### Step 3: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 4: Test the System (30 seconds)

```bash
python setup_and_test.py
```

You should see:
```
✓ RAG Engine initialized
✓ LLM Connection
✓ Vector Store
✓ Added 5 sample documents
```

### Step 5: Launch! (30 seconds)

**Terminal 1 - Start API:**
```bash
python api.py
```

**Terminal 2 - Start UI:**
```bash
streamlit run streamlit_app.py
```

**Open your browser:**
```
http://localhost:8501
```

## 🎉 You're Ready!

Try asking:
- "What products does TechCorp offer?"
- "What is the remote work policy?"
- "Explain machine learning to me"

## Quick Commands

```bash
# Start everything (use the quick start script)
./start.sh

# Test connectivity only
python setup_and_test.py quick

# Start API only
python api.py

# Start UI only
streamlit run streamlit_app.py

# Check Ollama models
ollama list

# Pull a different model
ollama pull mistral
```

## Using Docker (Alternative)

```bash
# Make sure Ollama is running on your host
ollama serve

# Start with Docker Compose
docker-compose up -d

# Access UI
open http://localhost:8501
```

## Common Issues & Fixes

### "Cannot connect to Ollama"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### "No module named X"
```bash
pip install -r requirements.txt --upgrade
```

### "Pinecone API error"
- Verify your API key in `.env`
- Check you're on the free tier (has limits)
- Ensure index name is unique

### Port already in use
```bash
# Change API port in .env
API_PORT=8001

# Or change Streamlit port
streamlit run streamlit_app.py --server.port 8502
```

## What to Do Next

1. **Add Your Own Knowledge:**
   - Click "Add Knowledge" in sidebar
   - Paste your documents
   - Start asking questions!

2. **Try Different Models:**
   ```bash
   ollama pull mistral
   # Update .env: OLLAMA_MODEL=mistral
   ```

3. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Interactive API documentation
   - Test endpoints directly

4. **Customize:**
   - Edit prompts in `llm_interface.py`
   - Adjust chunk size in `config.py`
   - Modify UI in `streamlit_app.py`

## Project Structure

```
jarvis-ai-assistant/
├── api.py                 # FastAPI backend
├── streamlit_app.py       # Streamlit UI
├── rag_engine.py         # RAG orchestration
├── vector_store.py       # Pinecone integration
├── llm_interface.py      # Ollama integration
├── setup_and_test.py     # Testing script
└── README.md             # Full documentation
```

## Need Help?

1. Check `README.md` for detailed docs
2. Check `ARCHITECTURE.md` for technical details
3. Run `python setup_and_test.py` to diagnose issues
4. Ensure all prerequisites are met

---

**Built with ❤️ using Ollama, Pinecone, FastAPI, and Streamlit**
