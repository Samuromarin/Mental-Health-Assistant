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
from typing import List, Optional

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
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Modo interactivo para múltiples consultas")
    parser.add_argument("--temperature", "-t", type=float, default=0.7,
                       help="Temperatura para la generación (0.1-1.5)")
    parser.add_argument("--max-tokens", "-mt", type=int, default=500,
                       help="Número máximo de tokens en la respuesta")
    return parser.parse_args()

def get_available_categories() -> List[str]:
    """Obtiene las categorías disponibles desde la configuración"""
    try:
        from src.config.settings import MENTAL_HEALTH_CATEGORIES
        return MENTAL_HEALTH_CATEGORIES
    except ImportError:
        return ["General", "Ansiedad", "Depresión", "Estrés", "Relaciones", "Autoestima", "Técnicas de relajación"]

def validate_category(category: str) -> str:
    """Valida que la categoría exista o devuelve 'General'"""
    categories = get_available_categories()
    if category in categories:
        return category
    
    print(f"⚠️ Categoría '{category}' no válida. Categorías disponibles: {', '.join(categories)}")
    print("Usando categoría 'General' por defecto.")
    return "General"

def interactive_mode(client, model_id: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 500):
    """Modo interactivo para múltiples consultas"""
    categories = get_available_categories()
    
    print("\n===== MODO INTERACTIVO DEL ASISTENTE DE SALUD MENTAL =====")
    print("Escribe 'salir', 'exit' o 'q' para terminar")
    print("Escribe 'categoria' o 'category' para cambiar la categoría actual")
    print("Escribe 'modelo' o 'model' para cambiar el modelo actual")
    
    category = "General"
    
    while True:
        print(f"\n[Categoría: {category}] [Modelo: {model_id}]")
        message = input(">>> ")
        
        # Comandos especiales
        if message.lower() in ["salir", "exit", "q"]:
            print("¡Hasta pronto!")
            break
        
        elif message.lower() in ["categoria", "category"]:
            print(f"Categorías disponibles: {', '.join(categories)}")
            new_category = input("Nueva categoría: ")
            if new_category in categories:
                category = new_category
                print(f"Categoría cambiada a: {category}")
            else:
                print(f"⚠️ Categoría no válida. Sigue usando: {category}")
            continue
        
        elif message.lower() in ["modelo", "model"]:
            models = client.get_available_models()
            print(f"Modelos disponibles: {', '.join(models)}")
            new_model = input("Nuevo modelo: ")
            if new_model in models:
                model_id = new_model
                print(f"Modelo cambiado a: {model_id}")
            else:
                print(f"⚠️ Modelo no válido. Sigue usando: {model_id}")
            continue
        
        elif not message.strip():
            continue
        
        # Enviar mensaje
        print("🤔 Generando respuesta...")
        start_time = time.time()
        
        try:
            response = client.generate_mental_health_response(
                message,
                category=category,
                model_id=model_id,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            elapsed_time = time.time() - start_time
            
            print("\n" + "=" * 80)
            print(response)
            print("=" * 80)
            print(f"⏱️  Tiempo: {elapsed_time:.2f} segundos")
        
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Función principal"""
    args = parse_args()
    
    try:
        # Importar el cliente de GroqCloud
        from src.utils.groq_client import GroqClient
        
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
        
        # Validar categoría
        category = validate_category(args.category)
        
        # Determinar qué modelo usar
        model = args.model
        if not model:
            # Usar el primer modelo disponible
            model = client.get_available_models()[0]
        
        # Modo interactivo
        if args.interactive:
            interactive_mode(client, model, args.temperature, args.max_tokens)
            return 0
        
        # Modo de mensaje único
        # Si no se proporcionó mensaje, solicitar uno
        message = args.message
        if not message:
            message = input("Escribe tu mensaje: ")
        
        # Mostrar información
        print(f"🔄 Enviando mensaje a GroqCloud...")
        print(f"📝 Mensaje: {message}")
        print(f"🧠 Modelo: {model}")
        print(f"📚 Categoría: {category}")
        print(f"🌡️ Temperatura: {args.temperature}")
        print(f"🔢 Tokens máximos: {args.max_tokens}")
        
        # Iniciar temporizador
        start_time = time.time()
        
        # Enviar solicitud
        response = client.generate_mental_health_response(
            message,
            category=category,
            model_id=model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
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