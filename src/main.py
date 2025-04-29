import sys
import os

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.settings import OPENAI_API_KEY, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS
import openai

def initialize_api():
    """Inicializa la API de OpenAI"""
    if not OPENAI_API_KEY:
        raise ValueError("No se ha encontrado la clave API de OpenAI. Verifica tu archivo .env")
    openai.api_key = OPENAI_API_KEY
    return True

def main():
    """Función principal para ejecutar el asistente"""
    try:
        initialize_api()
        print("🤖 Asistente de salud mental iniciado correctamente")
        print("💬 Escribe 'salir' para terminar la conversación")
        # Aquí irá tu código del chatbot
        # Por ahora solo imprimimos un mensaje
        print("✨ ¡Configuración completada exitosamente!")
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        return False

if __name__ == "__main__":
    main()