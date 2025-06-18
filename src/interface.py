"""
Interfaz de usuario mejorada con tonos naranja suaves para el asistente de salud mental
"""

import os
import sys
import gradio as gr
from typing import Dict, Any, List, Tuple, Union
import traceback
import time

# Añadir el directorio raíz al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.groq_client import GroqClient
from src.config.settings import MENTAL_HEALTH_CATEGORIES, RESOURCES, GROQ_MODELS
from src.utils.safety import detect_crisis, get_crisis_response

# CSS personalizado simplificado para mejor compatibilidad móvil
custom_css = """
/* Variables CSS para tonos naranja suaves */
:root {
    --primary-orange: #ff7b42;      
    --light-orange: #FF8F39;        
    --very-light-orange: #FFEDE0;   
    --orange-accent: #FFD4A3;       
    --warm-white: #FFF8F3;          
}

/* Estilo general del contenedor */
.gradio-container {
    background: linear-gradient(135deg, var(--warm-white) 0%, var(--very-light-orange) 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Encabezado principal */
.main-header {
    background: linear-gradient(90deg, var(--primary-orange) 0%, var(--light-orange) 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255, 140, 66, 0.2);
}

/* Botones de Gradio simplificados */
.gr-button {
    border-radius: 8px !important;
    font-weight: 500 !important;
}

.gr-button-primary {
    background: var(--primary-orange) !important;
    color: white !important;
    border: none !important;
}

.gr-button-secondary {
    background: var(--orange-accent) !important;
    border: 1px solid var(--light-orange) !important;
    color: #333 !important;
}

/* Input de texto */
.gr-textbox {
    border: 2px solid var(--orange-accent) !important;
    border-radius: 8px !important;
}

.gr-textbox:focus {
    border-color: var(--primary-orange) !important;
}

/* Radio buttons simplificados */
.gr-radio label {
    background: white !important;
    border: 2px solid var(--orange-accent) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 4px !important;
}

.gr-radio input:checked + label {
    background: var(--primary-orange) !important;
    color: white !important;
    border-color: var(--primary-orange) !important;
}

/* Responsive design mejorado */
@media (max-width: 768px) {
    .gradio-container {
        padding: 10px;
    }
    
    .main-header {
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .gr-button {
        font-size: 14px !important;
        padding: 10px !important;
        margin: 5px 2px !important;
    }
    
    .gr-radio label {
        font-size: 14px !important;
        padding: 10px !important;
        margin: 3px !important;
        display: block !important;
        width: 100% !important;
    }
}
"""

def create_mental_health_interface():
    """
    Crea la interfaz de usuario mejorada para el asistente de salud mental usando GroqCloud
    
    Returns:
        Objeto Gradio para lanzar la interfaz
    """
    
    # Crear cliente de GroqCloud
    try:
        client = GroqClient()
        available_models = client.get_available_models()
        print(f"✅ Modelos disponibles: {available_models}")
    except Exception as e:
        print(f"⚠️ Error al inicializar el cliente de GroqCloud: {e}")
        available_models = list(GROQ_MODELS.keys()) if GROQ_MODELS else ["meta-llama/llama-4-scout-17b-16e-instruct"]
    
    # Ejemplos de preguntas por categoría
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
    
    # Crear interfaz con Gradio usando CSS personalizado
    with gr.Blocks(
        title="🧠 Asistente de Salud Mental", 
        css=custom_css,
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="orange",
            neutral_hue="stone"
        )
    ) as demo:
        
        # Header y disclaimer combinados SIN espacio
        gr.HTML("""
        <div class="main-header fade-in" style="text-align: center; margin-bottom: 20px;">
            <h1 style="margin: 8px; font-size: 2.5em; font-weight: 900;">
                🧠 Asistente Virtual de Salud Mental
            </h1>
        </div>
        <div style="background: linear-gradient(135deg, #FFE5CC 0%, #FFD4A6 100%); 
                    border-left: 4px solid #FF8C42; 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin: 0 0 15px 0;
                    box-shadow: 0 2px 8px rgba(255, 140, 66, 0.1);">
            <p style="margin: 0; color: #5D4E37; font-weight: 500;">
                ⚠️ <strong>Importante:</strong> Este asistente proporciona apoyo emocional y psicoeducación, 
                pero no reemplaza la atención profesional. 
                Si experimentas una crisis, contacta inmediatamente:
            </p>
            <ul style="margin: 8px 0 0 20px; color: #5D4E37;">
                <li><strong>Emergencias:</strong> 112 </li>
                <li><strong>Línea de Prevención del Suicidio:</strong> 024</li>
            </ul>
        </div>
        """)
        
        # Selectores con diseño mejorado
        with gr.Row():
            with gr.Column(scale=2):
                topic = gr.Radio(
                    MENTAL_HEALTH_CATEGORIES,
                    label="🎯 Selecciona tu tema de interés",
                    info="Esto personaliza las respuestas según tus necesidades",
                    value="General",
                    elem_classes="radio-group"
                )
            
            with gr.Column(scale=1):
                model_selector = gr.Dropdown(
                    available_models,
                    label="🤖 Modelo de IA",
                    info="Modelos más grandes ofrecen respuestas más elaboradas",
                    value=available_models[0] if available_models else None,
                    elem_classes="dropdown-container"
                )
        
        # Status box (oculto por defecto)
        status_box = gr.Textbox(label="Estado", visible=False)
        
        # Área de chat con estilo mejorado
        with gr.Row():
            chatbot = gr.Chatbot(
                height=700, 
                show_label=False,
                elem_classes="chat-container",
                avatar_images=(None,None)
            )
        
        # Input y botón de envío
        with gr.Row():
            with gr.Column(scale=8):
                msg = gr.Textbox(
                    label="💬 Escribe tu mensaje aquí", 
                    placeholder="¿Cómo puedo ayudarte hoy? Siéntete libre de compartir lo que tienes en mente...",
                    show_label=False,
                    elem_classes="message-input"
                )
            
            with gr.Column(scale=1):
                submit_btn = gr.Button(
                    "Enviar 📤", 
                    variant="primary",
                    elem_classes="primary-button"
                )
        
        # Botones de acción con estilo mejorado
        with gr.Row():
            clear_btn = gr.Button(
                "🔄 Nueva conversación", 
                elem_classes="secondary-button"
            )
            example_btn = gr.Button(
                "💡 Ver ejemplos", 
                elem_classes="secondary-button"
            )
        
        # Ejemplos de preguntas
        with gr.Accordion("💡 Ejemplos de preguntas", open=False, visible=False) as example_container:
            
            with gr.Row():
                example_btns = []
                for i in range(3):
                    btn = gr.Button(
                        "Ejemplo", 
                        visible=True,
                        elem_classes="secondary-button"
                    )
                    example_btns.append(btn)
        
        # Variable para controlar visibilidad
        show_examples = gr.Checkbox(label="Mostrar ejemplos", value=False, visible=False)
        
        # Recursos con diseño mejorado
        with gr.Accordion("📚 Recursos adicionales", open=False, elem_classes="accordion"):
            resources_md = gr.Markdown("""
            ### 🌟 Recursos Generales
            - [🌍 OMS - Salud Mental](https://www.who.int/es/health-topics/mental-health)
            - [📞 Teléfono de la Esperanza](https://telefonodelaesperanza.org/)
            - [🤝 Confederación Salud Mental España](https://consaludmental.org/)
            """)
        
        # Configuración avanzada con mejor diseño
        with gr.Accordion("⚙️ Configuración avanzada", open=False, elem_classes="accordion"):
            with gr.Row():
                temperature = gr.Slider(
                    0.1, 1.5, 0.7, 
                    label="🌡️ Creatividad (Temperatura)", 
                    info="Valores más altos = respuestas más creativas",
                    elem_classes="slider-container"
                )
                max_tokens = gr.Slider(
                    64, 4096, 512, 
                    label="📏 Longitud máxima", 
                    step=64,
                    info="Máximo de palabras en la respuesta",
                    elem_classes="slider-container"
                )
                timeout = gr.Slider(
                    5, 120, 60,
                    label="⏱️ Tiempo máximo (segundos)",
                    info="Tiempo máximo para generar respuesta",
                    elem_classes="slider-container"
                )
        
        # Estado para almacenar datos entre interacciones
        state = gr.State({"category": "General", "history": []})
        
        # [Aquí van todas las funciones del código original sin cambios]
        # Función para procesar mensajes
        def process_message(message, history, state_data, model, temp, tokens, max_timeout):
            """Procesa el mensaje del usuario y genera una respuesta usando GroqCloud"""
            if not message.strip():
                return "", history, state_data, gr.update(visible=False, value="")
            
            # Actualizar historial en el estado
            if "history" not in state_data:
                state_data["history"] = []
                
            state_data["history"].append({"role": "user", "content": message})
            
            # Detectar palabras clave de crisis
            crisis_detected, keywords = detect_crisis(message)
            if crisis_detected:
                crisis_response = get_crisis_response(keywords)
                history.append((message, crisis_response))
                state_data["history"].append({"role": "assistant", "content": crisis_response})
                return "", history, state_data, gr.update(visible=False, value="")
            
            # Obtener categoría
            category = state_data.get("category", "General")
            
            try:
                groq = GroqClient()
                history.append((message, "🤔 Pensando..."))
                
                start_time = time.time()
                
                try:
                    response = groq.generate_mental_health_response(
                        message, 
                        category=category,
                        model_id=model,
                        temperature=temp,
                        max_tokens=int(tokens)
                    )
                    
                    history[-1] = (message, response)
                    state_data["history"].append({"role": "assistant", "content": response})
                    
                    return "", history, state_data, gr.update(visible=False, value="")
                    
                except Exception as e:
                    print(f"❌ Error al generar respuesta: {e}")
                    print(traceback.format_exc())
                    
                    error_message = "Lo siento, ha ocurrido un error al procesar tu solicitud. Por favor, inténtalo de nuevo."
                    history[-1] = (message, error_message)
                    
                    return "", history, state_data, gr.update(visible=True, value=f"Error: {str(e)}")
                
            except Exception as e:
                print(f"❌ Error al crear cliente o procesar mensaje: {e}")
                print(traceback.format_exc())
                
                error_message = "Lo siento, ha ocurrido un error al procesar tu solicitud. Por favor, inténtalo de nuevo."
                history.append((message, error_message))
                
                return "", history, state_data, gr.update(visible=True, value=f"Error: {str(e)}")
        
        # Función para actualizar la categoría
        def update_category(category, state_data):
            """Actualiza la categoría en el estado"""
            state_data["category"] = category
            
            try:
                if isinstance(RESOURCES, dict) and category in RESOURCES:
                    category_resources = RESOURCES[category]
                    resources_text = f"### 🌟 Recursos para {category}\n"
                    for resource in category_resources:
                        resources_text += f"- [📖 {resource['name']}]({resource['url']})\n"
                    
                    if category != "General" and "General" in RESOURCES:
                        resources_text += f"\n### 🌍 Recursos Generales\n"
                        for resource in RESOURCES["General"]:
                            resources_text += f"- [📖 {resource['name']}]({resource['url']})\n"
                else:
                    resources_text = "### ⚠️ No hay recursos disponibles para esta categoría"
            except Exception as e:
                print(f"Error al actualizar recursos: {e}")
                resources_text = "### ❌ Error al cargar recursos"
                
            return state_data, resources_text
        
        # Función para actualizar la sugerencia de prompt
        def update_prompt_suggestion(category):
            """Devuelve una sugerencia de mensaje basada en la categoría"""
            prompts = {
                "General": "Hola, me gustaría conversar contigo sobre mi bienestar emocional.",
                "Ansiedad": "Últimamente me siento ansioso y necesito ayuda para manejarlo.",
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
            return [], {"category": topic.value, "history": []}, gr.update(visible=False, value="")
        
        # Función para alternar ejemplos
        def toggle_examples(value):
            """Alterna la visibilidad del contenedor de ejemplos"""
            return not show_examples.value, gr.update(visible=not show_examples.value)
        
        # Función para actualizar ejemplos
        def update_examples(category):
            """Actualiza los textos de los botones de ejemplo según la categoría"""
            category_examples = examples.get(category, examples["General"])
            while len(category_examples) < 3:
                category_examples.append("¿Cómo puedo mejorar mi bienestar emocional?")
            
            return [category_examples[0], category_examples[1], category_examples[2]]
        
        # Función para usar un ejemplo como mensaje
        def use_example(example_text):
            """Establece el texto del ejemplo como mensaje"""
            return example_text
        
        # Conectar eventos (sin cambios en la funcionalidad)
        submit_btn.click(
            process_message, 
            [msg, chatbot, state, model_selector, temperature, max_tokens, timeout], 
            [msg, chatbot, state, status_box]
        )
        
        msg.submit(
            process_message, 
            [msg, chatbot, state, model_selector, temperature, max_tokens, timeout], 
            [msg, chatbot, state, status_box]
        )
        
        clear_btn.click(
            clear_conversation, 
            None, 
            [chatbot, state, status_box]
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
        
        topic.change(
            update_examples,
            [topic],
            example_btns
        )
        
        example_btn.click(
            toggle_examples,
            [show_examples],
            [show_examples, example_container]
        )
        
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