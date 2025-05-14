#!/usr/bin/env python
"""
Asistente de Salud Mental usando GroqCloud

Este script inicia el asistente de salud mental usando la API de GroqCloud
para procesar las consultas del usuario.
"""

import os
import sys
import argparse
import time
from dotenv import load_dotenv
import gradio as gr
from PIL import Image, ImageDraw, ImageFont

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno
load_dotenv()

def parse_args():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="Asistente de Salud Mental con GroqCloud")
    parser.add_argument("--port", type=int, default=7860, help="Puerto para la interfaz web")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host para la interfaz web")
    parser.add_argument("--share", action="store_true", help="Compartir la interfaz web con un enlace público")
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

def create_default_assets():
    """Crea archivos de assets por defecto si no existen"""
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Crear logo si no existe
    logo_path = os.path.join(assets_dir, "logo.png")
    if not os.path.exists(logo_path):
        # Intentar crear un logo minimalista con PIL
        try:
            # Crear imagen
            img = Image.new('RGB', (300, 100), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            
            # Dibujar texto
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()
                
            d.text((10, 40), "Asistente de Salud Mental", fill=(0, 0, 0), font=font)
            
            # Guardar imagen
            img.save(logo_path)
            
            print(f"✅ Creado logo por defecto en {logo_path}")
        except Exception as e:
            print(f"⚠️ No se pudo crear el logo: {e}")

def get_gradio_version():
    """Obtiene la versión de Gradio instalada"""
    try:
        return float(gr.__version__.split('.')[0])
    except (AttributeError, ValueError, IndexError):
        return 0  # No se pudo determinar la versión

def main():
    """Función principal"""
    try:
        args = parse_args()
        
        print("🧠 Iniciando Asistente de Salud Mental basado en LLMs...")
        
        # Verificar que tenemos todos los requisitos
        if not verify_groq_api_key():
            return 1
        
        # Crear assets por defecto
        create_default_assets()
        
        # Importar el cliente de GroqCloud y probar la conexión
        from src.utils.groq_client import GroqClient
        
        try:
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
        except Exception as e:
            print(f"⚠️ No se pudo conectar con GroqCloud: {e}")
            print("Continuando con configuración por defecto...")
        
        # Importar la interfaz
        from src.interface import create_mental_health_interface
        
        # Crear la interfaz
        print("🚀 Iniciando la interfaz de usuario...")
        demo = create_mental_health_interface()
        
        # Mostrar información de inicio
        print("\n" + "=" * 50)
        print("✨ ¡Asistente iniciado correctamente!")
        print(f"💬 Interfaz web disponible en http://localhost:{args.port}")
        if args.share:
            print("🌐 La interfaz también estará disponible con un enlace público")
        print("💡 Presiona Ctrl+C para detener el asistente")
        print("=" * 50 + "\n")
        
        # Verificar la versión de Gradio para compatibilidad
        gradio_version = get_gradio_version()
        
        # Activar la cola de forma compatible con la versión
        try:
            if gradio_version >= 3:
                # Versión 3.x o superior, que podría tener concurrency_count
                try:
                    demo.queue(concurrency_count=5)
                except TypeError:
                    # Fallback si no tiene concurrency_count
                    demo.queue()
            else:
                # Versión anterior
                demo.queue()
        except Exception as e:
            print(f"⚠️ No se pudo activar la cola de Gradio: {e}")
            print("Continuando sin cola...")
        
        # Iniciar la interfaz
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            # Usar show_error solo si está disponible (versiones más recientes)
            **({"show_error": args.debug} if hasattr(gr, "__version__") and gr.__version__ >= "3.0" else {})
        )
        
        return 0
    except KeyboardInterrupt:
        print("\n👋 Deteniendo el asistente...")
        return 0
    except Exception as e:
        print(f"❌ Error al iniciar el asistente: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())