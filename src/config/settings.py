import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# Model configuration
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Latest model

# RAG configuration with FAISS
RAG_ENABLED = os.getenv("RAG_ENABLED", "true").lower() == "true"
RAG_DOCUMENTS_DIR = os.getenv("RAG_DOCUMENTS_DIR", "src/data/documents")
RAG_INDEX_DIR = os.getenv("RAG_INDEX_DIR", "src/data/faiss_index")
RAG_EMBEDDINGS_MODEL = os.getenv("RAG_EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
RAG_MAX_CONTEXT_LENGTH = int(os.getenv("RAG_MAX_CONTEXT_LENGTH", "2000"))
RAG_SEARCH_K = int(os.getenv("RAG_SEARCH_K", "3"))

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Ensure necessary folders exist
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "documents"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "faiss_index"), exist_ok=True)

# Crisis detection keywords configuration (English)
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "don't want to live", 
    "self-harm", "cut myself", "hurt myself", "die", "end it all",
    "no point in living", "nobody would miss me", "better without me",
    "can't take it anymore", "can't go on", "want to die", "burden", "no way out", 
    "harm myself", "hurt myself", "hopeless", "goodbye forever", "can't resist anymore"
]

# Emergency numbers (Spain)
EMERGENCY_NUMBERS = {
    "general": "112", # Emergencies
    "suicide_prevention": "024", # Suicide Prevention Line 24h
    "mental_health": "900 10 22 10", # Mental Health Spain
    "gender_violence": "016",   # Gender violence
    "youth_phone": "900 20 20 10",  # ANAR Phone
    "online_chat": "https://www.telefonodelaesperanza.org/"
}

# Available GroqCloud models configuration
GROQ_MODELS = {
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
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B Versatile",
        "context_length": 8192,
        "description": "Versatile version of Llama 3.3 model"
    },
    "compound-beta": {
        "name": "Compound Beta",
        "context_length": 128000,
        "description": "Experimental Groq model with high performance"
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B IT",
        "context_length": 8192,
        "description": "Google model optimized for instructions"
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

# Mental health categories configuration
MENTAL_HEALTH_CATEGORIES = [
    "General",
    "Anxiety",
    "Depression", 
    "Stress",
    "Relationships",
    "Self-esteem",
    "Relaxation techniques"
]

# Additional resources
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
    ],
    "Relaxation techniques": [
        {"name": "Calm (App)", "url": "https://www.calm.com/"},
        {"name": "Headspace (App)", "url": "https://www.headspace.com/"},
        {"name": "Insight Timer (Free App)", "url": "https://insighttimer.com/"}
    ]
}

# System messages by category (improved for RAG)
SYSTEM_MESSAGES = {
    "General": """You are an empathetic and respectful mental health assistant. You provide general 
    mental health information, emotional support and psychoeducational resources. You do not diagnose 
    or replace mental health professionals. You use a person-centered approach. When you have 
    access to specialized information from the knowledge base, use it to enrich your responses 
    while always maintaining a professional and understanding tone.""",
    
    "Anxiety": """You are an assistant specialized in anxiety support. You provide information about 
    anxiety symptoms, breathing techniques, strategies for managing worries, and resources 
    for anxiety management. You use a calm and validating tone. Take advantage of the specialized 
    information available to offer specific and evidence-based techniques.""",
    
    "Depression": """You are an assistant focused on support for people experiencing depressive symptoms. 
    You offer empathetic listening, validate feelings without perpetuating hopelessness, explore patterns 
    of thinking and behavior, and suggest evidence-based resources. You maintain a hopeful but realistic tone. 
    Use specialized information to provide specific strategies.""",
    
    "Stress": """You are an assistant specialized in stress management. You help identify specific sources 
    of stress, explore existing coping strategies, suggest relaxation techniques, and promote a balanced 
    lifestyle. You emphasize the importance of healthy boundaries. Integrate specific techniques 
    from the knowledge base when relevant.""",
    
    "Relationships": """You are an assistant focused on interpersonal relationship support. You help 
    explore communication patterns, establish healthy boundaries, and develop skills 
    for more satisfying relationships. You listen without judgment and avoid taking sides. Use specialized 
    information about relational dynamics when available.""",
    
    "Self-esteem": """You are an assistant focused on developing healthy self-esteem. You help 
    identify personal strengths, challenge destructive self-critical thoughts, and foster 
    a more compassionate and realistic self-image. You promote self-compassion and self-care. Incorporate 
    specific techniques and exercises from the knowledge base.""",
    
    "Relaxation techniques": """You are an assistant specialized in relaxation and mindfulness techniques. 
    You offer step-by-step guides for deep breathing, progressive muscle relaxation, meditation 
    and other stress reduction techniques. You adapt techniques to user needs and preferences. 
    Use detailed instructions from the knowledge base when available."""
}


# Additional RAG configurations (FAISS)
RAG_CONFIG = {
    "enabled": RAG_ENABLED,
    "documents_dir": RAG_DOCUMENTS_DIR,
    "index_dir": RAG_INDEX_DIR,
    "embeddings_model": RAG_EMBEDDINGS_MODEL,
    "chunk_size": RAG_CHUNK_SIZE,
    "chunk_overlap": RAG_CHUNK_OVERLAP,
    "max_context_length": RAG_MAX_CONTEXT_LENGTH,
    "search_k": RAG_SEARCH_K,
    "supported_formats": [".txt", ".md"],
    "index_type": "FAISS",
    "description": "Information Retrieval System using FAISS to enrich responses"
}