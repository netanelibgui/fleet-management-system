#!/usr/bin/env python3
"""
Start Fleet Management System
Starts ngrok and the Flask server, then displays webhook URL
"""

import time
import sys
import requests

def get_ngrok_url(max_retries=10, delay=2):
    """Get ngrok URL with retries"""
    for attempt in range(max_retries):
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            data = response.json()
            
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
            
            if attempt < max_retries - 1:
                time.sleep(delay)
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    return None

def main():
    print("\n========================================")
    print("   SYSTEM STARTED SUCCESSFULLY")
    print("========================================\n")
    
    print("Server: http://localhost:5000")
    
    # Get ngrok URL
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        webhook_url = f"{ngrok_url}/webhook"
        print(f"Ngrok URL: {ngrok_url}")
        print(f"Webhook URL: {webhook_url}")
        print("\nSystem is ready!")
        print("\nPlease update Twilio webhook URL:")
        print("1. Go to: https://console.twilio.com")
        print("2. Navigate to: Messaging > Settings > WhatsApp sandbox settings")
        print(f"3. Set webhook URL to: {webhook_url}")
        print("4. Save configuration")
    else:
        print("WARNING: Ngrok URL not yet available")
        print("TIP: Use option 4 to get the webhook URL once ngrok is ready")
    
    print("\n========================================\n")

if __name__ == "__main__":
    main()

