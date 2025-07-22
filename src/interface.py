"""
Mental Health Assistant - User Interface

Web-based interface using Gradio for therapeutic AI interactions.
Provides accessible design optimized for mental health support contexts.
"""

import os
import sys
import gradio as gr
from typing import Dict, Any, List, Tuple, Union
import traceback
import time

# Add root directory to path for relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.groq_client import GroqClient
from src.config.settings import MENTAL_HEALTH_CATEGORIES, RESOURCES, GROQ_MODELS
from src.utils.safety import detect_crisis, get_crisis_response

# Custom CSS
custom_css = """
:root {
    --primary-orange: #ff7b42;      
    --light-orange: #FF8F39;        
    --very-light-orange: #FFEDE0;   
    --orange-accent: #FFD4A3;       
    --warm-white: #FFF8F3;          
}

.gradio-container {
    background: linear-gradient(135deg, var(--warm-white) 0%, var(--very-light-orange) 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.main-header {
    background: linear-gradient(90deg, var(--primary-orange) 0%, var(--light-orange) 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(255, 140, 66, 0.2);
}

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

.gr-textbox {
    border: 2px solid var(--orange-accent) !important;
    border-radius: 8px !important;
}

.gr-textbox:focus {
    border-color: var(--primary-orange) !important;
}

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

@media (max-width: 768px) {
    .gradio-container {
        padding: 10px;
    }
    
    .main-header {
        padding: 15px;
        margin-bottom: 15px;
    }
    
    .gr-button {
        font-size: 20x !important;
        padding: 10px !important;
        margin: 5px 2px !important;
    }
    
    .gr-radio label {
        font-size: 20px !important;
        padding: 10px !important;
        margin: 3px !important;
        display: block !important;
        width: 100% !important;
    }
}
"""

def create_mental_health_interface():
    """
    Creates the user interface
    
    Returns:
        Gradio object to launch the interface
    """
    
    # Create GroqCloud client
    try:
        client = GroqClient()
        available_models = client.get_available_models()
    except Exception as e:
        print(f"⚠️ Error initializing GroqCloud client: {e}")
        available_models = list(GROQ_MODELS.keys()) if GROQ_MODELS else ["meta-llama/llama-4-scout-17b-16e-instruct"]
    
    # Example questions by category
    examples = {
        "General": [
            "Could you give me some tips to improve my emotional well-being?",
            "What daily habits are good for mental health?",
            "How can I know if I need professional help?"
        ],
        "Anxiety": [
            "I've been feeling anxious lately. Could you help me?",
            "How can I manage panic attacks?",
            "What breathing techniques are good for anxiety?"
        ],
        "Depression": [
            "I've been feeling really sad and empty lately. I have no motivation to do anything",
            "How can I deal with recurring negative thoughts?",
            "I have trouble getting up in the mornings. What can I do?"
        ],
        "Stress": [
            "I've been feeling really stressed and overwhelmed lately. Can you help me?",
            "I need techniques to relax after a difficult day",
            "What quick exercises would help me reduce stress?"
        ],
        "Relationships": [
            "I have problems communicating with my partner",
            "How can I establish healthy boundaries with my family?",
            "I have trouble trusting others after a bad experience"
        ],
        "Self-esteem": [
            "I always compare myself to others and feel inferior",
            "How can I improve my self-image?",
            "What exercises can I do to strengthen my self-esteem?"
        ]
    }
    
    # Create interface with Gradio using custom CSS
    with gr.Blocks(
        title="🧠 Mental Health Assistant", 
        css=custom_css,
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="orange",
            neutral_hue="stone"
        )
    ) as demo:
        
        # Header and disclaimer
        gr.HTML("""
        <div style="max-width: 2000px; margin: 0 auto; width: 100%;">
            <div class="main-header fade-in" style="text-align: center; margin-bottom: 10px;">
                <h1 style="margin: 10px; font-size: 2.5em; font-weight: 1000;">
                   🧠 Virtual Mental Health Assistant
                </h1>
            </div>
            <div style="background: linear-gradient(135deg, #FFE5CC 0%, #FFD4A6 100%); 
                    border-left: 4px solid #FF8C42; 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin: 0 0 15px 0;
                    box-shadow: 0 2px 8px rgba(255, 140, 66, 0.1);">
                <p style="margin: 0; color: #5D4E37; font-weight: 500;">
                   ⚠️ <strong>Important:</strong> This assistant provides emotional support and psychoeducation, 
                   but does not replace professional care. 
                   If you experience a crisis, contact immediately:
                </p>
                <ul style="margin: 8px 0 0 20px; color: #5D4E37;">
                    <li><strong>Emergencies:</strong> 112 </li>
                    <li><strong>Suicide Prevention Line:</strong> 024</li>
                </ul>
            </div>
        </div>
        """)
        
        # Category and model selectors
        with gr.Row():
            with gr.Column(scale=2):
                topic = gr.Radio(
                    MENTAL_HEALTH_CATEGORIES,
                    label="🎯 Select your topic of interest",
                    info="This personalizes responses according to your needs",
                    value="General",
                    elem_classes="radio-group"
                )
            
            with gr.Column(scale=1):
                model_selector = gr.Dropdown(
                    available_models,
                    label="🤖 AI Model",
                    info="Larger models offer more elaborate responses",
                    value=available_models[0] if available_models else None,
                    elem_classes="dropdown-container"
                )
        
        # Status box
        status_box = gr.Textbox(label="Status", visible=False)
        
        # Main chat interface
        with gr.Row():
            chatbot = gr.Chatbot(
                height=600, 
                show_label=False,
                elem_classes="chat-container",
                avatar_images=(None,None),
                type="messages"  # Fix Gradio warning
            )
        
        # Message input and controls
        with gr.Row():
            with gr.Column(scale=8):
                msg = gr.Textbox(
                    label="💬 Write your message here", 
                    placeholder="How can I help you today? Feel free to share what's on your mind...",
                    show_label=False,
                    elem_classes="message-input"
                )
            
            with gr.Column(scale=1):
                submit_btn = gr.Button(
                    "Send 📤", 
                    variant="primary",
                    elem_classes="primary-button"
                )
        
        # Action buttons
        with gr.Row():
            clear_btn = gr.Button(
                "🔄 New conversation", 
                elem_classes="secondary-button"
            )
            example_btn = gr.Button(
                "💡 View examples", 
                elem_classes="secondary-button"
            )
        
        # Question examples
        with gr.Accordion("💡 Example questions", open=False, visible=False) as example_container:
            
            with gr.Row():
                example_btns = []
                general_examples = examples.get("General", [
                    "Could you give me some tips to improve my emotional well-being?",
                    "What daily habits are good for mental health?", 
                    "How can I know if I need professional help?"
                ])

                
                for i in range(3):
                    btn = gr.Button(
                        "Example", 
                        visible=True,
                        elem_classes="secondary-button"
                    )
                    example_btns.append(btn)
        
        # Variable to control visibility
        show_examples = gr.Checkbox(label="Show examples", value=False, visible=False)
        
        # Resources
        with gr.Accordion("📚 Additional resources", open=False, elem_classes="accordion"):
            resources_md = gr.Markdown("""
            ### 🌟 General Resources
            - [🌍 WHO - Mental Health](https://www.who.int/es/health-topics/mental-health)
            - [📞 Teléfono de la Esperanza](https://telefonodelaesperanza.org/)
            - [🤝 Spanish Mental Health Confederation](https://consaludmental.org/)
            """)
        
        # Advanced configuration
        with gr.Accordion("⚙️ Advanced configuration", open=False, elem_classes="accordion"):
            with gr.Row():
                temperature = gr.Slider(
                    0.1, 1.5, 0.7, 
                    label="🌡️ Creativity (Temperature)", 
                    info="Higher values = more creative responses",
                    elem_classes="slider-container"
                )
                max_tokens = gr.Slider(
                    64, 4096, 512, 
                    label="📏 Maximum length", 
                    step=64,
                    info="Maximum words in the response",
                    elem_classes="slider-container"
                )
                timeout = gr.Slider(
                    5, 120, 10,
                    label="⏱️ Maximum time (seconds)",
                    info="Maximum time to generate response",
                    elem_classes="slider-container"
                )
        
        # State to store data between interactions
        state = gr.State({"category": "General", "history": []})
        
        # Function to process messages
        def process_message(message, history, state_data, model, temp, tokens, max_timeout):
            """Processes user message and generates response using GroqCloud"""
            if not message.strip():
                return "", history, state_data, gr.update(visible=False, value="")
            
            # Update history in state
            if "history" not in state_data:
                state_data["history"] = []
                
            state_data["history"].append({"role": "user", "content": message})
            
            # Detect crisis keywords
            crisis_detected, keywords = detect_crisis(message)
            if crisis_detected:
                crisis_response = get_crisis_response(keywords)
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": crisis_response})
                state_data["history"].append({"role": "assistant", "content": crisis_response})
                return "", history, state_data, gr.update(visible=False, value="")
            
            # Get category
            category = state_data.get("category", "General")
            
            try:
                groq = GroqClient()
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": "🤔 Thinking..."})
                
                start_time = time.time()
                
                try:
                    # Pass conversation history to maintain context
                    response = groq.generate_mental_health_response(
                        message, 
                        category=category,
                        model_id=model,
                        temperature=temp,
                        max_tokens=int(tokens),
                        conversation_history=state_data["history"][:-1]  # Exclude current message
                    )
                    
                    history[-1] = {"role": "assistant", "content": response}
                    state_data["history"].append({"role": "assistant", "content": response})
                    
                    return "", history, state_data, gr.update(visible=False, value="")
                    
                except Exception as e:
                    print(f"❌ Error generating response: {e}")
                    print(traceback.format_exc())
                    
                    error_message = "I'm sorry, an error occurred while processing your request. Please try again."
                    history[-1] = {"role": "assistant", "content": error_message}
                    
                    return "", history, state_data, gr.update(visible=True, value=f"Error: {str(e)}")
                
            except Exception as e:
                print(f"❌ Error creating client or processing message: {e}")
                print(traceback.format_exc())
                
                error_message = "I'm sorry, an error occurred while processing your request. Please try again."
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": error_message})
                
                return "", history, state_data, gr.update(visible=True, value=f"Error: {str(e)}")
        
        # Function to update category
        def update_category(category, state_data):
            """Updates category in state"""
            state_data["category"] = category
            
            try:
                if isinstance(RESOURCES, dict) and category in RESOURCES:
                    category_resources = RESOURCES[category]
                    resources_text = f"### 🌟 Resources for {category}\n"
                    for resource in category_resources:
                        resources_text += f"- [📖 {resource['name']}]({resource['url']})\n"
                else:
                    resources_text = "### ⚠️ No resources available for this category"
            except Exception as e:
                print(f"Error updating resources: {e}")
                resources_text = "### ❌ Error loading resources"
                
            return state_data, resources_text
        
        # Function to clear conversation
        def clear_conversation():
            """Clears conversation and state"""
            return [], {"category": topic.value, "history": []}, gr.update(visible=False, value="")
        
        # Function to toggle examples
        def toggle_examples(value):
            """Toggles visibility of examples container"""
            return not show_examples.value, gr.update(visible=not show_examples.value)
        
        # Function to update examples
        def update_examples(category):
            """Updates example button texts according to category"""
            category_examples = examples.get(category, examples["General"])
            while len(category_examples) < 3:
                category_examples.append("How can I improve my emotional well-being?")
            
            return [gr.update(value=category_examples[0]), gr.update(value=category_examples[1]), gr.update(value=category_examples[2])]
        
        # Function to use an example as message
        def use_example(example_text):
            """Sets example text as message"""
            return example_text
        
        # Connect events (no changes in functionality)
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

        demo.load(
            lambda: update_examples("General"),
            outputs=example_btns
        )
    return demo

if __name__ == "__main__":
    # Interface test
    demo = create_mental_health_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)