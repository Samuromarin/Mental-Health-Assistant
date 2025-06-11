"""
Módulo de seguridad para detectar mensajes de crisis y manejarlos adecuadamente
"""

from typing import Tuple, List

def detect_crisis(message: str) -> Tuple[bool, List[str]]:
    from src.config.settings import CRISIS_KEYWORDS
    
    message_lower = message.lower()
    keywords_found = [word for word in CRISIS_KEYWORDS if word in message_lower]
    
    return bool(keywords_found), keywords_found

def get_crisis_response(keywords: List[str]) -> str:
    """
    Genera una respuesta de protocolo de crisis mejorada
    """
    from src.config.settings import EMERGENCY_NUMBERS
    
    # Detectar si es riesgo alto
    high_risk_words = ["suicidio", "matarme", "quitarme la vida", "quiero morir","autolesión", "cortarme", "hacerme daño", "morir", "acabar con todo"]
    is_high_risk = any(word in keywords for word in high_risk_words)
    
    if is_high_risk:
        response = """
🚨 **SITUACIÓN DE CRISIS DETECTADA**

He detectado que podrías estar en riesgo inmediato. Es MUY IMPORTANTE que busques ayuda AHORA:

📞 **CONTACTO INMEDIATO:**
- Emergencias: 112
- Línea Prevención Suicidio: 024 (24h, gratuita)

🆘 **Si estás en peligro, ve al hospital más cercano**
        """
    else:
        response = """
**Mensaje importante de seguridad**

He detectado contenido que indica que estás pasando por un momento muy difícil.
Es importante que sepas que hay ayuda disponible:
        """
    
    # Recursos comunes para ambos casos
    response += f"""

📞 **Recursos de ayuda:**
- Emergencias: {EMERGENCY_NUMBERS['general']}
- Línea Prevención Suicidio: {EMERGENCY_NUMBERS['suicide_prevention']} (24h)
- Salud Mental España: {EMERGENCY_NUMBERS['mental_health']}
- Teléfono ANAR (jóvenes): {EMERGENCY_NUMBERS['youth_phone']}
- Online: {EMERGENCY_NUMBERS['online_chat']}
"""
    
    if "gender_violence" in EMERGENCY_NUMBERS and any(word in keywords for word in ["violencia", "maltrato", "abusan"]):
        response += f"• Violencia de Género: {EMERGENCY_NUMBERS['gender_violence']}\n"
    
    response += """
Este asistente no está diseñado para manejar situaciones de crisis y no reemplaza 
la ayuda profesional. Si estás en peligro inmediato, contacta con los servicios 
de emergencia.

Tu vida tiene valor. No estás solo/a.
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