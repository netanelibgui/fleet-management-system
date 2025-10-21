#!/usr/bin/env python3
"""
System Status Checker
Checks the status of all Fleet Management System components
"""

import os
import sys
import json
import requests
import subprocess
from datetime import datetime
import logging

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_system_status():
    """Check the status of all system components"""
    print("Fleet Management System - Status Check")
    print("=" * 50)
    
    status = {
        'timestamp': datetime.now().isoformat(),
        'components': {}
    }
    
    # Check Python processes
    print("\nChecking Python processes...")
    python_status = check_python_processes()
    status['components']['python'] = python_status
    print(f"   Status: {'Running' if python_status['running'] else 'Not running'}")
    if python_status['running']:
        print(f"   Processes: {python_status['count']}")
    
    # Check ngrok
    print("\nChecking ngrok tunnel...")
    ngrok_status = check_ngrok()
    status['components']['ngrok'] = ngrok_status
    print(f"   Status: {'Running' if ngrok_status['running'] else 'Not running'}")
    if ngrok_status['running']:
        print(f"   URL: {ngrok_status['url']}")
    
    # Check main server
    print("\nChecking main server...")
    server_status = check_main_server()
    status['components']['server'] = server_status
    print(f"   Status: {'Running' if server_status['running'] else 'Not running'}")
    if server_status['running']:
        print(f"   Port: {server_status['port']}")
        print(f"   Health: {server_status['health']}")
    
    # Check data files
    print("\nChecking data files...")
    data_status = check_data_files()
    status['components']['data'] = data_status
    print(f"   Vehicle catalog: {'Found' if data_status['vehicle_catalog'] else 'Missing'}")
    print(f"   Maintenance records: {'Found' if data_status['maintenance_records'] else 'Missing'}")
    print(f"   Fault reports: {'Found' if data_status['fault_reports'] else 'Missing'}")
    if data_status['vehicle_catalog']:
        print(f"   Vehicles: {data_status['vehicle_count']}")
    if data_status['maintenance_records']:
        print(f"   Maintenance records: {data_status['maintenance_count']}")
    
    # Check configuration
    print("\nChecking configuration...")
    config_status = check_configuration()
    status['components']['config'] = config_status
    if config_status['twilio_config'] == True:
        print(f"   Twilio config: Found (Valid credentials)")
    elif config_status['twilio_config'] == 'placeholder':
        print(f"   Twilio config: Found (Placeholder values - needs configuration)")
    else:
        print(f"   Twilio config: Missing")
    print(f"   Requirements: {'Found' if config_status['requirements'] else 'Missing'}")
    
    # Overall status
    print("\n" + "=" * 50)
    overall_status = determine_overall_status(status)
    print(f"Overall Status: {overall_status}")
    print("=" * 50)
    
    # Save status report
    save_status_report(status)
    
    return overall_status == "✅ All Systems Operational"

def check_python_processes():
    """Check if Python processes are running"""
    try:
        result = subprocess.run(['tasklist', '/fi', 'imagename eq python.exe'], 
                              capture_output=True, text=True)
        
        if 'python.exe' in result.stdout:
            lines = [line for line in result.stdout.split('\n') if 'python.exe' in line]
            return {
                'running': True,
                'count': len(lines),
                'details': lines
            }
        else:
            return {
                'running': False,
                'count': 0,
                'details': []
            }
    except Exception as e:
        return {
            'running': False,
            'count': 0,
            'error': str(e)
        }

def check_ngrok():
    """Check if ngrok is running and get URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        data = response.json()
        
        for tunnel in data.get('tunnels', []):
            if tunnel.get('proto') == 'https':
                return {
                    'running': True,
                    'url': tunnel.get('public_url'),
                    'name': tunnel.get('name'),
                    'config': tunnel.get('config', {})
                }
        
        return {
            'running': False,
            'url': None
        }
    except Exception as e:
        return {
            'running': False,
            'url': None,
            'error': str(e)
        }

def check_main_server():
    """Check if main server is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            return {
                'running': True,
                'port': 5000,
                'health': 'Healthy',
                'details': health_data
            }
        else:
            return {
                'running': False,
                'port': 5000,
                'health': f'Error: {response.status_code}'
            }
    except Exception as e:
        return {
            'running': False,
            'port': 5000,
            'health': f'Error: {str(e)}'
        }

def check_data_files():
    """Check if data files exist and are valid"""
    status = {
        'vehicle_catalog': False,
        'maintenance_records': False,
        'fault_reports': False,
        'vehicle_count': 0,
        'maintenance_count': 0
    }
    
    # Check vehicle catalog
    vehicle_path = os.path.join(project_root, 'data', 'large_vehicle_catalog.json')
    if os.path.exists(vehicle_path):
        try:
            with open(vehicle_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['vehicle_catalog'] = True
                status['vehicle_count'] = len(data.get('vehicles', []))
        except Exception as e:
            status['vehicle_catalog_error'] = str(e)
    
    # Check maintenance records
    maintenance_path = os.path.join(project_root, 'data', 'vehicles', 'maintenance_records.json')
    if os.path.exists(maintenance_path):
        try:
            with open(maintenance_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['maintenance_records'] = True
                status['maintenance_count'] = len(data.get('records', []))
        except Exception as e:
            status['maintenance_records_error'] = str(e)
    
    # Check fault reports
    fault_path = os.path.join(project_root, 'data', 'fault_reports.json')
    if os.path.exists(fault_path):
        try:
            with open(fault_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status['fault_reports'] = True
        except Exception as e:
            status['fault_reports_error'] = str(e)
    
    return status

def check_configuration():
    """Check configuration files"""
    status = {
        'twilio_config': False,
        'requirements': False
    }
    
    # Check Twilio config
    twilio_path = os.path.join(project_root, 'config', 'twilio_config.json')
    if os.path.exists(twilio_path):
        try:
            with open(twilio_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check for Twilio credentials (nested under 'twilio' key)
                twilio_data = data.get('twilio', {})
                if (twilio_data.get('account_sid') and 
                    twilio_data.get('auth_token') and 
                    twilio_data.get('account_sid') != 'YOUR_TWILIO_ACCOUNT_SID' and
                    twilio_data.get('auth_token') != 'YOUR_TWILIO_AUTH_TOKEN'):
                    status['twilio_config'] = True
                else:
                    status['twilio_config'] = 'placeholder'  # File exists but has placeholder values
        except Exception as e:
            status['twilio_config_error'] = str(e)
    
    # Check requirements
    requirements_path = os.path.join(project_root, 'config', 'requirements.txt')
    if os.path.exists(requirements_path):
        status['requirements'] = True
    
    return status

def determine_overall_status(status):
    """Determine overall system status"""
    components = status['components']
    
    # Check critical components
    critical_components = ['server', 'data']
    critical_ok = all(
        components.get(comp, {}).get('running', False) or 
        components.get(comp, {}).get('vehicle_catalog', False)
        for comp in critical_components
    )
    
    if critical_ok:
        return "All Systems Operational"
    else:
        return "System Issues Detected"

def save_status_report(status):
    """Save status report to file"""
    try:
        report_path = os.path.join(project_root, 'logs', 'system_status.json')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        
        print(f"\nStatus report saved to: {report_path}")
    except Exception as e:
        print(f"\nCould not save status report: {e}")

def main():
    """Main function"""
    try:
        success = check_system_status()
        return 0 if success else 1
    except Exception as e:
        logger.error(f"❌ Status check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
