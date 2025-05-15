#!/usr/bin/env python
"""
Script para verificar la conexión con GroqCloud y listar los modelos disponibles.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def main():
    # Obtener la clave API
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: No se ha encontrado la clave API de GroqCloud")
        print("Por favor, configura la variable de entorno GROQ_API_KEY en el archivo .env")
        return 1
    
    # Endpoint para listar modelos
    url = "https://api.groq.com/openai/v1/models"
    
    # Cabeceras de la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔄 Conectando con GroqCloud para listar modelos disponibles...")
    
    try:
        # Realizar la solicitud
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        # Procesar la respuesta
        models_data = response.json()
        
        print("✅ Conexión exitosa!")
        print("\n📋 Modelos disponibles en tu cuenta de GroqCloud:")
        
        if "data" in models_data and isinstance(models_data["data"], list):
            for model in models_data["data"]:
                model_id = model.get("id", "Sin ID")
                print(f"- {model_id}")
                
                # Mostrar detalles adicionales si están disponibles
                if "created" in model:
                    created_timestamp = model["created"]
                    print(f"  • Creado: {created_timestamp}")
                
                if "owned_by" in model:
                    owned_by = model["owned_by"]
                    print(f"  • Propietario: {owned_by}")
                
                print("")  # Línea en blanco para separar modelos
            
            print("\n💡 Consejo: Usa exactamente estos IDs de modelos en tu configuración")
            print("   Actualiza el archivo src/config/settings.py con estos valores")
        else:
            print("⚠️ Estructura de respuesta inesperada. Respuesta completa:")
            print(models_data)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con GroqCloud: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Detalles del error: {e.response.text}")
        return 1
    
    # Probar una solicitud simple de chat completion
    print("\n🔄 Probando una solicitud simple de chat completion...")
    
    try:
        # Usar el primer modelo de la lista
        if "data" in models_data and models_data["data"]:
            model_id = models_data["data"][0]["id"]
            
            # Endpoint para chat completions
            chat_url = "https://api.groq.com/openai/v1/chat/completions"
            
            # Cuerpo de la solicitud
            data = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "Eres un asistente útil."},
                    {"role": "user", "content": "Hola, ¿cómo estás?"}
                ],
                "temperature": 0.7,
                "max_tokens": 50
            }
            
            print(f"Usando modelo: {model_id}")
            
            # Realizar la solicitud
            response = requests.post(chat_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # Lanzar excepción si hay error HTTP
            
            # Procesar la respuesta
            chat_response = response.json()
            
            print("✅ Solicitud de chat completion exitosa!")
            
            if "choices" in chat_response and len(chat_response["choices"]) > 0:
                message_content = chat_response["choices"][0]["message"]["content"]
                print(f"\nRespuesta: {message_content}")
            else:
                print("⚠️ Estructura de respuesta inesperada. Respuesta completa:")
                print(chat_response)
        else:
            print("⚠️ No se encontraron modelos para probar")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al realizar solicitud de chat completion: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Detalles del error: {e.response.text}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())