"""
Safety module to detect crisis messages and handle them appropriately
"""

from typing import Tuple, List

def detect_crisis(message: str) -> Tuple[bool, List[str]]:
    from src.config.settings import CRISIS_KEYWORDS
    
    message_lower = message.lower()
    keywords_found = [word for word in CRISIS_KEYWORDS if word in message_lower]
    
    return bool(keywords_found), keywords_found

def get_crisis_response(keywords: List[str]) -> str:
    """
    Generates a crisis protocol response
    """
    from src.config.settings import EMERGENCY_NUMBERS
    
    # Detect if it's high risk
    high_risk_words = ["suicide", "kill myself", "end my life", "want to die", "self-harm", "cut myself", "hurt myself", "die", "end it all"]
    is_high_risk = any(word in keywords for word in high_risk_words)
    
    if is_high_risk:
        response = """
🚨 **CRISIS SITUATION DETECTED**

I've detected that you might be at immediate risk. It's VERY IMPORTANT that you seek help NOW:

📞 **IMMEDIATE CONTACT:**
- Emergency Services: 112
- Suicide Prevention Line: 024 (24/7, free)

🆘 **If you're in danger, go to the nearest hospital**
        """
    else:
        response = """
**Important safety message**

I've detected content that indicates you're going through a very difficult time.
It's important that you know help is available:
        """
    
    # Common resources for both cases
    response += f"""

📞 **Help resources:**
- Emergency Services: {EMERGENCY_NUMBERS['general']}
- Suicide Prevention Line: {EMERGENCY_NUMBERS['suicide_prevention']} (24/7)
- Mental Health Spain: {EMERGENCY_NUMBERS['mental_health']}
- ANAR Phone (youth): {EMERGENCY_NUMBERS['youth_phone']}
- Online: {EMERGENCY_NUMBERS['online_chat']}
"""
    
    if "gender_violence" in EMERGENCY_NUMBERS and any(word in keywords for word in ["violence", "abuse", "mistreat"]):
        response += f"• Gender Violence: {EMERGENCY_NUMBERS['gender_violence']}\n"
    
    response += """
This assistant is not designed to handle crisis situations and does not replace 
professional help. If you are in immediate danger, contact emergency services.

Your life has value. You are not alone.
    """
    
    return response

def check_message_safety(message: str) -> Tuple[bool, str]:
    """
    Checks message safety to detect inappropriate content
    
    Args:
        message: Message to check
        
    Returns:
        Tuple with (is_safe, warning_message)
    """
    # List of words that might indicate inappropriate content not related to crisis
    inappropriate_keywords = [
        "hack", "hacker", "pornography", "steal", "pirate", 
        "crack", "illegal drugs", "impersonate", "identity theft"
    ]
    
    message_lower = message.lower()
    
    # Check inappropriate words
    for word in inappropriate_keywords:
        if word in message_lower:
            return False, "Your message seems to contain topics that are outside the scope of this mental health assistant. Please formulate your query focusing on emotional well-being and mental health topics."
    
    # If no problems detected
    return True, ""

if __name__ == "__main__":
    # Functionality tests
    test_messages = [
        "Hello, how are you?",
        "I can't take this situation anymore, I want to end it all",
        "Sometimes I think it would be better to kill myself",
        "I've been feeling very sad lately",
        "How can I hack someone's account?"
    ]
    
    for message in test_messages:
        print(f"\nMessage: {message}")
        
        # Crisis detection test
        crisis_detected, keywords = detect_crisis(message)
        print(f"Crisis detected?: {crisis_detected}")
        if crisis_detected:
            print(f"Keywords: {keywords}")
            print("Crisis response:")
            print(get_crisis_response(keywords))
        
        # General safety test
        is_safe, warning = check_message_safety(message)
        print(f"Safe message?: {is_safe}")
        if not is_safe:
            print(f"Warning: {warning}")