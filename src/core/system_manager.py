#!/usr/bin/env python3
"""
System Manager - Handles initialization, server management, and data synchronization
"""

import os
import sys
import json
import time
import subprocess
import pandas as pd
from datetime import datetime
import logging

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemManager:
    """Manages the entire Fleet Management System"""
    
    def __init__(self):
        self.project_root = project_root
        self.server_process = None
        self.ngrok_process = None
        
    def initialize_system(self):
        """Initialize the entire system"""
        logger.info("🚀 Initializing Fleet Management System...")
        
        try:
            # Step 1: Clean up existing processes
            self.cleanup_existing_processes()
            
            # Step 2: Update data from Excel
            self.update_data_from_excel()
            
            # Step 3: Update fault reports
            self.update_fault_reports()
            
            # Step 4: Check if ngrok is already running, if not start it
            ngrok_url = self.get_ngrok_url()
            if not ngrok_url:
                logger.info("ngrok not running, starting it...")
                ngrok_url = self.start_ngrok()
            else:
                logger.info(f"ngrok already running: {ngrok_url}")
            
            # Step 5: Start main server
            self.start_main_server()
            
            # Step 6: Display webhook URL and optionally update Twilio
            if ngrok_url:
                webhook_url = f"{ngrok_url}/webhook"
                print("\n" + "="*60)
                print("🌐 NGROK TUNNEL ACTIVE")
                print("="*60)
                print(f"📱 Webhook URL: {webhook_url}")
                
                # Try to automatically update Twilio webhook
                print("\n🔄 Attempting to update Twilio webhook automatically...")
                try:
                    import subprocess
                    result = subprocess.run([
                        'python', 'scripts/update_twilio_webhook.py'
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print("✅ Twilio webhook updated automatically!")
                    else:
                        print("⚠️ Automatic update failed, manual update required:")
                        print("   1. Go to: https://console.twilio.com")
                        print("   2. Navigate to: Messaging > Settings > WhatsApp sandbox settings")
                        print(f"   3. Set webhook URL to: {webhook_url}")
                        print("   4. Save configuration")
                except Exception as e:
                    print(f"⚠️ Could not update Twilio automatically: {e}")
                    print("   Please update manually in Twilio Console:")
                    print(f"   {webhook_url}")
                
                print("="*60)
            else:
                print("\n❌ WARNING: Could not start ngrok tunnel!")
                print("   WhatsApp messages will not work without ngrok.")
            
            logger.info("✅ System initialization completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            return False
    
    def cleanup_existing_processes(self):
        """Clean up any existing Python and ngrok processes"""
        logger.info("🧹 Cleaning up existing processes...")
        
        try:
            # Kill Python processes
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
            time.sleep(2)
            
            # Kill ngrok processes
            subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                         capture_output=True, text=True)
            time.sleep(2)
            
            logger.info("✅ Existing processes cleaned up")
            
        except Exception as e:
            logger.warning(f"⚠️ Warning during cleanup: {e}")
    
    def update_data_from_excel(self):
        """Update JSON data from Excel files using Excel Sync Manager"""
        logger.info("📊 Updating data from Excel files...")
        
        try:
            # Import the new Excel sync manager
            from scripts.excel_sync_manager import ExcelSyncManager
            
            # Use the new Excel sync manager
            sync_manager = ExcelSyncManager()
            success = sync_manager.sync_excel_data()
            
            if success:
                logger.info("✅ Data updated from Excel successfully")
            else:
                logger.warning("⚠️ Excel sync completed with warnings")
                
        except Exception as e:
            logger.error(f"❌ Error updating data from Excel: {e}")
    
    def update_vehicle_catalog(self, df_vehicles):
        """Update vehicle catalog JSON from Excel data"""
        try:
            vehicles = []
            
            for _, row in df_vehicles.iterrows():
                vehicle = {
                    'id': f"V{row.get('ID', ''):03d}",
                    'license_plate': str(row.get('License Plate', '')),
                    'vin': str(row.get('VIN', '')),
                    'make': str(row.get('Make', '')),
                    'model': str(row.get('Model', '')),
                    'year': int(row.get('Year', 0)) if pd.notna(row.get('Year', 0)) else 0,
                    'type': str(row.get('Type', '')),
                    'category': str(row.get('Category', '')),
                    'status': str(row.get('Status', 'active')),
                    'location': str(row.get('Location', '')),
                    'driver': {
                        'name': str(row.get('Driver Name', '')),
                        'id': str(row.get('Driver ID', 'D000')),
                        'phone': str(row.get('Driver Phone', '')),
                        'email': str(row.get('Driver Email', '')),
                        'license_number': int(row.get('Driver License', 0)) if pd.notna(row.get('Driver License', 0)) else 0
                    },
                    'specifications': {
                        'seating_capacity': int(row.get('Seating Capacity', 0)) if pd.notna(row.get('Seating Capacity', 0)) else 0,
                        'fuel_type': str(row.get('Fuel Type', '')),
                        'transmission': str(row.get('Transmission', '')),
                        'engine_size': str(row.get('Engine Size', '')),
                        'fuel_economy_km_l': float(row.get('Fuel Economy', 0)) if pd.notna(row.get('Fuel Economy', 0)) else 0,
                        'horsepower': int(row.get('Horsepower', 0)) if pd.notna(row.get('Horsepower', 0)) else 0,
                        'drivetrain': str(row.get('Drivetrain', '')),
                        'color': str(row.get('Color', '')),
                        'interior_color': str(row.get('Interior Color', ''))
                    }
                }
                vehicles.append(vehicle)
            
            # Save to JSON
            catalog_path = os.path.join(self.project_root, 'data', 'large_vehicle_catalog.json')
            with open(catalog_path, 'w', encoding='utf-8') as f:
                json.dump({'vehicles': vehicles}, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Updated vehicle catalog with {len(vehicles)} vehicles")
            
        except Exception as e:
            logger.error(f"❌ Error updating vehicle catalog: {e}")
    
    def update_maintenance_records(self, df_maintenance):
        """Update maintenance records JSON from Excel data"""
        try:
            records = []
            
            for _, row in df_maintenance.iterrows():
                record = {
                    'id': f"M{row.get('ID', ''):03d}",
                    'license_plate': str(row.get('License Plate', '')),
                    'date': str(row.get('Date', '')),
                    'type': str(row.get('Type', '')),
                    'description': str(row.get('Description', '')),
                    'cost': float(row.get('Cost', 0)) if pd.notna(row.get('Cost', 0)) else 0,
                    'status': str(row.get('Status', '')),
                    'fault_type': str(row.get('Fault Type', '')) if pd.notna(row.get('Fault Type', '')) else None,
                    'fault_severity': str(row.get('Fault Severity', '')) if pd.notna(row.get('Fault Severity', '')) else None,
                    'repair_cost': float(row.get('Repair Cost', 0)) if pd.notna(row.get('Repair Cost', 0)) else 0,
                    'repair_days': int(row.get('Repair Days', 0)) if pd.notna(row.get('Repair Days', 0)) else 0
                }
                records.append(record)
            
            # Save to JSON
            records_path = os.path.join(self.project_root, 'data', 'vehicles', 'maintenance_records.json')
            os.makedirs(os.path.dirname(records_path), exist_ok=True)
            
            with open(records_path, 'w', encoding='utf-8') as f:
                json.dump({'records': records}, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Updated maintenance records with {len(records)} records")
            
        except Exception as e:
            logger.error(f"❌ Error updating maintenance records: {e}")
    
    def update_fault_reports(self):
        """Update fault reports from maintenance data"""
        logger.info("🔧 Updating fault reports...")
        
        try:
            # Load maintenance records
            records_path = os.path.join(self.project_root, 'data', 'vehicles', 'maintenance_records.json')
            
            if not os.path.exists(records_path):
                logger.warning("⚠️ Maintenance records not found")
                return
            
            with open(records_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                records = data.get('records', [])
            
            # Filter fault records
            fault_records = [r for r in records if r.get('fault_type')]
            
            # Create fault reports summary
            fault_summary = {
                'total_faults': len(fault_records),
                'faults_by_type': {},
                'faults_by_severity': {},
                'total_repair_cost': sum(r.get('repair_cost', 0) for r in fault_records),
                'last_updated': datetime.now().isoformat()
            }
            
            # Count by type and severity
            for record in fault_records:
                fault_type = record.get('fault_type', 'Unknown')
                fault_severity = record.get('fault_severity', 'Unknown')
                
                fault_summary['faults_by_type'][fault_type] = fault_summary['faults_by_type'].get(fault_type, 0) + 1
                fault_summary['faults_by_severity'][fault_severity] = fault_summary['faults_by_severity'].get(fault_severity, 0) + 1
            
            # Save fault summary
            fault_path = os.path.join(self.project_root, 'data', 'fault_reports.json')
            with open(fault_path, 'w', encoding='utf-8') as f:
                json.dump(fault_summary, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ Updated fault reports: {len(fault_records)} faults found")
            
        except Exception as e:
            logger.error(f"❌ Error updating fault reports: {e}")
    
    def start_ngrok(self):
        """Start ngrok tunnel"""
        logger.info("🌐 Starting ngrok tunnel...")
        
        try:
            # Check if ngrok is already running
            existing_url = self.get_ngrok_url()
            if existing_url:
                logger.info(f"✅ Ngrok already running: {existing_url}")
                return existing_url
            
            # Start ngrok in background
            self.ngrok_process = subprocess.Popen(
                ['ngrok', 'http', '5000'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for ngrok to start with retries
            max_retries = 10
            for attempt in range(max_retries):
                time.sleep(2)
                ngrok_url = self.get_ngrok_url()
                if ngrok_url:
                    logger.info(f"✅ Ngrok started successfully: {ngrok_url}")
                    return ngrok_url
                logger.info(f"⏳ Waiting for ngrok... (attempt {attempt + 1}/{max_retries})")
            
            logger.warning("⚠️ Could not get ngrok URL after multiple attempts")
            return None
                
        except Exception as e:
            logger.error(f"❌ Error starting ngrok: {e}")
            return None
    
    def get_ngrok_url(self):
        """Get ngrok public URL"""
        try:
            import requests
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            data = response.json()
            
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
            
            return None
            
        except Exception as e:
            logger.warning(f"⚠️ Could not get ngrok URL: {e}")
            return None
    
    def start_main_server(self):
        """Start the main Flask server"""
        logger.info("🚀 Starting main server...")
        
        try:
            # Start server in background
            self.server_process = subprocess.Popen(
                [sys.executable, 'src/services/simple_server.py'],
                cwd=self.project_root
            )
            
            time.sleep(3)  # Wait for server to start
            
            logger.info("✅ Main server started on port 5000")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting main server: {e}")
            return False
    
    def get_system_status(self):
        """Get current system status"""
        status = {
            'server_running': self.server_process and self.server_process.poll() is None,
            'ngrok_running': self.ngrok_process and self.ngrok_process.poll() is None,
            'ngrok_url': self.get_ngrok_url(),
            'timestamp': datetime.now().isoformat()
        }
        return status
    
    def stop_system(self):
        """Stop the entire system"""
        logger.info("🛑 Stopping Fleet Management System...")
        
        try:
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait()
            
            if self.ngrok_process:
                self.ngrok_process.terminate()
                self.ngrok_process.wait()
            
            logger.info("✅ System stopped successfully")
            
        except Exception as e:
            logger.error(f"❌ Error stopping system: {e}")

def main():
    """Main function for system management"""
    manager = SystemManager()
    
    try:
        # Initialize system
        success = manager.initialize_system()
        
        if success:
            print("\n" + "="*50)
            print("🎉 FLEET MANAGEMENT SYSTEM READY!")
            print("="*50)
            print(f"📱 Server: http://localhost:5000")
            print(f"🌐 Webhook: {manager.get_ngrok_url()}/webhook")
            print(f"❤️ Health: http://localhost:5000/health")
            print("\n📋 Available Commands:")
            print("• חיפוש [לוחית רישוי] - Vehicle search")
            print("• דוח תחזוקה [לוחית רישוי] - Maintenance report")
            print("• דוח תקלות [לוחית רישוי] - Fault report")
            print("\nPress Ctrl+C to stop the system")
            print("="*50)
            
            # Keep system running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down system...")
                manager.stop_system()
        else:
            print("❌ System initialization failed!")
            return 1
            
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
