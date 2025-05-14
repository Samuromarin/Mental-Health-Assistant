"""
Interfaz de usuario para el asistente de salud mental usando Gradio
"""

import os
import sys
import gradio as gr
from typing import Dict, Any, List, Tuple, Union

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.groq_client import GroqClient
from src.config.settings import MENTAL_HEALTH_CATEGORIES, RESOURCES, GROQ_MODELS
from src.utils.safety import detect_crisis, get_crisis_response

def create_mental_health_interface():
    """
    Crea la interfaz de usuario para el asistente de salud mental usando GroqCloud
    
    Returns:
        Objeto Gradio para lanzar la interfaz
    """
    
    # Crear cliente de GroqCloud
    try:
        client = GroqClient()
        available_models = client.get_available_models()
    except Exception as e:
        print(f"Error al inicializar el cliente de GroqCloud: {e}")
        available_models = list(GROQ_MODELS.keys()) if GROQ_MODELS else ["llama2-70b-4096"]
    
    # Ejemplos de preguntas por categoría para mejorar la experiencia de usuario
    examples = {
        "General": [
            "¿Podrías darme algunos consejos para mejorar mi bienestar emocional?",
            "¿Qué hábitos diarios son buenos para la salud mental?",
            "¿Cómo puedo saber si necesito ayuda profesional?"
        ],
        "Ansiedad": [
            "Últimamente me siento ansioso. ¿Podrías ayudarme?",
            "¿Cómo puedo manejar los ataques de pánico?",
            "¿Qué técnicas de respiración son buenas para la ansiedad?"
        ],
        "Depresión": [
            "He estado sintiéndome sin energía y con poco interés en las cosas",
            "¿Cómo puedo lidiar con pensamientos negativos recurrentes?",
            "Me cuesta levantarme por las mañanas. ¿Qué puedo hacer?"
        ],
        "Estrés": [
            "El trabajo me está causando mucho estrés, ¿cómo puedo manejarlo?",
            "Necesito técnicas para relajarme después de un día difícil",
            "¿Qué ejercicios rápidos me ayudarían a reducir el estrés?"
        ],
        "Relaciones": [
            "Tengo problemas para comunicarme con mi pareja",
            "¿Cómo puedo establecer límites saludables con mi familia?",
            "Me cuesta confiar en los demás después de una mala experiencia"
        ],
        "Autoestima": [
            "Siempre me comparo con los demás y me siento inferior",
            "¿Cómo puedo mejorar mi autoimagen?",
            "¿Qué ejercicios puedo hacer para fortalecer mi autoestima?"
        ],
        "Técnicas de relajación": [
            "Me gustaría aprender técnicas para relajarme",
            "¿Puedes guiarme en una meditación corta?",
            "¿Qué es la relajación muscular progresiva y cómo se practica?"
        ]
    }
    
    # Crear interfaz con Gradio
    with gr.Blocks(title="Asistente de Salud Mental") as demo:
        # Encabezado
        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown(
                    """# 🧠 Asistente Virtual de Salud Mental
                    
                    Este chatbot está diseñado para proporcionar soporte emocional y psicoeducación.
                    No reemplaza a profesionales de salud mental. Si experimentas una crisis o emergencia,
                    contacta con servicios de emergencia locales o líneas de crisis.
                    
                    **Recursos de emergencia:**
                    - Línea de Prevención del Suicidio: 024
                    - Emergencias: 112
                    """
                )
                
            with gr.Column(scale=1):
                # Intentar cargar logo si existe
                logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
                if os.path.exists(logo_path):
                    gr.Image(value=logo_path, show_label=False, container=False)
        
        # Selectores de categoría y modelo
        with gr.Row():
            with gr.Column(scale=2):
                # Categorías de salud mental
                topic = gr.Radio(
                    MENTAL_HEALTH_CATEGORIES,
                    label="Selecciona un tema",
                    info="Esto ayuda al asistente a contextualizar mejor tu consulta",
                    value="General"
                )
            
            with gr.Column(scale=1):
                # Modelo de GroqCloud a usar
                model_selector = gr.Dropdown(
                    available_models,
                    label="Modelo de IA",
                    info="Modelos más grandes dan mejores resultados pero pueden ser más lentos",
                    value=available_models[0] if available_models else None
                )
        
        # Interfaz de chat
        chatbot = gr.Chatbot(height=500, show_label=False)
        
        with gr.Row():
            with gr.Column(scale=8):
                msg = gr.Textbox(
                    label="Escribe tu mensaje aquí", 
                    placeholder="¿Cómo puedo ayudarte hoy?",
                    show_label=False
                )
            
            with gr.Column(scale=1):
                submit_btn = gr.Button("Enviar", variant="primary")
        
        # Botones de acción
        with gr.Row():
            clear_btn = gr.Button("Nueva conversación")
            example_btn = gr.Button("Mostrar ejemplos")
        
        # Ejemplos de preguntas (en un Accordion para evitar problemas con Box)
        with gr.Accordion("Ejemplos de preguntas", open=False) as example_container:
            gr.Markdown("### Ejemplos de preguntas para esta categoría")
            
            # Botones de ejemplo todos en la misma fila
            with gr.Row():
                example_btns = []
                for i in range(3):  # Mostraremos 3 ejemplos por categoría
                    btn = gr.Button("Ejemplo", visible=True)
                    example_btns.append(btn)
        
        # Variable para controlar visibilidad (evitamos usar directly .visible)
        show_examples = gr.Checkbox(label="Mostrar ejemplos", value=False, visible=False)
        
        # Área para recursos
        with gr.Accordion("Recursos", open=False):
            resources_md = gr.Markdown("""
            ### Recursos Generales
            - [OMS - Salud Mental](https://www.who.int/es/health-topics/mental-health)
            - [Teléfono de la Esperanza](https://telefonodelaesperanza.org/)
            """)
        
        # Configuración avanzada
        with gr.Accordion("Configuración avanzada", open=False):
            temperature = gr.Slider(0.1, 1.5, 0.7, 
                                   label="Temperatura", 
                                   info="Controla la creatividad de las respuestas")
            max_tokens = gr.Slider(64, 4096, 512, 
                                  label="Longitud máxima", 
                                  step=64)
        
        # Estado para almacenar datos entre interacciones
        state = gr.State({"category": "General", "history": []})
        
        # Función para procesar mensajes
        def process_message(message, history, state_data, model, temp, tokens):
            """
            Procesa el mensaje del usuario y genera una respuesta usando GroqCloud
            """
            if not message.strip():
                return "", history, state_data
            
            # Actualizar historial en el estado
            if "history" not in state_data:
                state_data["history"] = []
                
            state_data["history"].append({"role": "user", "content": message})
            
            # Detectar palabras clave de crisis
            crisis_detected, keywords = detect_crisis(message)
            if crisis_detected:
                # Generar respuesta de crisis
                crisis_response = get_crisis_response(keywords)
                history.append((message, crisis_response))
                state_data["history"].append({"role": "assistant", "content": crisis_response})
                return "", history, state_data
            
            # Obtener categoría
            category = state_data.get("category", "General")
            
            try:
                # Crear cliente de GroqCloud
                groq = GroqClient()
                
                # Añadir mensaje de espera
                history.append((message, "Pensando..."))
                yield "", history, state_data
                
                # Generar respuesta
                response = groq.generate_mental_health_response(
                    message, 
                    category=category,
                    model_id=model,
                    temperature=temp,
                    max_tokens=int(tokens)
                )
                
                # Reemplazar el mensaje de espera con la respuesta real
                history[-1] = (message, response)
                state_data["history"].append({"role": "assistant", "content": response})
                
            except Exception as e:
                print(f"Error al generar respuesta: {e}")
                response = "Lo siento, estoy teniendo problemas para responder en este momento. Por favor, inténtalo de nuevo."
                # Reemplazar el mensaje de espera con el mensaje de error
                if len(history) > 0 and history[-1][0] == message:
                    history[-1] = (message, response)
                else:
                    history.append((message, response))
                state_data["history"].append({"role": "assistant", "content": response})
            
            return "", history, state_data
        
        # Función para actualizar la categoría
        def update_category(category, state_data):
            """Actualiza la categoría en el estado"""
            state_data["category"] = category
            
            # Actualizar recursos mostrados
            try:
                if isinstance(RESOURCES, dict) and category in RESOURCES:
                    category_resources = RESOURCES[category]
                    resources_text = f"### Recursos para {category}\n"
                    for resource in category_resources:
                        resources_text += f"- [{resource['name']}]({resource['url']})\n"
                    
                    # Añadir recursos generales si no estamos en esa categoría
                    if category != "General" and "General" in RESOURCES:
                        resources_text += f"\n### Recursos Generales\n"
                        for resource in RESOURCES["General"]:
                            resources_text += f"- [{resource['name']}]({resource['url']})\n"
                else:
                    resources_text = "### No hay recursos disponibles para esta categoría"
            except Exception as e:
                print(f"Error al actualizar recursos: {e}")
                resources_text = "### Error al cargar recursos"
                
            return state_data, resources_text
        
        # Función para actualizar la sugerencia de prompt
        def update_prompt_suggestion(category):
            """Devuelve una sugerencia de mensaje basada en la categoría"""
            prompts = {
                "General": "Hola, me gustaría conversar contigo.",
                "Ansiedad": "Últimamente me siento ansioso. ¿Podrías ayudarme?",
                "Depresión": "He estado sintiéndome sin energía y con poco interés en las cosas.",
                "Estrés": "El estrés me está afectando mucho últimamente.",
                "Relaciones": "Estoy teniendo dificultades en mis relaciones personales.",
                "Autoestima": "He notado que tengo pensamientos muy negativos sobre mí mismo.",
                "Técnicas de relajación": "Me gustaría aprender algunas técnicas para relajarme."
            }
            
            return prompts.get(category, f"Me gustaría hablar sobre {category.lower()}.")
        
        # Función para limpiar la conversación
        def clear_conversation():
            """Limpia la conversación y el estado"""
            return [], {"category": topic.value, "history": []}
        
        # Función para alternar ejemplos (cambiamos la implementación)
        def toggle_examples(value):
            """
            Alterna la visibilidad del contenedor de ejemplos
            
            Args:
                value: Valor actual del checkbox (ignorado)
                
            Returns:
                Nuevo valor para el checkbox y configuración para el accordion
            """
            return not show_examples.value, gr.Accordion.update(visible=not show_examples.value)
        
        # Función para actualizar ejemplos
        def update_examples(category):
            """
            Actualiza los textos de los botones de ejemplo según la categoría
            """
            category_examples = examples.get(category, examples["General"])
            # Asegurar que hay suficientes ejemplos
            while len(category_examples) < 3:
                category_examples.append("¿Cómo puedo mejorar mi bienestar emocional?")
            
            return [category_examples[0], category_examples[1], category_examples[2]]
        
        # Función para usar un ejemplo como mensaje
        def use_example(example_text):
            """Establece el texto del ejemplo como mensaje"""
            return example_text
        
        # Conectar eventos
        submit_btn.click(
            process_message, 
            [msg, chatbot, state, model_selector, temperature, max_tokens], 
            [msg, chatbot, state]
        )
        
        msg.submit(
            process_message, 
            [msg, chatbot, state, model_selector, temperature, max_tokens], 
            [msg, chatbot, state]
        )
        
        clear_btn.click(
            clear_conversation, 
            None, 
            [chatbot, state]
        )
        
        topic.change(
            update_category, 
            [topic, state], 
            [state, resources_md]
        )
        
        topic.change(
            update_prompt_suggestion, 
            [topic], 
            [msg]
        )
        
        # Conectar cambio de tema con actualización de ejemplos
        topic.change(
            update_examples,
            [topic],
            example_btns
        )
        
        # Arreglar la lógica de mostrar/ocultar ejemplos
        example_btn.click(
            toggle_examples,
            [show_examples],
            [show_examples, example_container]
        )
        
        # Conectar cada botón de ejemplo para establecer el mensaje
        for btn in example_btns:
            btn.click(
                use_example,
                [btn],
                [msg]
            )
        
    return demo

if __name__ == "__main__":
    # Prueba de la interfaz
    demo = create_mental_health_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)