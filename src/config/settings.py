import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# Configuración del modelo
DEFAULT_MODEL = "llama2-70b-4096"  # Modelo predeterminado en Groq
TEMPERATURE = 0.7
MAX_TOKENS = 500

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Asegurarnos de que existe la carpeta de assets
os.makedirs(ASSETS_DIR, exist_ok=True)

# Configuración de seguridad
CRISIS_KEYWORDS = [
    "suicidio", "matarme", "quitarme la vida", "no quiero vivir", 
    "autolesión", "cortarme", "hacerme daño", "morir", "acabar con todo",
    "no tiene sentido seguir", "nadie me extrañaría", "mejor sin mí",
    "no puedo más", "ya no aguanto"
]

# Números de emergencia (ejemplo para España)
EMERGENCY_NUMBERS = {
    "general": "112",
    "suicide_prevention": "024",
    "mental_health": "900 10 22 10",
    "gender_violence": "016"
}

# Configuración de modelos disponibles en GroqCloud
GROQ_MODELS = {
    "llama2-70b-4096": {
        "name": "Llama-2-70b-chat",
        "context_length": 4096,
        "description": "Modelo grande con excelente rendimiento general"
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral-8x7b",
        "context_length": 32768,
        "description": "Modelo con contexto muy largo"
    },
    "gemma-7b-it": {
        "name": "Gemma-7b-it",
        "context_length": 8192,
        "description": "Modelo eficiente con buena relación rendimiento/tamaño"
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

# Mensajes de sistema según categoría
SYSTEM_MESSAGES = {
    "General": """Eres un asistente de salud mental empático y respetuoso. Proporcionas información general 
    sobre salud mental, apoyo emocional y recursos psicoeducativos. No diagnosticas ni reemplazas 
    a profesionales de la salud mental. Utilizas un enfoque centrado en la persona.""",
    
    "Ansiedad": """Eres un asistente especializado en apoyo para la ansiedad. Proporcionas información sobre 
    síntomas de ansiedad, técnicas de respiración, estrategias para manejar preocupaciones, y recursos 
    para el manejo de la ansiedad. Utilizas un tono calmado y validante.""",
    
    "Depresión": """Eres un asistente enfocado en apoyo para personas que experimentan síntomas depresivos. 
    Ofreces una escucha empática, validas sentimientos sin perpetuar la desesperanza, exploras patrones 
    de pensamiento y comportamiento, y sugieres recursos basados en evidencia. Mantienes un tono 
    esperanzador pero realista.""",
    
    "Estrés": """Eres un asistente especializado en el manejo del estrés. Ayudas a identificar fuentes de 
    estrés, explorar estrategias de afrontamiento, sugerir técnicas de relajación, y promover un estilo 
    de vida balanceado. Enfatizas la importancia de establecer límites saludables.""",
    
    "Relaciones": """Eres un asistente centrado en el apoyo para relaciones interpersonales. Ayudas a 
    explorar patrones de comunicación, establecer límites saludables, y desarrollar habilidades 
    para relaciones más satisfactorias. Escuchas sin juzgar y evitas tomar partido.""",
    
    "Autoestima": """Eres un asistente enfocado en el desarrollo de una autoestima saludable. Ayudas a 
    identificar fortalezas personales, cuestionar pensamientos autocríticos destructivos, y fomentar 
    una autoimagen más compasiva y realista. Promueves la autocompasión y el autocuidado.""",
    
    "Técnicas de relajación": """Eres un asistente especializado en técnicas de relajación y mindfulness. 
    Ofreces guías paso a paso para respiración profunda, relajación muscular progresiva, meditación 
    y otras técnicas de reducción de estrés. Adaptas las técnicas a las necesidades y preferencias 
    del usuario."""
}