# Asistente de Salud Mental con GroqCloud

Este proyecto implementa un asistente virtual de salud mental basado en Grandes Modelos de Lenguaje (LLMs) utilizando la API de GroqCloud. Proporciona apoyo emocional y recursos psicoeducativos a través de una interfaz de chat accesible.

## Características

- **Interfaz web intuitiva** basada en Gradio
- **Categorías especializadas** para diferentes temas de salud mental
- **Detección de crisis** para identificar mensajes que requieren derivación a servicios profesionales
- **Respuestas personalizadas** según la categoría seleccionada
- **Recursos útiles** para cada categoría de salud mental
- **Acceso a múltiples modelos** a través de GroqCloud

## Requisitos previos

- Python 3.8 o superior
- Una clave API de GroqCloud (regístrate en [console.groq.com](https://console.groq.com))

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Samuromarin/Mental-Health-Assistant.git
cd mental-health-assistant
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz del proyecto con tu clave API:

```
GROQ_API_KEY=tu_clave_api_aquí
```

## Uso

### Iniciar el asistente web

Para iniciar el asistente con la interfaz web:

```bash
python run_groq_assistant.py
```

Opciones disponibles:
- `--port PUERTO`: Especifica el puerto para la interfaz web (por defecto: 7860)
- `--host HOST`: Especifica el host (por defecto: 0.0.0.0)
- `--share`: Comparte la interfaz con un enlace público temporal
- `--model MODELO`: Usa un modelo específico de GroqCloud
- `--debug`: Activa el modo de depuración

### Probar la API directamente

Para probar rápidamente si tu configuración funciona correctamente:

```bash
python test_groq_api.py --message "¿Cómo puedo manejar el estrés?"
```

O para modo interactivo:

```bash
python test_groq_api.py --interactive
```

Opciones disponibles:
- `--message MENSAJE`, `-m MENSAJE`: Mensaje a enviar
- `--category CATEGORÍA`, `-c CATEGORÍA`: Categoría de salud mental
- `--model MODELO`: Modelo específico de GroqCloud
- `--list-models`, `-l`: Listar modelos disponibles
- `--interactive`, `-i`: Modo interactivo para múltiples consultas
- `--temperature TEMP`, `-t TEMP`: Temperatura para la generación (0.1-1.5)
- `--max-tokens TOKENS`, `-mt TOKENS`: Número máximo de tokens en la respuesta

## Estructura del proyecto

```
mental-health-assistant/
│
├── run_groq_assistant.py     # Script principal para iniciar el asistente
├── test_groq_api.py          # Script para probar la API directamente
├── requirements.txt          # Dependencias
├── setup.py                  # Configuración de instalación
│
├── assets/                   # Recursos estáticos (logo, etc.)
│
└── src/
    ├── config/
    │   ├── settings.py       # Configuraciones centralizadas
    │
    ├── interface.py          # Interfaz Gradio
    │
    └── utils/
        ├── groq_client.py    # Cliente para GroqCloud
        └── safety.py         # Detección de crisis y seguridad
```

## Categorías de salud mental

El asistente proporciona apoyo en las siguientes categorías:

1. **General**: Información general sobre salud mental y bienestar emocional
2. **Ansiedad**: Apoyo para comprender y manejar la ansiedad
3. **Depresión**: Información sobre síntomas depresivos y estrategias de afrontamiento
4. **Estrés**: Técnicas para manejar el estrés cotidiano
5. **Relaciones**: Apoyo para mejorar la comunicación y establecer límites saludables
6. **Autoestima**: Estrategias para desarrollar una autoimagen positiva
7. **Técnicas de relajación**: Guías paso a paso para técnicas de relajación y mindfulness

## Consideraciones éticas

Este asistente está diseñado como una herramienta de apoyo y psicoeducación, y **no reemplaza a profesionales de salud mental**. Se debe utilizar como complemento, no como sustituto, de la atención profesional.

Características de seguridad implementadas:
- Detección de mensajes que indican riesgo de crisis
- Protocolos de derivación a servicios de emergencia
- Recordatorios claros sobre las limitaciones del asistente

## Personalización

Puedes personalizar varios aspectos del asistente editando el archivo `src/config/settings.py`:

- **Modelos disponibles**: Añade o modifica los modelos de GroqCloud
- **Categorías**: Personaliza o añade categorías de salud mental
- **Recursos**: Actualiza los enlaces a recursos útiles
- **Mensajes del sistema**: Modifica las instrucciones para cada categoría
- **Palabras clave de crisis**: Personaliza la detección de mensajes de crisis

## Limitaciones

- El asistente no proporciona diagnósticos clínicos
- Las respuestas dependen de la calidad de los modelos de GroqCloud
- No sustituye la atención profesional de salud mental

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

---

**Nota**: Este asistente es una herramienta educativa y de apoyo. Si experimentas una crisis de salud mental, busca ayuda profesional inmediatamente a través de servicios de emergencia locales o líneas de crisis.
