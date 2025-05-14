"""
Cliente para interactuar con la API de GroqCloud para el asistente de salud mental
"""

import os
import time
import requests
from typing import List, Dict, Any, Optional, Union

class GroqClient:
    """Cliente para interactuar con la API de GroqCloud"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        """
        Inicializa el cliente de GroqCloud
        
        Args:
            api_key: Clave API de GroqCloud. Si no se proporciona, se usa la de settings.
            api_base: URL base de la API. Si no se proporciona, se usa la de settings.
        """
        from src.config.settings import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODELS

        self.api_key = api_key or GROQ_API_KEY
        self.api_base = api_base or GROQ_API_BASE
        self.models = GROQ_MODELS
        
        if not self.api_key:
            raise ValueError("No se ha proporcionado una clave API para GroqCloud. "
                           "Configúrala en el archivo .env o pásala como parámetro.")
    
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
            print(f"Modelo no disponible en Groq. Usando {model_id} en su lugar.")
        
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
                print(f"Intento {attempts}/{retry_attempts} falló: {e}")
                if hasattr(e, 'response') and e.response:
                    print(f"Detalles del error: {e.response.text}")
                
                # Si hemos agotado los intentos, propagar la excepción
                if attempts >= retry_attempts:
                    break
                    
                # Esperar con backoff exponencial antes de reintentar
                wait_time = retry_delay * (2 ** (attempts - 1))
                print(f"Reintentando en {wait_time:.1f} segundos...")
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
                                       max_tokens: int = 500) -> str:
        """
        Genera una respuesta específica para salud mental
        
        Args:
            user_message: Mensaje del usuario
            category: Categoría de salud mental. Por defecto "General".
            model_id: ID del modelo a usar. Por defecto usa el primero disponible.
            temperature: Temperatura para la generación. Por defecto 0.7.
            max_tokens: Máximo de tokens a generar. Por defecto 500.
            
        Returns:
            Respuesta generada como texto
        """
        from src.config.settings import SYSTEM_MESSAGES
        
        # Obtener el mensaje del sistema para la categoría
        system_message = SYSTEM_MESSAGES.get(category, SYSTEM_MESSAGES["General"])
        
        # Crear la lista de mensajes
        messages = [
            {"role": "system", "content": system_message},
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
            return response["choices"][0]["message"]["content"]
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


if __name__ == "__main__":
    # Ejemplo de uso
    import sys
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear cliente
    try:
        client = GroqClient()
        
        # Mostrar modelos disponibles
        print("Modelos disponibles:")
        for model_id in client.get_available_models():
            model_info = client.get_model_info(model_id)
            print(f"- {model_id}: {model_info['name']} (contexto: {model_info['context_length']})")
        
        # Generar respuesta
        message = input("\nPrueba el asistente (Escribe un mensaje): ")
        category = "General"
        
        print(f"\nGenerando respuesta (Categoría: {category})")
        response = client.generate_mental_health_response(message, category)
        print("\nRespuesta:")
        print(response)
        
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)