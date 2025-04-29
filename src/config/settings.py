import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Configuración del modelo
DEFAULT_MODEL = "gpt-4"  # o "claude-3-opus-20240229" si usas Anthropic
TEMPERATURE = 0.7
MAX_TOKENS = 500

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")

# Configuración de seguridad
CRISIS_KEYWORDS = [
    "suicidio", "matarme", "quitarme la vida", "no quiero vivir", 
    "autolesión", "cortarme", "hacerme daño"
]

# Números de emergencia (ejemplo para España)
EMERGENCY_NUMBERS = {
    "general": "112",
    "suicide_prevention": "024"
}