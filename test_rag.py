#!/usr/bin/env python
"""
Script para probar el sistema RAG del asistente de salud mental

Permite comparar respuestas con y sin RAG para evaluar las mejoras.
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
    parser = argparse.ArgumentParser(description="Prueba del sistema RAG")
    parser.add_argument("--message", "-m", type=str, help="Mensaje a probar")
    parser.add_argument("--category", "-c", type=str, default="General", 
                       help="Categoría de salud mental")
    parser.add_argument("--model", type=str, help="Modelo de GroqCloud a usar")
    parser.add_argument("--compare", action="store_true", 
                       help="Comparar respuestas con y sin RAG")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Modo interactivo")
    parser.add_argument("--setup", action="store_true",
                       help="Configurar sistema RAG (crear ejemplos e indexar)")
    return parser.parse_args()

def setup_rag_system():
    """Configura el sistema RAG desde cero con FAISS"""
    print("🚀 Configurando sistema RAG con FAISS...")
    
    try:
        # Crear documentos de ejemplo
        print("\n1. Creando documentos de ejemplo...")
        import subprocess
        result = subprocess.run([sys.executable, "manage_rag.py", "create-examples", "--overwrite"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Documentos de ejemplo creados")
        else:
            print(f"⚠️ Error creando documentos: {result.stderr}")
        
        # Inicializar RAG Manager
        print("\n2. Inicializando RAG Manager...")
        from src.utils.rag_manager import initialize_rag_manager
        rag_manager = initialize_rag_manager(
            embeddings_model='all-MiniLM-L6-v2'
        )
        
        if not rag_manager:
            print("❌ Error inicializando RAG Manager")
            return False
        
        # Indexar documentos
        print("\n3. Indexando documentos...")
        success = rag_manager.index_documents()
        
        if success:
            print("✅ Sistema RAG configurado correctamente")
            
            # Mostrar estadísticas
            stats = rag_manager.get_stats()
            print(f"\n📊 Estadísticas:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
            return True
        else:
            print("❌ Error indexando documentos")
            return False
            
    except Exception as e:
        print(f"❌ Error en la configuración: {e}")
        return False

def test_rag_response(message, category="General", model=None, compare=False):
    """Prueba una respuesta con RAG"""
    
    try:
        from src.utils.groq_client import GroqClient
        
        # Crear cliente con RAG habilitado
        print("🔄 Inicializando cliente con RAG...")
        client = GroqClient(enable_rag=True)
        
        # Verificar estado de RAG
        rag_status = client.get_rag_status()
        print(f"📊 Estado RAG: {rag_status}")
        
        if not rag_status.get("enabled", False):
            print("⚠️ RAG no está habilitado.")
            print("💡 Verifica que tengas FAISS instalado: pip install faiss-cpu")
            print("💡 Y que hayas indexado documentos: python manage_rag.py index")
            return False
        
        print(f"\n💬 Probando mensaje: '{message}'")
        print(f"📚 Categoría: {category}")
        print(f"🧠 Modelo: {model or 'Por defecto'}")
        
        if compare:
            print("\n" + "="*60)
            print("🔍 COMPARACIÓN: CON RAG vs SIN RAG")
            print("="*60)
            
            # Respuesta SIN RAG
            print("\n🚫 Respuesta SIN RAG:")
            print("-" * 40)
            start_time = time.time()
            response_no_rag = client.generate_mental_health_response(
                message, 
                category=category,
                model_id=model,
                use_rag=False
            )
            time_no_rag = time.time() - start_time
            print(response_no_rag)
            print(f"\n⏱️ Tiempo: {time_no_rag:.2f}s")
            
            # Respuesta CON RAG
            print("\n✅ Respuesta CON RAG:")
            print("-" * 40)
            start_time = time.time()
            response_with_rag = client.generate_mental_health_response(
                message, 
                category=category,
                model_id=model,
                use_rag=True
            )
            time_with_rag = time.time() - start_time
            print(response_with_rag)
            print(f"\n⏱️ Tiempo: {time_with_rag:.2f}s")
            
            # Análisis de diferencias
            print("\n📈 ANÁLISIS:")
            print(f"  Longitud sin RAG: {len(response_no_rag)} caracteres")
            print(f"  Longitud con RAG: {len(response_with_rag)} caracteres")
            print(f"  Diferencia de tiempo: {abs(time_with_rag - time_no_rag):.2f}s")
            
            # Verificar si se usó contexto RAG
            if "base de conocimiento" in response_with_rag.lower():
                print("  ✅ Respuesta RAG incluye contexto especializado")
            else:
                print("  ⚠️ No se detectó uso de contexto RAG")
        
        else:
            # Solo respuesta con RAG
            print("\n✅ Respuesta con RAG:")
            print("-" * 40)
            start_time = time.time()
            response = client.generate_mental_health_response(
                message, 
                category=category,
                model_id=model,
                use_rag=True
            )
            elapsed_time = time.time() - start_time
            print(response)
            print(f"\n⏱️ Tiempo: {elapsed_time:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando RAG: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_rag_test():
    """Modo interactivo para probar RAG"""
    print("\n" + "="*50)
    print("🧪 MODO INTERACTIVO DE PRUEBA RAG")
    print("="*50)
    print("Comandos especiales:")
    print("  'exit' o 'salir' - Terminar")
    print("  'compare' - Activar/desactivar comparación")
    print("  'category <nombre>' - Cambiar categoría")
    print("  'status' - Ver estado del sistema")
    print("="*50)
    
    try:
        from src.utils.groq_client import GroqClient
        from src.config.settings import MENTAL_HEALTH_CATEGORIES
        
        client = GroqClient(enable_rag=True)
        category = "General"
        compare_mode = False
        
        while True:
            print(f"\n[Categoría: {category}] [Comparación: {'ON' if compare_mode else 'OFF'}]")
            message = input(">>> ")
            
            if message.lower() in ['exit', 'salir', 'q']:
                print("👋 ¡Hasta luego!")
                break
            
            elif message.lower() == 'compare':
                compare_mode = not compare_mode
                print(f"🔄 Modo comparación: {'Activado' if compare_mode else 'Desactivado'}")
                continue
            
            elif message.lower().startswith('category '):
                new_category = message[9:].strip()
                if new_category in MENTAL_HEALTH_CATEGORIES:
                    category = new_category
                    print(f"📚 Categoría cambiada a: {category}")
                else:
                    print(f"❌ Categoría inválida. Opciones: {', '.join(MENTAL_HEALTH_CATEGORIES)}")
                continue
            
            elif message.lower() == 'status':
                rag_status = client.get_rag_status()
                print("📊 Estado del sistema RAG:")
                for key, value in rag_status.items():
                    print(f"  {key}: {value}")
                continue
            
            elif not message.strip():
                continue
            
            # Procesar mensaje
            print("\n🔄 Procesando...")
            test_rag_response(message, category, compare=compare_mode)
    
    except KeyboardInterrupt:
        print("\n👋 Interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error en modo interactivo: {e}")

def main():
    """Función principal"""
    args = parse_args()
    
    print("🧪 Prueba del Sistema RAG - Asistente de Salud Mental")
    print("=" * 60)
    
    try:
        # Verificar clave API
        if not os.getenv("GROQ_API_KEY"):
            print("❌ Error: Variable GROQ_API_KEY no configurada")
            print("Configure su clave API en el archivo .env")
            return 1
        
        if args.setup:
            success = setup_rag_system()
            if not success:
                return 1
            
            if not args.interactive and not args.message:
                print("\n💡 Sistema configurado. Ahora puedes:")
                print("  - Probar un mensaje: python test_rag.py -m 'tu mensaje'")
                print("  - Modo interactivo: python test_rag.py -i")
                print("  - Comparar respuestas: python test_rag.py -m 'mensaje' --compare")
                return 0
        
        if args.interactive:
            interactive_rag_test()
            return 0
        
        # Modo de mensaje único
        message = args.message
        if not message:
            message = input("Escribe tu mensaje de prueba: ")
        
        if not message.strip():
            print("❌ Mensaje vacío")
            return 1
        
        success = test_rag_response(
            message, 
            args.category, 
            args.model, 
            args.compare
        )
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())