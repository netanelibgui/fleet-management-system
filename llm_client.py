#!/usr/bin/env python3
"""
LLM Client for Personal Coaching Assistant
Interfaces with Ollama to generate coaching responses using Mistral.
"""

import requests
import json
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from intent_classifier import MessageIntent, IntentResult

@dataclass
class CoachingContext:
    """Context information for generating coaching responses."""
    user_message: str
    sender: str
    intent: MessageIntent
    confidence: float
    personal_profile: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    relevant_principles: List[str]
    timestamp: datetime

class LLMClient:
    """
    Client for interacting with local LLM (Ollama/Mistral) for coaching responses.
    """
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 model_name: str = "mistral:v0.3",
                 temperature: float = 0.7,
                 max_tokens: int = 300):
        """
        Initialize LLM client.
        
        Args:
            ollama_url: URL of Ollama API
            model_name: Name of the model to use
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
        """
        self.ollama_url = ollama_url.rstrip('/')
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self.logger = logging.getLogger(__name__)
        
        # Test connection on initialization
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test connection to Ollama API."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                if self.model_name in model_names:
                    self.logger.info(f"✅ Connected to Ollama - Model '{self.model_name}' available")
                    return True
                else:
                    self.logger.warning(f"⚠️ Model '{self.model_name}' not found. Available: {model_names}")
                    return False
            else:
                self.logger.error(f"❌ Ollama API error: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.logger.error("❌ Cannot connect to Ollama - is it running?")
            return False
        except Exception as e:
            self.logger.error(f"❌ Ollama connection test failed: {e}")
            return False
    
    def _build_system_prompt(self, context: CoachingContext) -> str:
        """
        Build system prompt based on context and intent.
        
        Args:
            context: The coaching context
            
        Returns:
            Formatted system prompt
        """
        # Base coaching personality
        base_prompt = """You are a personal coaching assistant. Your role is to provide thoughtful, empathetic, and actionable guidance.

CORE PRINCIPLES:
- Be genuinely helpful and supportive
- Provide concrete, actionable advice
- Keep responses concise but meaningful (under 200 words)
- Use a warm, encouraging tone
- Ask clarifying questions when helpful
- Reference the user's personal context when relevant

"""
        
        # Add intent-specific guidance
        intent_guidance = {
            MessageIntent.EMOTIONAL: """
EMOTIONAL SUPPORT MODE:
- Validate feelings without dismissing them
- Offer coping strategies and perspective
- Be empathetic and understanding
- Suggest healthy ways to process emotions
""",
            MessageIntent.PRACTICAL: """
PRACTICAL GUIDANCE MODE:
- Provide clear, step-by-step advice
- Break down complex tasks into manageable parts
- Suggest specific tools or methods
- Focus on actionable solutions
""",
            MessageIntent.REFLECTIVE: """
REFLECTIVE COACHING MODE:
- Ask thought-provoking questions
- Help explore values and meaning
- Encourage deeper self-awareness
- Connect situations to broader life principles
""",
            MessageIntent.MOTIVATIONAL: """
MOTIVATIONAL SUPPORT MODE:
- Provide encouragement and confidence building
- Suggest small, achievable first steps
- Reframe challenges as opportunities
- Remind of past successes and strengths
""",
            MessageIntent.SOCIAL: """
RELATIONSHIP GUIDANCE MODE:
- Help understand different perspectives
- Suggest communication strategies
- Validate concerns about relationships
- Offer diplomatic solutions
""",
            MessageIntent.DECISION: """
DECISION SUPPORT MODE:
- Help clarify values and priorities
- Suggest decision-making frameworks
- Explore pros and cons objectively
- Ask questions to reveal preferences
""",
            MessageIntent.PROGRESS: """
PROGRESS COACHING MODE:
- Celebrate achievements and progress
- Learn from setbacks constructively
- Plan next steps and continued growth
- Maintain momentum and motivation
"""
        }
        
        prompt = base_prompt + intent_guidance.get(context.intent, "")
        
        # Add personal context if available
        if context.personal_profile:
            communication_style = context.personal_profile.get('communication_style', {})
            if communication_style:
                prompt += f"\nPERSONAL COMMUNICATION STYLE:\n"
                for key, value in communication_style.items():
                    if isinstance(value, str):
                        prompt += f"- {key}: {value}\n"
        
        # Add relevant principles
        if context.relevant_principles:
            prompt += f"\nRELEVANT PERSONAL PRINCIPLES:\n"
            for principle in context.relevant_principles[:3]:  # Limit to top 3
                prompt += f"- {principle}\n"
        
        # Add conversation context
        if context.conversation_history:
            prompt += f"\nRECENT CONVERSATION CONTEXT:\n"
            for exchange in context.conversation_history[-2:]:  # Last 2 exchanges
                prompt += f"User: {exchange.get('user', '')}\n"
                prompt += f"Assistant: {exchange.get('assistant', '')}\n"
        
        prompt += f"""
CURRENT SITUATION:
- Intent: {context.intent.value} (confidence: {context.confidence:.1f})
- User message: "{context.user_message}"

Provide a helpful, coaching-style response that addresses their specific need."""
        
        return prompt
    
    def generate_response(self, context: CoachingContext) -> Optional[str]:
        """
        Generate a coaching response using the LLM.
        
        Args:
            context: The coaching context
            
        Returns:
            Generated response or None if failed
        """
        try:
            system_prompt = self._build_system_prompt(context)
            
            # Prepare the request
            payload = {
                "model": self.model_name,
                "prompt": system_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            self.logger.debug(f"Sending request to LLM for intent: {context.intent.value}")
            start_time = time.time()
            
            # Make the API call
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                if generated_text:
                    self.logger.info(f"✅ Generated response ({response_time:.1f}s): {generated_text[:50]}...")
                    return generated_text
                else:
                    self.logger.error("❌ Empty response from LLM")
                    return None
            else:
                self.logger.error(f"❌ LLM API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("❌ LLM request timeout")
            return None
        except Exception as e:
            self.logger.error(f"❌ Error generating LLM response: {e}")
            return None
    
    def generate_fallback_response(self, context: CoachingContext) -> str:
        """
        Generate a fallback response when LLM is unavailable.
        
        Args:
            context: The coaching context
            
        Returns:
            Fallback response based on intent
        """
        fallback_responses = {
            MessageIntent.EMOTIONAL: f"I understand you're dealing with some difficult feelings right now. While I can't provide my full response at the moment, I want you to know that what you're experiencing is valid. Take a moment to breathe, and remember that challenging emotions are temporary.",
            
            MessageIntent.PRACTICAL: f"I can see you're looking for practical guidance. While I'm having a technical issue right now, here's a quick suggestion: try breaking down what you need to do into the smallest possible first step, and start there.",
            
            MessageIntent.REFLECTIVE: f"That's a thoughtful question that deserves a deeper response. While I work through a technical issue, I encourage you to sit with that question for a moment. Sometimes our own reflection reveals insights that external advice cannot.",
            
            MessageIntent.MOTIVATIONAL: f"I can sense you're looking for some encouragement right now. Even though I'm having a technical issue, I want you to know that the fact you're reaching out shows strength and self-awareness. You've got this.",
            
            MessageIntent.SOCIAL: f"Relationship situations can be complex and deserve thoughtful discussion. While I'm experiencing a technical issue, consider what outcome you truly want from this situation and what small step might move you toward that.",
            
            MessageIntent.DECISION: f"Decisions can feel overwhelming, especially important ones. While I work through a technical issue, try writing down what matters most to you about this choice. Sometimes clarity comes from seeing our values on paper.",
            
            MessageIntent.PROGRESS: f"Thank you for sharing your progress with me! While I'm having a technical issue that prevents my full response, I want to acknowledge your efforts. Progress isn't always linear, and every step counts.",
            
            MessageIntent.GENERAL: f"I'm experiencing a technical issue right now that's preventing me from giving you the thoughtful response you deserve. Please try again in a moment, and I'll be here to help however I can."
        }
        
        return fallback_responses.get(context.intent, fallback_responses[MessageIntent.GENERAL])
    
    def test_coaching_response(self) -> bool:
        """
        Test the LLM with a simple coaching scenario.
        
        Returns:
            True if test successful, False otherwise
        """
        try:
            test_context = CoachingContext(
                user_message="I'm feeling stuck and don't know what to do next",
                sender="TestUser",
                intent=MessageIntent.MOTIVATIONAL,
                confidence=0.8,
                personal_profile={},
                conversation_history=[],
                relevant_principles=[],
                timestamp=datetime.now()
            )
            
            response = self.generate_response(test_context)
            
            if response and len(response) > 20:
                self.logger.info("✅ LLM coaching test successful")
                return True
            else:
                self.logger.error("❌ LLM coaching test failed - insufficient response")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ LLM coaching test failed: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                for model in models:
                    if model['name'] == self.model_name:
                        return {
                            "name": model['name'],
                            "size": model.get('size', 'Unknown'),
                            "modified": model.get('modified_at', 'Unknown'),
                            "status": "Available"
                        }
                
                return {"status": "Not Found", "available_models": [m['name'] for m in models]}
            else:
                return {"status": "API Error", "code": response.status_code}
                
        except Exception as e:
            return {"status": "Connection Error", "error": str(e)}

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test the LLM client
    client = LLMClient()
    
    print("🤖 LLM Client Test")
    print("=" * 40)
    
    # Test model info
    model_info = client.get_model_info()
    print(f"📋 Model Info: {model_info}")
    
    # Test coaching response
    if client.test_coaching_response():
        print("✅ LLM Client is ready for coaching!")
    else:
        print("❌ LLM Client needs attention")
    
    # Example coaching context
    example_context = CoachingContext(
        user_message="I'm feeling overwhelmed with all my tasks and don't know where to start",
        sender="ExampleUser",
        intent=MessageIntent.EMOTIONAL,
        confidence=0.9,
        personal_profile={
            "communication_style": {
                "tone": "direct but supportive",
                "approach": "practical with empathy"
            }
        },
        conversation_history=[],
        relevant_principles=["Take things one step at a time", "Progress over perfection"],
        timestamp=datetime.now()
    )
    
    print(f"\n🧪 Example Response:")
    response = client.generate_response(example_context)
    if response:
        print(f"📝 {response}")
    else:
        fallback = client.generate_fallback_response(example_context)
        print(f"🔄 Fallback: {fallback}") 