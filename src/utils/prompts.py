"""
- Formats messages for different LLM models
- Provides specific instructions for each mental health category
- Defines example prompts by category
"""

from src.config.settings import VICUNA_PROMPT_TEMPLATE, MENTAL_HEALTH_CATEGORIES

def format_prompt_for_vicuna(message, category="General"):
    """
    Formats the user message for the Vicuna model,
    optimizing for mental health context
    
    Args:
        message (str): User message
        category (str): Selected mental health category
    
    Returns:
        str: Formatted prompt for Vicuna
    """
    # Add specific instructions based on category
    category_instructions = get_category_specific_instructions(category)
    
    # If user selected a specific category, include it in context
    if category != "General":
        context_message = f"{category_instructions}\n\nThe user wants to talk about topics related to {category.lower()}:\n{message}"
    else:
        context_message = f"{message}"
    
    return VICUNA_PROMPT_TEMPLATE.format(message=context_message)

def get_category_specific_instructions(category):
    """
    Returns specific instructions according to mental health category
    
    Args:
        category (str): Mental health category
    
    Returns:
        str: Specific instructions for that category
    """
    instructions = {
        "Anxiety": """
        For this anxiety topic:
        - Use a calm tone and validate the user's feelings.
        - Teach breathing and relaxation techniques when appropriate.
        - Explore specific triggers with open-ended questions.
        - Normalize anxiety experiences without minimizing them.
        - Provide accurate information about anxiety and its symptoms.
        - Suggest evidence-based strategies (diaphragmatic breathing, mindfulness, gradual exposure).
        - Encourage seeking professional help for more structured treatment.
        """,
        
        "Depression": """
        For this depression topic:
        - Use an empathetic listening approach and validate their experiences without minimizing them.
        - Explore thought patterns tactfully and ask about activities they used to enjoy.
        - Maintain a hopeful but realistic tone.
        - Validate their feelings without perpetuating hopelessness.
        - Ask about suicidal thoughts if appropriate, recommending immediate help if necessary.
        - Gradually explore elements like sleep patterns, appetite, and energy.
        - Suggest small meaningful activities that might be manageable.
        """,
        
        "Stress": """
        For this stress management topic:
        - Help identify specific sources of stress in their life.
        - Explore existing coping strategies and their effectiveness.
        - Suggest mindfulness techniques when appropriate.
        - Emphasize the importance of self-care and healthy boundaries.
        - Normalize stress as a natural human response.
        - Distinguish between acute and chronic stress if relevant.
        - Explore how stress affects different areas of their life.
        """,
        
        "Relationships": """
        For this relationships topic:
        - Listen without judgment and avoid taking sides.
        - Help explore communication patterns in their relationships.
        - Encourage considering different perspectives.
        - Explore how current dynamics might relate to past experiences.
        - Emphasize the importance of healthy boundaries and clear communication.
        - Ask questions that promote reflection on personal needs and values.
        - Recognize when there might be abusive situations and suggest appropriate resources.
        """,
        
        "Self-esteem": """
        For this self-esteem topic:
        - Help identify personal strengths and past achievements.
        - Question self-critical thoughts with gentleness.
        - Encourage a more compassionate and realistic self-image.
        - Explore the origin of negative beliefs about themselves.
        - Distinguish between constructive and destructive self-criticism.
        - Promote self-compassion as an alternative to self-criticism.
        - Suggest practices like writing gratitude journals or realistic affirmations.
        """
    }
    
    # General instructions for any category
    general_instructions = """
    Remember to always maintain an empathetic attitude, validate feelings, use open-ended questions,
    offer appropriate educational resources, and encourage seeking professional help when necessary.
    Do not diagnose or replace professional mental health care.
    """
    
    # Combine specific instructions with general ones
    specific_instructions = instructions.get(category, "")
    if specific_instructions:
        return f"{specific_instructions}\n\n{general_instructions}"
    else:
        return general_instructions

def create_system_message(category="General"):
    """
    Creates a system message for ChatCompletion compatible models
    
    Args:
        category (str): Mental health category
    
    Returns:
        str: Formatted system message
    """
    base_system_message = """You are an empathetic and respectful mental health assistant that provides emotional support, 
    active listening and psychoeducation. You do not provide clinical diagnoses or replace mental health professionals. 
    Your approach is personalized, based on scientific evidence, and you offer responses that promote psychological well-being."""
    
    # Add specific instructions according to category
    category_instructions = get_category_specific_instructions(category)
    
    return f"{base_system_message}\n\n{category_instructions}"

def get_example_prompts():
    """
    Returns example prompts for each category
    
    Returns:
        dict: Dictionary with example prompts by category
    """
    return {
        "General": [
            "Could you give me some tips to improve my emotional well-being?",
            "I haven't been feeling well emotionally lately, what can I do?",
            "What resources do you recommend for learning more about mental health?"
        ],
        "Anxiety": [
            "I feel anxious all the time, what can I do?",
            "How can I manage panic attacks?",
            "I have constant fear that something bad is going to happen"
        ],
        "Depression": [
            "I have no motivation to do anything lately",
            "How can I deal with recurring negative thoughts?",
            "I feel sad for no apparent reason"
        ],
        "Stress": [
            "Work is causing me a lot of stress, how can I manage it?",
            "I feel like I'm always under pressure",
            "I need techniques to relax after a difficult day"
        ],
        "Relationships": [
            "I have problems communicating with my partner",
            "How can I establish healthy boundaries with my family?",
            "I have trouble trusting others"
        ],
        "Self-esteem": [
            "I always compare myself to others and feel inferior",
            "How can I improve my self-image?",
            "I feel like I'm not good enough at anything"
        ]
    }