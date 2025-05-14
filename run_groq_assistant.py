#!/usr/bin/env python
"""
Asistente de Salud Mental usando GroqCloud

Este script inicia el asistente de salud mental usando la API de GroqCloud
para procesar las consultas del usuario.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno
load_dotenv()

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="Asistente de Salud Mental con GroqCloud")
    parser.add_argument("--port", type=int, default=7860, help="Puerto para la interfaz web")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host para la interfaz web")
    parser.add_argument("--share", action="store_true", help="Compartir la interfaz web")
    parser.add_argument("--model", type=str, help="Modelo de GroqCloud a usar")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    return parser.parse_args()

def verify_groq_api_key():
    """Verifica que la clave API de GroqCloud está configurada"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: No se ha encontrado la clave API de GroqCloud")
        print("Por favor, configura la variable de entorno GROQ_API_KEY en el archivo .env")
        print("Puedes obtener una clave API en https://console.groq.com/")
        return False
    return True

def main():
    """Función principal"""
    args = parse_args()
    
    # Verificar clave API
    if not verify_groq_api_key():
        return 1
    
    try:
        # Importar el cliente de GroqCloud
        from src.utils.groq_client import GroqClient
        
        # Probar la conexión
        client = GroqClient()
        models = client.get_available_models()
        print("✅ Conexión con GroqCloud establecida")
        print(f"📋 Modelos disponibles: {', '.join(models)}")
        
        # Si se especificó un modelo, verificar que exista
        if args.model and args.model not in models:
            print(f"⚠️  El modelo {args.model} no está disponible. Modelos disponibles: {', '.join(models)}")
            print(f"Se usará el modelo predeterminado: {models[0]}")
            args.model = models[0]
        elif args.model:
            print(f"✅ Se usará el modelo: {args.model}")
        else:
            print(f"✅ Se usará el modelo predeterminado: {models[0]}")
        
        # Importar la interfaz
        from src.groq_interface import create_mental_health_interface
        
        # Crear la interfaz
        print("🚀 Iniciando la interfaz de usuario...")
        demo = create_mental_health_interface()
        
        # Iniciar la interfaz
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug
        )
        
        return 0
    except Exception as e:
        print(f"❌ Error al iniciar el asistente: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
