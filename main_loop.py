#!/usr/bin/env python3
"""
Personal Coaching Assistant - Main Loop
Handles WhatsApp input, invokes LLM, and orchestrates the coaching system.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import modules (to be implemented)
# from whatsapp_driver import WhatsAppDriver
# from llm_client import LLMClient
# from profile_manager import ProfileManager
# from knowledge_base import KnowledgeBase
# from intent_classifier import IntentClassifier
# from task_manager import TaskManager
# from logger_manager import LoggerManager

class PersonalCoachingAssistant:
    """
    Main orchestrator for the Personal Coaching Assistant.
    Manages the conversation flow between WhatsApp and the LLM.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the coaching assistant."""
        self.config_path = config_path
        self.running = False
        
        # Initialize components (placeholders for now)
        self.whatsapp_driver = None  # WhatsAppDriver()
        self.llm_client = None       # LLMClient()
        self.profile_manager = None  # ProfileManager()
        self.knowledge_base = None   # KnowledgeBase()
        self.intent_classifier = None  # IntentClassifier()
        self.task_manager = None     # TaskManager()
        self.logger_manager = None   # LoggerManager()
        
        self.setup_logging()
        self.load_configuration()
        
    def setup_logging(self):
        """Set up logging configuration."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"coaching_assistant_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_configuration(self):
        """Load system configuration."""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.create_default_config()
                self.save_configuration()
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            self.config = self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        return {
            "llm": {
                "model": "mistral:latest",
                "temperature": 0.7,
                "max_tokens": 500
            },
            "whatsapp": {
                "check_interval": 2,
                "response_delay": 1
            },
            "profile": {
                "file": "profile.json"
            },
            "reminders": {
                "file": "reminders.xlsx"
            }
        }
    
    def save_configuration(self):
        """Save current configuration."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
    
    def initialize_components(self):
        """Initialize all system components."""
        try:
            self.logger.info("Initializing components...")
            
            # Initialize WhatsApp driver
            from whatsapp_driver import WhatsAppDriver
            self.whatsapp_driver = WhatsAppDriver(headless=False)
            self.logger.info("✓ WhatsApp Driver initialized")
            
            # Initialize intent classifier
            from intent_classifier import IntentClassifier
            self.intent_classifier = IntentClassifier()
            self.logger.info("✓ Intent Classifier initialized")
            
            # Initialize LLM client
            from llm_client import LLMClient
            self.llm_client = LLMClient()
            self.logger.info("✓ LLM Client initialized")
            
            # Initialize conversation history tracking
            self.conversation_history = []
            self.logger.info("✓ Conversation History initialized")
            
            # Load profile from profile.json
            profile_path = Path(self.config.get('profile', {}).get('file', 'profile.json'))
            if profile_path.exists():
                with open(profile_path, 'r', encoding='utf-8') as f:
                    self.profile = json.load(f)
                self.logger.info("✓ Profile loaded from profile.json")
            else:
                self.profile = {}
                self.logger.warning("⚠️ Profile file not found - using empty profile")
            
            # TODO: Initialize additional components when ready
            # self.knowledge_base = KnowledgeBase()
            # self.task_manager = TaskManager()
            
            self.logger.info("✓ All core components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing components: {e}")
            return False
    
    def process_message(self, message: str, sender: str) -> Optional[str]:
        """
        Process incoming WhatsApp message and generate response.
        
        Args:
            message: The incoming message text
            sender: The sender identifier
            
        Returns:
            Generated response or None if no response needed
        """
        try:
            self.logger.info(f"Processing message from {sender}: {message[:50]}...")
            
            # 1. Classify intent
            if not hasattr(self, 'intent_classifier'):
                from intent_classifier import IntentClassifier
                self.intent_classifier = IntentClassifier()
            
            intent_result = self.intent_classifier.classify_intent(message)
            self.logger.info(f"Classified intent: {intent_result.intent.value} (confidence: {intent_result.confidence:.2f})")
            
            # 2. Load personal profile
            profile = getattr(self, 'profile', {})
            
            # 3. Get relevant principles from profile
            relevant_principles = []
            if 'principles' in profile:
                # For now, use all principles - can be enhanced with RAG later
                relevant_principles = profile['principles'][:3]  # Limit to top 3
            
            # 4. Build conversation history (simplified - last few exchanges)
            conversation_history = getattr(self, 'conversation_history', [])
            
            # 5. Create coaching context
            from llm_client import CoachingContext
            context = CoachingContext(
                user_message=message,
                sender=sender,
                intent=intent_result.intent,
                confidence=intent_result.confidence,
                personal_profile=profile,
                conversation_history=conversation_history[-4:],  # Last 2 exchanges
                relevant_principles=relevant_principles,
                timestamp=datetime.now()
            )
            
            # 6. Generate response using LLM
            if not hasattr(self, 'llm_client'):
                from llm_client import LLMClient
                self.llm_client = LLMClient()
            
            response = self.llm_client.generate_response(context)
            
            # 7. Use fallback if LLM fails
            if not response:
                response = self.llm_client.generate_fallback_response(context)
                self.logger.warning("Using fallback response due to LLM failure")
            
            # 8. Update conversation history
            if not hasattr(self, 'conversation_history'):
                self.conversation_history = []
            
            self.conversation_history.append({
                'user': message,
                'assistant': response,
                'intent': intent_result.intent.value,
                'timestamp': datetime.now().isoformat(),
                'sender': sender
            })
            
            # Keep only last 10 exchanges to manage memory
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # 9. Handle any tasks or reminders (if message indicates scheduling need)
            try:
                self._handle_task_creation(message, response, intent_result, sender)
            except AttributeError:
                pass  # Method will be added later
            
            # 10. Log the interaction
            try:
                self._log_interaction(sender, message, response, intent_result)
            except AttributeError:
                pass  # Method will be added later
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return "I encountered an error processing your message. Please try again. If this continues, there might be a technical issue I need to resolve."
    
    def run(self):
        """Main execution loop."""
        self.logger.info("Starting Personal Coaching Assistant...")
        
        if not self.initialize_components():
            self.logger.error("Failed to initialize components. Exiting.")
            return
        
        self.running = True
        self.logger.info("✓ Personal Coaching Assistant is running!")
        
        try:
            while self.running:
                # TODO: Implement actual message checking and processing
                # messages = self.whatsapp_driver.get_new_messages()
                # for message in messages:
                #     response = self.process_message(message.text, message.sender)
                #     if response:
                #         self.whatsapp_driver.send_message(message.sender, response)
                
                # Placeholder - just sleep for now
                time.sleep(self.config["whatsapp"]["check_interval"])
                
        except KeyboardInterrupt:
            self.logger.info("Shutting down Personal Coaching Assistant...")
            self.running = False
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources before shutdown."""
        self.logger.info("Cleaning up resources...")
        # TODO: Cleanup components
        self.logger.info("✓ Cleanup completed")
    
    def stop(self):
        """Stop the assistant."""
        self.running = False

def main():
    """Entry point for the application."""
    assistant = PersonalCoachingAssistant()
    
    try:
        assistant.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 