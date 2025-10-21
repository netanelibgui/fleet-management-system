# 🚗 **Fleet Management System - Management Guide**

## 📋 **System Overview**

The Fleet Management System now includes comprehensive management tools for initialization, data synchronization, and system monitoring.

## 🎯 **Management Components**

### **1. System Manager** (`src/core/system_manager.py`)
- **Purpose**: Central system management and initialization
- **Features**:
  - Process cleanup and restart
  - Excel data synchronization
  - Fault report updates
  - ngrok tunnel management
  - Main server startup

### **2. Data Synchronization** (`scripts/sync_excel_data.py`)
- **Purpose**: Update JSON data from Excel files
- **Features**:
  - Vehicle catalog updates
  - Maintenance records updates
  - Fault report generation
  - Data validation and error handling

### **3. System Status Checker** (`scripts/check_system_status.py`)
- **Purpose**: Monitor system health and components
- **Features**:
  - Python process monitoring
  - ngrok tunnel status
  - Server health checks
  - Data file validation
  - Configuration verification

## 🚀 **Startup Scripts**

### **1. Main Management** (`manage_fleet_system.bat`)
- **Purpose**: Complete system initialization
- **Process**:
  1. Check Python installation
  2. Install/verify dependencies
  3. Initialize system components
  4. Start ngrok tunnel
  5. Start main server

### **2. System Management** (`manage_fleet_system.bat`)
- **Purpose**: Control panel for system management
- **Options**:
  - Start System (Full Initialization)
  - Sync Data from Excel
  - Check System Status
  - Stop System
  - Restart System
  - View Logs
  - Exit

## 🔄 **Data Synchronization Process**

### **Excel to JSON Sync**
1. **Read Excel Data**:
   - `Fleet Overview` sheet → Vehicle catalog
   - `Maintenance Records` sheet → Maintenance records

2. **Data Processing**:
   - Clean and validate data
   - Convert to JSON format
   - Handle missing values
   - Generate unique IDs

3. **JSON Updates**:
   - `data/large_vehicle_catalog.json` - Vehicle database
   - `data/vehicles/maintenance_records.json` - Maintenance records
   - `data/fault_reports.json` - Fault summary

### **Fault Report Generation**
- **Source**: Maintenance records with fault data
- **Processing**: Filter fault records, generate summaries
- **Output**: Fault statistics and cost analysis

## 📊 **System Monitoring**

### **Status Checks**
- **Python Processes**: Running server processes
- **ngrok Tunnel**: Public URL availability
- **Main Server**: Health endpoint response
- **Data Files**: JSON file existence and validity
- **Configuration**: Twilio and system config

### **Health Endpoints**
- **Server Health**: `http://localhost:5000/health`
- **ngrok Status**: `http://localhost:4040/api/tunnels`
- **System Status**: `logs/system_status.json`

## 🛠️ **Usage Instructions**

### **1. First Time Setup**
```bash
# Run the main startup script
manage_fleet_system.bat
```

### **2. Data Updates**
```bash
# Sync data from Excel
python scripts/sync_excel_data.py

# Or use the management panel
manage_fleet_system.bat
```

### **3. System Monitoring**
```bash
# Check system status
python scripts/check_system_status.py

# Or use the management panel
manage_fleet_system.bat
```

### **4. System Management**
```bash
# Use the control panel
manage_fleet_system.bat
```

## 🔧 **Configuration**

### **Required Files**
- `config/twilio_config.json` - Twilio configuration
- `config/requirements.txt` - Python dependencies
- `Large_Enhanced_Fleet_Report_20251018_230415.xlsx` - Excel data source

### **Data Files**
- `data/large_vehicle_catalog.json` - Vehicle database
- `data/vehicles/maintenance_records.json` - Maintenance records
- `data/fault_reports.json` - Fault summary
- `data/gazetteer.json` - Keyword extraction

## 📱 **WhatsApp Commands**

### **Vehicle Search**
- `חיפוש 21-599-58`
- `search 22-727-57`
- `מצא 10-600-42`

### **Maintenance Reports**
- `דוח תחזוקה 21-599-58`
- `maintenance report 22-727-57`

### **Fault Reports**
- `דוח תקלות 21-599-58`
- `fault report 22-727-57`

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Python not found**: Install Python 3.11+
2. **Missing dependencies**: Run `pip install -r config/requirements.txt`
3. **ngrok not working**: Check ngrok installation and authentication
4. **Server not starting**: Check port 5000 availability
5. **Data sync errors**: Verify Excel file format and data

### **Log Files**
- **System Status**: `logs/system_status.json`
- **Server Logs**: Console output
- **Error Logs**: Check console for error messages

## 📈 **Performance Monitoring**

### **Key Metrics**
- **Response Time**: < 2 seconds for vehicle search
- **PDF Generation**: < 5 seconds for reports
- **Data Sync**: < 30 seconds for full sync
- **Uptime**: 99.9% availability target

### **System Resources**
- **Memory**: ~100MB for server process
- **CPU**: Low usage during idle
- **Disk**: ~50MB for data files
- **Network**: ngrok tunnel bandwidth

## 🎯 **Best Practices**

### **Data Management**
- Regular Excel data synchronization
- Backup JSON files before updates
- Monitor data file sizes
- Validate data integrity

### **System Maintenance**
- Regular system status checks
- Monitor log files
- Update dependencies regularly
- Test all commands periodically

### **Security**
- Keep Twilio credentials secure
- Use environment variables for sensitive data
- Regular security updates
- Monitor access logs

## 🚀 **Production Deployment**

### **Prerequisites**
- Python 3.11+ installed
- ngrok account and authentication
- Twilio account and credentials
- Excel data file available

### **Deployment Steps**
1. **Setup Environment**:
   ```bash
   pip install -r config/requirements.txt
   ```

2. **Configure Twilio**:
   - Update `config/twilio_config.json`
   - Set webhook URL to ngrok URL

3. **Start System**:
   ```bash
   manage_fleet_system.bat
   ```

4. **Verify Operation**:
   ```bash
   python scripts/check_system_status.py
   ```

## 📞 **Support**

### **System Status**
- Check system status regularly
- Monitor log files for errors
- Use management panel for operations

### **Data Issues**
- Verify Excel file format
- Check data synchronization logs
- Validate JSON file integrity

### **WhatsApp Issues**
- Verify Twilio configuration
- Check ngrok tunnel status
- Test webhook endpoint

---

*Fleet Management System - Comprehensive Management Guide*
*Last updated: 2025-10-19*
