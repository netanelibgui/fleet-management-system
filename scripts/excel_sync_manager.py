#!/usr/bin/env python3
"""
Excel Synchronization Manager
Handles synchronization between main Excel file and fault report file
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
import hashlib
import logging
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_root, 'logs', 'excel_sync.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ExcelSyncManager:
    """Manages synchronization between Excel files and JSON data"""
    
    def __init__(self):
        self.project_root = project_root
        self.data_dir = os.path.join(project_root, 'data')
        self.main_excel_path = os.path.join(project_root, 'Large_Enhanced_Fleet_Report_20251018_230415.xlsx')
        self.vehicle_catalog_path = os.path.join(self.data_dir, 'large_vehicle_catalog.json')
        self.fault_reports_path = os.path.join(self.data_dir, 'fault_reports.json')
        self.maintenance_records_path = os.path.join(self.data_dir, 'vehicles', 'maintenance_records.json')
        
        # Create sync tracking file
        self.sync_tracking_path = os.path.join(self.data_dir, 'sync_tracking.json')
        self.sync_tracking = self.load_sync_tracking()
    
    def load_sync_tracking(self):
        """Load sync tracking data"""
        try:
            if os.path.exists(self.sync_tracking_path):
                with open(self.sync_tracking_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'last_sync': None,
                    'vehicle_hashes': {},
                    'maintenance_hashes': {},
                    'sync_history': []
                }
        except Exception as e:
            logger.error(f"Error loading sync tracking: {e}")
            return {
                'last_sync': None,
                'vehicle_hashes': {},
                'maintenance_hashes': {},
                'sync_history': []
            }
    
    def save_sync_tracking(self):
        """Save sync tracking data"""
        try:
            with open(self.sync_tracking_path, 'w', encoding='utf-8') as f:
                json.dump(self.sync_tracking, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving sync tracking: {e}")
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def detect_vehicle_changes(self):
        """Detect changes in vehicle data"""
        try:
            # Calculate current hash of main Excel file
            current_hash = self.calculate_file_hash(self.main_excel_path)
            if not current_hash:
                logger.warning("Could not calculate hash for main Excel file")
                return False
            
            # Check if file has changed
            last_hash = self.sync_tracking.get('vehicle_hashes', {}).get('main_excel')
            if current_hash == last_hash:
                logger.info("No changes detected in main Excel file")
                return False
            
            logger.info(f"Changes detected in main Excel file (hash: {current_hash[:8]}...)")
            return True
            
        except Exception as e:
            logger.error(f"Error detecting vehicle changes: {e}")
            return False
    
    def load_main_excel_data(self):
        """Load data from main Excel file"""
        try:
            # Try different sheet names
            sheet_names = ['Vehicles', 'Vehicle Data', 'Main Data', 'Sheet1']
            df = None
            
            for sheet in sheet_names:
                try:
                    df = pd.read_excel(self.main_excel_path, sheet_name=sheet)
                    logger.info(f"Successfully loaded data from sheet: {sheet}")
                    break
                except:
                    continue
            
            if df is None:
                # Try to read the first sheet
                df = pd.read_excel(self.main_excel_path, sheet_name=0)
                logger.info("Loaded data from first available sheet")
            
            # Since we're using the English Excel file, no column mapping needed
            # The columns are already in English
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading main Excel data: {e}")
            return None
    
    def update_vehicle_catalog(self, df):
        """Update vehicle catalog from Excel data"""
        try:
            vehicles = []
            
            for index, row in df.iterrows():
                # Extract vehicle data using correct English column names
                vehicle = {
                    'id': str(row.get('Vehicle ID', f"V{index:03d}")).strip(),
                    'license_plate': str(row.get('License Plate', '')).strip(),
                    'vin': str(row.get('VIN', '')).strip(),
                    'make': str(row.get('Make', '')).strip(),
                    'model': str(row.get('Model', '')).strip(),
                    'year': int(row.get('Year', 0)) if pd.notna(row.get('Year')) else 0,
                    'type': str(row.get('Vehicle Type', '')).strip(),
                    'category': str(row.get('Category Name', '')).strip(),
                    'status': str(row.get('Status', 'active')).strip(),
                    'location': str(row.get('Location Name', '')).strip(),
                    'driver': {
                        'name': str(row.get('Driver Name', '')).strip(),
                        'id': str(row.get('Driver ID', 'D000')).strip(),
                        'phone': str(row.get('Driver Phone', '')).strip(),
                        'email': str(row.get('Driver Email', '')).strip(),
                        'license_number': str(row.get('Driver License', '')).strip()
                    },
                    'specifications': {
                        'color': str(row.get('Color', '')).strip(),
                        'engine': str(row.get('Engine Size', '')).strip(),
                        'transmission': str(row.get('Transmission', '')).strip(),
                        'fuel_type': str(row.get('Fuel Type', '')).strip()
                    },
                    'insurance': {
                        'provider': str(row.get('Insurance Provider', '')).strip(),
                        'policy_number': str(row.get('Policy Number', '')).strip(),
                        'expiry_date': str(row.get('Insurance Expires', '')).strip()
                    },
                    'last_updated': datetime.now().isoformat()
                }
                
                # Only add vehicles with valid license plates
                if vehicle['license_plate'] and vehicle['license_plate'] != 'nan':
                    vehicles.append(vehicle)
            
            # Update vehicle catalog
            catalog_data = {
                'vehicles': vehicles,
                'total_vehicles': len(vehicles),
                'last_updated': datetime.now().isoformat(),
                'source_file': self.main_excel_path
            }
            
            with open(self.vehicle_catalog_path, 'w', encoding='utf-8') as f:
                json.dump(catalog_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Updated vehicle catalog with {len(vehicles)} vehicles")
            return True
            
        except Exception as e:
            logger.error(f"Error updating vehicle catalog: {e}")
            return False
    
    def update_fault_reports(self, df):
        """Update fault reports based on vehicle data"""
        try:
            # Extract maintenance/fault data from Excel
            maintenance_data = []
            fault_data = []
            
            # Look for maintenance-related columns
            maintenance_columns = [col for col in df.columns if any(keyword in col.lower() 
                                for keyword in ['maintenance', 'repair', 'fault', 'service', 'cost', 'last', 'next'])]
            
            logger.info(f"Found maintenance columns: {maintenance_columns}")
            
            for index, row in df.iterrows():
                license_plate = str(row.get('License Plate', '')).strip()
                if not license_plate or license_plate == 'nan':
                    continue
                
                # Get driver name for the record
                driver_name = str(row.get('Driver Name', '')).strip()
                
                # Get repair cost from Hebrew columns
                repair_cost = 0
                cost_columns = ['עלות תיקון (₪)', 'עלות תיקון (שקל)', 'עלות תיקון', 'Repair Cost']
                for col in cost_columns:
                    if col in row and pd.notna(row[col]):
                        try:
                            repair_cost = float(row[col])
                            break
                        except (ValueError, TypeError):
                            continue
                
                # Create maintenance record
                maintenance_record = {
                    'vehicle_id': f"V{index:03d}",
                    'license_plate': license_plate,
                    'driver_name': driver_name,
                    'date': str(row.get('Last Maintenance', '')).strip(),
                    'type': 'Routine Maintenance',
                    'description': f"Maintenance for vehicle {license_plate}",
                    'cost': repair_cost,
                    'status': 'Completed',
                    'provider': 'Internal',
                    'mileage': int(row.get('Mileage', 0)) if pd.notna(row.get('Mileage')) else 0,
                    'next_service': str(row.get('Next Maintenance', '')).strip(),
                    'created_at': datetime.now().isoformat()
                }
                
                # Check if it's a fault record - look for fault data
                fault_type = str(row.get('Fault Type', '')).strip()
                if fault_type and fault_type != 'nan' and fault_type != 'None':
                    fault_record = {
                        'vehicle_id': f"V{index:03d}",
                        'license_plate': license_plate,
                        'driver_name': driver_name,
                        'fault_type': fault_type,
                        'fault_severity': 'Medium',
                        'description': str(row.get('Fault Description', '')).strip(),
                        'repair_cost': repair_cost,  # Use the same repair cost we found above
                        'repair_date': str(row.get('Report Date', '')).strip(),
                        'status': str(row.get('Fault Status', 'Open')).strip(),
                        'reported_by': str(row.get('Reported By', driver_name)).strip(),
                        'created_at': datetime.now().isoformat()
                    }
                    fault_data.append(fault_record)
                    logger.info(f"Added fault record for {license_plate}: {fault_type}")
                
                maintenance_data.append(maintenance_record)
            
            # Update maintenance records
            maintenance_records = {
                'records': maintenance_data,
                'total_records': len(maintenance_data),
                'last_updated': datetime.now().isoformat(),
                'source_file': self.main_excel_path
            }
            
            with open(self.maintenance_records_path, 'w', encoding='utf-8') as f:
                json.dump(maintenance_records, f, ensure_ascii=False, indent=2)
            
            # Update fault reports summary
            fault_summary = {
                'total_faults': len(fault_data),
                'faults_by_type': {},
                'faults_by_severity': {},
                'total_repair_cost': sum(f.get('repair_cost', 0) for f in fault_data),
                'last_updated': datetime.now().isoformat(),
                'source_file': self.main_excel_path
            }
            
            # Count by type and severity
            for fault in fault_data:
                fault_type = fault.get('fault_type', 'Unknown')
                fault_severity = fault.get('fault_severity', 'Unknown')
                
                fault_summary['faults_by_type'][fault_type] = fault_summary['faults_by_type'].get(fault_type, 0) + 1
                fault_summary['faults_by_severity'][fault_severity] = fault_summary['faults_by_severity'].get(fault_severity, 0) + 1
            
            with open(self.fault_reports_path, 'w', encoding='utf-8') as f:
                json.dump(fault_summary, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Updated maintenance records: {len(maintenance_data)} records")
            logger.info(f"Updated fault reports: {len(fault_data)} faults")
            return True
            
        except Exception as e:
            logger.error(f"Error updating fault reports: {e}")
            return False
    
    def sync_excel_data(self):
        """Main synchronization method"""
        try:
            logger.info("Starting Excel data synchronization...")
            
            # Check if main Excel file exists
            if not os.path.exists(self.main_excel_path):
                logger.error(f"Main Excel file not found: {self.main_excel_path}")
                return False
            
            # Detect changes
            if not self.detect_vehicle_changes():
                logger.info("No changes detected, skipping sync")
                return True
            
            # Load Excel data
            df = self.load_main_excel_data()
            if df is None:
                logger.error("Failed to load Excel data")
                return False
            
            logger.info(f"Loaded Excel data with {len(df)} rows")
            
            # Update vehicle catalog
            if not self.update_vehicle_catalog(df):
                logger.error("Failed to update vehicle catalog")
                return False
            
            # Update fault reports
            if not self.update_fault_reports(df):
                logger.error("Failed to update fault reports")
                return False
            
            # Update sync tracking
            current_hash = self.calculate_file_hash(self.main_excel_path)
            self.sync_tracking['last_sync'] = datetime.now().isoformat()
            self.sync_tracking['vehicle_hashes']['main_excel'] = current_hash
            
            # Add to sync history
            sync_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'full_sync',
                'vehicles_updated': len(df),
                'file_hash': current_hash[:8] if current_hash else 'unknown'
            }
            self.sync_tracking['sync_history'].append(sync_entry)
            
            # Keep only last 50 sync entries
            if len(self.sync_tracking['sync_history']) > 50:
                self.sync_tracking['sync_history'] = self.sync_tracking['sync_history'][-50:]
            
            self.save_sync_tracking()
            
            logger.info("Excel data synchronization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during Excel synchronization: {e}")
            return False
    
    def get_sync_status(self):
        """Get current synchronization status"""
        try:
            status = {
                'last_sync': self.sync_tracking.get('last_sync'),
                'main_excel_exists': os.path.exists(self.main_excel_path),
                'vehicle_catalog_exists': os.path.exists(self.vehicle_catalog_path),
                'fault_reports_exists': os.path.exists(self.fault_reports_path),
                'maintenance_records_exists': os.path.exists(self.maintenance_records_path),
                'sync_history_count': len(self.sync_tracking.get('sync_history', [])),
                'last_sync_hash': self.sync_tracking.get('vehicle_hashes', {}).get('main_excel', 'unknown')[:8] if self.sync_tracking.get('vehicle_hashes', {}).get('main_excel') else 'none'
            }
            
            # Get file sizes
            if status['main_excel_exists']:
                status['main_excel_size'] = os.path.getsize(self.main_excel_path)
            
            if status['vehicle_catalog_exists']:
                with open(self.vehicle_catalog_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    status['vehicle_count'] = data.get('total_vehicles', 0)
            
            if status['fault_reports_exists']:
                with open(self.fault_reports_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    status['fault_count'] = data.get('total_faults', 0)
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting sync status: {e}")
            return {'error': str(e)}

def main():
    """Main function"""
    print("Excel Synchronization Manager")
    print("=" * 40)
    
    sync_manager = ExcelSyncManager()
    
    # Get current status
    status = sync_manager.get_sync_status()
    print(f"Last sync: {status.get('last_sync', 'Never')}")
    print(f"Main Excel exists: {status.get('main_excel_exists', False)}")
    print(f"Vehicle count: {status.get('vehicle_count', 0)}")
    print(f"Fault count: {status.get('fault_count', 0)}")
    print()
    
    # Perform synchronization
    print("Starting synchronization...")
    success = sync_manager.sync_excel_data()
    
    if success:
        print("Synchronization completed successfully!")
        
        # Show updated status
        status = sync_manager.get_sync_status()
        print(f"Updated vehicle count: {status.get('vehicle_count', 0)}")
        print(f"Updated fault count: {status.get('fault_count', 0)}")
    else:
        print("Synchronization failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
