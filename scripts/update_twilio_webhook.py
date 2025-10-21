#!/usr/bin/env python3
"""
Script to automatically update Twilio webhook URL when ngrok starts
"""

import os
import sys
import json
import time
import requests
from twilio.rest import Client

def get_ngrok_url():
    """Get the current ngrok public URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        data = response.json()
        
        for tunnel in data.get('tunnels', []):
            if tunnel.get('proto') == 'https':
                return tunnel.get('public_url')
        
        return None
    except Exception as e:
        print(f"ERROR: Error getting ngrok URL: {e}")
        return None

def load_twilio_config():
    """Load Twilio configuration"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'twilio_config.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        twilio_config = config.get('twilio', {})
        account_sid = twilio_config.get('account_sid')
        auth_token = twilio_config.get('auth_token')
        
        # Check if credentials are real (not placeholders)
        if (account_sid and auth_token and 
            account_sid != 'YOUR_TWILIO_ACCOUNT_SID' and 
            auth_token != 'YOUR_TWILIO_AUTH_TOKEN'):
            return account_sid, auth_token
        else:
            print("WARNING: Twilio credentials are not configured (placeholder values)")
            return None, None
            
    except Exception as e:
        print(f"ERROR: Error loading Twilio config: {e}")
        return None, None

def update_webhook_url(account_sid, auth_token, webhook_url):
    """Update Twilio webhook URL"""
    try:
        client = Client(account_sid, auth_token)
        
        # Get WhatsApp sandbox configuration
        messaging_services = client.messaging.v1.services.list()
        
        if not messaging_services:
            print("❌ No messaging services found in Twilio account")
            return False
        
        # Update webhook for WhatsApp sandbox
        for service in messaging_services:
            try:
                # Update the service webhook
                service.update(
                    webhook_url=webhook_url,
                    webhook_method='POST'
                )
                print(f"SUCCESS: Updated webhook URL for service {service.sid}: {webhook_url}")
                return True
            except Exception as e:
                print(f"WARNING: Could not update service {service.sid}: {e}")
                continue
        
        print("ERROR: No services could be updated")
        return False
        
    except Exception as e:
        print(f"ERROR: Error updating Twilio webhook: {e}")
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Twilio webhook URL')
    parser.add_argument('--webhook_url', help='Specific webhook URL to use')
    parser.add_argument('--test', action='store_true', help='Test mode - just verify credentials')
    args = parser.parse_args()
    
    print("Twilio Webhook Updater")
    print("=" * 40)
    
    # Load Twilio config first
    print("Loading Twilio configuration...")
    account_sid, auth_token = load_twilio_config()
    
    if not account_sid or not auth_token:
        print("ERROR: Twilio credentials not configured!")
        print("   Please run setup_twilio_credentials.bat first")
        return 1
    
    if args.test:
        print("SUCCESS: Twilio credentials are configured")
        print(f"   Account SID: {account_sid[:8]}...")
        return 0
    
    # Get ngrok URL
    if args.webhook_url:
        webhook_url = args.webhook_url
        print(f"Using provided webhook URL: {webhook_url}")
    else:
        print("Getting ngrok URL...")
        ngrok_url = get_ngrok_url()
        
        if not ngrok_url:
            print("ERROR: Could not get ngrok URL. Is ngrok running?")
            return 1
        
        webhook_url = f"{ngrok_url}/webhook"
        print(f"Webhook URL: {webhook_url}")
    
    # Update webhook
    print("\nUpdating Twilio webhook URL...")
    success = update_webhook_url(account_sid, auth_token, webhook_url)
    
    if success:
        print("\nSUCCESS: Webhook URL updated successfully!")
        print("WhatsApp messages should now work!")
    else:
        print("\nERROR: Failed to update webhook URL")
        print("   Please update manually in Twilio Console:")
        print(f"   {webhook_url}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
