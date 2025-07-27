# Personal Coaching Assistant - Complete TODO List

## Project Overview
A locally hosted personal coaching assistant powered by an LLM, designed to provide reflective conversations, behavioral analysis, motivational nudges, and tailored micro-actions through WhatsApp.

**Core Architecture:** WhatsApp Web ↔ Local LLM (Ollama) ↔ Personal Profile Database (Vectors)

---

## 📋 Project Foundation
- [ ] Initialize Git repository and set up version control
- [ ] Create Python virtual environment and requirements.txt
- [ ] Create folder structure: main_loop.py, profile.json, embeddings/, logs/, etc.
- [ ] Install Python dependencies: ollama, sentence-transformers, pandas, selenium

---

## 🤖 Local LLM Setup
- [ ] Research Ollama installation and model selection (Mistral/Phi-3/LLaMA)
- [ ] Download and install Ollama on local machine
- [ ] Download and test Mistral, Phi-3, or LLaMA models via Ollama
- [ ] Create basic Python script to test LLM API connectivity
- [ ] Design and test persistent system prompts for coaching behavior

---

## 📱 WhatsApp Integration
- [ ] Research WhatsApp Web automation options (Selenium, API alternatives)
- [ ] Install and configure Selenium WebDriver for WhatsApp Web
- [ ] Build whatsapp_driver.py for sending/receiving messages
- [ ] Parse incoming WhatsApp messages and extract content
- [ ] Test bidirectional WhatsApp messaging functionality

---

## 👤 Personal Profile System
- [ ] Design profile.json structure for personality, rules, tone, responses
- [ ] Create comprehensive profile.json template with examples
- [ ] Create system to load and validate personal profile configuration
- [ ] Allow real-time updates to personality and rules without restart

---

## 🧠 RAG Knowledge Base
- [ ] Set up sentence-transformers for text embeddings
- [ ] Build system to create embeddings from personal knowledge base
- [ ] Create vector similarity search for context retrieval
- [ ] Inject relevant personal context into LLM prompts
- [ ] Test full RAG pipeline from query to context retrieval

---

## ⚡ Core Agent Logic
- [ ] Create intent classification (emotional, practical, reflective, task-oriented)
- [ ] Route messages to appropriate response handlers based on intent
- [ ] Handle open dialogue and reflective conversations
- [ ] Generate micro-tasks and actionable suggestions
- [ ] Dynamically pull and apply personal rules/values in context
- [ ] Build main_loop.py to orchestrate WhatsApp input and LLM processing

---

## ⏰ Reminder & Task System
- [ ] Set up pandas integration for reminders.xlsx management
- [ ] Create system to schedule and trigger timed follow-ups
- [ ] Track micro-tasks and their completion status
- [ ] Send scheduled WhatsApp reminders at specified times
- [ ] Implement background process for timed reminders

---

## 📊 Logging & Analytics
- [ ] Log all conversations to structured files in logs/ directory
- [ ] Add sentiment/emotion detection and logging per message
- [ ] Analyze conversation patterns and behavioral trends
- [ ] Generate automated daily/weekly behavior summaries

---

## 💬 Conversation Engine
- [ ] Maintain conversation history and context across sessions
- [ ] Manage conversation memory and context window limits
- [ ] Generate responses that reference previous conversations
- [ ] Track conversation state and multi-turn interactions
- [ ] Implement different tones/responses based on time of day

---

## 🔧 Testing & Validation
- [ ] Write unit tests for core components and functions
- [ ] Test LLM response quality and consistency
- [ ] Validate that responses align with coaching objectives
- [ ] Test complete flow from WhatsApp message to response
- [ ] Test system performance and response times

---

## 🚀 Deployment Setup
- [ ] Create scripts to start all system components
- [ ] Configure environment variables and settings
- [ ] Add comprehensive error handling and recovery
- [ ] Configure proper logging for debugging and monitoring
- [ ] Implement backup system for profiles, logs, and data

---

## 📖 Documentation & Guides
- [ ] Create comprehensive setup and installation guide
- [ ] Write user guide for configuring personality and using the system
- [ ] Document internal APIs and component interfaces
- [ ] Create troubleshooting guide for common issues

---

## 🎯 Key Capabilities to Implement

### Core Functionality
| Capability | Description |
|------------|-------------|
| **Open Dialogue** | Understands emotional/situational input and responds with reflections, clarity, or micro-tasks |
| **Intent Classification** | Detects message type (emotional, practical, reflective, task-oriented) and routes accordingly |
| **Task Generation** | Suggests small, focused actions based on situation + user profile |
| **Principle Recall** | Dynamically pulls personal rules or values in context |
| **Timed Follow-up** | Saves reminders/actions and triggers them later via WhatsApp |
| **Daily/Weekly Review** | Prompts for reflection and tracks patterns across time |

### Example Interactions
- **Input:** "I can't get out of bed"  
  **Response:** "That's the loop again, right? One small step. Just get up and splash water on your face. Nothing else."

- **Input:** "I'm annoyed I delayed this again"  
  **Response:** "Let's call it what it is: avoidance out of fear. But you've broken this before. Want to walk through it together?"

- **Input:** "Remind me this evening"  
  **Action:** Adds task to reminders.xlsx and sends message at set time

---

## 🏗️ Project File Structure
```
personal-coaching-assistant/
├── main_loop.py              # Handles WhatsApp input, invokes LLM
├── profile.json              # Defines personality, rules, tone, responses
├── whatsapp_driver.py        # Sends WhatsApp messages (via Selenium)
├── embeddings/               # Vector-based personalized reflections
├── logs/                     # Archives of interactions, actions, feedback
├── reminders.xlsx            # Reminder and micro-task scheduling
├── requirements.txt          # Python dependencies
└── README.md                 # Setup and usage instructions
```

---

## 🔒 Privacy & Control Features
- **Local-only Execution:** No cloud, no third parties, full control
- **Manual Data Access:** All info stored in editable files (Excel/JSON)
- **Open Source:** Easy to audit and modify
- **Self-Updatable:** Adjust rules or personality profile at any time

---

## 🚀 Getting Started
1. Complete **Project Foundation** tasks to set up development environment
2. Set up **Local LLM** with Ollama and chosen model  
3. Implement **WhatsApp Integration** for messaging
4. Build **Personal Profile System** for customization
5. Add **RAG Knowledge Base** for personalized responses
6. Develop **Core Agent Logic** for intelligent routing and responses

---

*Last Updated: [Current Date]*  
*Total Tasks: 49*  
*Estimated Timeline: 4-6 weeks for MVP* 