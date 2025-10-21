#!/usr/bin/env python3
"""
Simple Fleet Management Server
One server, one port, handles everything
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from flask import Flask, request, Response, send_file, jsonify
from twilio.twiml.messaging_response import MessagingResponse

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ngrok_url():
    """Get the current ngrok public URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        data = response.json()
        
        for tunnel in data.get('tunnels', []):
            if tunnel.get('proto') == 'https':
                return tunnel.get('public_url')
        
        return None
    except Exception as e:
        logger.error(f"Error getting ngrok URL: {e}")
        return None

app = Flask(__name__)

# Simple data loading
def load_vehicles():
    """Load vehicle data"""
    try:
        vehicle_path = os.path.join(project_root, 'data', 'large_vehicle_catalog.json')
        with open(vehicle_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('vehicles', [])
    except Exception as e:
        logger.error(f"Error loading vehicles: {e}")
        return []

def load_maintenance_records():
    """Load maintenance records"""
    try:
        maintenance_path = os.path.join(project_root, 'data', 'vehicles', 'maintenance_records.json')
        with open(maintenance_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('records', [])
    except Exception as e:
        logger.error(f"Error loading maintenance records: {e}")
        return []

def find_vehicle_by_license_plate(license_plate):
    """Find vehicle by license plate"""
    vehicles = load_vehicles()
    for vehicle in vehicles:
        if vehicle.get('license_plate', '').upper() == license_plate.upper():
            return vehicle
    return None

def get_maintenance_records_for_vehicle(license_plate):
    """Get maintenance records for a vehicle by license plate"""
    records = load_maintenance_records()
    return [record for record in records if record.get('license_plate', '').upper() == license_plate.upper()]

def format_vehicle_search_response(vehicle):
    """Format vehicle information as a structured table response"""
    try:
        # Get driver information
        driver = vehicle.get('driver', {})
        if isinstance(driver, dict):
            driver_name = driver.get('name', 'לא זמין')
            driver_phone = driver.get('phone', 'לא זמין')
            driver_email = driver.get('email', 'לא זמין')
        else:
            driver_name = str(driver) if driver else 'לא זמין'
            driver_phone = 'לא זמין'
            driver_email = 'לא זמין'
        
        # Get vehicle color
        specs = vehicle.get('specifications', {})
        color = specs.get('color', vehicle.get('color', 'לא זמין'))
        
        # Create structured response
        response = f"""**תוצאות חיפוש רכב**

**פרטי הרכב:**
• מספר רישוי: {vehicle.get('license_plate', 'לא זמין')}
• יצרן/דגם: {vehicle.get('make', 'לא זמין')} {vehicle.get('model', 'לא זמין')}
• שנה: {vehicle.get('year', 'לא זמין')}
• צבע: {color}
• סטטוס: {vehicle.get('status', 'לא זמין')}

**פרטי נהג:**
• שם נהג: {driver_name}
• טלפון: {driver_phone}
• אימייל: {driver_email}"""
        
        return response
        
    except Exception as e:
        logger.error(f"Error formatting vehicle search response: {e}")
        return f"שגיאה בעיבוד פרטי הרכב: {str(e)}"

def generate_simple_pdf_report(vehicle, maintenance_records):
    """Generate a Hebrew PDF report"""
    try:
        from src.core.template_hebrew_pdf import TemplateHebrewPDFGenerator
        
        # Create PDF
        reports_dir = os.path.join(project_root, 'reports', 'maintenance_reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"maintenance_report_{timestamp}_{vehicle.get('license_plate', 'unknown')}.pdf"
        file_path = os.path.join(reports_dir, filename)
        
        # Use template-based Hebrew PDF generator
        generator = TemplateHebrewPDFGenerator()
        generator.generate_maintenance_report(vehicle, maintenance_records, file_path)
        
        return file_path
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return None

@app.route('/webhook', methods=['POST'])
def webhook():
    """Main webhook endpoint for WhatsApp messages"""
    try:
        # Get message data
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        if not incoming_msg:
            logger.warning("Empty message received")
            return Response("Empty message", status=400)
        
        logger.info(f"Raw message from {sender}: '{incoming_msg}'")
        
        # Check if it's a maintenance report request
        is_maintenance_report = any(keyword in incoming_msg.lower() for keyword in [
            'maintenance report', 'דוח תחזוקה', 'דוח טיפולים', 'תחזוקה', 'טיפולים'
        ])
        
        # Check if it's a fault report request
        is_fault_report = any(keyword in incoming_msg.lower() for keyword in [
            'fault report', 'דוח תקלות', 'תקלות', 'דוח תקלה'
        ])
        
        # Check if it's a vehicle search request
        is_vehicle_search = any(keyword in incoming_msg.lower() for keyword in [
            'search', 'חיפוש', 'מצא', 'find', 'חפש'
        ])
        
        if is_vehicle_search:
            # Extract license plate from search request
            import re
            license_pattern = r'(\d{2}[- ]?\d{3}[- ]?\d{2})'
            matches = re.findall(license_pattern, incoming_msg)
            
            if matches:
                license_plate = matches[0].replace(' ', '-')
                logger.info(f"Vehicle search for license plate: {license_plate}")
                
                # Find vehicle
                vehicle = find_vehicle_by_license_plate(license_plate)
                if vehicle:
                    # Format vehicle information as a structured table
                    vehicle_info = format_vehicle_search_response(vehicle)
                    
                    twiml_response = MessagingResponse()
                    twiml_response.message(vehicle_info)
                    return Response(str(twiml_response), mimetype='text/xml')
                else:
                    error_msg = f"רכב עם לוחית רישוי {license_plate} לא נמצא במערכת."
                    twiml_response = MessagingResponse()
                    twiml_response.message(error_msg)
                    return Response(str(twiml_response), mimetype='text/xml')
            else:
                error_msg = "לא נמצאה לוחית רישוי בהודעה. אנא ציין לוחית רישוי לחיפוש."
                twiml_response = MessagingResponse()
                twiml_response.message(error_msg)
                return Response(str(twiml_response), mimetype='text/xml')
        
        elif is_fault_report:
            # Extract license plate from fault report request
            import re
            license_pattern = r'(\d{2}[- ]?\d{3}[- ]?\d{2})'
            matches = re.findall(license_pattern, incoming_msg)
            
            if matches:
                license_plate = matches[0].replace(' ', '-')
                logger.info(f"Fault report request for license plate: {license_plate}")
                
                # Find vehicle
                vehicle = find_vehicle_by_license_plate(license_plate)
                if vehicle:
                    # Get maintenance records (fault reports are part of maintenance records)
                    maintenance_records = get_maintenance_records_for_vehicle(license_plate)
                    
                    # Generate PDF (same as maintenance report for now)
                    pdf_path = generate_simple_pdf_report(vehicle, maintenance_records)
                    if pdf_path:
                        filename = os.path.basename(pdf_path)
                        # Get current ngrok URL dynamically
                        ngrok_url = get_ngrok_url()
                        if ngrok_url:
                            download_url = f"{ngrok_url}/download/{filename}"
                        else:
                            download_url = f"http://localhost:5000/download/{filename}"
                        
                        # Generate TwiML response with media
                        twiml_response = MessagingResponse()
                        message = twiml_response.message(f"דוח התקלות עבור {license_plate} מוכן. הקובץ מצורף להודעה.")
                        message.media(download_url)
                        
                        logger.info(f"Sending fault report to {sender}: {download_url}")
                        return Response(str(twiml_response), mimetype='text/xml')
                    else:
                        error_msg = "שגיאה ביצירת דוח התקלות."
                        twiml_response = MessagingResponse()
                        twiml_response.message(error_msg)
                        return Response(str(twiml_response), mimetype='text/xml')
                else:
                    error_msg = f"רכב עם לוחית רישוי {license_plate} לא נמצא."
                    twiml_response = MessagingResponse()
                    twiml_response.message(error_msg)
                    return Response(str(twiml_response), mimetype='text/xml')
            else:
                error_msg = "לא נמצאה לוחית רישוי בהודעה. אנא ציין לוחית רישוי."
                twiml_response = MessagingResponse()
                twiml_response.message(error_msg)
                return Response(str(twiml_response), mimetype='text/xml')
        
        elif is_maintenance_report:
            # Extract license plate
            import re
            license_pattern = r'(\d{2}[- ]?\d{3}[- ]?\d{2})'
            matches = re.findall(license_pattern, incoming_msg)
            
            if matches:
                license_plate = matches[0].replace(' ', '-')
                logger.info(f"Found license plate: {license_plate}")
                
                # Find vehicle
                vehicle = find_vehicle_by_license_plate(license_plate)
                if vehicle:
                    # Get maintenance records
                    maintenance_records = get_maintenance_records_for_vehicle(license_plate)
                    
                    # Generate PDF
                    pdf_path = generate_simple_pdf_report(vehicle, maintenance_records)
                    if pdf_path:
                        filename = os.path.basename(pdf_path)
                        # Get current ngrok URL dynamically
                        ngrok_url = get_ngrok_url()
                        if ngrok_url:
                            download_url = f"{ngrok_url}/download/{filename}"
                        else:
                            download_url = f"http://localhost:5000/download/{filename}"
                        
                        # Generate TwiML response with media
                        twiml_response = MessagingResponse()
                        message = twiml_response.message(f"דוח התחזוקה עבור {license_plate} מוכן. הקובץ מצורף להודעה.")
                        message.media(download_url)
                        
                        logger.info(f"Sending media response to {sender}: {download_url}")
                        return Response(str(twiml_response), mimetype='text/xml')
                    else:
                        error_msg = "שגיאה ביצירת דוח התחזוקה."
                        twiml_response = MessagingResponse()
                        twiml_response.message(error_msg)
                        return Response(str(twiml_response), mimetype='text/xml')
                else:
                    error_msg = f"רכב עם לוחית רישוי {license_plate} לא נמצא."
                    twiml_response = MessagingResponse()
                    twiml_response.message(error_msg)
                    return Response(str(twiml_response), mimetype='text/xml')
            else:
                error_msg = "לא נמצאה לוחית רישוי בהודעה. אנא ציין לוחית רישוי."
                twiml_response = MessagingResponse()
                twiml_response.message(error_msg)
                return Response(str(twiml_response), mimetype='text/xml')
        else:
            # Handle other requests - show available commands
            twiml_response = MessagingResponse()
            help_message = """**מערכת ניהול צי רכבים**

**פקודות זמינות:**
• חיפוש [לוחית רישוי] - חיפוש פרטי רכב
• דוח תחזוקה [לוחית רישוי] - דוח תחזוקה PDF
• דוח תקלות [לוחית רישוי] - דוח תקלות PDF

**דוגמאות:**
• חיפוש 21-599-58
• דוח תחזוקה 22-727-57
• דוח תקלות 10-600-42"""
            twiml_response.message(help_message)
            return Response(str(twiml_response), mimetype='text/xml')
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        twiml_response = MessagingResponse()
        twiml_response.message("מצטער, אירעה שגיאה בעיבוד הבקשה שלך.")
        return Response(str(twiml_response), mimetype='text/xml')

@app.route('/download/<filename>')
def download_file(filename):
    """Download PDF files"""
    try:
        reports_dir = os.path.join(project_root, 'reports', 'maintenance_reports')
        file_path = os.path.join(reports_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        return jsonify({"error": "File serving error"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "simple_fleet_server",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    try:
        logger.info("Starting Simple Fleet Management Server on port 5000")
        logger.info("Available endpoints:")
        logger.info("  POST /webhook - Main webhook for WhatsApp messages")
        logger.info("  GET  /download/<filename> - Download PDF files")
        logger.info("  GET  /health - Health check")
        
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
