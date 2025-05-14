from src.config.settings import VICUNA_PROMPT_TEMPLATE, MENTAL_HEALTH_CATEGORIES

def format_prompt_for_vicuna(message, category="General"):
    """
    Formatea el mensaje del usuario para el modelo Vicuna,
    optimizando para el contexto de salud mental
    
    Args:
        message (str): Mensaje del usuario
        category (str): Categoría de salud mental seleccionada
    
    Returns:
        str: Prompt formateado para Vicuna
    """
    # Añadir instrucciones específicas basadas en la categoría
    category_instructions = get_category_specific_instructions(category)
    
    # Si el usuario seleccionó una categoría específica, la incluimos en el contexto
    if category != "General":
        context_message = f"{category_instructions}\n\nEl usuario quiere hablar sobre temas relacionados con {category.lower()}:\n{message}"
    else:
        context_message = f"{message}"
    
    return VICUNA_PROMPT_TEMPLATE.format(message=context_message)

def get_category_specific_instructions(category):
    """
    Devuelve instrucciones específicas según la categoría de salud mental
    
    Args:
        category (str): Categoría de salud mental
    
    Returns:
        str: Instrucciones específicas para esa categoría
    """
    instructions = {
        "Ansiedad": """
        Para este tema de ansiedad:
        - Utiliza un tono calmado y valida los sentimientos del usuario.
        - Enseña técnicas de respiración y relajación cuando sea apropiado.
        - Explora desencadenantes específicos con preguntas abiertas.
        - Normaliza las experiencias de ansiedad sin minimizarlas.
        - Proporciona información precisa sobre la ansiedad y sus síntomas.
        - Sugiere estrategias basadas en evidencia (respiración diafragmática, mindfulness, exposición gradual).
        - Anima a buscar ayuda profesional para un tratamiento más estructurado.
        """,
        
        "Depresión": """
        Para este tema de depresión:
        - Utiliza un enfoque de escucha empática y valida sus experiencias sin minimizarlas.
        - Explora patrones de pensamiento con tacto y pregunta sobre actividades que antes disfrutaban.
        - Mantén un tono esperanzador pero realista.
        - Valida sus sentimientos sin perpetuar la desesperanza.
        - Pregunta sobre pensamientos suicidas si es apropiado, recomendando ayuda inmediata si es necesario.
        - Explora gradualmente elementos como patrones de sueño, apetito y energía.
        - Sugiere pequeñas actividades significativas que podrían ser manejables.
        """,
        
        "Estrés": """
        Para este tema de manejo del estrés:
        - Ayuda a identificar fuentes específicas de estrés en su vida.
        - Explora estrategias de afrontamiento existentes y su efectividad.
        - Sugiere técnicas de mindfulness cuando sea apropiado.
        - Enfatiza la importancia del autocuidado y los límites saludables.
        - Normaliza el estrés como una respuesta humana natural.
        - Distingue entre estrés agudo y crónico si es relevante.
        - Explora cómo el estrés afecta diferentes áreas de su vida.
        """,
        
        "Relaciones": """
        Para este tema de relaciones:
        - Escucha sin juzgar y evita tomar partido.
        - Ayuda a explorar patrones de comunicación en sus relaciones.
        - Anima a considerar diferentes perspectivas.
        - Explora cómo las dinámicas actuales pueden relacionarse con experiencias pasadas.
        - Enfatiza la importancia de límites saludables y comunicación clara.
        - Formula preguntas que promuevan la reflexión sobre necesidades y valores personales.
        - Reconoce cuando pueda haber situaciones de abuso y sugiere recursos apropiados.
        """,
        
        "Autoestima": """
        Para este tema de autoestima:
        - Ayuda a identificar fortalezas personales y logros pasados.
        - Cuestiona pensamientos autocríticos con gentileza.
        - Fomenta una autoimagen más compasiva y realista.
        - Explora el origen de creencias negativas sobre sí mismo.
        - Distingue entre autocrítica constructiva y destructiva.
        - Promueve la autocompasión como alternativa a la autocrítica.
        - Sugiere prácticas como escribir diarios de gratitud o afirmaciones realistas.
        """,
        
        "Técnicas de relajación": """
        Para este tema de técnicas de relajación:
        - Guía en respiración profunda, relajación muscular progresiva, visualización o mindfulness.
        - Ofrece instrucciones paso a paso cuando sea apropiado.
        - Adapta las técnicas al contexto y preferencias específicas del usuario.
        - Explica brevemente la base científica de las técnicas sugeridas.
        - Anima a practicar regularmente, comenzando con sesiones cortas.
        - Pregunta sobre experiencias previas con técnicas de relajación.
        - Ofrece alternativas si una técnica particular no resuena con el usuario.
        """
    }
    
    # Instrucciones generales para cualquier categoría
    general_instructions = """
    Recuerda mantener siempre una actitud empática, validar sentimientos, usar preguntas abiertas,
    ofrecer recursos educativos apropiados, y animar a buscar ayuda profesional cuando sea necesario.
    No diagnostiques ni reemplaces la atención profesional de salud mental.
    """
    
    # Combinar instrucciones específicas con las generales
    specific_instructions = instructions.get(category, "")
    if specific_instructions:
        return f"{specific_instructions}\n\n{general_instructions}"
    else:
        return general_instructions

def create_system_message(category="General"):
    """
    Crea un mensaje de sistema para modelos compatibles con ChatCompletion
    
    Args:
        category (str): Categoría de salud mental
    
    Returns:
        str: Mensaje de sistema formateado
    """
    base_system_message = """Eres un asistente de salud mental empático y respetuoso que proporciona apoyo emocional, 
    escucha activa y psicoeducación. No proporcionas diagnósticos clínicos ni reemplazas a profesionales de la salud mental. 
    Tu enfoque es personalizado, basado en evidencia científica, y ofreces respuestas que promueven el bienestar psicológico."""
    
    # Añadir instrucciones específicas según la categoría
    category_instructions = get_category_specific_instructions(category)
    
    return f"{base_system_message}\n\n{category_instructions}"

def get_example_prompts():
    """
    Devuelve ejemplos de prompts para cada categoría
    
    Returns:
        dict: Diccionario con ejemplos de prompts por categoría
    """
    return {
        "General": [
            "¿Podrías darme algunos consejos para mejorar mi bienestar emocional?",
            "Últimamente no me siento bien emocionalmente, ¿qué puedo hacer?",
            "¿Qué recursos recomiendas para aprender más sobre salud mental?"
        ],
        "Ansiedad": [
            "Me siento ansioso todo el tiempo, ¿qué puedo hacer?",
            "¿Cómo puedo manejar los ataques de pánico?",
            "Tengo miedo constante a que algo malo va a pasar"
        ],
        "Depresión": [
            "No tengo motivación para hacer nada últimamente",
            "¿Cómo puedo lidiar con pensamientos negativos recurrentes?",
            "Me siento triste sin razón aparente"
        ],
        "Estrés": [
            "El trabajo me está causando mucho estrés, ¿cómo puedo manejarlo?",
            "Siento que estoy siempre bajo presión",
            "Necesito técnicas para relajarme después de un día difícil"
        ],
        "Relaciones": [
            "Tengo problemas para comunicarme con mi pareja",
            "¿Cómo puedo establecer límites saludables con mi familia?",
            "Me cuesta mucho confiar en los demás"
        ],
        "Autoestima": [
            "Siempre me comparo con los demás y me siento inferior",
            "¿Cómo puedo mejorar mi autoimagen?",
            "Siento que no soy lo suficientemente bueno en nada"
        ],
        "Técnicas de relajación": [
            "Necesito técnicas para calmarme rápidamente",
            "¿Podrías guiarme en una meditación corta?",
            "¿Qué ejercicios de respiración recomiendas para la ansiedad?"
        ]
    }