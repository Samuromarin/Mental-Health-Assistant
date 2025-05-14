import sys
import os
import time
import importlib
import argparse
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
load_dotenv()

from src.config.settings import FASTCHAT_CONFIG
from src.fastchat.controller import launch_controller
from src.fastchat.model_worker import launch_worker
from src.fastchat.api_server import launch_api_server
from src.fastchat.web_ui import launch_web_server

def verify_gpu():
    """Verifica si hay GPU disponible y configura variables de entorno"""
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            os.environ["CUDA_AVAILABLE"] = "1"
            os.environ["DEVICE"] = "cuda"
            num_gpus = torch.cuda.device_count()
            os.environ["NUM_GPUS"] = str(num_gpus)
            
            # Información de la GPU
            for i in range(num_gpus):
                print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
                gpu_mem = torch.cuda.get_device_properties(i).total_memory / 1024**3
                print(f"   Memoria: {gpu_mem:.2f} GB")
            
            print(f"✅ CUDA disponible con {num_gpus} GPU(s)")
            return True
        else:
            os.environ["CUDA_AVAILABLE"] = "0"
            os.environ["DEVICE"] = "cpu"
            os.environ["NUM_GPUS"] = "0"
            print("⚠️ CUDA no disponible. Usando CPU (será considerablemente más lento)")
            return False
    except ImportError:
        os.environ["CUDA_AVAILABLE"] = "0"
        os.environ["DEVICE"] = "cpu"
        os.environ["NUM_GPUS"] = "0"
        print("⚠️ PyTorch no está instalado correctamente. Usando CPU.")
        return False
    except Exception as e:
        os.environ["CUDA_AVAILABLE"] = "0"
        os.environ["DEVICE"] = "cpu"
        os.environ["NUM_GPUS"] = "0"
        print(f"⚠️ Error al verificar GPU: {e}. Usando CPU.")
        return False

def import_module_safely(name):
    """Importa un módulo de forma segura, mostrando un error claro si falla"""
    try:
        return importlib.import_module(name)
    except ImportError as e:
        print(f"❌ Error al importar {name}: {e}")
        return None
    
def check_api_keys():
    """Verifica que las claves API necesarias estén configuradas"""
    from src.config.settings import OPENAI_API_KEY
    
    if not OPENAI_API_KEY and FASTCHAT_CONFIG["model_worker"]["model_path"] == "facebook/opt-350m":
        print("⚠️ No se ha encontrado la clave API de OpenAI ni un modelo local.")
        print("   Se utilizará un modelo pequeño OPT-350M para demostraciones.")
        print("   Para mejor rendimiento, configura MODEL_PATH en .env con un modelo de LLM local")
        print("   o configura OPENAI_API_KEY para usar la API de OpenAI.")
        return True
    return True

def create_default_assets():
    """Crea archivos de assets por defecto si no existen"""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Crear favicon si no existe
    favicon_path = os.path.join(assets_dir, "favicon.ico")
    if not os.path.exists(favicon_path):
        # Contenido base64 de un favicon minimalista
        import base64
        favicon_data = base64.b64decode("AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8AAAD/AAAA/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAA/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/wAAAP8AAAD/AAAA/wAAAP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAA/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        
        with open(favicon_path, "wb") as f:
            f.write(favicon_data)
        
        print(f"✅ Creado favicon por defecto en {favicon_path}")
    
    # Crear logo si no existe
    logo_path = os.path.join(assets_dir, "logo.png")
    if not os.path.exists(logo_path):
        # Intentar crear un logo minimalista con PIL si está disponible
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Crear imagen
            img = Image.new('RGB', (300, 100), color = (255, 255, 255))
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
        except ImportError:
            print("⚠️ PIL no está instalado. No se creó el logo por defecto.")
            pass

def initialize_fastchat():
    """Inicializa todos los componentes de FastChat"""
    # 1. Iniciar controlador
    controller_thread = launch_controller()
    
    # 2. Iniciar trabajador del modelo
    worker_thread = launch_worker()
    
    # 3. Iniciar servidor API
    api_thread = launch_api_server()
    
    # 4. Iniciar interfaz web
    web_thread = launch_web_server()
    
    return {
        "controller": controller_thread,
        "worker": worker_thread,
        "api": api_thread,
        "web": web_thread
    }

def parse_arguments():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="Asistente de Salud Mental con FastChat")
    parser.add_argument("--no-download", action="store_true", help="No descargar el modelo automáticamente")
    parser.add_argument("--cpu-only", action="store_true", help="Forzar el uso de CPU incluso si hay GPU disponible")
    parser.add_argument("--port", type=int, default=None, help="Puerto para la interfaz web")
    parser.add_argument("--share", action="store_true", help="Compartir la interfaz web con un enlace público")
    
    return parser.parse_args()

def main():
    """Función principal para ejecutar el asistente"""
    args = parse_arguments()
    
    # Configurar variables de entorno según argumentos
    if args.cpu_only:
        os.environ["DEVICE"] = "cpu"
        os.environ["CUDA_AVAILABLE"] = "0"
    
    if args.port:
        FASTCHAT_CONFIG["web_server"]["port"] = args.port
        
    if args.share:
        os.environ["SHARE_GRADIO"] = "True"
        FASTCHAT_CONFIG["web_server"]["share"] = True
    
    try:
        print("🤖 Iniciando Asistente de Salud Mental con FastChat...")
        
        # Verificar GPU
        if not args.cpu_only:
            verify_gpu()
        
        # Crear assets por defecto
        create_default_assets()
        
        # Verificar si el modelo está descargado
        if not args.no_download:
            try:
                from src.utils.download_model import is_model_downloaded, download_vicuna
                
                model_path = os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5")
                print(f"📦 Modelo configurado: {model_path}")
                
                if not is_model_downloaded(model_path):
                    print(f"⚠️ El modelo {model_path} no está descargado.")
                    download = input("¿Deseas descargarlo ahora? (s/n): ")
                    if download.lower() == "s":
                        downloaded_path = download_vicuna(model_path)
                        if downloaded_path:
                            os.environ["MODEL_PATH"] = downloaded_path
                            print(f"✅ Modelo descargado en: {downloaded_path}")
                        else:
                            print("❌ No se pudo descargar el modelo. El asistente podría no funcionar correctamente.")
                    else:
                        print("⚠️ Continuando sin descargar el modelo. El asistente podría no funcionar correctamente.")
                else:
                    print(f"✅ Modelo encontrado: {model_path}")
            except ImportError:
                print("⚠️ No se pudo verificar el modelo. Asegúrate de tener el módulo download_model.py")
        
        # Verificar dependencias
        try:
            import fastchat
            print(f"✅ FastChat instalado (versión: {getattr(fastchat, '__version__', 'desconocida')})")
        except ImportError:
            print("❌ FastChat no está instalado correctamente.")
            print("   Ejecuta: pip install 'fschat[model_worker,webui]'")
            return False
        
        try:
            import gradio
            print(f"✅ Gradio instalado (versión: {getattr(gradio, '__version__', 'desconocida')})")
        except ImportError:
            print("❌ Gradio no está instalado correctamente.")
            print("   Ejecuta: pip install gradio")
            return False
            
        # Importar módulos de FastChat
        print("📦 Cargando componentes...")
        controller_module = import_module_safely("src.fastchat.controller")
        model_worker_module = import_module_safely("src.fastchat.model_worker")
        web_ui_module = import_module_safely("src.fastchat.web_ui")
        api_server_module = import_module_safely("src.fastchat.api_server")
        
        if not (controller_module and model_worker_module and web_ui_module and api_server_module):
            print("❌ No se pudieron cargar todos los módulos necesarios.")
            return False
            
        # Inicializar componentes
        print("🚀 Iniciando componentes...")
        controller_thread = controller_module.launch_controller()
        time.sleep(2)  # Esperar a que el controlador se inicie
        
        worker_thread = model_worker_module.launch_worker()
        time.sleep(5)  # Esperar a que el worker se inicie
        
        api_thread = api_server_module.launch_api_server()
        time.sleep(1)  # Esperar a que el API se inicie
        
        web_thread = web_ui_module.launch_web_server()
        
        print("\n" + "=" * 50)
        print("✨ ¡Asistente iniciado correctamente!")
        print(f"💬 Interfaz web disponible en http://localhost:{FASTCHAT_CONFIG['web_server']['port']}")
        print(f"🔌 API REST disponible en http://localhost:{FASTCHAT_CONFIG['api_server']['port']}")
        print("💡 Presiona Ctrl+C para detener el asistente")
        print("=" * 50 + "\n")
        
        # Mantener el programa en ejecución
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Deteniendo el asistente...")
            
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()