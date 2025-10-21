#!/usr/bin/env python3
"""
Maintenance Tracker for Fleet Management System
Handles maintenance scheduling, tracking, cost analysis, and reporting.
Integrates with vehicle data and maintenance records.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import os

@dataclass
class MaintenanceAlert:
    """Maintenance alert data structure"""
    vehicle_id: str
    vehicle_name: str
    license_plate: str
    alert_type: str  # 'due', 'overdue', 'upcoming'
    days_until_due: int
    last_service_date: str
    next_service_date: str
    service_type: str
    priority: str  # 'low', 'medium', 'high', 'critical'
    estimated_cost: float
    description: str

@dataclass
class MaintenanceStats:
    """Maintenance statistics data structure"""
    total_vehicles: int
    vehicles_due: int
    vehicles_overdue: int
    total_cost_30_days: float
    total_cost_90_days: float
    total_cost_year: float
    average_cost_per_vehicle: float
    most_common_service: str
    maintenance_frequency: float

class MaintenanceTracker:
    """
    Maintenance Tracker for fleet maintenance management
    Handles scheduling, tracking, cost analysis, and reporting
    """
    
    def __init__(self, maintenance_records_path: str, vehicle_catalog_path: str):
        self.logger = logging.getLogger(__name__)
        self.maintenance_records_path = maintenance_records_path
        self.vehicle_catalog_path = vehicle_catalog_path
        
        # Data caches
        self._maintenance_records_cache = None
        self._vehicles_cache = None
        
        # Maintenance intervals (in days)
        self.maintenance_intervals = {
            'oil_change': 90,
            'brake_inspection': 180,
            'tire_rotation': 120,
            'engine_service': 365,
            'transmission_service': 730,
            'general_inspection': 180,
            'preventive_maintenance': 90
        }
        
        # Service costs (estimated)
        self.service_costs = {
            'oil_change': 85.00,
            'brake_inspection': 120.00,
            'tire_rotation': 25.00,
            'engine_service': 300.00,
            'transmission_service': 450.00,
            'general_inspection': 150.00,
            'preventive_maintenance': 200.00
        }
        
        self.logger.info("Maintenance Tracker initialized")
    
    def _load_maintenance_records(self) -> List[Dict]:
        """Load maintenance records from JSON file"""
        if self._maintenance_records_cache is not None:
            return self._maintenance_records_cache
            
        try:
            with open(self.maintenance_records_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._maintenance_records_cache = data.get('records', [])
                return self._maintenance_records_cache
        except Exception as e:
            self.logger.error(f"Error loading maintenance records: {e}")
            return []
    
    def _load_vehicles(self) -> List[Dict]:
        """Load vehicle catalog from JSON file"""
        if self._vehicles_cache is not None:
            return self._vehicles_cache
            
        try:
            with open(self.vehicle_catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._vehicles_cache = data.get('vehicles', [])
                return self._vehicles_cache
        except Exception as e:
            self.logger.error(f"Error loading vehicle catalog: {e}")
            return []
    
    def get_vehicle_maintenance_history(self, vehicle_id: str) -> List[Dict]:
        """
        Get maintenance history for a specific vehicle
        
        Args:
            vehicle_id: Vehicle ID
            
        Returns:
            List of maintenance records sorted by date (newest first)
        """
        if not vehicle_id:
            return []
        
        maintenance_records = self._load_maintenance_records()
        vehicle_records = [record for record in maintenance_records 
                          if record.get('vehicle_id') == vehicle_id]
        
        # Sort by date (newest first)
        vehicle_records.sort(key=lambda x: x.get('date', ''), reverse=True)
        return vehicle_records
    
    def get_vehicle_maintenance_status(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Get current maintenance status for a vehicle
        
        Args:
            vehicle_id: Vehicle ID
            
        Returns:
            Dictionary with maintenance status information
        """
        if not vehicle_id:
            return {}
        
        vehicles = self._load_vehicles()
        vehicle = next((v for v in vehicles if v.get('id') == vehicle_id), None)
        
        if not vehicle:
            return {}
        
        maintenance_records = self.get_vehicle_maintenance_history(vehicle_id)
        
        if not maintenance_records:
            return {
                'vehicle_id': vehicle_id,
                'vehicle_name': vehicle.get('name', 'Unknown'),
                'license_plate': vehicle.get('license_plate', 'N/A'),
                'status': 'no_records',
                'last_service_date': None,
                'next_service_date': None,
                'days_since_last_service': None,
                'days_until_next_service': None,
                'overdue': False,
                'recommended_service': 'general_inspection'
            }
        
        # Get latest record
        latest_record = maintenance_records[0]
        last_service_date = latest_record.get('date', '')
        
        # Calculate days since last service
        days_since_last_service = None
        if last_service_date:
            try:
                last_date = datetime.strptime(last_service_date, '%Y-%m-%d')
                days_since_last_service = (datetime.now() - last_date).days
            except ValueError:
                pass
        
        # Determine next service date and type
        service_type = latest_record.get('type', 'general_inspection')
        interval_days = self.maintenance_intervals.get(service_type, 180)
        
        next_service_date = None
        days_until_next_service = None
        if last_service_date:
            try:
                last_date = datetime.strptime(last_service_date, '%Y-%m-%d')
                next_date = last_date + timedelta(days=interval_days)
                next_service_date = next_date.strftime('%Y-%m-%d')
                days_until_next_service = (next_date - datetime.now()).days
            except ValueError:
                pass
        
        # Determine status
        overdue = False
        if days_until_next_service is not None and days_until_next_service < 0:
            overdue = True
            status = 'overdue'
        elif days_until_next_service is not None and days_until_next_service <= 7:
            status = 'due_soon'
        elif days_until_next_service is not None and days_until_next_service <= 30:
            status = 'upcoming'
        else:
            status = 'current'
        
        return {
            'vehicle_id': vehicle_id,
            'vehicle_name': vehicle.get('name', 'Unknown'),
            'license_plate': vehicle.get('license_plate', 'N/A'),
            'status': status,
            'last_service_date': last_service_date,
            'next_service_date': next_service_date,
            'days_since_last_service': days_since_last_service,
            'days_until_next_service': days_until_next_service,
            'overdue': overdue,
            'recommended_service': service_type,
            'last_service_type': latest_record.get('type', 'Unknown'),
            'last_service_cost': latest_record.get('cost', 0.0)
        }
    
    def get_maintenance_alerts(self, days_ahead: int = 30) -> List[MaintenanceAlert]:
        """
        Get maintenance alerts for vehicles due or overdue
        
        Args:
            days_ahead: Number of days to look ahead for alerts
            
        Returns:
            List of maintenance alerts
        """
        vehicles = self._load_vehicles()
        alerts = []
        current_date = datetime.now()
        
        for vehicle in vehicles:
            vehicle_id = vehicle.get('id')
            if not vehicle_id:
                continue
            
            maintenance_status = self.get_vehicle_maintenance_status(vehicle_id)
            
            if maintenance_status.get('status') == 'no_records':
                # No maintenance records - recommend general inspection
                alert = MaintenanceAlert(
                    vehicle_id=vehicle_id,
                    vehicle_name=vehicle.get('name', 'Unknown'),
                    license_plate=vehicle.get('license_plate', 'N/A'),
                    alert_type='due',
                    days_until_due=0,
                    last_service_date='Never',
                    next_service_date=current_date.strftime('%Y-%m-%d'),
                    service_type='general_inspection',
                    priority='high',
                    estimated_cost=self.service_costs.get('general_inspection', 150.0),
                    description='No maintenance records found - general inspection recommended'
                )
                alerts.append(alert)
                continue
            
            days_until_due = maintenance_status.get('days_until_next_service')
            if days_until_due is None:
                continue
            
            # Determine alert type and priority
            if days_until_due < 0:
                alert_type = 'overdue'
                priority = 'critical'
            elif days_until_due <= 7:
                alert_type = 'due'
                priority = 'high'
            elif days_until_due <= days_ahead:
                alert_type = 'upcoming'
                priority = 'medium'
            else:
                continue  # Not within alert window
            
            service_type = maintenance_status.get('recommended_service', 'general_inspection')
            estimated_cost = self.service_costs.get(service_type, 150.0)
            
            alert = MaintenanceAlert(
                vehicle_id=vehicle_id,
                vehicle_name=vehicle.get('name', 'Unknown'),
                license_plate=vehicle.get('license_plate', 'N/A'),
                alert_type=alert_type,
                days_until_due=days_until_due,
                last_service_date=maintenance_status.get('last_service_date', 'Unknown'),
                next_service_date=maintenance_status.get('next_service_date', 'Unknown'),
                service_type=service_type,
                priority=priority,
                estimated_cost=estimated_cost,
                description=f"{service_type.replace('_', ' ').title()} due in {abs(days_until_due)} days"
            )
            alerts.append(alert)
        
        # Sort by priority and days until due
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        alerts.sort(key=lambda x: (priority_order.get(x.priority, 4), x.days_until_due))
        
        return alerts
    
    def get_maintenance_statistics(self) -> MaintenanceStats:
        """
        Get comprehensive maintenance statistics
        
        Returns:
            MaintenanceStats object with statistics
        """
        vehicles = self._load_vehicles()
        maintenance_records = self._load_maintenance_records()
        
        total_vehicles = len(vehicles)
        
        # Get alerts to count due/overdue vehicles
        alerts = self.get_maintenance_alerts(days_ahead=30)
        vehicles_due = len([a for a in alerts if a.alert_type == 'due'])
        vehicles_overdue = len([a for a in alerts if a.alert_type == 'overdue'])
        
        # Calculate costs for different periods
        current_date = datetime.now()
        thirty_days_ago = current_date - timedelta(days=30)
        ninety_days_ago = current_date - timedelta(days=90)
        one_year_ago = current_date - timedelta(days=365)
        
        total_cost_30_days = 0.0
        total_cost_90_days = 0.0
        total_cost_year = 0.0
        
        for record in maintenance_records:
            record_date_str = record.get('date', '')
            if not record_date_str:
                continue
            
            try:
                record_date = datetime.strptime(record_date_str, '%Y-%m-%d')
                cost = record.get('cost', 0.0)
                
                if record_date >= thirty_days_ago:
                    total_cost_30_days += cost
                if record_date >= ninety_days_ago:
                    total_cost_90_days += cost
                if record_date >= one_year_ago:
                    total_cost_year += cost
            except ValueError:
                continue
        
        # Calculate average cost per vehicle
        average_cost_per_vehicle = total_cost_year / total_vehicles if total_vehicles > 0 else 0.0
        
        # Find most common service type
        service_types = [record.get('type', '') for record in maintenance_records if record.get('type')]
        most_common_service = max(set(service_types), key=service_types.count) if service_types else 'Unknown'
        
        # Calculate maintenance frequency (services per vehicle per year)
        maintenance_frequency = len(maintenance_records) / total_vehicles if total_vehicles > 0 else 0.0
        
        return MaintenanceStats(
            total_vehicles=total_vehicles,
            vehicles_due=vehicles_due,
            vehicles_overdue=vehicles_overdue,
            total_cost_30_days=total_cost_30_days,
            total_cost_90_days=total_cost_90_days,
            total_cost_year=total_cost_year,
            average_cost_per_vehicle=average_cost_per_vehicle,
            most_common_service=most_common_service,
            maintenance_frequency=maintenance_frequency
        )
    
    def generate_maintenance_report(self, vehicle_id: str, language: str = "english") -> Dict[str, Any]:
        """
        Generate a comprehensive maintenance report for a vehicle
        
        Args:
            vehicle_id: Vehicle ID
            language: Report language
            
        Returns:
            Dictionary with formatted maintenance report
        """
        if not vehicle_id:
            return {"error": "Vehicle ID is required"}
        
        vehicles = self._load_vehicles()
        vehicle = next((v for v in vehicles if v.get('id') == vehicle_id), None)
        
        if not vehicle:
            return {"error": "Vehicle not found"}
        
        maintenance_status = self.get_vehicle_maintenance_status(vehicle_id)
        maintenance_history = self.get_vehicle_maintenance_history(vehicle_id)
        
        # Get recent maintenance (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        recent_maintenance = []
        
        for record in maintenance_history:
            record_date_str = record.get('date', '')
            if record_date_str:
                try:
                    record_date = datetime.strptime(record_date_str, '%Y-%m-%d')
                    if record_date >= six_months_ago:
                        recent_maintenance.append(record)
                except ValueError:
                    continue
        
        # Format the report
        if language == "hebrew":
            report = {
                "vehicle_info": {
                    "name": vehicle.get('name', 'Unknown'),
                    "license_plate": vehicle.get('license_plate', 'N/A'),
                    "type": vehicle.get('type', 'Unknown'),
                    "year": vehicle.get('year', 'N/A'),
                    "mileage": vehicle.get('mileage', 'N/A')
                },
                "maintenance_status": {
                    "status": maintenance_status.get('status', 'Unknown'),
                    "last_service_date": maintenance_status.get('last_service_date', 'N/A'),
                    "next_service_date": maintenance_status.get('next_service_date', 'N/A'),
                    "days_since_last_service": maintenance_status.get('days_since_last_service', 'N/A'),
                    "days_until_next_service": maintenance_status.get('days_until_next_service', 'N/A'),
                    "overdue": maintenance_status.get('overdue', False),
                    "recommended_service": maintenance_status.get('recommended_service', 'Unknown')
                },
                "recent_maintenance": recent_maintenance[:10],  # Last 10 records
                "total_records": len(maintenance_history),
                "message": self._format_hebrew_maintenance_report(vehicle, maintenance_status, recent_maintenance)
            }
        else:
            report = {
                "vehicle_info": {
                    "name": vehicle.get('name', 'Unknown'),
                    "license_plate": vehicle.get('license_plate', 'N/A'),
                    "type": vehicle.get('type', 'Unknown'),
                    "year": vehicle.get('year', 'N/A'),
                    "mileage": vehicle.get('mileage', 'N/A')
                },
                "maintenance_status": {
                    "status": maintenance_status.get('status', 'Unknown'),
                    "last_service_date": maintenance_status.get('last_service_date', 'N/A'),
                    "next_service_date": maintenance_status.get('next_service_date', 'N/A'),
                    "days_since_last_service": maintenance_status.get('days_since_last_service', 'N/A'),
                    "days_until_next_service": maintenance_status.get('days_until_next_service', 'N/A'),
                    "overdue": maintenance_status.get('overdue', False),
                    "recommended_service": maintenance_status.get('recommended_service', 'Unknown')
                },
                "recent_maintenance": recent_maintenance[:10],  # Last 10 records
                "total_records": len(maintenance_history),
                "message": self._format_english_maintenance_report(vehicle, maintenance_status, recent_maintenance)
            }
        
        return report
    
    def _format_english_maintenance_report(self, vehicle: Dict, status: Dict, recent_maintenance: List[Dict]) -> str:
        """Format maintenance report in English"""
        message = f"🔧 **Vehicle Maintenance Report**\n\n"
        message += f"🚗 **Vehicle:** {vehicle.get('name', 'Unknown')}\n"
        message += f"📋 **License Plate:** {vehicle.get('license_plate', 'N/A')}\n"
        message += f"🚙 **Vehicle Type:** {vehicle.get('type', 'Unknown')}\n"
        message += f"📅 **Year:** {vehicle.get('year', 'N/A')}\n"
        message += f"🛣️ **Mileage:** {vehicle.get('mileage', 'N/A')}\n\n"
        
        message += f"📊 **Maintenance Status:**\n"
        message += f"  • Status: {status.get('status', 'Unknown').replace('_', ' ').title()}\n"
        message += f"  • Last Service: {status.get('last_service_date', 'N/A')}\n"
        message += f"  • Next Service: {status.get('next_service_date', 'N/A')}\n"
        message += f"  • Days Since Last: {status.get('days_since_last_service', 'N/A')}\n"
        message += f"  • Days Until Next: {status.get('days_until_next_service', 'N/A')}\n"
        message += f"  • Overdue: {'Yes' if status.get('overdue', False) else 'No'}\n"
        message += f"  • Recommended: {status.get('recommended_service', 'Unknown').replace('_', ' ').title()}\n\n"
        
        if recent_maintenance:
            message += f"📝 **Recent Maintenance (Last 6 months):**\n"
            for record in recent_maintenance[:5]:  # Show last 5
                message += f"  • {record.get('date', 'N/A')} - {record.get('type', 'Unknown').replace('_', ' ').title()}\n"
                message += f"    Cost: ${record.get('cost', 0.0):.2f} | Technician: {record.get('technician', 'N/A')}\n"
        else:
            message += f"📝 **Recent Maintenance:** No records in the last 6 months\n"
        
        return message
    
    def _format_hebrew_maintenance_report(self, vehicle: Dict, status: Dict, recent_maintenance: List[Dict]) -> str:
        """Format maintenance report in Hebrew"""
        message = f"🔧 **דוח תחזוקה לרכב**\n\n"
        message += f"🚗 **רכב:** {vehicle.get('name', 'Unknown')}\n"
        message += f"📋 **לוחית רישוי:** {vehicle.get('license_plate', 'N/A')}\n"
        message += f"🚙 **סוג רכב:** {vehicle.get('type', 'Unknown')}\n"
        message += f"📅 **שנה:** {vehicle.get('year', 'N/A')}\n"
        message += f"🛣️ **קילומטרז':** {vehicle.get('mileage', 'N/A')}\n\n"
        
        message += f"📊 **סטטוס תחזוקה:**\n"
        message += f"  • סטטוס: {status.get('status', 'Unknown').replace('_', ' ').title()}\n"
        message += f"  • שירות אחרון: {status.get('last_service_date', 'N/A')}\n"
        message += f"  • שירות הבא: {status.get('next_service_date', 'N/A')}\n"
        message += f"  • ימים מאז אחרון: {status.get('days_since_last_service', 'N/A')}\n"
        message += f"  • ימים עד הבא: {status.get('days_until_next_service', 'N/A')}\n"
        message += f"  • בפיגור: {'כן' if status.get('overdue', False) else 'לא'}\n"
        message += f"  • מומלץ: {status.get('recommended_service', 'Unknown').replace('_', ' ').title()}\n\n"
        
        if recent_maintenance:
            message += f"📝 **תחזוקה אחרונה (6 חודשים אחרונים):**\n"
            for record in recent_maintenance[:5]:  # Show last 5
                message += f"  • {record.get('date', 'N/A')} - {record.get('type', 'Unknown').replace('_', ' ').title()}\n"
                message += f"    עלות: ${record.get('cost', 0.0):.2f} | טכנאי: {record.get('technician', 'N/A')}\n"
        else:
            message += f"📝 **תחזוקה אחרונה:** אין רשומות ב-6 החודשים האחרונים\n"
        
        return message
    
    def get_vehicles_due_for_maintenance(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get vehicles due for maintenance within specified days
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of vehicles with maintenance status
        """
        alerts = self.get_maintenance_alerts(days_ahead)
        vehicles = []
        
        for alert in alerts:
            if alert.alert_type in ['due', 'overdue']:
                vehicles.append({
                    'vehicle_id': alert.vehicle_id,
                    'vehicle_name': alert.vehicle_name,
                    'license_plate': alert.license_plate,
                    'alert_type': alert.alert_type,
                    'days_until_due': alert.days_until_due,
                    'service_type': alert.service_type,
                    'priority': alert.priority,
                    'estimated_cost': alert.estimated_cost,
                    'description': alert.description
                })
        
        return vehicles
    
    def refresh_data(self):
        """Refresh all cached data"""
        self._maintenance_records_cache = None
        self._vehicles_cache = None
        self.logger.info("Maintenance Tracker data refreshed")


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Initialize tracker
    tracker = MaintenanceTracker(
        maintenance_records_path="data/vehicles/maintenance_records.json",
        vehicle_catalog_path="data/vehicle_catalog.json"
    )
    
    # Test maintenance alerts
    print("=== Maintenance Alerts ===")
    alerts = tracker.get_maintenance_alerts(days_ahead=30)
    print(f"Found {len(alerts)} maintenance alerts")
    
    for alert in alerts[:3]:  # Show first 3
        print(f"  - {alert.vehicle_name} ({alert.license_plate}): {alert.description}")
    
    # Test maintenance statistics
    print("\n=== Maintenance Statistics ===")
    stats = tracker.get_maintenance_statistics()
    print(f"Total vehicles: {stats.total_vehicles}")
    print(f"Vehicles due: {stats.vehicles_due}")
    print(f"Vehicles overdue: {stats.vehicles_overdue}")
    print(f"Total cost (30 days): ${stats.total_cost_30_days:.2f}")
    print(f"Total cost (90 days): ${stats.total_cost_90_days:.2f}")
    print(f"Total cost (year): ${stats.total_cost_year:.2f}")
    print(f"Average cost per vehicle: ${stats.average_cost_per_vehicle:.2f}")
    print(f"Most common service: {stats.most_common_service}")
    print(f"Maintenance frequency: {stats.maintenance_frequency:.2f} services/vehicle/year")
