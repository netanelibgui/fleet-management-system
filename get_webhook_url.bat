@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    Get Current Webhook URL
echo ========================================
echo.

python -c "
import requests
import json

try:
    response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
    data = response.json()
    
    ngrok_url = None
    for tunnel in data.get('tunnels', []):
        if tunnel.get('proto') == 'https':
            ngrok_url = tunnel.get('public_url')
            break
    
    if ngrok_url:
        webhook_url = f'{ngrok_url}/webhook'
        print('Current ngrok URL:', ngrok_url)
        print('Webhook URL:', webhook_url)
        print()
        print('Copy this URL to Twilio Console:')
        print('https://console.twilio.com')
        print('Navigate to: Messaging > Settings > WhatsApp sandbox settings')
        print('Set webhook URL to:', webhook_url)
    else:
        print('ERROR: Could not get ngrok URL. Is ngrok running?')
        
except Exception as e:
    print(f'ERROR: {e}')
"

echo.
pause
