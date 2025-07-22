"""
GroqCloud Client

Client implementation for GroqCloud API integration with RAG support.
Handles LLM requests and therapeutic response generation.

"""

import os
import time
import requests
import logging
from typing import List, Dict, Any, Optional, Union

class GroqClient:
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 api_base: Optional[str] = None,
                 enable_rag: bool = True): 
        """
        Initializes the GroqCloud client
        
        Args:
            api_key: GroqCloud API key. If not provided, uses the one from settings.
            api_base: API base URL. If not provided, uses the one from settings.
            enable_rag: Whether to enable RAG or not
        """
        from src.config.settings import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODELS

        self.api_key = api_key or GROQ_API_KEY
        self.api_base = api_base or GROQ_API_BASE
        self.models = GROQ_MODELS
        self.enable_rag = enable_rag
        
        if not self.api_key:
            raise ValueError("No API key has been provided for GroqCloud. "
                           "Configure it in the .env file or pass it as a parameter.")
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize RAG Manager if enabled
        self.rag_manager = None
        if self.enable_rag:
            self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize RAG manager using centralized configuration"""
        try:
            from src.utils.rag_manager import initialize_rag_manager
            from src.config.settings import RAG_CONFIG
            
            # Initialize RAG manager with centralized configuration
            self.rag_manager = initialize_rag_manager(
                documents_dir=RAG_CONFIG["documents_dir"],
                embeddings_model=RAG_CONFIG["embeddings_model"], 
                index_directory=RAG_CONFIG["index_dir"],
                chunk_size=RAG_CONFIG["chunk_size"],
                chunk_overlap=RAG_CONFIG["chunk_overlap"]
            )
            
            if self.rag_manager:
                self.logger.info("RAG Manager initialized successfully with centralized configuration")
            else:
                self.logger.warning("Could not initialize RAG Manager")
                self.enable_rag = False
                
        except ImportError as e:
            self.logger.warning(f"RAG not available (missing dependencies): {e}")
            self.enable_rag = False
        except Exception as e:
            self.logger.error(f"Error initializing RAG Manager: {e}")
            self.enable_rag = False
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model_id: Optional[str] = None, 
                       temperature: float = 0.7, 
                       max_tokens: int = 500,
                       retry_attempts: int = 3,
                       retry_delay: float = 1.0) -> Dict[str, Any]:
        """
        Sends a chat completion request to GroqCloud
        
        Args:
            messages: List of messages in OpenAI format
            model_id: Model ID to use. By default uses the first available.
            temperature: Temperature for generation. Default 0.7.
            max_tokens: Maximum tokens to generate. Default 500.
            retry_attempts: Number of attempts if request fails
            retry_delay: Seconds between retries
            
        Returns:
            API response as dictionary
        """
        if not model_id:
            model_id = next(iter(self.models.keys()))
            
        # Ensure it's a model available in Groq
        if model_id not in self.models:
            model_id = next(iter(self.models.keys()))
            self.logger.warning(f"Model not available in Groq. Using {model_id} instead.")
        
        # Endpoint for chat completions
        url = f"{self.api_base}/chat/completions"
        
        # Headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Request body
        data = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Implement retry with exponential backoff
        attempts = 0
        last_error = None
        
        while attempts < retry_attempts:
            try:
                # Make the request
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()  # Raise exception if HTTP error
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                last_error = e
                attempts += 1
                
                # Log the error
                self.logger.warning(f"Attempt {attempts}/{retry_attempts} failed: {e}")
                if hasattr(e, 'response') and e.response:
                    self.logger.warning(f"Error details: {e.response.text}")
                
                # If we've exhausted attempts, propagate the exception
                if attempts >= retry_attempts:
                    break
                    
                # Wait with exponential backoff before retrying
                wait_time = retry_delay * (2 ** (attempts - 1))
                self.logger.info(f"Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        
        # If we reach here, all attempts failed
        return {
            "error": str(last_error),
            "choices": [{
                "message": {
                    "content": "I'm sorry, I'm having connection problems. Please try again later."
                }
            }]
        }
    
    def generate_mental_health_response(self, 
                                       user_message: str, 
                                       category: str = "General", 
                                       model_id: Optional[str] = None,
                                       temperature: float = 0.7, 
                                       max_tokens: int = 500,
                                       use_rag: bool = True,
                                       conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate therapeutic response using specialized mental health prompts.
        
        Combines conversation context with RAG-enhanced knowledge to provide
        evidence-based mental health support tailored to specific categories.

        Args:
            user_message: User's input message
            category: Mental health category for specialized response
            model_id: GroqCloud model identifier
            temperature: Response creativity level (0.1-1.0)
            max_tokens: Maximum response length
            use_rag: Enable knowledge base enhancement
            conversation_history: Previous conversation context
            
        Returns:
            Generated therapeutic response as text

        Raises:
            Exception: If API request fails or response invalid
        """
        from src.config.settings import SYSTEM_MESSAGES
        
        # Get the system message for the category
        system_message = SYSTEM_MESSAGES.get(category, SYSTEM_MESSAGES["General"])
        
        # If RAG is enabled and requested, get relevant context
        rag_context = ""
        if self.enable_rag and use_rag and self.rag_manager:
            try:
                rag_context = self.rag_manager.get_context_for_query(
                    user_message, 
                    category=category,
                    max_context_length=1500  # Limit context to leave space for response
                )
                
                if rag_context:
                    self.logger.info("RAG context obtained for query")
                else:
                    self.logger.info("No relevant RAG context found")
                    
            except Exception as e:
                self.logger.error(f"Error getting RAG context: {e}")
                rag_context = ""
        
        # Build system message with RAG context if available
        enhanced_system_message = system_message
        if rag_context:
            enhanced_system_message += f"\n\n{rag_context}\n\nWhen the user asks for specific techniques mentioned in this context, provide them directly rather than asking permission first. Use this information when relevant to answer the user's query."
        
        # Build complete message list with conversation history
        messages = [{"role": "system", "content": enhanced_system_message}]
        
        # Add conversation history if provided
        if conversation_history:
            # Limit history to avoid token limits (keep last 20 messages = 10 exchanges)
            recent_history = conversation_history[-20:]
            messages.extend(recent_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Send the request
        response = self.chat_completion(
            messages, 
            model_id=model_id,
            temperature=temperature, 
            max_tokens=max_tokens
        )
        
        # Extract the response
        if "choices" in response and len(response["choices"]) > 0:
            generated_response = response["choices"][0]["message"]["content"]
            
            # Add note only if RAG context was used
            specific_keywords = ["steps:", "1.", "2.", "4-7-8", "Here's how it works:", "Best Friend Technique:", "Gratitude Journal:", "5-4-3-2-1"]
            if rag_context and any(keyword in generated_response for keyword in specific_keywords):  
                generated_response += "\n\n*Note: This response includes information from our specialized knowledge base.*"
            
            return generated_response
        else:
            return "I'm sorry, I'm having problems responding at the moment."
    
    def get_available_models(self) -> List[str]:
        """
        Gets the list of available models in GroqCloud
        
        Returns:
            List of available model IDs
        """
        return list(self.models.keys())
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets information about a specific model
        
        Args:
            model_id: Model ID
            
        Returns:
            Model information or None if it doesn't exist
        """
        return self.models.get(model_id)
    
    def get_rag_status(self) -> Dict[str, Any]:
        """
        Gets the RAG system status
        
        Returns:
            Dictionary with RAG status information
        """
        if not self.enable_rag:
            return {"enabled": False, "reason": "RAG disabled"}
        
        if not self.rag_manager:
            return {"enabled": False, "reason": "RAG Manager not initialized"}
        
        try:
            stats = self.rag_manager.get_stats()
            return {
                "enabled": True,
                "status": "Working",
                "stats": stats
            }
        except Exception as e:
            return {
                "enabled": False,
                "reason": f"Error in RAG Manager: {e}"
            }
    
    def index_rag_documents(self) -> bool:
        """
        Indexes documents in the RAG system
        
        Returns:
            True if indexed correctly
        """
        if not self.enable_rag or not self.rag_manager:
            self.logger.warning("RAG is not enabled")
            return False
        
        try:
            return self.rag_manager.index_documents()
        except Exception as e:
            self.logger.error(f"Error indexing documents: {e}")
            return False
    
    def add_rag_document(self, text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Adds a document to the RAG system
        
        Args:
            text: Document content
            metadata: Document metadata
            
        Returns:
            True if added correctly
        """
        if not self.enable_rag or not self.rag_manager:
            self.logger.warning("RAG is not enabled")
            return False
        
        try:
            return self.rag_manager.add_document_from_text(text, metadata)
        except Exception as e:
            self.logger.error(f"Error adding RAG document: {e}")
            return False


if __name__ == "__main__":
    # Example usage with RAG
    import sys
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Create client with RAG
    try:
        client = GroqClient(enable_rag=True)
        
        # Show RAG status
        rag_status = client.get_rag_status()
        print("RAG Status:")
        print(rag_status)
        
        # Show available models
        print("\nAvailable models:")
        for model_id in client.get_available_models():
            model_info = client.get_model_info(model_id)
            print(f"- {model_id}: {model_info['name']} (context: {model_info['context_length']})")
        
        # Generate response with RAG
        message = input("\nTest the assistant with RAG (Write a message): ")
        category = "General"
        
        print(f"\nGenerating response (Category: {category}, RAG: enabled)")
        response = client.generate_mental_health_response(message, category, use_rag=True)
        print("\nResponse:")
        print(response)
        
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)