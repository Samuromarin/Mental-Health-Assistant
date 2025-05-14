#!/usr/bin/env python
"""
Script para probar la API de GroqCloud

Este script te permite probar rápidamente si tu configuración de GroqCloud funciona correctamente,
enviando un mensaje de prueba y mostrando la respuesta.
"""

import os
import sys
import argparse
import time
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno
load_dotenv()

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="Prueba de la API de GroqCloud")
    parser.add_argument("--message", "-m", type=str, help="Mensaje a enviar")
    parser.add_argument("--category", "-c", type=str, default="General", 
                       help="Categoría de salud mental: General, Ansiedad, Depresión, etc.")
    parser.add_argument("--model", type=str, help="Modelo de GroqCloud a usar")
    parser.add_argument("--list-models", "-l", action="store_true", help="Listar modelos disponibles")
    return parser.parse_args()

def main():
    """Función principal"""
    args = parse_args()
    
    try:
        # Importar el cliente de GroqCloud
        from src.utils.groq_client import GroqClient
        from src.config.settings import GROQ_MODELS
        
        # Crear cliente
        client = GroqClient()
        
        # Listar modelos si se solicitó
        if args.list_models:
            print("📋 Modelos disponibles en GroqCloud:")
            for model_id in client.get_available_models():
                model_info = client.get_model_info(model_id)
                print(f"- {model_id}: {model_info['name']} (contexto: {model_info['context_length']} tokens)")
                print(f"  {model_info['description']}")
            return 0
        
        # Si no se proporcionó mensaje, solicitar uno
        message = args.message
        if not message:
            message = input("Escribe tu mensaje: ")
        
        # Determinar qué modelo usar
        model = args.model
        if not model:
            # Usar el primer modelo disponible
            model = client.get_available_models()[0]
        
        # Mostrar información
        print(f"🔄 Enviando mensaje a GroqCloud...")
        print(f"📝 Mensaje: {message}")
        print(f"🧠 Modelo: {model}")
        print(f"📚 Categoría: {args.category}")
        
        # Iniciar temporizador
        start_time = time.time()
        
        # Enviar solicitud
        response = client.generate_mental_health_response(
            message,
            category=args.category,
            temperature=0.7,
            max_tokens=500
        )
        
        # Calcular tiempo
        elapsed_time = time.time() - start_time
        
        # Mostrar respuesta
        print("\n" + "=" * 80)
        print("✅ Respuesta recibida:")
        print("-" * 80)
        print(response)
        print("=" * 80)
        print(f"⏱️  Tiempo de respuesta: {elapsed_time:.2f} segundos")
        
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
