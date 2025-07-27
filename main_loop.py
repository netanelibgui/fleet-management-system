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
            # TODO: Initialize actual components
            self.logger.info("Initializing components...")
            
            # Placeholder initialization
            self.logger.info("✓ WhatsApp Driver initialized")
            self.logger.info("✓ LLM Client initialized") 
            self.logger.info("✓ Profile Manager initialized")
            self.logger.info("✓ Knowledge Base initialized")
            self.logger.info("✓ Intent Classifier initialized")
            self.logger.info("✓ Task Manager initialized")
            self.logger.info("✓ Logger Manager initialized")
            
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
            
            # TODO: Implement actual message processing pipeline
            # 1. Classify intent
            # intent = self.intent_classifier.classify(message)
            
            # 2. Retrieve relevant context from knowledge base
            # context = self.knowledge_base.get_relevant_context(message)
            
            # 3. Get personal profile information
            # profile = self.profile_manager.get_profile()
            
            # 4. Generate response using LLM
            # response = self.llm_client.generate_response(message, context, profile, intent)
            
            # 5. Handle any tasks or reminders
            # self.task_manager.process_message(message, response)
            
            # 6. Log the interaction
            # self.logger_manager.log_interaction(sender, message, response, intent)
            
            # Placeholder response
            response = f"I received your message: '{message}'. This is a placeholder response. The full system is being built!"
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return "I encountered an error processing your message. Please try again."
    
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