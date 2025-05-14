import os
import requests
from src.config.settings import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODELS, SYSTEM_MESSAGES

class GroqClient:
    """Cliente para interactuar con la API de GroqCloud"""
    
    def __init__(self, api_key=None, api_base=None):
        """
        Inicializa el cliente de GroqCloud
        
        Args:
            api_key (str, optional): Clave API de GroqCloud. Si no se proporciona, se usa la de settings.
            api_base (str, optional): URL base de la API. Si no se proporciona, se usa la de settings.
        """
        self.api_key = api_key or GROQ_API_KEY
        self.api_base = api_base or GROQ_API_BASE
        
        if not self.api_key:
            raise ValueError("No se ha proporcionado una clave API para GroqCloud. Configúrala en el archivo .env")
    
    def chat_completion(self, messages, model_id=None, temperature=0.7, max_tokens=500):
        """
        Envía una solicitud de chat completion a GroqCloud
        
        Args:
            messages (list): Lista de mensajes en formato OpenAI
            model_id (str, optional): ID del modelo a usar. Por defecto usa el primero disponible.
            temperature (float, optional): Temperatura para la generación. Por defecto 0.7.
            max_tokens (int, optional): Máximo de tokens a generar. Por defecto 500.
            
        Returns:
            dict: Respuesta de la API
        """
        if not model_id:
            model_id = list(GROQ_MODELS.keys())[0]
            
        # Asegurarse de que es un modelo disponible en Groq
        if model_id not in GROQ_MODELS:
            model_id = list(GROQ_MODELS.keys())[0]
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
        
        try:
            # Realizar la solicitud
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Lanzar excepción si hay error HTTP
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al llamar a la API de GroqCloud: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Detalles del error: {e.response.text}")
            return {"error": str(e)}
    
    def generate_mental_health_response(self, user_message, category="General", temperature=0.7, max_tokens=500):
        """
        Genera una respuesta específica para salud mental
        
        Args:
            user_message (str): Mensaje del usuario
            category (str, optional): Categoría de salud mental. Por defecto "General".
            temperature (float, optional): Temperatura para la generación. Por defecto 0.7.
            max_tokens (int, optional): Máximo de tokens a generar. Por defecto 500.
            
        Returns:
            str: Respuesta generada
        """
        # Obtener el mensaje del sistema para la categoría
        system_message = SYSTEM_MESSAGES.get(category, SYSTEM_MESSAGES["General"])
        
        # Crear la lista de mensajes
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Enviar la solicitud
        response = self.chat_completion(messages, temperature=temperature, max_tokens=max_tokens)
        
        # Extraer la respuesta
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        else:
            return "Lo siento, estoy teniendo problemas para responder en este momento."
    
    def get_available_models(self):
        """
        Obtiene la lista de modelos disponibles en GroqCloud
        
        Returns:
            list: Lista de modelos disponibles
        """
        return list(GROQ_MODELS.keys())
    
    def get_model_info(self, model_id):
        """
        Obtiene información sobre un modelo específico
        
        Args:
            model_id (str): ID del modelo
            
        Returns:
            dict: Información del modelo o None si no existe
        """
        return GROQ_MODELS.get(model_id)


# Ejemplo de uso
if __name__ == "__main__":
    # Crear cliente
    client = GroqClient()
    
    # Mostrar modelos disponibles
    print("Modelos disponibles:")
    for model_id in client.get_available_models():
        model_info = client.get_model_info(model_id)
        print(f"- {model_id}: {model_info['name']} (contexto: {model_info['context_length']})")
    
    # Generar respuesta
    message = "He estado sintiéndome triste últimamente y no sé qué hacer."
    category = "Depresión"
    
    print(f"\nGenerando respuesta para: '{message}' (Categoría: {category})")
    response = client.generate_mental_health_response(message, category)
    print("\nRespuesta:")
    print(response)