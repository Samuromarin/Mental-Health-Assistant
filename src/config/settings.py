"""
Configuration module for Mental Health Assistant

Centralizes all system configuration including API keys, model settings,
RAG configuration, and mental health categories.


"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# Model configuration
DEFAULT_MODEL = "gemma2-9b-it"

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Ensure necessary folders exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "documents"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "faiss_index"), exist_ok=True)

# RAG Configuration (Centralized)
RAG_CONFIG = {
    "enabled": os.getenv("RAG_ENABLED", "true").lower() == "true",
    "documents_dir": os.getenv("RAG_DOCUMENTS_DIR", "src/data/documents"),
    "index_dir": os.getenv("RAG_INDEX_DIR", "src/data/faiss_index"),
    "embeddings_model": os.getenv("RAG_EMBEDDINGS_MODEL", "all-MiniLM-L6-v2"),
    "chunk_size": int(os.getenv("RAG_CHUNK_SIZE", "1000")),
    "chunk_overlap": int(os.getenv("RAG_CHUNK_OVERLAP", "200")),
    "max_context_length": int(os.getenv("RAG_MAX_CONTEXT_LENGTH", "2000")),
    "search_k": int(os.getenv("RAG_SEARCH_K", "3")),
    "supported_formats": [".txt", ".md"],
    "index_type": "FAISS",
    "description": "Information Retrieval System using FAISS to enrich responses"
}

# Crisis detection keywords
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "don't want to live", 
    "self-harm", "cut myself", "hurt myself", "die", "end everything", "end it all",
    "no point living", "nobody would miss me", "better without me",
    "I can't take it anymore", "can't go on", "want to die", "burden", "no way out", 
    "harm myself", "hurt myself", "hopeless", "goodbye forever", "can't resist anymore"
]

# Emergency numbers (Spain)
EMERGENCY_NUMBERS = {
    "general": "112",  # Emergencies
    "suicide_prevention": "024",  # Suicide Prevention Line 24h
    "mental_health": "900 10 22 10",  # Mental Health Spain
    "gender_violence": "016",  # Gender violence
    "youth_phone": "900 20 20 10",  # ANAR Phone
    "online_chat": "https://www.telefonodelaesperanza.org/"
}

# Available GroqCloud models
GROQ_MODELS = {
    "gemma2-9b-it": {
        "name": "Gemma 2 9B IT",
        "context_length": 8192,
        "description": "Google model optimized for instructions"
    },
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "name": "Llama 4 Scout 17B",
        "context_length": 128000,
        "description": "Latest Meta Llama 4 model, optimized for instructions"
    },
    "meta-llama/llama-4-maverick-17b-128e-instruct": {
        "name": "Llama 4 Maverick 17B",
        "context_length": 128000,
        "description": "Maverick model from Meta Llama 4 with extended context"
    },
    "llama3-70b-8192": {
        "name": "Llama 3 70B",
        "context_length": 8192,
        "description": "Large Llama 3 model with excellent performance"
    },
    "qwen/qwen3-32b": {
        "name": "Qwen 3 32B",
        "context_length": 131072,  
        "description": "Advanced model with reasoning and multilingual capabilities (100+ languages)"
    },
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B Versatile",
        "context_length": 8192,
        "description": "Versatile version of Llama 3.3 model"
    },
    "deepseek-r1-distill-llama-70b": {
        "name": "DeepSeek R1 Distill 70B",
        "context_length": 8192,
        "description": "Distilled DeepSeek model with Llama base"
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant",
        "context_length": 8192,
        "description": "Fast Llama 3.1 model for instant responses"
    },
    "llama3-8b-8192": {
        "name": "Llama 3 8B",
        "context_length": 8192,
        "description": "Base Llama 3 model, fast and efficient"
    }
}

# Mental health categories
MENTAL_HEALTH_CATEGORIES = [
    "General",
    "Anxiety",
    "Depression", 
    "Stress",
    "Relationships",
    "Self-esteem"
]

# Additional resources by category
RESOURCES = {
    "General": [
        {"name": "WHO - Mental Health", "url": "https://www.who.int/es/health-topics/mental-health"},
        {"name": "Teléfono de la Esperanza", "url": "https://telefonodelaesperanza.org/"},
        {"name": "Spanish Mental Health Confederation", "url": "https://consaludmental.org/"}
    ],
    "Anxiety": [
        {"name": "Spanish OCD Association", "url": "https://asociaciontoc.org/"},
        {"name": "Mind (English)", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/"},
        {"name": "Anxiety Guide - NHS (English)", "url": "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/anxiety-fear-panic/"}
    ],
    "Depression": [
        {"name": "Spanish Psychiatry Association", "url": "https://www.sepsiq.org/"},
        {"name": "Depression Alliance (English)", "url": "https://www.depressionalliance.org/"},
        {"name": "Depression Guide - NHS (English)", "url": "https://www.nhs.uk/mental-health/conditions/clinical-depression/overview/"}
    ],
    "Stress": [
        {"name": "American Psychological Association - Stress (English)", "url": "https://www.apa.org/topics/stress"},
        {"name": "Mental Health Foundation - Stress (English)", "url": "https://www.mentalhealth.org.uk/explore-mental-health/a-z-topics/stress"},
        {"name": "Mindfulness Based Stress Reduction", "url": "https://www.mindfulnessapps.com/"}
    ],
    "Relationships": [
        {"name": "Psychology Today - Relationships (English)", "url": "https://www.psychologytoday.com/intl/basics/relationships"},
        {"name": "The Gottman Institute (English)", "url": "https://www.gottman.com/"},
        {"name": "Relate - Relationships and counselling (English)", "url": "https://www.relate.org.uk/"}
    ],
    "Self-esteem": [
        {"name": "Mind - Self-esteem (English)", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/self-esteem/about-self-esteem/"},
        {"name": "Self-Compassion (English)", "url": "https://self-compassion.org/"},
        {"name": "Rethink Mental Illness (English)", "url": "https://www.rethink.org/"}
    ]
}

# System messages by category
SYSTEM_MESSAGES = {
    "General": """You are an empathetic and respectful mental health assistant. You provide general 
    mental health information, emotional support and psychoeducational resources. You do not diagnose or replace mental health professionals. 
    You provide supportive guidance and refer users to qualified healthcare providers when appropriate. You use a person-centered approach. When you have 
    access to specialized information from the knowledge base, use it to enrich your responses 
    while always maintaining a professional and understanding tone. 
    
    IMPORTANT: Instead of automatically providing mental health tips, ask the user first if they would like 
    you to share some helpful tips and strategies for emotional well-being. Only provide resources if they confirm they want them.""",
    
    "Anxiety": """You are an assistant specialized in anxiety support. You provide information about 
    anxiety symptoms, breathing techniques, strategies for managing worries, and resources 
    for anxiety management. You use a calm and validating tone. You do not diagnose or replace mental health professionals. 
    You provide supportive guidance and refer users to qualified healthcare providers when appropriate.

    IMPORTANT: Instead of automatically providing breathing techniques or anxiety resources, ask the user first if they would like you to share some specific techniques that might help them.
    Only provide techniques and resources if they confirm they want them.""",
    
    "Depression": """You are an assistant focused on support for people experiencing depressive symptoms. 
    You offer empathetic listening, validate feelings without perpetuating hopelessness, explore patterns 
    of thinking and behavior, and suggest evidence-based resources. You maintain a hopeful but realistic tone. 
    Use specialized information to provide specific strategies. You do not diagnose or replace mental health professionals. 
    You provide supportive guidance and refer users to qualified healthcare providers when appropriate.
    
    IMPORTANT: Instead of automatically listing resources, ask if they would like you to share some depression support resources.""",
    
    "Stress": """You are an assistant specialized in stress management. You help identify specific 
    sources of stress, explore existing coping strategies, and promote a balanced lifestyle. 
    You emphasize the importance of healthy boundaries. You do not diagnose or replace mental health professionals.

    IMPORTANT: When users describe stress, first provide empathetic support, then ask if they would like 
    to learn specific stress management techniques like the STOP technique or 5-4-3-2-1 grounding. 
    Only provide detailed techniques after they confirm they want them.

    Always mention technique names when offering so users can choose which one they'd like to learn.""",
    
    "Relationships": """You are an assistant focused on interpersonal relationship support. You help 
    explore communication patterns, establish healthy boundaries, and develop skills 
    for more satisfying relationships. You listen without judgment and avoid taking sides. Use specialized 
    information about relational dynamics when available. You do not diagnose or replace mental health professionals.
    You provide supportive guidance and refer users to qualified healthcare providers when appropriate.
    
    IMPORTANT: Offer to share relationship support resources only if the user expresses interest.""",
    
    "Self-esteem": """You are an assistant focused on developing healthy self-esteem. You help 
    identify personal strengths, challenge destructive self-critical thoughts, and foster 
    a more compassionate and realistic self-image. You promote self-compassion and self-care. Incorporate 
    specific techniques and exercises from the knowledge base. You do not diagnose or replace mental health professionals. 
    You provide supportive guidance and refer users to qualified healthcare providers when appropriate.
    
    IMPORTANT: Ask if they would like self-esteem building resources rather than providing them automatically."""
}