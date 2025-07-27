# Personal Coaching Assistant

A locally hosted personal coaching assistant powered by an LLM, designed to provide reflective conversations, behavioral analysis, motivational nudges, and tailored micro-actions through WhatsApp.

## 🎯 What This Does

This isn't a general chatbot – it's a deeply personalized companion trained on your principles, tone, life context, and decision-making style. It provides:

- **Open Dialogue**: Understands emotional/situational input and responds with reflections, clarity, or micro-tasks
- **Intent Classification**: Detects message type (emotional, practical, reflective, task-oriented) and routes accordingly  
- **Task Generation**: Suggests small, focused actions based on situation + user profile
- **Principle Recall**: Dynamically pulls personal rules or values in context
- **Timed Follow-up**: Saves reminders/actions and triggers them later via WhatsApp
- **Daily/Weekly Review**: Prompts for reflection and tracks patterns across time

## 🏗️ Architecture

```
[WhatsApp Web] ↔ [LLM Coach (local)] ↔ [Personal Profile DB (Vectors)]
                                        ↕
                                [Logic Router]
                                        ↕
                      [Personalized Response + Micro-action]
                                        ↕
                      [WhatsApp Message + Excel Logging]
```

## 📋 Project Status

### ✅ Completed
- [x] Git repository setup
- [x] Python virtual environment  
- [x] Project structure created
- [x] Core file templates (main_loop.py, whatsapp_driver.py, profile.json)
- [x] Reminders.xlsx system
- [x] Requirements.txt with all dependencies

### 🚧 In Progress
- [ ] Installing core dependencies
- [ ] Local LLM setup (Ollama)
- [ ] WhatsApp integration development

### 📅 Next Steps
- [ ] LLM setup and configuration
- [ ] WhatsApp Web automation
- [ ] RAG knowledge base implementation
- [ ] Core agent logic development

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Activate virtual environment
personal-coaching-env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Your Profile
Edit `profile.json` to customize:
- Communication style and tone
- Personal values and principles  
- Response templates
- Behavioral patterns
- Micro-actions library

### 3. Run the Assistant
```bash
python main_loop.py
```

## 📁 Project Structure

```
personal-coaching-assistant/
├── main_loop.py              # Main orchestrator
├── whatsapp_driver.py        # WhatsApp Web automation
├── profile.json              # Personal coaching profile
├── reminders.xlsx            # Task scheduling
├── requirements.txt          # Dependencies
├── config.json              # System configuration
├── embeddings/              # Vector knowledge base
├── logs/                    # Interaction logs
├── temp/                    # Temporary files
└── personal-coaching-env/   # Virtual environment
```

## 🔒 Privacy & Security

- **Local-only execution**: No cloud, no third parties, full control
- **Manual data access**: All info stored in editable files (Excel/JSON)
- **Open source**: Easy to audit and modify
- **Self-updatable**: Adjust rules or personality profile at any time

## 🛠️ Dependencies

### Core Components
- **LLM**: Ollama (Mistral/Phi-3/LLaMA)
- **WhatsApp**: Selenium WebDriver automation
- **Vector DB**: Sentence-transformers + FAISS/ChromaDB
- **Data**: Pandas + Excel integration
- **Scheduling**: APScheduler for reminders

### Full Requirements
See `requirements.txt` for complete dependency list.

## 📖 Example Interactions

**User**: "I can't get out of bed"  
**Assistant**: "That's the loop again, right? One small step. Just get up and splash water on your face. Nothing else."

**User**: "I'm annoyed I delayed this again"  
**Assistant**: "Let's call it what it is: avoidance out of fear. But you've broken this before. Want to walk through it together?"

**User**: "Remind me this evening"  
**Assistant**: *Adds task to reminders.xlsx and sends message at set time*

## 🔧 Development Status

This project is currently in **foundation setup phase**. Core infrastructure is ready, next steps involve:

1. Local LLM integration (Ollama)
2. WhatsApp Web automation
3. RAG knowledge base development
4. Agent logic implementation

## 📝 License

This project is open source. Modify and adapt as needed for your personal use.

---

*A personalized coaching companion that knows you, understands you, and helps you grow.* 