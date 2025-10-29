@echo off
chcp 65001 >nul
title Fleet Management System - Control Panel

:menu
cls
echo.
echo ========================================
echo    🚗 Fleet Management System
echo    📋 Control Panel
echo ========================================
echo.
echo [1] 🚀 Start System (Full Initialization)
echo [2] 🔄 Sync Data from Excel
echo [3] 🔍 Check System Status
echo [4] 🌐 Get Webhook URL (Manual Update)
echo [5] 🛑 Stop System
echo [6] 🔧 Restart System
echo [7] 📊 View Logs
echo [8] ❌ Exit
echo.
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto start_system
if "%choice%"=="2" goto sync_data
if "%choice%"=="3" goto check_status
if "%choice%"=="4" goto update_webhook
if "%choice%"=="5" goto stop_system
if "%choice%"=="6" goto restart_system
if "%choice%"=="7" goto view_logs
if "%choice%"=="8" goto exit
goto menu

:start_system
cls
echo.
echo 🚀 Starting Fleet Management System...
echo ========================================
echo.

echo [1/4] Cleaning up existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im ngrok.exe 2>nul
timeout /t 2 >nul
echo ✅ Cleanup complete
echo.

echo [2/4] Starting ngrok tunnel...
start /B ngrok http 5000
timeout /t 5 >nul
echo ✅ Ngrok started
echo.

echo [3/4] Starting webhook server...
start /B python src/services/simple_server.py
timeout /t 3 >nul
echo ✅ Server started
echo.

echo [4/4] Getting webhook URL...
timeout /t 2 >nul
python scripts/start_system.py
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:update_webhook
cls
echo.
echo 🌐 Get Webhook URL for Manual Update
echo ========================================
echo.
call get_webhook_url.bat
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:sync_data
cls
echo.
echo 🔄 Synchronizing data from Excel...
echo ========================================
echo.
python scripts/sync_excel_data.py
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:check_status
cls
echo.
echo 🔍 Checking system status...
echo ========================================
echo.
python scripts/check_system_status.py
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:stop_system
cls
echo.
echo 🛑 Stopping Fleet Management System...
echo ========================================
echo.
echo Stopping Python processes...
taskkill /f /im python.exe 2>nul
echo Stopping ngrok processes...
taskkill /f /im ngrok.exe 2>nul
echo.
echo ✅ System stopped successfully!
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:restart_system
cls
echo.
echo 🔧 Restarting Fleet Management System...
echo ========================================
echo.
echo Stopping existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im ngrok.exe 2>nul
timeout /t 3 >nul
echo ✅ Processes stopped
echo.
goto start_system

:view_logs
cls
echo.
echo 📊 System Logs
echo ========================================
echo.
if exist "logs\system_status.json" (
    echo System Status Log:
    type "logs\system_status.json"
) else (
    echo No status logs found.
)
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:exit
cls
echo.
echo 👋 Goodbye!
echo.
exit /b 0
