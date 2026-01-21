"""
Streamlit UI for Jarvis AI Assistant
"""
import streamlit as st
import requests
from config import settings

# Page configuration
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom header */
    .hero-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
    }

    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .assistant-message {
        background: rgba(255, 255, 255, 0.1);
        color: #e2e8f0;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
    }

    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Status cards */
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.5rem 0;
    }

    .status-online {
        color: #48bb78;
        font-weight: 600;
    }

    .status-offline {
        color: #fc8181;
        font-weight: 600;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        color: #a0aec0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }

    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 2rem 0;
    }

    /* Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .thinking {
        animation: pulse 1.5s infinite;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = f"http://localhost:{settings.api_port}"

def query_api(question: str) -> dict:
    """Send question to the API"""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"question": question},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Make sure to run 'python api.py' first."}
    except Exception as e:
        return {"error": str(e)}

def add_document(text: str, doc_name: str = None) -> dict:
    """Add document to knowledge base"""
    try:
        payload = {"text": text}
        if doc_name:
            payload["doc_name"] = doc_name
        response = requests.post(
            f"{API_URL}/knowledge/add",
            json=payload,
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def check_api_status() -> bool:
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 2rem; margin: 0;">🤖</h1>
            <h2 style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0.5rem 0;">JARVIS</h2>
            <p style="color: #a0aec0; font-size: 0.8rem;">AI Assistant</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Status section
    st.markdown("### 📊 System Status")

    col1, col2 = st.columns(2)
    with col1:
        api_status = check_api_status()
        if api_status:
            st.markdown('<p class="status-online">● API Online</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-offline">● API Offline</p>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<p style="color: #a0aec0;">Model: {settings.ollama_model}</p>', unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Add Knowledge section
    st.markdown("### 📚 Knowledge Base")

    with st.expander("➕ Add New Knowledge", expanded=False):
        new_doc = st.text_area(
            "Paste your text here:",
            height=150,
            placeholder="Enter text to add to the knowledge base..."
        )
        doc_name = st.text_input(
            "Document Name:",
            placeholder="e.g., Company Policy, Product Info..."
        )

        if st.button("🚀 Add to Knowledge Base", use_container_width=True):
            if new_doc.strip():
                with st.spinner("Processing..."):
                    result = add_document(new_doc, doc_name if doc_name else None)
                    if "error" in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success("✅ Knowledge added successfully!")
            else:
                st.warning("⚠️ Please enter some text.")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Info
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #a0aec0; font-size: 0.75rem;">
            <p>Powered by</p>
            <p>🦙 Ollama • 🌲 Pinecone • ⚡ FastAPI</p>
        </div>
    """, unsafe_allow_html=True)

# Main content area
st.markdown('<h1 class="hero-header">JARVIS AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Your Intelligent Personal Assistant with RAG-Powered Knowledge</p>', unsafe_allow_html=True)

# Stats row
if check_api_status():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">RAG</div>
                <div class="metric-label">Retrieval Augmented</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">LLM</div>
                <div class="metric-label">Local Language Model</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">∞</div>
                <div class="metric-label">Knowledge Capacity</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                <div class="user-message">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                <div class="assistant-message">
                    <strong>🤖 Jarvis:</strong><br>{message["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)

        if "sources" in message and message["sources"]:
            with st.expander("📄 View Sources"):
                for source in message["sources"]:
                    st.markdown(f"- {source}")

# Chat input
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Create input with custom styling
prompt = st.chat_input("💬 Ask Jarvis anything...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message immediately
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
            <div class="user-message">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)

    # Get response
    with st.spinner("🤔 Jarvis is thinking..."):
        result = query_api(prompt)

        if "error" in result:
            response = f"❌ {result['error']}"
            sources = []
        else:
            response = result.get("answer", "I couldn't generate a response.")
            sources = [doc.get("text", "")[:100] + "..." for doc in result.get("context", []) if doc.get("text")]

    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources
    })

    # Rerun to display the new messages
    st.rerun()

# Empty state
if not st.session_state.messages:
    st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #a0aec0;">
            <h2 style="font-size: 3rem; margin-bottom: 1rem;">👋</h2>
            <h3 style="color: #e2e8f0; margin-bottom: 0.5rem;">Welcome to Jarvis AI!</h3>
            <p>I'm your intelligent assistant. Ask me anything or add knowledge to my database.</p>
            <br>
            <p style="font-size: 0.9rem;">Try asking:</p>
            <p style="color: #667eea;">"What can you help me with?"</p>
            <p style="color: #764ba2;">"Tell me about your capabilities"</p>
        </div>
    """, unsafe_allow_html=True)
