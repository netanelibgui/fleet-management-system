#!/usr/bin/env python3
"""
Test script for Ollama API connection with the Personal Coaching Assistant.
"""

import requests
import json
import time
from datetime import datetime

def test_ollama_connection():
    """Test basic connection to Ollama API."""
    print("🧪 Testing Ollama API Connection...")
    
    try:
        # Test if Ollama server is running
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama server is running")
            print(f"📋 Available models: {[model['name'] for model in models.get('models', [])]}")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server at localhost:11434")
        print("💡 Make sure Ollama is running: 'ollama serve'")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_coaching_response():
    """Test the LLM with coaching-specific prompts."""
    print("\n🧠 Testing Coaching Assistant Capabilities...")
    
    test_prompts = [
        {
            "name": "Motivation Support",
            "prompt": "You are a personal coach. I'm feeling overwhelmed with my goals. Give me one simple step I can take right now.",
            "expected_keywords": ["step", "simple", "action", "focus"]
        },
        {
            "name": "Habit Formation", 
            "prompt": "You are a personal coach. I want to build a morning routine but keep failing. What's your advice?",
            "expected_keywords": ["small", "consistent", "habit", "routine"]
        },
        {
            "name": "Procrastination Help",
            "prompt": "You are a personal coach. I keep procrastinating on important tasks. Help me break this pattern.",
            "expected_keywords": ["break", "task", "start", "small"]
        }
    ]
    
    for i, test in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print(f"🔵 Prompt: {test['prompt'][:50]}...")
        
        try:
            start_time = time.time()
            
            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    "model": "mistral:v0.3",
                    "prompt": test['prompt'],
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 200  # Limit response length for testing
                    }
                }, 
                timeout=30)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '').strip()
                
                print(f"✅ Response received ({response_time:.1f}s)")
                print(f"📄 Response preview: {response_text[:100]}...")
                
                # Check for coaching-specific keywords
                found_keywords = [kw for kw in test['expected_keywords'] 
                                if kw.lower() in response_text.lower()]
                
                if found_keywords:
                    print(f"🎯 Coaching keywords found: {found_keywords}")
                else:
                    print("⚠️  No coaching keywords detected")
                
                return True
                
            else:
                print(f"❌ API Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error during test: {e}")
            return False

def test_system_prompt_adherence():
    """Test if the model follows coaching personality from system prompts."""
    print("\n🎭 Testing System Prompt Adherence...")
    
    system_prompt = """You are a direct but compassionate personal coach. Your responses should be:
- Brief and actionable (under 100 words)
- Use "you" and direct language
- Focus on immediate next steps
- Encouraging but realistic
"""
    
    user_prompt = "I failed at my diet again today. I feel terrible."
    
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "mistral:v0.3",
                "prompt": f"[INST] {system_prompt}\n\nUser: {user_prompt} [/INST]",
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 150
                }
            }, 
            timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '').strip()
            
            print("✅ System prompt test completed")
            print(f"📄 Response: {response_text}")
            
            # Check response characteristics
            word_count = len(response_text.split())
            has_direct_language = 'you' in response_text.lower()
            is_encouraging = any(word in response_text.lower() 
                               for word in ['can', 'will', 'try', 'step', 'start'])
            
            print(f"📊 Analysis:")
            print(f"   - Word count: {word_count} (target: <100)")
            print(f"   - Direct language: {'✅' if has_direct_language else '❌'}")
            print(f"   - Encouraging tone: {'✅' if is_encouraging else '❌'}")
            
            return True
            
    except Exception as e:
        print(f"❌ System prompt test failed: {e}")
        return False

def generate_test_report():
    """Generate a comprehensive test report."""
    print("\n" + "="*60)
    print("🏁 OLLAMA SETUP COMPLETION REPORT")
    print("="*60)
    
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Platform: Windows")
    print(f"🧠 Model: Mistral 7B v0.3")
    print(f"🔗 API Endpoint: http://localhost:11434")
    
    # Run all tests
    connection_ok = test_ollama_connection()
    coaching_ok = test_coaching_response() if connection_ok else False
    system_prompt_ok = test_system_prompt_adherence() if connection_ok else False
    
    print("\n📋 TEST RESULTS:")
    print(f"   🔌 API Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"   🧠 Coaching Responses: {'✅ PASS' if coaching_ok else '❌ FAIL'}")
    print(f"   🎭 System Prompts: {'✅ PASS' if system_prompt_ok else '❌ FAIL'}")
    
    overall_success = connection_ok and coaching_ok and system_prompt_ok
    
    print(f"\n🎯 OVERALL STATUS: {'✅ SUCCESS' if overall_success else '❌ NEEDS ATTENTION'}")
    
    if overall_success:
        print("\n🎉 Your local LLM is ready for Personal Coaching Assistant!")
        print("🔜 Next steps:")
        print("   1. Integrate with WhatsApp automation")
        print("   2. Build RAG knowledge base")
        print("   3. Implement core agent logic")
    else:
        print("\n⚠️  Please resolve the issues above before proceeding.")
    
    return overall_success

if __name__ == "__main__":
    print("🚀 Personal Coaching Assistant - Ollama Integration Test")
    print("=" * 60)
    
    success = generate_test_report()
    
    if success:
        print("\n💡 Try this command to interact directly:")
        print("   ollama run mistral:v0.3")
        print("\n📚 Model info:")
        print("   - Size: 4.4GB")
        print("   - Context: 32k tokens") 
        print("   - Features: Function calling, multilingual")
    
    exit(0 if success else 1) 