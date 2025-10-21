@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚗 Fleet Management System Startup
echo ========================================
echo.

echo [1/4] Initializing system components...
python -c "import sys; print('Python version:', sys.version)" 2>nul
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

echo [2/4] Checking dependencies...
python -c "import flask, reportlab, twilio, pandas" 2>nul
if errorlevel 1 (
    echo ❌ Missing dependencies! Installing...
    pip install -r config/requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo [3/4] Starting Fleet Management System...
echo.
echo 🚀 Initializing system with automatic webhook updates...
echo.

REM Use the PowerShell script that handles everything automatically
powershell -ExecutionPolicy Bypass -File "start_fleet_system.ps1"

echo.
echo [4/4] System startup completed.
echo.
echo Press any key to exit...
pause >nul