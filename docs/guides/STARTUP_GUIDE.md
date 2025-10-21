# Fleet Management System - Startup Guide

This guide provides detailed instructions for starting and managing the Fleet Management System.

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)
```bash
start_fleet_system.bat
```

This single command will:
1. Clean up any existing processes
2. Start ngrok tunnel
3. Launch the webhook server
4. Sync Excel data
5. Check system status
6. Guide you through webhook setup

### Option 2: Manual Management
```bash
manage_fleet_system.bat
```

Choose from the menu:
- `[1]` Start System (Full Initialization)
- `[2]` Sync Data from Excel
- `[3]` Check System Status
- `[4]` Get Webhook URL (Manual Update)
- `[5]` Stop System
- `[6]` Restart System
- `[7]` View Logs

## 📋 Prerequisites

Before starting the system, ensure you have:

### Required Software
- ✅ Python 3.8+ installed
- ✅ ngrok installed and accessible
- ✅ Twilio account with WhatsApp Sandbox

### Required Files
- ✅ `Large_Enhanced_Fleet_Report_20251018_230415.xlsx` (main data file)
- ✅ `config/twilio_config.json` (configured with your credentials)

### Network Requirements
- ✅ Internet connection
- ✅ Port 5000 available
- ✅ Firewall allows ngrok connections

## 🔧 Initial Setup

### Step 1: Configure Twilio Credentials
```bash
setup_twilio_credentials.bat
```

Enter your Twilio details:
- Account SID
- Auth Token
- WhatsApp Number

### Step 2: Verify Installation
```bash
python scripts/check_system_status.py
```

Expected output:
```
Fleet Management System - Status Check
==================================================
Checking Python processes... Status: Running
Checking ngrok tunnel... Status: Not running
Checking main server... Status: Not running
Checking data files... Vehicle catalog: Found
Checking configuration... Twilio config: Found
==================================================
Overall Status: Ready to Start
```

## 🚀 Starting the System

### Automated Startup Process

When you run `start_fleet_system.bat`, the system will:

#### Phase 1: Process Cleanup
```
[1/6] Cleaning up existing processes...
- Terminating Python processes
- Stopping ngrok tunnels
- Clearing port 5000
```

#### Phase 2: ngrok Tunnel
```
[2/6] Starting ngrok tunnel...
- Launching ngrok on port 5000
- Waiting for tunnel establishment
- Verifying tunnel status
```

#### Phase 3: Server Startup
```
[3/6] Starting webhook server...
- Launching Flask server on port 5000
- Initializing webhook endpoints
- Starting background processes
```

#### Phase 4: Data Synchronization
```
[4/6] Synchronizing Excel data...
- Loading vehicle catalog
- Updating maintenance records
- Processing fault reports
- Syncing 220+ vehicles
```

#### Phase 5: System Verification
```
[5/6] Checking system status...
- Verifying server health
- Testing data integrity
- Confirming all services running
```

#### Phase 6: Webhook Configuration
```
[6/6] Getting webhook URL for manual update...

========================================
   MANUAL TWILIO WEBHOOK UPDATE
========================================

Current ngrok URL: https://abc123.ngrok-free.app
Webhook URL: https://abc123.ngrok-free.app/webhook

Please update Twilio webhook URL:
1. Go to: https://console.twilio.com
2. Navigate to: Messaging > Settings > WhatsApp sandbox settings
3. Set webhook URL to: https://abc123.ngrok-free.app/webhook
4. Save configuration

Press ENTER after updating Twilio...
```

## 📱 Testing the System

### Test Vehicle Search
Send to WhatsApp: `חיפוש 56-722-64`

Expected response:
```
**תוצאות חיפוש רכב**

**פרטי הרכב:**
• מספר רישוי: 56-722-64
• יצרן/דגם: Volvo V90
• שנה: 2021
• צבע: Gray
• סטטוס: active

**פרטי נהג:**
• שם נהג: יוסי כהן
• טלפון: +972-55-4669164
• אימייל: יוסי.כהן@company.co.il
```

### Test Maintenance Report
Send to WhatsApp: `דוח תחזוקה 56-722-64`

Expected: PDF file attachment with maintenance report

### Test Fault Report
Send to WhatsApp: `דוח תקלות 56-722-64`

Expected: PDF file attachment with fault report

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Issue: "No response from WhatsApp"
**Symptoms:**
- Messages sent but no response received
- System appears to be running

**Solutions:**
1. Check webhook URL in Twilio console
2. Verify ngrok is running: `ngrok http 5000`
3. Restart the system: `manage_fleet_system.bat` → Option 6

#### Issue: "Cannot connect to server"
**Symptoms:**
- Error: "Connection refused"
- Server not responding

**Solutions:**
1. Check if server is running: `python scripts/check_system_status.py`
2. Restart server: `manage_fleet_system.bat` → Option 6
3. Check port 5000 availability

#### Issue: "Vehicle not found"
**Symptoms:**
- Search returns "vehicle not found"
- Data appears outdated

**Solutions:**
1. Sync data: `manage_fleet_system.bat` → Option 2
2. Check Excel file exists and has data
3. Verify license plate format (e.g., 56-722-64)

#### Issue: "UnicodeEncodeError"
**Symptoms:**
- Console shows encoding errors
- Scripts fail to run

**Solutions:**
1. All emojis have been removed from the codebase
2. Ensure you're using the latest version
3. Check Windows console encoding settings

### System Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ Running | All systems operational | Ready to use |
| ⚠️ Partial | Some components down | Check logs, restart |
| ❌ Error | System not functional | Full restart required |

## 📊 Monitoring

### Real-time Status
```bash
python scripts/check_system_status.py
```

### View Logs
```bash
manage_fleet_system.bat
# Choose option 7: View Logs
```

### System Health Check
The system automatically monitors:
- Python processes
- ngrok tunnel status
- Server health
- Data file integrity
- Twilio configuration

## 🔄 Maintenance

### Daily Operations
1. Start system: `start_fleet_system.bat`
2. Test with sample queries
3. Monitor for any issues

### Weekly Maintenance
1. Sync Excel data: `manage_fleet_system.bat` → Option 2
2. Check system logs
3. Verify data integrity

### Monthly Maintenance
1. Update Excel data file
2. Review system performance
3. Clean up old PDF reports

## 🛑 Shutting Down

### Graceful Shutdown
```bash
manage_fleet_system.bat
# Choose option 5: Stop System
```

### Force Stop
```bash
taskkill /F /IM python.exe
taskkill /F /IM ngrok.exe
```

## 📞 Support

If you encounter issues not covered in this guide:

1. Check the main README.md
2. Review system logs in `logs/` directory
3. Verify all prerequisites are met
4. Try a full system restart

---

**Note**: This system is designed for professional fleet management and requires proper Twilio setup for full functionality.
