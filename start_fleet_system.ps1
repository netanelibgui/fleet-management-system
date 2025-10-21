# Fleet Management System - PowerShell Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🚗 Fleet Management System Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/5] Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process ngrok -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "[2/5] Starting ngrok tunnel..." -ForegroundColor Yellow
Start-Process -FilePath "ngrok" -ArgumentList "http", "5000" -WindowStyle Hidden
Start-Sleep -Seconds 5

Write-Host "[3/5] Starting main server..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "src/services/simple_server.py" -WindowStyle Hidden
Start-Sleep -Seconds 3

Write-Host "[4/5] Checking system status..." -ForegroundColor Yellow
python scripts/check_system_status.py

Write-Host "[5/5] Getting webhook URL for manual update..." -ForegroundColor Yellow

# Get ngrok URL and display it for manual update
try {
    $ngrokResponse = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -TimeoutSec 5
    $ngrokUrl = $null
    
    foreach ($tunnel in $ngrokResponse.tunnels) {
        if ($tunnel.proto -eq "https") {
            $ngrokUrl = $tunnel.public_url
            break
        }
    }
    
    if ($ngrokUrl) {
        $webhookUrl = "$ngrokUrl/webhook"
        
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "   MANUAL TWILIO WEBHOOK UPDATE" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Current ngrok URL: $ngrokUrl" -ForegroundColor Green
        Write-Host "Webhook URL: $webhookUrl" -ForegroundColor Green
        Write-Host ""
        Write-Host "Please update Twilio webhook URL:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://console.twilio.com" -ForegroundColor White
        Write-Host "2. Navigate to: Messaging > Settings > WhatsApp sandbox settings" -ForegroundColor White
        Write-Host "3. Set webhook URL to: $webhookUrl" -ForegroundColor White
        Write-Host "4. Save configuration" -ForegroundColor White
        Write-Host ""
        Write-Host "Press ENTER after updating Twilio..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        
        Write-Host ""
        Write-Host "Testing webhook connection..." -ForegroundColor Yellow
        Write-Host "Send a test message to WhatsApp to verify connection works" -ForegroundColor White
        Write-Host ""
        Write-Host "Press ENTER when ready to continue..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        
    } else {
        Write-Host "ERROR: Could not get ngrok URL" -ForegroundColor Red
    }
} catch {
    Write-Host "ERROR: Could not get ngrok URL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "[6/6] System initialization completed!" -ForegroundColor Green
Write-Host ""
Write-Host "System is ready! You can now use WhatsApp to interact with the fleet management system." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
