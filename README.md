# 🧠 Asistente de Salud Mental

Asistente virtual inteligente que combina LLMs de GroqCloud con sistema RAG (FAISS) para proporcionar apoyo emocional especializado y recursos psicoeducativos.

## ✨ Características

- **🤖 Interfaz web intuitiva** con Gradio
- **📚 Sistema RAG avanzado** con FAISS para respuestas enriquecidas
- **🎯 7 categorías especializadas** de salud mental
- **🚨 Detección automática de crisis** con protocolos de seguridad
- **⚡ Múltiples modelos LLM** de GroqCloud
- **🛠️ Scripts de gestión completos**

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/Samuromarin/Mental-Health-Assistant.git
cd Mental-Health-Assistant
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API de GroqCloud
1. Ve a [console.groq.com](https://console.groq.com/) y obtén tu clave API gratuita
2. Crea un archivo `.env` en la raíz del proyecto con tu clave:
```
GROQ_API_KEY=tu_clave_api_aquí
```

### 5. Verificar configuración
```bash
# Verificar que la API funciona
python check_groq_models.py
```

### 6. Configurar RAG (opcional pero recomendado)
```bash
# Crear documentos de ejemplo
python manage_rag.py create-examples

# Indexar documentos en FAISS
python manage_rag.py index

# Verificar estado
python manage_rag.py status
```

### 7. Iniciar asistente
```bash
python run_groq_assistant.py
```

¡Listo! Accede en: **http://localhost:7860**

## 🎯 Categorías de Salud Mental

| Categoría | Enfoque |
|-----------|---------|
| 🌟 **General** | Bienestar emocional general |
| 😰 **Ansiedad** | Técnicas de respiración, manejo de crisis |
| 😔 **Depresión** | Apoyo emocional, estrategias de afrontamiento |
| ⚡ **Estrés** | Técnicas de relajación, mindfulness |
| 💕 **Relaciones** | Comunicación, límites saludables |
| 💪 **Autoestima** | Fortalecimiento personal, autocompasión |
| 🧘 **Relajación** | Mindfulness, respiración, meditación |

## 🏗️ Estructura del Proyecto

```
mental-health-assistant/
├── 🚀 run_groq_assistant.py     # Script principal
├── 🧪 test_groq_api.py          # Pruebas API
├── ✅ check_groq_models.py      # Verificar modelos
├── 🔧 manage_rag.py             # Gestión RAG
├── 📋 requirements.txt          # Dependencias
│
└── src/
    ├── config/settings.py       # ⚙️ Configuraciones
    ├── interface.py             # 🖥️ Interfaz Gradio
    └── utils/
        ├── groq_client.py       # 🤖 Cliente GroqCloud
        ├── rag_manager.py       # 📚 Sistema RAG
        ├── safety.py            # 🚨 Detección crisis
        └── prompts.py           # 💬 Formateo prompts
```

## 🛠️ Scripts Disponibles

| Script | Uso | Ejemplo |
|--------|-----|---------|
| `run_groq_assistant.py` | Interfaz web principal | `python run_groq_assistant.py --share` |
| `test_groq_api.py` | Pruebas rápidas de API | `python test_groq_api.py -i` |
| `check_groq_models.py` | Verificar modelos | `python check_groq_models.py` |
| `manage_rag.py` | Gestión documentos RAG | `python manage_rag.py status` |

### Ejemplos de uso:

```bash
# Interfaz web con puerto personalizado
python run_groq_assistant.py --port 8080 --share

# Prueba rápida de API
python test_groq_api.py -m "¿Cómo manejar la ansiedad?" -c Ansiedad

# Modo interactivo
python test_groq_api.py --interactive
```

## 📚 Sistema RAG

### Configuración inicial:
```bash
python manage_rag.py create-examples  # Crear documentos ejemplo
python manage_rag.py index            # Indexar documentos
python manage_rag.py status           # Ver estado
python manage_rag.py search "técnicas de respiración"  # Buscar en base de conocimientos
```

### Gestión de documentos:
```bash
python manage_rag.py search "ansiedad" --category Ansiedad
python manage_rag.py add "Nuevo contenido" --title "Mi documento"
python manage_rag.py list-docs
```

## ⚙️ Configuración

### Variables de entorno (.env):
```env
GROQ_API_KEY=gsk_tu_clave_api_aquí
RAG_ENABLED=true
RAG_CHUNK_SIZE=1000
RAG_SEARCH_K=3
```

### Modelos disponibles:
- `meta-llama/llama-4-scout-17b-16e-instruct` (recomendado)
- `llama3-70b-8192`
- `compound-beta`
- `gemma2-9b-it`
- `llama-3.3-70b-versatile`

## 🛡️ Seguridad

### Detección automática de crisis:
- **Palabras clave de riesgo** suicida/autolesión
- **Derivación inmediata** a servicios profesionales
- **Protocolos de emergencia** integrados

### Números de emergencia (España):
- **🚨 Emergencias**: 112
- **💙 Prevención Suicidio**: 024
- **🆘 Salud Mental**: 900 10 22 10
- **👥 Violencia de Género**: 016

## 🐛 Resolución de Problemas

### Problemas comunes y soluciones:

#### Error de codificación en .env
```bash
# Si ves errores de UTF-8, elimina y recrea el archivo .env
del .env  # Windows
rm .env   # Linux/Mac

# Luego créalo manualmente con editor de texto (UTF-8)
```

#### Verificar configuración
```bash
# Verificar conexión GroqCloud
python check_groq_models.py

# Verificar estado RAG
python manage_rag.py status

# Probar API básica
python test_groq_api.py -m "Hola" --list-models
```

#### Reindexar documentos RAG
```bash
python manage_rag.py clean
python manage_rag.py create-examples
python manage_rag.py index
```

### Dependencias faltantes:
```bash
# Si falta FAISS
pip install faiss-cpu

# Si falta SentenceTransformers
pip install sentence-transformers

# Reinstalar todas las dependencias
pip install -r requirements.txt --force-reinstall
```

## 📜 Licencia

MIT License - Ver `LICENSE`

## ⚠️ Disclaimer Importante

**Este asistente NO reemplaza atención profesional de salud mental.**

En caso de emergencia, contacta inmediatamente:
- **🚨 España**: 112 (Emergencias), 024 (Prevención Suicidio)
- **🌍 Internacional**: Servicios de emergencia locales

---

**Desarrollado con ❤️ para apoyar el bienestar mental de la comunidad**

*¿Dudas? [Abre un issue](https://github.com/Samuromarin/Mental-Health-Assistant/issues)*
