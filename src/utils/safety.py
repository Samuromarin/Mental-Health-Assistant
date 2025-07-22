"""
Safety Module 

Crisis detection and emergency response system for user safety.
Implements keyword-based risk assessment and intervention protocols.
"""


from typing import Tuple, List

import re

def detect_crisis(message: str) -> Tuple[bool, List[str]]:
    from src.config.settings import CRISIS_KEYWORDS
    
    message_lower = message.lower()
    
    # Search for complete words instead of substrings
    keywords_found = []
    for keyword in CRISIS_KEYWORDS:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, message_lower):
            keywords_found.append(keyword)
    
    return bool(keywords_found), keywords_found

def get_crisis_response(keywords: List[str]) -> str:
    """
    Generates a crisis protocol response
    """
    from src.config.settings import EMERGENCY_NUMBERS
    
    # Analyze severity level for appropriate response
    high_risk_words = ["suicide", "kill myself", "I can't take it anymore", "end my life", "want to die", "self-harm", "cut myself", "hurt myself", "die", "end it all"]
    is_high_risk = any(word in keywords for word in high_risk_words)
    
    if is_high_risk:
        response = """
🚨 **CRISIS SITUATION DETECTED** 🚨

I've detected that you might be at immediate risk. It's VERY IMPORTANT that you seek help NOW:

📞 **IMMEDIATE CONTACT:**
- Emergency Services: 112
- Suicide Prevention Line: 024 (24/7, free)

🆘 **If you're in danger, go to the nearest hospital**
        """
        # Final message for HIGH RISK
        final_message = """
This assistant is not designed to handle crisis situations and does not replace 
professional help. If you are in immediate danger, contact emergency services.

Your life has value. You are not alone. 🧡
        """
    else:
        response = """
⚠️ **Important safety message** ⚠️

I notice you're going through some challenges right now, and I want you to know that support is here for you. 
You don't have to face this alone:
        """
        # Final message for MODERATE RISK
        final_message = """
Remember, reaching out for help is a sign of strength. 
These resources are here to provide you with professional guidance and support.

You matter, and things can get better. 🧡
        """
    
    # Common resources for both cases
    response += f"""

🤝 **Help resources:**
- Mental Health Spain: {EMERGENCY_NUMBERS['mental_health']}
- ANAR Phone (youth): {EMERGENCY_NUMBERS['youth_phone']}
- Online: {EMERGENCY_NUMBERS['online_chat']}
"""
    
    if "gender_violence" in EMERGENCY_NUMBERS and any(word in keywords for word in ["violence", "abuse", "mistreat"]):
        response += f"• Gender Violence: {EMERGENCY_NUMBERS['gender_violence']}\n"
    
    # Add the appropriate final message
    response += final_message
    
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