"""
Interface for interacting with self-hosted LLM (Ollama)
"""
import logging
import httpx
from typing import Optional, List, Dict, Any
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMInterface:
    """Manages interactions with the self-hosted LLM"""
    
    def __init__(self):
        """Initialize LLM interface"""
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.conversation_history: List[Dict[str, str]] = []
    
    async def generate_response(
        self,
        query: str,
        context: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            query: User's query
            context: Retrieved context from vector store
            system_prompt: Custom system prompt
            stream: Whether to stream the response
        
        Returns:
            Generated response text
        """
        try:
            # Build the prompt with context
            prompt = self._build_prompt(query, context, system_prompt)
            
            # Make request to Ollama
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "")
                    
                    # Store in conversation history
                    self.conversation_history.append({
                        "role": "user",
                        "content": query
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": generated_text
                    })
                    
                    return generated_text
                else:
                    logger.error(f"LLM API error: {response.status_code}")
                    return "I apologize, but I'm having trouble generating a response right now."
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error while processing your request."
    
    def _build_prompt(
        self,
        query: str,
        context: Optional[List[str]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """Build the complete prompt with context"""
        
        # Default system prompt
        if system_prompt is None:
            system_prompt = """You are Jarvis, a helpful AI assistant. You answer questions based on the provided context and your knowledge. 
If the context doesn't contain relevant information, you can use your general knowledge to help, but mention when you're doing so.
Be concise, accurate, and helpful."""
        
        # Build prompt
        prompt_parts = [system_prompt, "\n\n"]
        
        # Add context if available
        if context:
            prompt_parts.append("Context information:\n")
            for i, ctx in enumerate(context, 1):
                prompt_parts.append(f"{i}. {ctx}\n")
            prompt_parts.append("\n")
        
        # Add conversation history (last 5 exchanges)
        if self.conversation_history:
            prompt_parts.append("Recent conversation:\n")
            for msg in self.conversation_history[-10:]:
                role = msg['role'].capitalize()
                prompt_parts.append(f"{role}: {msg['content']}\n")
            prompt_parts.append("\n")
        
        # Add current query
        prompt_parts.append(f"User: {query}\n")
        prompt_parts.append("Assistant:")
        
        return "".join(prompt_parts)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Cleared conversation history")
    
    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Cannot connect to Ollama: {e}")
            return False
    
    async def list_models(self) -> List[str]:
        """List available models"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
        return []
