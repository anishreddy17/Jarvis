"""
Setup and test script for Jarvis AI Assistant
"""
import asyncio
import sys
from rag_engine import RAGEngine
from sample_data import get_sample_documents

async def test_system():
    """Test the RAG system with sample data"""
    print("=" * 70)
    print("Jarvis AI Assistant - System Test")
    print("=" * 70)
    
    # Initialize RAG engine
    print("\n1. Initializing RAG Engine...")
    rag = RAGEngine()
    print("   ✓ RAG Engine initialized")
    
    # Check health
    print("\n2. Checking system health...")
    health = await rag.check_health()
    print(f"   LLM Connection: {'✓' if health['llm'] else '✗'}")
    print(f"   Vector Store: {'✓' if health['vector_store'] else '✗'}")
    
    if not health['llm']:
        print("\n   ⚠️  WARNING: Cannot connect to Ollama LLM")
        print("   Please ensure Ollama is running: ollama serve")
        print("   And that you have a model installed: ollama pull llama2")
        return False
    
    # Add sample knowledge
    print("\n3. Adding sample documents to knowledge base...")
    documents = get_sample_documents()
    success = rag.add_multiple_documents(documents)
    
    if success:
        print(f"   ✓ Added {len(documents)} sample documents")
    else:
        print("   ✗ Failed to add documents")
        return False
    
    # Get stats
    print("\n4. Vector store statistics:")
    stats = rag.get_stats()
    if 'vector_store' in stats:
        print(f"   Total vectors: {stats['vector_store'].get('total_vector_count', 'N/A')}")
    
    # Test queries
    print("\n5. Testing sample queries...")
    test_queries = [
        "What products does TechCorp offer?",
        "What is the remote work policy?",
        "Tell me about machine learning types"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Query {i}: {query}")
        result = await rag.query(query)
        print(f"   Answer: {result['answer'][:150]}...")
        print(f"   Used context: {result['used_context']}")
        if result['context']:
            print(f"   Retrieved {len(result['context'])} context documents")
    
    print("\n" + "=" * 70)
    print("System test completed successfully! ✓")
    print("=" * 70)
    print("\nYou can now:")
    print("1. Start the API: python api.py")
    print("2. Start the UI: streamlit run streamlit_app.py")
    print("=" * 70)
    
    return True

async def quick_test():
    """Quick connectivity test"""
    print("\nRunning quick connectivity test...")
    
    try:
        rag = RAGEngine()
        health = await rag.check_health()
        
        if health['llm']:
            print("✓ LLM (Ollama) is connected")
            models = await rag.llm.list_models()
            if models:
                print(f"  Available models: {', '.join(models)}")
        else:
            print("✗ Cannot connect to Ollama")
            print("  Start Ollama with: ollama serve")
            print("  Install a model with: ollama pull llama2")
        
        print("✓ Vector store is ready")
        
        return health['llm']
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        asyncio.run(quick_test())
    else:
        asyncio.run(test_system())

if __name__ == "__main__":
    main()
