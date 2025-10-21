# Fleet Management System

A comprehensive WhatsApp-based fleet management system that enables users to search for vehicles, generate maintenance reports, and manage fault reports through simple text messages.

## 🚀 Features

### Core Functionality
- **Vehicle Search**: Find vehicle information by license plate
- **Maintenance Reports**: Generate PDF maintenance reports for any vehicle
- **Fault Reports**: Create and manage vehicle fault reports
- **Multi-language Support**: Full Hebrew and English support
- **Real-time Sync**: Excel data synchronization with JSON database

### Technical Features
- **WhatsApp Integration**: Direct communication via Twilio WhatsApp API
- **PDF Generation**: Professional Hebrew PDF reports with RTL support
- **Excel Integration**: Automatic data synchronization from Excel files
- **Fuzzy Search**: Intelligent vehicle search with partial matching
- **Webhook Support**: Real-time message processing

## 📁 Project Structure

```
Fleet Management System/
├── src/                          # Core application code
│   ├── core/                     # Core business logic
│   │   ├── maintenance_tracker.py    # Maintenance tracking system
│   │   ├── system_manager.py         # System management utilities
│   │   └── template_hebrew_pdf.py    # Hebrew PDF report generator
│   └── services/                 # External service integrations
│       ├── simple_server.py          # Main Flask webhook server
│       └── twilio_driver.py          # Twilio WhatsApp integration
├── scripts/                      # Utility scripts
│   ├── check_system_status.py       # System health monitoring
│   └── excel_sync_manager.py        # Excel data synchronization
├── data/                         # Data storage
│   ├── large_vehicle_catalog.json   # Main vehicle database
│   ├── gazetteer.json              # Keyword mapping for search
│   ├── fault_reports.json          # Fault report summaries
│   └── vehicles/
│       └── maintenance_records.json # Detailed maintenance records
├── config/                       # Configuration files
│   ├── twilio_config.json          # Twilio API credentials
│   └── requirements.txt            # Python dependencies
├── reports/                      # Generated PDF reports
│   └── maintenance_reports/         # Vehicle maintenance PDFs
├── logs/                         # System logs
└── docs/                         # Documentation
    ├── archive/                     # Historical documentation
    └── guides/                      # User guides
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Twilio Account with WhatsApp Sandbox
- ngrok (for local development)

### 1. Install Dependencies
```bash
pip install -r config/requirements.txt
```

### 2. Configure Twilio
Run the setup script to configure your Twilio credentials:
```bash
setup_twilio_credentials.bat
```

### 3. Start the System
Use the main startup script:
```bash
start_fleet_system.bat
```

## 🚀 Quick Start Guide

### Starting the System

The `start_fleet_system.bat` script provides a complete system initialization:

1. **Process Cleanup**: Terminates any existing Python/ngrok processes
2. **ngrok Tunnel**: Starts ngrok to expose local server to internet
3. **Server Startup**: Launches the Flask webhook server
4. **Data Sync**: Synchronizes Excel data with JSON database
5. **Status Check**: Verifies all components are running
6. **Webhook Setup**: Provides ngrok URL for Twilio webhook configuration

### Manual Webhook Configuration

When you run `start_fleet_system.bat`, you'll see:
```
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

### Alternative Management

For advanced users, use the management interface:
```bash
manage_fleet_system.bat
```

Options available:
- Start System (Full Initialization)
- Sync Data from Excel
- Check System Status
- Get Webhook URL (Manual Update)
- Stop System
- Restart System
- View Logs

## 📱 WhatsApp Commands

### Vehicle Search
```
חיפוש [license_plate]
search [license_plate]
```
Example: `חיפוש 56-722-64`

### Maintenance Report
```
דוח תחזוקה [license_plate]
maintenance report [license_plate]
```
Example: `דוח תחזוקה 56-722-64`

### Fault Report
```
דוח תקלות [license_plate]
fault report [license_plate]
```
Example: `דוח תקלות 56-722-64`

## 📊 Data Management

### Excel Integration
The system automatically synchronizes data from `Large_Enhanced_Fleet_Report_20251018_230415.xlsx`:

- **Vehicle Information**: License plates, make, model, year, driver details
- **Maintenance Data**: Service dates, costs, status
- **Fault Records**: Repair requests, fault types, costs

### Manual Data Sync
To manually sync Excel data:
```bash
python scripts/excel_sync_manager.py
```

### System Status Check
Monitor system health:
```bash
python scripts/check_system_status.py
```

## 🔧 Configuration

### Twilio Setup
1. Create a Twilio account
2. Set up WhatsApp Sandbox
3. Run `setup_twilio_credentials.bat`
4. Enter your Account SID, Auth Token, and WhatsApp Number

### Excel Data Format
The system expects Excel files with these columns:
- `License Plate`: Vehicle license plate number
- `Make`: Vehicle manufacturer
- `Model`: Vehicle model
- `Driver Name`: Driver's name
- `Driver Phone`: Driver's phone number
- `Driver Email`: Driver's email address
- And many more...

## 📋 System Requirements

### Hardware
- Windows 10/11
- 4GB RAM minimum
- 1GB free disk space

### Software
- Python 3.8+
- ngrok (for webhook tunneling)
- Microsoft Excel (for data management)

### Network
- Internet connection for Twilio API
- Port 5000 available for local server

## 🐛 Troubleshooting

### Common Issues

**"No response from WhatsApp"**
- Check if ngrok is running: `ngrok http 5000`
- Verify webhook URL in Twilio console
- Ensure server is running on port 5000

**"UnicodeEncodeError"**
- All emojis have been removed from the codebase
- Ensure you're using the latest version of the scripts

**"Vehicle not found"**
- Run data sync: `python scripts/excel_sync_manager.py`
- Check if license plate exists in Excel file
- Verify license plate format (e.g., 56-722-64)

### Getting Help

1. Check system status: `python scripts/check_system_status.py`
2. View logs in `logs/` directory
3. Run management interface: `manage_fleet_system.bat`

## 📈 Performance

- **Response Time**: < 2 seconds for vehicle search
- **PDF Generation**: < 5 seconds for maintenance reports
- **Data Sync**: < 30 seconds for 220+ vehicles
- **Concurrent Users**: Supports multiple WhatsApp users simultaneously

## 🔒 Security

- **API Keys**: Stored securely in `config/twilio_config.json`
- **Data Privacy**: All data stored locally
- **Webhook Security**: Validates incoming requests from Twilio
- **No External Dependencies**: Works offline after initial setup

## 📝 License

This project is developed for educational and portfolio purposes.

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome.

## 📞 Support

For technical support or questions about this fleet management system, please refer to the documentation in the `docs/` directory.

---

**Fleet Management System v1.0**  
*Professional WhatsApp-based vehicle management solution*