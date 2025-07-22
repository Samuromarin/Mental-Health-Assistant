# 🧠 Mental Health Assistant

AI-powered mental health support system combining Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) for evidence-based therapeutic assistance

## ✨ Features

- **🎯 6 specialized categories** for mental health
- **🤖 Intuitive web interface** with Gradio
- **📚 RAG system** for enriched responses
- **🚨 Automatic crisis detection** with safety protocols
- **⚡ Multiple LLM models** from GroqCloud
- **🛠️ Complete management scripts**

## 🚀 Installation

### 1. Clone repository
```bash
git clone https://github.com/Samuromarin/Mental-Health-Assistant.git
cd Mental-Health-Assistant
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure GroqCloud API
1. Go to [console.groq.com](https://console.groq.com/) and get your free API key
2. Create a `.env` file in the project root with your key:
```
GROQ_API_KEY=your_api_key_here
```

### 5. Verify configuration
```bash
# Verify API works
python check_groq_models.py
```

### 6. Configure RAG (optional but recommended)
```bash
# Create example documents
python manage_rag.py create-examples

# Index documents in FAISS
python manage_rag.py index

# Check status
python manage_rag.py status
```

### 7. Start assistant
```bash
python run_groq_assistant.py
```

Ready! Access at: **http://localhost:7860**

## 🎯 Mental Health Categories

| Category | Focus |
|----------|-------|
| 🌟 **General** | General emotional well-being |
| 😰 **Anxiety** | Breathing techniques, crisis management |
| 😔 **Depression** | Emotional support, coping strategies |
| ⚡ **Stress** | Relaxation techniques, mindfulness |
| 💕 **Relationships** | Communication, healthy boundaries |
| 💪 **Self-esteem** | Personal strengthening, self-compassion |

## 🏗️ Project Structure

```
mental-health-assistant/
├── 🚀 run_groq_assistant.py     # Main script
├── 🧪 test_groq_api.py          # API tests
├── ✅ check_groq_models.py      # Verify models
├── 🔧 manage_rag.py             # RAG management
├── 📋 requirements.txt          # Dependencies
│
└── src/
    ├── config/settings.py       # ⚙️ Configurations
    ├── interface.py             # 🖥️ Gradio interface
    └── utils/
        ├── groq_client.py       # 🤖 GroqCloud client
        ├── rag_manager.py       # 📚 RAG system
        ├── safety.py            # 🚨 Crisis detection
```

## 🛠️ Available Scripts

| Script | Usage | Example |
|--------|-------|---------|
| `run_groq_assistant.py` | Main web interface | `python run_groq_assistant.py --share` |
| `test_groq_api.py` | Quick API tests | `python test_groq_api.py -i` |
| `check_groq_models.py` | Verify models | `python check_groq_models.py` |
| `manage_rag.py` | RAG document management | `python manage_rag.py status` |

### Usage examples:

```bash
# Web interface with custom port
python run_groq_assistant.py --port 8080 --share

# Quick API test
python test_groq_api.py -m "How to manage anxiety?" -c Anxiety

# Interactive mode
python test_groq_api.py --interactive
```

## 📚 RAG System

```bash
python manage_rag.py status           # View status
python manage_rag.py create-examples  # Create example documents
python manage_rag.py index            # Index documents
python manage_rag.py list-docs        # List available documents
python manage_rag.py search "breathing techniques"  # Search knowledge base
python manage_rag.py add "New content" --title "My document"  # Add document from text
```

## ⚙️ Configuration

### Environment variables (.env):
```env
GROQ_API_KEY=gsk_your_api_key_here
RAG_ENABLED=true
RAG_CHUNK_SIZE=1000
RAG_SEARCH_K=3
```

## 🛡️ Safety

### Automatic crisis detection:
- **Risk keywords** for suicide/self-harm
- **Immediate referral** to professional services
- **Integrated emergency protocols**

### Emergency numbers (Spain):
- **🚨 Emergencies**: 112
- **💙 Suicide Prevention**: 024
- **🆘 Mental Health Spain**: 900 10 22 10
- **👥 Gender Violence**: 016

## 🐛 Troubleshooting

### Common problems and solutions:

#### Encoding error in .env
```bash
# If you see UTF-8 errors, delete and recreate .env file
del .env  # Windows
rm .env   # Linux/Mac

# Then create manually with text editor (UTF-8)
```

#### Verify configuration
```bash
# Verify GroqCloud connection
python check_groq_models.py

# Verify RAG status
python manage_rag.py status

# Test basic API
python test_groq_api.py -m "Hello" --list-models
```

#### Reindex RAG documents
```bash
python manage_rag.py clean
python manage_rag.py create-examples
python manage_rag.py index
```

### Missing dependencies:
```bash
# If FAISS is missing
pip install faiss-cpu

# If SentenceTransformers is missing
pip install sentence-transformers

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## 📜 License

MIT License - See `LICENSE`

## ⚠️ Important Disclaimer

**This assistant does NOT replace professional mental health care.**

In case of emergency, contact immediately:
- **🚨 Spain**: 112 (Emergencies), 024 (Suicide Prevention)
- **🌍 International**: Local emergency services

---

**Developed with ❤️ to support community mental wellness**

*Questions? [Open an issue](https://github.com/Samuromarin/Mental-Health-Assistant/issues)*
