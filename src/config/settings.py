import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# Configuración del modelo
# Modelos disponibles confirmados por check_groq_models.py
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # Modelo que funcionó en la prueba

# Configuración RAG con FAISS
RAG_ENABLED = os.getenv("RAG_ENABLED", "true").lower() == "true"
RAG_DOCUMENTS_DIR = os.getenv("RAG_DOCUMENTS_DIR", "src/data/documents")
RAG_INDEX_DIR = os.getenv("RAG_INDEX_DIR", "src/data/faiss_index")
RAG_EMBEDDINGS_MODEL = os.getenv("RAG_EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
RAG_MAX_CONTEXT_LENGTH = int(os.getenv("RAG_MAX_CONTEXT_LENGTH", "2000"))
RAG_SEARCH_K = int(os.getenv("RAG_SEARCH_K", "3"))

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Asegurarnos de que existen las carpetas necesarias
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "documents"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "faiss_index"), exist_ok=True)

# Configuración de seguridad
CRISIS_KEYWORDS = [
    "suicidio", "matarme", "quitarme la vida", "no quiero vivir", 
    "autolesión", "cortarme", "hacerme daño", "morir", "acabar con todo",
    "no tiene sentido seguir", "nadie me extrañaría", "mejor sin mí",
    "no puedo más", "ya no aguanto"
]

# Números de emergencia (España)
EMERGENCY_NUMBERS = {
    "general": "112",
    "suicide_prevention": "024",
    "mental_health": "900 10 22 10",
    "gender_violence": "016"
}

# Configuración de modelos disponibles en GroqCloud
# Actualizado según los resultados de check_groq_models.py
# Seleccionando modelos adecuados para texto conversacional
GROQ_MODELS = {
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "name": "Llama 4 Scout 17B",
        "context_length": 128000,
        "description": "Modelo Scout de Meta Llama 4, optimizado para instrucciones"
    },
    "llama3-70b-8192": {
        "name": "Llama 3 70B",
        "context_length": 8192,
        "description": "Modelo grande de Llama 3 con amplio contexto"
    },
    "compound-beta": {
        "name": "Compound Beta",
        "context_length": 128000,
        "description": "Modelo de Groq optimizado para rendimiento"
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B IT",
        "context_length": 8192,
        "description": "Modelo de Google optimizado para instrucciones"
    },
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B Versatile",
        "context_length": 8192,
        "description": "Versión versátil del modelo Llama 3.3"
    }
}

# Configuración de categorías de salud mental
MENTAL_HEALTH_CATEGORIES = [
    "General",
    "Ansiedad",
    "Depresión",
    "Estrés",
    "Relaciones",
    "Autoestima",
    "Técnicas de relajación"
]

# Recursos adicionales
RESOURCES = {
    "General": [
        {"name": "OMS - Salud Mental", "url": "https://www.who.int/es/health-topics/mental-health"},
        {"name": "Teléfono de la Esperanza", "url": "https://telefonodelaesperanza.org/"},
        {"name": "Confederación Salud Mental España", "url": "https://consaludmental.org/"}
    ],
    "Ansiedad": [
        {"name": "Asociación TOC España", "url": "https://asociaciontoc.org/"},
        {"name": "Mind (Inglés)", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/"},
        {"name": "Guía para la ansiedad - NHS (Inglés)", "url": "https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/anxiety-fear-panic/"}
    ],
    "Depresión": [
        {"name": "Asociación Española de Psiquiatría", "url": "https://www.sepsiq.org/"},
        {"name": "Depression Alliance (Inglés)", "url": "https://www.depressionalliance.org/"},
        {"name": "Guía para la depresión - NHS (Inglés)", "url": "https://www.nhs.uk/mental-health/conditions/clinical-depression/overview/"}
    ],
    "Estrés": [
        {"name": "American Psychological Association - Estrés (Inglés)", "url": "https://www.apa.org/topics/stress"},
        {"name": "Mental Health Foundation - Estrés (Inglés)", "url": "https://www.mentalhealth.org.uk/explore-mental-health/a-z-topics/stress"},
        {"name": "Mindfulness Based Stress Reduction", "url": "https://www.mindfulnessapps.com/"}
    ],
    "Relaciones": [
        {"name": "Psychology Today - Relaciones (Inglés)", "url": "https://www.psychologytoday.com/intl/basics/relationships"},
        {"name": "The Gottman Institute (Inglés)", "url": "https://www.gottman.com/"},
        {"name": "Relate - Relaciones y counselling (Inglés)", "url": "https://www.relate.org.uk/"}
    ],
    "Autoestima": [
        {"name": "Mind - Autoestima (Inglés)", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/self-esteem/about-self-esteem/"},
        {"name": "Self-Compassion (Inglés)", "url": "https://self-compassion.org/"},
        {"name": "Rethink Mental Illness (Inglés)", "url": "https://www.rethink.org/"}
    ],
    "Técnicas de relajación": [
        {"name": "Calm (Aplicación)", "url": "https://www.calm.com/"},
        {"name": "Headspace (Aplicación)", "url": "https://www.headspace.com/"},
        {"name": "Insight Timer (Aplicación gratuita)", "url": "https://insighttimer.com/"}
    ]
}

# Mensajes de sistema según categoría (mejorados para RAG)
SYSTEM_MESSAGES = {
    "General": """Eres un asistente de salud mental empático y respetuoso. Proporcionas información general 
    sobre salud mental, apoyo emocional y recursos psicoeducativos. No diagnosticas ni reemplazas 
    a profesionales de la salud mental. Utilizas un enfoque centrado en la persona. Cuando tengas 
    acceso a información especializada de la base de conocimiento, úsala para enriquecer tus respuestas 
    manteniendo siempre un tono profesional y comprensivo.""",
    
    "Ansiedad": """Eres un asistente especializado en apoyo para la ansiedad. Proporcionas información sobre 
    síntomas de ansiedad, técnicas de respiración, estrategias para manejar preocupaciones, y recursos 
    para el manejo de la ansiedad. Utilizas un tono calmado y validante. Aprovecha la información 
    especializada disponible para ofrecer técnicas específicas y basadas en evidencia.""",
    
    "Depresión": """Eres un asistente enfocado en apoyo para personas que experimentan síntomas depresivos. 
    Ofreces una escucha empática, validas sentimientos sin perpetuar la desesperanza, exploras patrones 
    de pensamiento y comportamiento, y sugieres recursos basados en evidencia. Mantienes un tono 
    esperanzador pero realista. Usa información especializada para proporcionar estrategias específicas.""",
    
    "Estrés": """Eres un asistente especializado en el manejo del estrés. Ayudas a identificar fuentes de 
    estrés, explorar estrategias de afrontamiento, sugerir técnicas de relajación, y promover un estilo 
    de vida balanceado. Enfatizas la importancia de establecer límites saludables. Integra técnicas 
    específicas de la base de conocimiento cuando sea relevante.""",
    
    "Relaciones": """Eres un asistente centrado en el apoyo para relaciones interpersonales. Ayudas a 
    explorar patrones de comunicación, establecer límites saludables, y desarrollar habilidades 
    para relaciones más satisfactorias. Escuchas sin juzgar y evitas tomar partido. Utiliza información 
    especializada sobre dinámicas relacionales cuando esté disponible.""",
    
    "Autoestima": """Eres un asistente enfocado en el desarrollo de una autoestima saludable. Ayudas a 
    identificar fortalezas personales, cuestionar pensamientos autocríticos destructivos, y fomentar 
    una autoimagen más compasiva y realista. Promueves la autocompasión y el autocuidado. Incorpora 
    técnicas específicas y ejercicios de la base de conocimiento.""",
    
    "Técnicas de relajación": """Eres un asistente especializado en técnicas de relajación y mindfulness. 
    Ofreces guías paso a paso para respiración profunda, relajación muscular progresiva, meditación 
    y otras técnicas de reducción de estrés. Adaptas las técnicas a las necesidades y preferencias 
    del usuario. Utiliza instrucciones detalladas de la base de conocimiento cuando estén disponibles."""
}

# Definir la plantilla para Vicuna si es necesaria
VICUNA_PROMPT_TEMPLATE = """A continuación hay una conversación entre un usuario y un asistente especializado en salud mental.
El asistente es empático, respetuoso, y proporciona información útil basada en evidencia científica, aunque no reemplaza a un profesional de salud mental.

Usuario: {message}
Asistente:"""

# Configuraciones adicionales para RAG con FAISS
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
    "description": "Sistema de Recuperación de Información usando FAISS para enriquecer respuestas"
}