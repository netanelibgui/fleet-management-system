#!/usr/bin/env python3
"""
Twilio Driver - Handles WhatsApp/SMS messaging via Twilio API
Much more reliable than browser automation!
"""

import os
import logging
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

@dataclass
class TwilioMessage:
    """Represents a Twilio message."""
    sender: str
    text: str
    timestamp: datetime
    message_sid: str = ""
    media_urls: List[str] = None
    is_whatsapp: bool = True

class TwilioDriver:
    """
    Handles WhatsApp and SMS messaging using Twilio API.
    Much more reliable than browser automation!
    """
    
    def __init__(self, 
                 account_sid: str = None,
                 auth_token: str = None,
                 whatsapp_number: str = None):
        """
        Initialize Twilio driver.
        
        Args:
            account_sid: Twilio Account SID (or set TWILIO_ACCOUNT_SID env var)
            auth_token: Twilio Auth Token (or set TWILIO_AUTH_TOKEN env var)
            whatsapp_number: Your Twilio WhatsApp number (or set TWILIO_WHATSAPP_NUMBER env var)
        """
        # Get credentials from environment or parameters
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = whatsapp_number or os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            raise ValueError("Missing Twilio credentials. Set environment variables or pass parameters.")
        
        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)
        self.logger = logging.getLogger(__name__)
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test Twilio API connection."""
        try:
            # Test by getting account info
            account = self.client.api.accounts(self.account_sid).fetch()
            self.logger.info(f"✅ Connected to Twilio - Account: {account.friendly_name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Twilio connection failed: {e}")
            return False
    
    def send_whatsapp_message(self, to_number: str, message: str, media_url: str = None, voice_url: str = None) -> bool:
        """
        Send WhatsApp message via Twilio.
        
        Args:
            to_number: Recipient's phone number (with country code, e.g., '+1234567890')
            message: Message text to send
            media_url: Optional URL to media file (image, video, etc.)
            voice_url: Optional URL to voice message file
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Format numbers for WhatsApp
            from_whatsapp = f"whatsapp:{self.whatsapp_number}"
            # Check if to_number already has whatsapp: prefix
            if to_number.startswith('whatsapp:'):
                to_whatsapp = to_number
            else:
                to_whatsapp = f"whatsapp:{to_number}"
            
            # Prepare message parameters
            message_params = {
                'body': message,
                'from_': from_whatsapp,
                'to': to_whatsapp
            }
            
            # Add media if provided
            if media_url:
                message_params['media_url'] = [media_url]
            
            # Add voice message if provided
            if voice_url:
                message_params['media_url'] = message_params.get('media_url', []) + [voice_url]
            
            # Send message
            message_obj = self.client.messages.create(**message_params)
            
            self.logger.info(f"✅ WhatsApp message sent to {to_number}: {message[:50]}...")
            self.logger.debug(f"Message SID: {message_obj.sid}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send WhatsApp message to {to_number}: {e}")
            return False
    
    def send_voice_message(self, to_number: str, voice_file_path: str, message: str = "") -> bool:
        """
        Send voice message via WhatsApp.
        
        Args:
            to_number: Recipient's phone number (with country code)
            voice_file_path: Path to the voice file to send
            message: Optional text message to accompany the voice
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # For voice messages, we need to upload the file to a publicly accessible URL first
            # This is a simplified version - in production you'd want to use a proper file hosting service
            
            # For now, we'll send a text message indicating voice processing
            if message:
                return self.send_whatsapp_message(to_number, f"🎤 Voice message: {message}")
            else:
                return self.send_whatsapp_message(to_number, "🎤 I've processed your voice message and am responding with text.")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to send voice message to {to_number}: {e}")
            return False
    
    def send_sms_message(self, to_number: str, message: str) -> bool:
        """
        Send SMS message via Twilio.
        
        Args:
            to_number: Recipient's phone number (with country code)
            message: Message text to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,  # Can use same number for SMS
                to=to_number
            )
            
            self.logger.info(f"✅ SMS sent to {to_number}: {message[:50]}...")
            self.logger.debug(f"Message SID: {message_obj.sid}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send SMS to {to_number}: {e}")
            return False
    
    def get_message_history(self, 
                           phone_number: str = None, 
                           limit: int = 20) -> List[TwilioMessage]:
        """
        Get message history from Twilio.
        
        Args:
            phone_number: Filter by specific phone number (optional)
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of TwilioMessage objects
        """
        try:
            messages = []
            
            # Get messages from Twilio
            message_list = self.client.messages.list(limit=limit)
            
            for msg in message_list:
                # Filter by phone number if specified
                if phone_number and phone_number not in [msg.to, msg.from_]:
                    continue
                
                # Determine if it's WhatsApp or SMS
                is_whatsapp = msg.from_.startswith('whatsapp:') or msg.to.startswith('whatsapp:')
                
                # Extract phone number (remove whatsapp: prefix if present)
                sender = msg.from_.replace('whatsapp:', '')
                
                # Create message object
                twilio_msg = TwilioMessage(
                    sender=sender,
                    text=msg.body or "",
                    timestamp=msg.date_created,
                    message_sid=msg.sid,
                    media_urls=list(msg.media.list()) if hasattr(msg, 'media') else [],
                    is_whatsapp=is_whatsapp
                )
                
                messages.append(twilio_msg)
            
            self.logger.info(f"✅ Retrieved {len(messages)} messages from Twilio")
            return messages
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get message history: {e}")
            return []
    
    def create_webhook_response(self, incoming_message: str, response_text: str) -> str:
        """
        Create a TwiML response for incoming webhooks.
        
        Args:
            incoming_message: The incoming message text
            response_text: The response to send back
            
        Returns:
            TwiML XML string
        """
        try:
            response = MessagingResponse()
            response.message(response_text)
            
            self.logger.info(f"✅ Created webhook response: {response_text[:50]}...")
            return str(response)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create webhook response: {e}")
            return str(MessagingResponse())  # Empty response
    
    def validate_webhook(self, request_url: str, post_params: dict, signature: str) -> bool:
        """
        Validate incoming webhook signature for security.
        
        Args:
            request_url: The full URL of the webhook request
            post_params: POST parameters from the request
            signature: X-Twilio-Signature header value
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            from twilio.request_validator import RequestValidator
            
            validator = RequestValidator(self.auth_token)
            return validator.validate(request_url, post_params, signature)
            
        except Exception as e:
            self.logger.error(f"❌ Webhook validation failed: {e}")
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get Twilio account information.
        
        Returns:
            Dictionary with account details
        """
        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            
            info = {
                'account_sid': account.sid,
                'friendly_name': account.friendly_name,
                'status': account.status,
                'type': account.type,
                'date_created': account.date_created,
                'whatsapp_number': self.whatsapp_number
            }
            
            self.logger.info("✅ Retrieved account information")
            return info
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get account info: {e}")
            return {}

# Configuration helper
def setup_twilio_config():
    """
    Helper function to set up Twilio configuration.
    Creates a config file with Twilio settings.
    """
    config = {
        "twilio": {
            "account_sid": "YOUR_TWILIO_ACCOUNT_SID",
            "auth_token": "YOUR_TWILIO_AUTH_TOKEN", 
            "whatsapp_number": "YOUR_TWILIO_WHATSAPP_NUMBER",
            "webhook_url": "https://your-domain.com/webhook"
        },
        "coaching": {
            "default_response": "Hi! I'm your personal training assistant. How can I help you today?",
            "enable_media_support": True,
            "max_message_length": 1600
        }
    }
    
    with open('twilio_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created twilio_config.json")
    print("📝 Please update it with your Twilio credentials")

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Check if config exists
    if not os.path.exists('twilio_config.json'):
        print("🔧 Setting up Twilio configuration...")
        setup_twilio_config()
        print("\n📋 Next steps:")
        print("1. Get Twilio credentials from https://console.twilio.com/")
        print("2. Set up WhatsApp Business on Twilio")
        print("3. Update twilio_config.json with your credentials")
        print("4. Set environment variables:")
        print("   export TWILIO_ACCOUNT_SID=your_account_sid")
        print("   export TWILIO_AUTH_TOKEN=your_auth_token")
        print("   export TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890")
    else:
        try:
            # Test the driver (if credentials are set)
            driver = TwilioDriver()
            
            print("🎉 Twilio driver initialized successfully!")
            
            # Show account info
            account_info = driver.get_account_info()
            if account_info:
                print(f"📱 Account: {account_info.get('friendly_name', 'Unknown')}")
                print(f"📞 WhatsApp Number: {account_info.get('whatsapp_number', 'Not set')}")
        
        except Exception as e:
            print(f"❌ Twilio setup incomplete: {e}")
            print("💡 Make sure to set your environment variables!") 