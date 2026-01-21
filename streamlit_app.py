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
    layout="wide"
)

# API endpoint
API_URL = f"http://{settings.api_host}:{settings.api_port}"

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

def add_document(text: str, doc_id: str = None) -> dict:
    """Add document to knowledge base"""
    try:
        payload = {"text": text}
        if doc_id:
            payload["id"] = doc_id
        response = requests.post(
            f"{API_URL}/documents",
            json=payload,
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Main UI
st.title("🤖 Jarvis AI Assistant")
st.markdown("Your intelligent assistant powered by RAG (Retrieval-Augmented Generation)")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.write(f"**Model:** {settings.ollama_model}")
    st.write(f"**API:** {API_URL}")

    st.divider()

    # Add Knowledge section
    st.header("📚 Add Knowledge")
    new_doc = st.text_area("Paste text to add to knowledge base:", height=150)
    doc_id = st.text_input("Document ID (optional):")

    if st.button("Add Document", type="primary"):
        if new_doc.strip():
            with st.spinner("Adding document..."):
                result = add_document(new_doc, doc_id if doc_id else None)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Document added successfully!")
        else:
            st.warning("Please enter some text.")

    st.divider()

    # Health check
    if st.button("🔄 Check API Status"):
        try:
            response = requests.get(f"{API_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("API is running!")
            else:
                st.error("API returned an error")
        except:
            st.error("Cannot connect to API")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📄 Sources"):
                for source in message["sources"]:
                    st.write(f"- {source}")

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = query_api(prompt)

            if "error" in result:
                response = f"❌ {result['error']}"
                sources = []
            else:
                response = result.get("answer", "No response received.")
                sources = result.get("sources", [])

            st.markdown(response)

            if sources:
                with st.expander("📄 Sources"):
                    for source in sources:
                        st.write(f"- {source}")

    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources
    })

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with Ollama, Pinecone, FastAPI & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
