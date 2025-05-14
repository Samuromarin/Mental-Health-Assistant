import threading
import time
import importlib
import sys
import uvicorn

def start_controller():
    """Inicia el controlador de FastChat en un hilo separado"""
    try:
        # Importar directamente el controlador y la app de FastChat
        from fastchat.serve.controller import Controller, app
        
        # Crear el controlador con dispatch_method requerido
        controller = Controller(dispatch_method="shortest_queue")
        
        # Iniciar la app con uvicorn en un hilo
        def run_controller():
            uvicorn.run(app, host="localhost", port=21001)
        
        # Iniciar en un nuevo hilo
        thread = threading.Thread(target=run_controller)
        thread.daemon = True
        thread.start()
        
        return controller
    except Exception as e:
        print(f"Error al iniciar el controlador: {e}")
        import traceback
        traceback.print_exc()
        return None

def launch_controller():
    """Lanza el controlador como un proceso daemon"""
    controller_thread = threading.Thread(target=start_controller)
    controller_thread.daemon = True
    controller_thread.start()
    # Esperar a que el controlador se inicie
    time.sleep(2)
    print(f"✅ Controlador iniciado en localhost:21001")
    return controller_thread