import threading
import time
import os
import importlib
import sys  # Importar sys para el método alternativo
import torch
import subprocess
from src.config.settings import FASTCHAT_CONFIG, VICUNA_GENERATION_CONFIG

def start_worker():
    """Inicia el trabajador del modelo de FastChat para Vicuna"""
    # Obtener configuración desde settings
    cfg = FASTCHAT_CONFIG["model_worker"]
    
    # Configuración básica
    model_path = cfg.get("model_path", os.getenv("MODEL_PATH", "lmsys/vicuna-7b-v1.5"))
    device = cfg.get("device", os.getenv("DEVICE", "cpu"))
    controller_addr = f"http://{FASTCHAT_CONFIG['controller']['host']}:{FASTCHAT_CONFIG['controller']['port']}"
    worker_addr = f"http://{cfg.get('host', 'localhost')}:{cfg.get('port', 21002)}"
    worker_id = cfg.get("worker_id", "mental_health_assistant_worker")
    
    # Configuración avanzada
    load_8bit = cfg.get("load_8bit", os.getenv("LOAD_8BIT", "False").lower() == "true")
    cpu_offloading = cfg.get("cpu_offloading", os.getenv("CPU_OFFLOADING", "False").lower() == "true")
    gpus = os.getenv("GPUS", "")
    num_gpus = int(cfg.get("num_gpus", os.getenv("NUM_GPUS", "1")))
    max_gpu_memory = cfg.get("max_gpu_memory", None)
    
    # Configurar GPUs visibles
    if gpus:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpus
    
    try:
        # Método alternativo: ejecutar un script externo usando python -m
        print("Iniciando worker vía subprocess...")
        
        # Construir comando
        cmd = [
            sys.executable,  # Usar el ejecutable Python actual
            "-m", "fastchat.serve.model_worker",
            "--model-path", model_path,
            "--controller-address", controller_addr,
            "--worker-address", worker_addr,
            "--device", device
        ]
        
        # Añadir argumentos opcionales
        if worker_id:
            cmd.extend(["--worker-name", worker_id])
        
        if load_8bit:
            cmd.append("--load-8bit")
            
        if cpu_offloading:
            cmd.append("--cpu-offloading")
            
        # Añadir argumentos de generación
        for key, value in VICUNA_GENERATION_CONFIG.items():
            if key == "temperature":
                cmd.extend(["--temperature", str(value)])
            elif key == "max_new_tokens":
                cmd.extend(["--max-new-tokens", str(value)])
            elif key == "repetition_penalty":
                cmd.extend(["--repetition-penalty", str(value)])
        
        # Ejecutar en un proceso separado
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Devolver el proceso
        return process
    except Exception as e:
        print(f"Error al iniciar el trabajador: {e}")
        import traceback
        traceback.print_exc()
        return None

def launch_worker():
    """Lanza el trabajador del modelo como un proceso daemon"""
    worker_process = start_worker()
    
    # No es un hilo, es un proceso, así que no usamos thread.daemon
    # Esperar a que el worker se inicie
    time.sleep(6)  # Vicuna puede tardar un poco en cargar
    print(f"✅ Trabajador del modelo iniciado en {FASTCHAT_CONFIG['model_worker'].get('host', 'localhost')}:{FASTCHAT_CONFIG['model_worker'].get('port', 21002)}")
    return worker_process