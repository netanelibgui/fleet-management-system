# Ollama Setup Guide for Personal Coaching Assistant

## 🚀 Installation Process

### Step 1: Download Ollama for Windows

1. **Visit the official Ollama website**: [https://ollama.com/download/windows](https://ollama.com/download/windows)
2. **Download the Windows installer** (`.exe` file)
3. **Run the installer** with administrator privileges
4. **Follow the installation wizard** - accept license terms and choose installation directory
5. **Complete installation** - Ollama will be ready to use

### Step 2: Verify Installation

Open PowerShell or Command Prompt and run:
```bash
ollama --version
```

You should see version information if installation was successful.

### Step 3: Start Ollama Service

Ollama runs as a background service by default. You can verify it's running by checking:
```bash
curl http://localhost:11434
```

---

## 🧠 Model Selection for Personal Coaching

Based on extensive research, here are the **top 3 recommended models** for your coaching assistant:

### 🥇 **Recommended: Mistral Small 3.2 (24B)**
- **Size**: ~15GB
- **Context Window**: 32k tokens
- **License**: Apache 2.0 (commercial use allowed)
- **Why it's perfect for coaching**:
  - ✅ **Excellent instruction following** - crucial for coaching prompts
  - ✅ **Reduced repetition errors** - more natural conversations
  - ✅ **Advanced function calling** - perfect for task generation and reminders
  - ✅ **Conversational excellence** - designed for agent-centric applications
  - ✅ **Multilingual support** - dozens of languages
  - ✅ **Strong system prompt adherence** - maintains coaching personality

**Download command**:
```bash
ollama pull mistral-small3.2:24b
```

### 🥈 **Lightweight Alternative: Mistral 7B (v0.3)**
- **Size**: ~4.4GB
- **Context Window**: 32k tokens
- **License**: Apache 2.0
- **Why it's good for coaching**:
  - ✅ **Fast responses** - ideal for real-time WhatsApp interaction
  - ✅ **Function calling support** - can handle task management
  - ✅ **Much smaller** - runs on lower-end hardware
  - ✅ **Proven performance** - outperforms larger models on many benchmarks

**Download command**:
```bash
ollama pull mistral:v0.3
```

### 🥉 **Microsoft Option: Phi-4 (14B)**
- **Size**: ~8GB
- **Context Window**: 16k tokens
- **License**: MIT (most permissive)
- **Why it's worth considering**:
  - ✅ **Recent release** (December 2024) - latest improvements
  - ✅ **MIT license** - maximum commercial flexibility
  - ✅ **Balanced size** - between small and large models
  - ✅ **Microsoft backing** - strong continued development

**Download command**:
```bash
ollama pull phi4:14b
```

---

## 📊 Model Comparison Summary

| Model | Size | Context | Strengths | Best For |
|-------|------|---------|-----------|----------|
| **Mistral Small 3.2** | 15GB | 32k | Instruction following, Function calling, Conversation quality | **Primary coaching assistant** |
| **Mistral 7B** | 4.4GB | 32k | Speed, Efficiency, Good performance | **Fast responses, Limited hardware** |
| **Phi-4** | 8GB | 16k | Latest tech, MIT license, Balanced | **Commercial applications** |

---

## 🔧 Installation Commands

### Install Your Chosen Model

For **Mistral Small 3.2** (recommended):
```bash
ollama pull mistral-small3.2:24b
```

### Test Your Installation

Run a quick test to ensure everything works:
```bash
ollama run mistral-small3.2:24b
```

Then type a test message:
```
Hello! I'm setting up a personal coaching assistant. Can you help me with motivation today?
```

You should get a coherent, helpful response that demonstrates the model's coaching capabilities.

---

## ⚡ Hardware Requirements

### Minimum Requirements:
- **RAM**: 16GB (for Mistral 7B)
- **Storage**: 5GB free space
- **OS**: Windows 10+

### Recommended for Mistral Small 3.2:
- **RAM**: 32GB+
- **GPU**: NVIDIA RTX 4090 or equivalent (optional but recommended)
- **Storage**: 20GB free space
- **OS**: Windows 10+ with latest updates

### Performance Notes:
- **GPU acceleration**: Ollama automatically detects and uses NVIDIA GPUs
- **CPU optimization**: Uses AVX/AVX2 instructions when available
- **RAM usage**: Model size + ~4-8GB overhead during inference

---

## 🛠️ API Configuration

Ollama exposes a REST API at `http://localhost:11434` that your Python application will use.

### Basic API Test:
```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral-small3.2:24b",
  "prompt": "You are a personal coach. Respond with encouragement.",
  "stream": false
}'
```

### Python Integration Example:
```python
import requests

def test_ollama_connection():
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            "model": "mistral-small3.2:24b",
            "prompt": "Hello! Are you ready to be my personal coach?",
            "stream": False
        })
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Ollama is working!")
        print(f"Response: {result['response']}")
        return True
    else:
        print("❌ Connection failed")
        return False

if __name__ == "__main__":
    test_ollama_connection()
```

---

## 🎯 Next Steps

Once Ollama is installed and your model is downloaded:

1. **✅ Update your `requirements.txt`** - Add `ollama` package
2. **✅ Create LLM client module** - Build the interface to Ollama API
3. **✅ Test basic connectivity** - Ensure Python can communicate with Ollama
4. **✅ Configure system prompts** - Set up coaching personality
5. **✅ Integrate with main application** - Connect to your WhatsApp bot

---

## 🔍 Troubleshooting

### Common Issues:

**Installation Problems:**
- Run installer as administrator
- Ensure Windows is up to date
- Check antivirus isn't blocking installation

**Model Loading Errors:**
- Verify model name spelling: `ollama list` to see installed models
- Ensure sufficient disk space and RAM
- Check internet connection during model download

**API Connectivity Issues:**
- Verify Ollama service is running: `ollama serve`
- Check if port 11434 is available
- Test with `curl` before Python integration

**Performance Issues:**
- Update GPU drivers for hardware acceleration
- Close unnecessary applications to free RAM
- Consider smaller model if hardware is limited

---

## 💡 Pro Tips

1. **Start with Mistral 7B** if you're unsure about hardware capabilities
2. **Monitor RAM usage** during initial testing
3. **Keep models updated** with `ollama pull <model>` occasionally
4. **Use function calling** for task generation and reminder features
5. **Test thoroughly** before integrating with WhatsApp automation

---

*Ready to proceed with LLM integration? Your local AI coaching assistant is just a few commands away!* 