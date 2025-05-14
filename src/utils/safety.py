"""
Módulo de seguridad para detectar mensajes de crisis y manejarlos adecuadamente
"""

from typing import Tuple, List

def detect_crisis(message: str) -> Tuple[bool, List[str]]:
    """
    Detecta palabras clave de crisis en el mensaje del usuario
    
    Args:
        message: Mensaje del usuario
    
    Returns:
        Tupla con (crisis_detectada, palabras_clave_encontradas)
    """
    from src.config.settings import CRISIS_KEYWORDS
    
    message_lower = message.lower()
    keywords_found = [word for word in CRISIS_KEYWORDS if word in message_lower]
    
    return bool(keywords_found), keywords_found

def get_crisis_response(keywords: List[str]) -> str:
    """
    Genera una respuesta de protocolo de crisis basada en las palabras clave detectadas
    
    Args:
        keywords: Lista de palabras clave detectadas
    
    Returns:
        Mensaje de respuesta a la crisis
    """
    from src.config.settings import EMERGENCY_NUMBERS
    
    # Clasificar tipo de crisis para una respuesta más específica
    is_suicide_risk = any(word in keywords for word in ["suicidio", "matarme", "quitarme la vida", "no quiero vivir"])
    
    response = """
    **Mensaje importante de seguridad**
    
    He detectado contenido en tu mensaje que puede indicar que estás pasando por un momento difícil.
    """
    
    # Mensaje específico según tipo de crisis
    if is_suicide_risk:
        response += """
    Es muy importante que sepas que hay ayuda disponible inmediatamente para ti. 
    Tus sentimientos son válidos, pero hay profesionales preparados para ayudarte 
    a superarlos y encontrar otras perspectivas.
        """
    else:
        response += """
    Es importante que sepas que hay ayuda disponible y que no estás solo/a 
    en lo que estás experimentando.
        """
    
    # Incluir recursos de ayuda
    response += f"""
    Recursos de ayuda inmediata:
    
    - Teléfono de Emergencias: {EMERGENCY_NUMBERS['general']}
    - Línea de Prevención del Suicidio: {EMERGENCY_NUMBERS['suicide_prevention']}
    """
    
    if "gender_violence" in EMERGENCY_NUMBERS and any(word in keywords for word in ["violencia", "maltrato", "abusan"]):
        response += f"- Línea contra la Violencia de Género: {EMERGENCY_NUMBERS['gender_violence']}\n"
    
    response += """
    Este asistente no está diseñado para manejar situaciones de crisis y no reemplaza 
    la ayuda profesional. Si estás en peligro inmediato, por favor contacta con los 
    servicios de emergencia.
    
    Si quieres seguir conversando sobre temas generales de salud mental una vez 
    hayas buscado apoyo profesional, estaré aquí para ayudarte.
    """
    
    return response

def check_message_safety(message: str) -> Tuple[bool, str]:
    """
    Comprueba la seguridad del mensaje para detectar contenido inapropiado
    
    Args:
        message: Mensaje a comprobar
        
    Returns:
        Tupla con (es_seguro, mensaje_de_advertencia)
    """
    # Lista de palabras que podrían indicar contenido inapropiado no relacionado con crisis
    inappropriate_keywords = [
        "hackear", "hacker", "pornografía", "pornografia", "robar", "piratear", 
        "crackear", "crack", "drogas ilegales", "suplantar", "identidad"
    ]
    
    message_lower = message.lower()
    
    # Comprobar palabras inapropiadas
    for word in inappropriate_keywords:
        if word in message_lower:
            return False, "Tu mensaje parece contener temas que están fuera del ámbito de este asistente de salud mental. Por favor, formula tu consulta enfocándola en temas de bienestar emocional y salud mental."
    
    # Si no se detectan problemas
    return True, ""

if __name__ == "__main__":
    # Pruebas de funcionamiento
    test_messages = [
        "Hola, ¿cómo estás?",
        "No puedo más con esta situación, quiero acabar con todo",
        "A veces pienso que sería mejor quitarme la vida",
        "Me siento muy triste últimamente",
        "¿Cómo puedo hackear la cuenta de alguien?"
    ]
    
    for message in test_messages:
        print(f"\nMensaje: {message}")
        
        # Prueba de detección de crisis
        crisis_detected, keywords = detect_crisis(message)
        print(f"¿Crisis detectada?: {crisis_detected}")
        if crisis_detected:
            print(f"Palabras clave: {keywords}")
            print("Respuesta de crisis:")
            print(get_crisis_response(keywords))
        
        # Prueba de seguridad general
        is_safe, warning = check_message_safety(message)
        print(f"¿Mensaje seguro?: {is_safe}")
        if not is_safe:
            print(f"Advertencia: {warning}")