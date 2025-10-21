@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🔧 Twilio Credentials Setup
echo ========================================
echo.
echo This will help you configure your Twilio credentials for automatic webhook updates.
echo.
echo You can find these values in your Twilio Console:
echo https://console.twilio.com/
echo.

set /p account_sid="Enter your Twilio Account SID: "
set /p auth_token="Enter your Twilio Auth Token: "
set /p whatsapp_number="Enter your Twilio WhatsApp Number (e.g., +1234567890): "

echo.
echo Updating Twilio configuration...

python -c "
import json
import os

# Load current config
config_path = 'config/twilio_config.json'
if os.path.exists(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {'twilio': {}, 'coaching': {}}

# Update Twilio credentials
config['twilio']['account_sid'] = '%account_sid%'
config['twilio']['auth_token'] = '%auth_token%'
config['twilio']['whatsapp_number'] = '%whatsapp_number%'
config['twilio']['webhook_url'] = 'https://your-domain.com/webhook'  # Will be updated automatically

# Save updated config
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print('✅ Twilio credentials updated successfully!')
print('✅ Automatic webhook updates will now work!')
"

echo.
echo ✅ Setup completed! Now when you run the system, it will automatically update the webhook URL.
echo.
echo Next steps:
echo 1. Run manage_fleet_system.bat
echo 2. The system will automatically update your Twilio webhook URL
echo 3. No more manual copying needed!
echo.
pause
