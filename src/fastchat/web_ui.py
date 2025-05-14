import threading
import time
import importlib
import os
import gradio as gr
from src.config.settings import MENTAL_HEALTH_CATEGORIES, FASTCHAT_CONFIG

def custom_mental_health_ui():
    """Crea una interfaz de usuario personalizada para el asistente de salud mental"""
    with gr.Blocks(title="Asistente de Salud Mental") as demo:
        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown(
                    """# Asistente Virtual de Salud Mental
                    
                    Este chatbot está diseñado para proporcionar soporte emocional y psicoeducación.
                    No reemplaza a profesionales de salud mental. Si experimentas una crisis o emergencia,
                    contacta con servicios de emergencia locales o líneas de crisis.
                    
                    **Recursos de emergencia:**
                    - Línea de Prevención del Suicidio: 024
                    - Emergencias: 112
                    """
                )
        
        categories = MENTAL_HEALTH_CATEGORIES if MENTAL_HEALTH_CATEGORIES else ["General", "Ansiedad", "Depresión", "Estrés", "Relaciones"]
        
        with gr.Row():
            topic = gr.Radio(
                categories,
                label="Selecciona un tema",
                info="Esto ayuda al asistente a contextualizar mejor tu consulta",
                value="General"
            )
                
        # Funciones para manejar la conversación - usar tuplas para compatibilidad
        chatbot = gr.Chatbot(height=500, show_label=False)
        msg = gr.Textbox(label="Escribe tu mensaje aquí", placeholder="¿Cómo puedo ayudarte hoy?")
        clear = gr.Button("Limpiar conversación")
        
        # Área para recursos
        with gr.Accordion("Recursos", open=False):
            resources_md = gr.Markdown("""
            ### Recursos Generales
            - [OMS - Salud Mental](https://www.who.int/es/health-topics/mental-health)
            - [Teléfono de la Esperanza](https://telefonodelaesperanza.org/)
            """)
        
        with gr.Accordion("Parámetros", open=False):
            temperature = gr.Slider(0.1, 1.5, 0.7, 
                                   label="Temperatura", 
                                   info="Controla la creatividad de las respuestas")
            max_new_tokens = gr.Slider(64, 4096, 512, 
                                      label="Longitud máxima", 
                                      step=64)
        
        # Estado para almacenar la categoría actual
        state = gr.State({"category": "General"})
        
        # Conversación con el modelo
        def process_message(message, history, state_data):
            """Procesa el mensaje del usuario y genera una respuesta"""
            if not message:
                return "", history, state_data
                
            # Formatear mensaje con categoría
            category = state_data.get("category", "General")
            
            # Aquí deberías llamar a tu modelo Vicuna
            try:
                # Usar la librería requests directamente
                import requests
                import json
                
                # URL de la API de FastChat
                api_url = "http://localhost:8000/v1/chat/completions"
                
                # Preparar la solicitud
                payload = {
                    "model": "vicuna",  # El nombre puede variar según tu configuración
                    "messages": [
                        {"role": "system", "content": f"Eres un asistente de salud mental especializado en temas de {category.lower()}."},
                        {"role": "user", "content": message}
                    ],
                    "temperature": float(temperature.value),
                    "max_tokens": int(max_new_tokens.value)
                }
                
                # Hacer la solicitud
                response = requests.post(api_url, json=payload)
                
                # Comprobar la respuesta
                if response.status_code == 200:
                    # Procesar la respuesta
                    result = response.json()
                    assistant_response = result['choices'][0]['message']['content']
                else:
                    # Si hay un error, devolver un mensaje de error
                    assistant_response = f"Error al llamar a la API: {response.status_code}"
                    
            except Exception as e:
                print(f"Error al llamar a la API: {e}")
                assistant_response = "Lo siento, estoy teniendo problemas para responder en este momento."
                
            # Actualizar el historial (usando formato de tuplas)
            history.append((message, assistant_response))
            return "", history, state_data
            
        def update_category(category, state_data):
            """Actualiza la categoría actual"""
            state_data["category"] = category
            return state_data, f"### Recursos para {category}\n- [Ejemplo](https://example.com)"
            
        def update_prompt_suggestion(category, state_data):
            """Actualiza la sugerencia de prompt basada en la categoría"""
            prompts = {
                "General": "Hola, me gustaría conversar contigo.",
                "Ansiedad": "Últimamente me siento ansioso. ¿Podrías ayudarme?",
                "Depresión": "He estado sintiéndome sin energía y con poco interés en las cosas.",
                "Estrés": "El estrés me está afectando mucho últimamente.",
                "Relaciones": "Estoy teniendo dificultades en mis relaciones personales."
            }
            
            return prompts.get(category, f"Me gustaría hablar sobre {category.lower()}.")
        
        # Eventos
        msg.submit(process_message, [msg, chatbot, state], [msg, chatbot, state])
        clear.click(lambda: [], None, [chatbot])
        topic.change(update_category, [topic, state], [state, resources_md])
        topic.change(update_prompt_suggestion, [topic, state], [msg])
        
    return demo

def start_web_server():
    """Inicia el servidor web de Gradio"""
    cfg = FASTCHAT_CONFIG["web_server"]
    host = cfg.get("host", "0.0.0.0")
    port = int(cfg.get("port", "7860"))
    share = cfg.get("share", False)
    
    try:
        ui = custom_mental_health_ui()
        ui.launch(
            server_name=host,
            server_port=port,
            share=share
        )
    except Exception as e:
        print(f"Error al iniciar la interfaz web: {e}")
        # Intento de fallback con la interfaz básica de gradio
        print("Intentando iniciar interfaz básica...")
        with gr.Blocks(title="Asistente de Salud Mental") as demo:
            gr.Markdown("# Asistente de Salud Mental (Modo Básico)")
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Limpiar")
            
            def respond(message, chat_history):
                chat_history.append((message, "Lo siento, el modelo no está disponible en este momento."))
                return "", chat_history
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)
            
        demo.launch(server_name=host, server_port=port, share=share)

def launch_web_server():
    """Lanza el servidor web como un proceso daemon"""
    web_thread = threading.Thread(target=start_web_server)
    web_thread.daemon = True
    web_thread.start()
    print(f"✅ Interfaz web iniciándose en http://localhost:{FASTCHAT_CONFIG['web_server'].get('port', 7860)}")
    return web_thread