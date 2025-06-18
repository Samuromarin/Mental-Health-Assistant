"""
Cliente para interactuar con la API de GroqCloud para el asistente de salud mental
Versión actualizada con soporte para RAG (Retrieval-Augmented Generation)
"""

import os
import time
import requests
import logging
from typing import List, Dict, Any, Optional, Union

class GroqClient:
    """Cliente para interactuar con la API de GroqCloud con soporte RAG"""
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 api_base: Optional[str] = None,
                 enable_rag: bool = True): 
        """
        Inicializa el cliente de GroqCloud
        
        Args:
            api_key: Clave API de GroqCloud. Si no se proporciona, se usa la de settings.
            api_base: URL base de la API. Si no se proporciona, se usa la de settings.
            enable_rag: Si activar RAG o no
        """
        from src.config.settings import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODELS

        self.api_key = api_key or GROQ_API_KEY
        self.api_base = api_base or GROQ_API_BASE
        self.models = GROQ_MODELS
        self.enable_rag = enable_rag
        
        if not self.api_key:
            raise ValueError("No se ha proporcionado una clave API para GroqCloud. "
                           "Configúrala en el archivo .env o pásala como parámetro.")
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        # Inicializar RAG Manager si está habilitado
        self.rag_manager = None
        if self.enable_rag:
            self._initialize_rag()
    
    def _initialize_rag(self):
        """Inicializa el gestor RAG"""
        try:
            from src.utils.rag_manager import initialize_rag_manager
            
            self.rag_manager = initialize_rag_manager()
            if self.rag_manager:
                self.logger.info("RAG Manager inicializado correctamente")
            else:
                self.logger.warning("No se pudo inicializar RAG Manager")
                self.enable_rag = False
                
        except ImportError as e:
            self.logger.warning(f"RAG no disponible (dependencias faltantes): {e}")
            self.enable_rag = False
        except Exception as e:
            self.logger.error(f"Error inicializando RAG: {e}")
            self.enable_rag = False
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model_id: Optional[str] = None, 
                       temperature: float = 0.7, 
                       max_tokens: int = 500,
                       retry_attempts: int = 3,
                       retry_delay: float = 1.0) -> Dict[str, Any]:
        """
        Envía una solicitud de chat completion a GroqCloud
        
        Args:
            messages: Lista de mensajes en formato OpenAI
            model_id: ID del modelo a usar. Por defecto usa el primero disponible.
            temperature: Temperatura para la generación. Por defecto 0.7.
            max_tokens: Máximo de tokens a generar. Por defecto 500.
            retry_attempts: Número de intentos si falla la solicitud
            retry_delay: Segundos entre reintentos
            
        Returns:
            Respuesta de la API como diccionario
        """
        if not model_id:
            model_id = next(iter(self.models.keys()))
            
        # Asegurarse de que es un modelo disponible en Groq
        if model_id not in self.models:
            model_id = next(iter(self.models.keys()))
            self.logger.warning(f"Modelo no disponible en Groq. Usando {model_id} en su lugar.")
        
        # Endpoint para chat completions
        url = f"{self.api_base}/chat/completions"
        
        # Cabeceras
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Cuerpo de la solicitud
        data = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Implementamos reintento con backoff exponencial
        attempts = 0
        last_error = None
        
        while attempts < retry_attempts:
            try:
                # Realizar la solicitud
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()  # Lanzar excepción si hay error HTTP
                
                return response.json()
                
            except requests.exceptions.RequestException as e:
                last_error = e
                attempts += 1
                
                # Registrar el error
                self.logger.warning(f"Intento {attempts}/{retry_attempts} falló: {e}")
                if hasattr(e, 'response') and e.response:
                    self.logger.warning(f"Detalles del error: {e.response.text}")
                
                # Si hemos agotado los intentos, propagar la excepción
                if attempts >= retry_attempts:
                    break
                    
                # Esperar con backoff exponencial antes de reintentar
                wait_time = retry_delay * (2 ** (attempts - 1))
                self.logger.info(f"Reintentando en {wait_time:.1f} segundos...")
                time.sleep(wait_time)
        
        # Si llegamos aquí, todos los intentos fallaron
        return {
            "error": str(last_error),
            "choices": [{
                "message": {
                    "content": "Lo siento, estoy teniendo problemas para conectarme. Por favor, inténtalo de nuevo más tarde."
                }
            }]
        }
    
    def generate_mental_health_response(self, 
                                       user_message: str, 
                                       category: str = "General", 
                                       model_id: Optional[str] = None,
                                       temperature: float = 0.7, 
                                       max_tokens: int = 500,
                                       use_rag: bool = True) -> str:
        """
        Genera una respuesta específica para salud mental con soporte RAG
        
        Args:
            user_message: Mensaje del usuario
            category: Categoría de salud mental. Por defecto "General".
            model_id: ID del modelo a usar. Por defecto usa el primero disponible.
            temperature: Temperatura para la generación. Por defecto 0.7.
            max_tokens: Máximo de tokens a generar. Por defecto 500.
            use_rag: Si usar RAG para esta consulta
            
        Returns:
            Respuesta generada como texto
        """
        from src.config.settings import SYSTEM_MESSAGES
        
        # Obtener el mensaje del sistema para la categoría
        system_message = SYSTEM_MESSAGES.get(category, SYSTEM_MESSAGES["General"])
        
        # Si RAG está habilitado y se solicita usarlo, obtener contexto relevante
        rag_context = ""
        if self.enable_rag and use_rag and self.rag_manager:
            try:
                rag_context = self.rag_manager.get_context_for_query(
                    user_message, 
                    category=category,
                    max_context_length=1500  # Limitar contexto para dejar espacio a la respuesta
                )
                
                if rag_context:
                    self.logger.info("Contexto RAG obtenido para la consulta")
                else:
                    self.logger.info("No se encontró contexto RAG relevante")
                    
            except Exception as e:
                self.logger.error(f"Error obteniendo contexto RAG: {e}")
                rag_context = ""
        
        # Construir mensaje del sistema con contexto RAG si está disponible
        enhanced_system_message = system_message
        if rag_context:
            enhanced_system_message += f"\n\n{rag_context}\n\nUsa esta información cuando sea relevante para responder la consulta del usuario."
        
        # Crear la lista de mensajes
        messages = [
            {"role": "system", "content": enhanced_system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Enviar la solicitud
        response = self.chat_completion(
            messages, 
            model_id=model_id,
            temperature=temperature, 
            max_tokens=max_tokens
        )
        
        # Extraer la respuesta
        if "choices" in response and len(response["choices"]) > 0:
            generated_response = response["choices"][0]["message"]["content"]
            
            # Añadir nota sobre fuentes si se usó RAG
            if rag_context and "Información relevante de la base de conocimiento:" in rag_context:
                generated_response += "\n\n*Nota: Esta respuesta incluye información de nuestra base de conocimiento especializada.*"
            
            return generated_response
        else:
            return "Lo siento, estoy teniendo problemas para responder en este momento."
    
    def get_available_models(self) -> List[str]:
        """
        Obtiene la lista de modelos disponibles en GroqCloud
        
        Returns:
            Lista de IDs de modelos disponibles
        """
        return list(self.models.keys())
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información sobre un modelo específico
        
        Args:
            model_id: ID del modelo
            
        Returns:
            Información del modelo o None si no existe
        """
        return self.models.get(model_id)
    
    def get_rag_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado del sistema RAG
        
        Returns:
            Diccionario con información del estado RAG
        """
        if not self.enable_rag:
            return {"enabled": False, "reason": "RAG deshabilitado"}
        
        if not self.rag_manager:
            return {"enabled": False, "reason": "RAG Manager no inicializado"}
        
        try:
            stats = self.rag_manager.get_stats()
            return {
                "enabled": True,
                "status": "Funcionando",
                "stats": stats
            }
        except Exception as e:
            return {
                "enabled": False,
                "reason": f"Error en RAG Manager: {e}"
            }
    
    def index_rag_documents(self) -> bool:
        """
        Indexa documentos en el sistema RAG
        
        Returns:
            True si se indexaron correctamente
        """
        if not self.enable_rag or not self.rag_manager:
            self.logger.warning("RAG no está habilitado")
            return False
        
        try:
            return self.rag_manager.index_documents()
        except Exception as e:
            self.logger.error(f"Error indexando documentos: {e}")
            return False
    
    def add_rag_document(self, text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Añade un documento al sistema RAG
        
        Args:
            text: Contenido del documento
            metadata: Metadatos del documento
            
        Returns:
            True si se añadió correctamente
        """
        if not self.enable_rag or not self.rag_manager:
            self.logger.warning("RAG no está habilitado")
            return False
        
        try:
            return self.rag_manager.add_document_from_text(text, metadata)
        except Exception as e:
            self.logger.error(f"Error añadiendo documento RAG: {e}")
            return False


if __name__ == "__main__":
    # Ejemplo de uso con RAG
    import sys
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear cliente con RAG
    try:
        client = GroqClient(enable_rag=True)
        
        # Mostrar estado de RAG
        rag_status = client.get_rag_status()
        print("Estado de RAG:")
        print(rag_status)
        
        # Mostrar modelos disponibles
        print("\nModelos disponibles:")
        for model_id in client.get_available_models():
            model_info = client.get_model_info(model_id)
            print(f"- {model_id}: {model_info['name']} (contexto: {model_info['context_length']})")
        
        # Generar respuesta con RAG
        message = input("\nPrueba el asistente con RAG (Escribe un mensaje): ")
        category = "General"
        
        print(f"\nGenerando respuesta (Categoría: {category}, RAG: habilitado)")
        response = client.generate_mental_health_response(message, category, use_rag=True)
        print("\nRespuesta:")
        print(response)
        
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)