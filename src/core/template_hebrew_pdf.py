#!/usr/bin/env python3
"""
Template-based Hebrew PDF Generator
Follows the professional design template specification
"""

import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Frame
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.colors import HexColor

class TemplateHebrewPDFGenerator:
    """Template-based Hebrew PDF Generator following professional design specs"""
    
    def __init__(self):
        """Initialize the template-based Hebrew PDF generator"""
        self.hebrew_font = self._find_best_hebrew_font()
        print(f"Using font: {self.hebrew_font}")
        
        # Template colors from the design spec
        self.colors = {
            'primary': HexColor('#003366'),
            'accent': HexColor('#E6B400'),
            'text': HexColor('#111111'),
            'muted': HexColor('#555555'),
            'surface': HexColor('#F7F8FA'),
            'tableHeaderBg': HexColor('#003366'),
            'tableHeaderFg': HexColor('#FFFFFF'),
            'tableStripeA': HexColor('#FFFFFF'),
            'tableStripeB': HexColor('#F0F2F5'),
            'border': HexColor('#D8DCE1')
        }
    
    def _find_best_hebrew_font(self):
        """Find the best available Hebrew font"""
        font_options = [
            ('Noto Sans Hebrew', 'NotoSansHebrew-Regular.ttf'),
            ('Assistant', 'Assistant-Regular.ttf'),
            ('Rubik', 'Rubik-Regular.ttf'),
            ('Arial Unicode MS', 'arial.ttf'),
            ('Tahoma', 'tahoma.ttf'),
            ('Times New Roman', 'times.ttf'),
            ('HeiseiKakuGo-W5', None),
            ('Helvetica', None)
        ]
        
        for font_name, font_file in font_options:
            try:
                if font_file:
                    font_path = self._find_font_file(font_file)
                    if font_path:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        print(f"Successfully registered TTF font: {font_name}")
                        return font_name
                else:
                    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
                    print(f"Successfully registered CID font: {font_name}")
                    return font_name
            except Exception as e:
                print(f"Failed to register {font_name}: {e}")
                continue
        
        print("Using Helvetica as ultimate fallback")
        return 'Helvetica'
    
    def _find_font_file(self, filename):
        """Find font file in common locations"""
        common_paths = [
            f'C:/Windows/Fonts/{filename}',
            f'C:/Windows/Fonts/{filename.upper()}',
            f'C:/Windows/Fonts/{filename.lower()}',
            f'fonts/{filename}',
            f'/System/Library/Fonts/{filename}',
            f'/usr/share/fonts/truetype/{filename}',
            f'/usr/share/fonts/{filename}'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _reverse_hebrew_text(self, text):
        """Reverse Hebrew text to fix RTL display issues"""
        if not text or not isinstance(text, str):
            return text
        
        words = text.split()
        reversed_words = []
        
        for word in words:
            if any('\u0590' <= char <= '\u05FF' for char in word):
                reversed_words.append(word[::-1])
            else:
                reversed_words.append(word)
        
        return ' '.join(reversed_words)
    
    def _get_vehicle_color(self, vehicle_data):
        """Get vehicle color from specifications"""
        try:
            specs = vehicle_data.get('specifications', {})
            color = specs.get('color', 'לא זמין')
            if color and color != 'לא זמין':
                return color
        except:
            pass
        return vehicle_data.get('color', 'לא זמין')
    
    def _get_driver_name(self, vehicle_data):
        """Get driver name from driver object"""
        try:
            driver = vehicle_data.get('driver', {})
            if isinstance(driver, dict):
                return driver.get('name', 'לא זמין')
            return str(driver) if driver else 'לא זמין'
        except:
            return 'לא זמין'
    
    def _get_driver_phone(self, vehicle_data):
        """Get driver phone from driver object"""
        try:
            driver = vehicle_data.get('driver', {})
            if isinstance(driver, dict):
                return driver.get('phone', 'לא זמין')
            return 'לא זמין'
        except:
            return 'לא זמין'
    
    def _get_driver_email(self, vehicle_data):
        """Get driver email from driver object"""
        try:
            driver = vehicle_data.get('driver', {})
            if isinstance(driver, dict):
                return driver.get('email', 'לא זמין')
            return 'לא זמין'
        except:
            return 'לא זמין'
    
    def create_template_styles(self):
        """Create styles following the template specification"""
        styles = getSampleStyleSheet()
        font_name = self.hebrew_font
        
        # Display style (22pt)
        display_style = ParagraphStyle(
            'Display',
            parent=styles['Heading1'],
            fontSize=22,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=self.colors['primary'],
            fontName=font_name,
            fontWeight='bold',
            letterSpacing=0.2
        )
        
        # Large style (18pt)
        large_style = ParagraphStyle(
            'Large',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=20,
            textColor=self.colors['primary'],
            fontName=font_name,
            fontWeight='bold'
        )
        
        # Medium style (14pt)
        medium_style = ParagraphStyle(
            'Medium',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=15,
            textColor=self.colors['primary'],
            fontName=font_name,
            fontWeight='bold'
        )
        
        # Small style (10.5pt)
        small_style = ParagraphStyle(
            'Small',
            parent=styles['Normal'],
            fontSize=10.5,
            spaceAfter=6,
            textColor=self.colors['muted'],
            fontName=font_name,
            lineHeight=1.35
        )
        
        # Regular style (12pt)
        regular_style = ParagraphStyle(
            'Regular',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            textColor=self.colors['text'],
            fontName=font_name,
            lineHeight=1.35
        )
        
        # Extra small style (9pt)
        xs_style = ParagraphStyle(
            'ExtraSmall',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            textColor=self.colors['muted'],
            fontName=font_name,
            lineHeight=1.35
        )
        
        return {
            'display': display_style,
            'large': large_style,
            'medium': medium_style,
            'small': small_style,
            'regular': regular_style,
            'xs': xs_style
        }
    
    def generate_maintenance_report(self, vehicle_data, maintenance_records, output_path):
        """Generate a maintenance report PDF following the template design"""
        
        # Create document with template margins (15mm = 42.5 points)
        doc = SimpleDocTemplate(
            output_path, 
            pagesize=A4,
            rightMargin=42.5,  # 15mm
            leftMargin=42.5,   # 15mm
            topMargin=42.5,    # 15mm
            bottomMargin=42.5  # 15mm
        )
        
        styles = self.create_template_styles()
        story = []
        
        # Header Section
        story.extend(self._create_header(vehicle_data, styles))
        
        # Vehicle Information Section
        story.extend(self._create_vehicle_info_section(vehicle_data, styles))
        
        # Maintenance Records Section
        story.extend(self._create_maintenance_records_section(maintenance_records, styles))
        
        # Fault Reports Section
        story.extend(self._create_faults_section(maintenance_records, styles))
        
        # Summary Section
        story.extend(self._create_summary_section(maintenance_records, styles))
        
        # Approvals Section
        story.extend(self._create_approvals_section(styles))
        
        # Footer
        story.extend(self._create_footer(styles))
        
        # Build PDF
        doc.build(story)
        print(f"Generated template-based Hebrew PDF report: {output_path}")
    
    def _create_header(self, vehicle_data, styles):
        """Create header section following template"""
        story = []
        
        # Main title - centered
        title_text = self._reverse_hebrew_text("דוח תחזוקת רכב")
        centered_display_style = ParagraphStyle(
            'CenteredDisplay',
            parent=styles['display'],
            alignment=TA_CENTER
        )
        story.append(Paragraph(title_text, centered_display_style))
        
        # Subline with document info
        doc_number = f"OPS-MAINT-{datetime.now().strftime('%Y-%m-%d')}"
        generated_date = datetime.now().strftime('%d/%m/%Y')
        vehicle_status = vehicle_data.get('status', 'פעיל')
        
        subline_data = [
            f"מחלקה: תפעול – יחידת רכב ותחזוקה",
            f"מס' דוח: {doc_number}",
            f"תאריך הפקה: {generated_date}",
            f"סטטוס רכב: {vehicle_status}"
        ]
        
        for line in subline_data:
            centered_small_style = ParagraphStyle(
                'CenteredSmall',
                parent=styles['small'],
                alignment=TA_CENTER
            )
            story.append(Paragraph(self._reverse_hebrew_text(line), centered_small_style))
        
        # Divider line
        story.append(Spacer(1, 10))
        story.append(Paragraph("<hr/>", styles['regular']))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_vehicle_info_section(self, vehicle_data, styles):
        """Create vehicle information section with card layout"""
        story = []
        
        # Section title - centered
        section_title = self._reverse_hebrew_text("פרטי רכב")
        centered_style = ParagraphStyle(
            'CenteredLarge',
            parent=styles['large'],
            alignment=TA_CENTER
        )
        story.append(Paragraph(section_title, centered_style))
        story.append(Spacer(1, 10))
        
        # Vehicle data
        vehicle_color = self._get_vehicle_color(vehicle_data)
        driver_name = self._get_driver_name(vehicle_data)
        driver_phone = self._get_driver_phone(vehicle_data)
        driver_email = self._get_driver_email(vehicle_data)
        
        # Create two-column layout with labels on the right
        vehicle_data = [
            [vehicle_data.get('license_plate', 'לא זמין'), self._reverse_hebrew_text("מספר רישוי")],
            [f"{vehicle_data.get('make', 'לא זמין')} / {vehicle_data.get('model', 'לא זמין')}", self._reverse_hebrew_text("יצרן / דגם")],
            [str(vehicle_data.get('year', 'לא זמין')), self._reverse_hebrew_text("שנה")],
            [vehicle_color, self._reverse_hebrew_text("צבע")],
            [vehicle_data.get('status', 'לא זמין'), self._reverse_hebrew_text("סטטוס")],
            [vehicle_data.get('location', 'לא זמין'), self._reverse_hebrew_text("מיקום")],
            [self._reverse_hebrew_text(driver_name), self._reverse_hebrew_text("נהג אחראי")],
            [driver_phone, self._reverse_hebrew_text("טלפון")],
            [driver_email, self._reverse_hebrew_text("אימייל")]
        ]
        
        # Create table with card styling - data on left, labels on right
        vehicle_table = Table(vehicle_data, colWidths=[3*inch, 2.5*inch])
        vehicle_table.setStyle(TableStyle([
            # Data column styling (left column)
            ('BACKGROUND', (0, 0), (0, -1), self.colors['tableStripeA']),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['text']),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            # Label column styling (right column)
            ('BACKGROUND', (1, 0), (1, -1), self.colors['surface']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['text']),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            # Common styling
            ('FONTNAME', (0, 0), (-1, -1), self.hebrew_font),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            # Borders
            ('BOX', (0, 0), (-1, -1), 1, self.colors['border']),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, self.colors['border']),
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.colors['tableStripeA'], self.colors['tableStripeB']])
        ]))
        
        story.append(vehicle_table)
        story.append(Spacer(1, 25))
        
        return story
    
    def _create_maintenance_records_section(self, maintenance_records, styles):
        """Create maintenance records section with professional table"""
        story = []
        
        # Section title - centered
        section_title = self._reverse_hebrew_text("רשומות תחזוקה")
        centered_style = ParagraphStyle(
            'CenteredLarge',
            parent=styles['large'],
            alignment=TA_CENTER
        )
        story.append(Paragraph(section_title, centered_style))
        story.append(Spacer(1, 10))
        
        if maintenance_records:
            # Table headers
            headers = [
                self._reverse_hebrew_text("תאריך"),
                self._reverse_hebrew_text("סוג טיפול"),
                self._reverse_hebrew_text("תיאור"),
                self._reverse_hebrew_text("עלות (₪)"),
                self._reverse_hebrew_text("סטטוס")
            ]
            
            # Table data
            table_data = [headers]
            for record in maintenance_records:
                # Create Hebrew description based on record type and cost
                record_type = record.get('type', '')
                cost = record.get('cost', 0)
                
                if cost > 0:
                    if 'תחזוקה' in record_type or 'Maintenance' in record_type:
                        description = f"תחזוקה שוטפת - עלות {cost:,.0f} ₪"
                    elif 'תיקון' in record_type or 'Repair' in record_type:
                        description = f"תיקון תקלה - עלות {cost:,.0f} ₪"
                    else:
                        description = f"טיפול כללי - עלות {cost:,.0f} ₪"
                else:
                    description = "בדיקה תקופתית ללא עלות"
                
                if len(description) > 50:
                    description = description[:50] + '...'
                
                status = record.get('status', 'לא זמין')
                cost_display = f"{cost:,.0f}" if cost > 0 else '0'
                
                table_data.append([
                    record.get('date', 'לא זמין'),
                    self._reverse_hebrew_text(record.get('type', 'לא זמין')),
                    self._reverse_hebrew_text(description),
                    cost_display,
                    self._reverse_hebrew_text(status)
                ])
            
            # Create table
            maintenance_table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 2.4*inch, 0.8*inch, 0.8*inch])
            maintenance_table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['tableHeaderBg']),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.colors['tableHeaderFg']),
                ('FONTNAME', (0, 0), (-1, 0), self.hebrew_font),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                # Data styling
                ('FONTNAME', (0, 1), (-1, -1), self.hebrew_font),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.colors['tableStripeA'], self.colors['tableStripeB']]),
                # Borders
                ('BOX', (0, 0), (-1, -1), 1, self.colors['border']),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, self.colors['border'])
            ]))
            
            story.append(maintenance_table)
        else:
            no_data_text = self._reverse_hebrew_text("אין רשומות תחזוקה זמינות")
            story.append(Paragraph(no_data_text, styles['regular']))
        
        story.append(Spacer(1, 25))
        return story
    
    def _create_faults_section(self, maintenance_records, styles):
        """Create fault reports section"""
        story = []
        
        # Filter fault records
        fault_records = [r for r in maintenance_records if r.get('fault_type')]
        
        if fault_records:
            # Section title - centered
            section_title = self._reverse_hebrew_text("דוחות תקלות")
            centered_style = ParagraphStyle(
                'CenteredLarge',
                parent=styles['large'],
                alignment=TA_CENTER
            )
            story.append(Paragraph(section_title, centered_style))
            story.append(Spacer(1, 10))
            
            # Table headers
            headers = [
                self._reverse_hebrew_text("תאריך"),
                self._reverse_hebrew_text("סוג תקלה"),
                self._reverse_hebrew_text("חומרה"),
                self._reverse_hebrew_text("עלות תיקון (₪)"),
                self._reverse_hebrew_text("זמן תיקון (ימים)")
            ]
            
            # Table data
            table_data = [headers]
            for record in fault_records:
                repair_cost = f"{record.get('repair_cost', 0):,.0f}" if record.get('repair_cost', 0) > 0 else '0'
                
                table_data.append([
                    record.get('date', 'לא זמין'),
                    self._reverse_hebrew_text(record.get('fault_type', 'לא זמין')),
                    self._reverse_hebrew_text(record.get('fault_severity', 'לא זמין')),
                    repair_cost,
                    str(record.get('repair_days', 0))
                ])
            
            # Create table
            fault_table = Table(table_data, colWidths=[1.2*inch, 1.4*inch, 1*inch, 1.2*inch, 1.2*inch])
            fault_table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['tableHeaderBg']),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.colors['tableHeaderFg']),
                ('FONTNAME', (0, 0), (-1, 0), self.hebrew_font),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                # Data styling
                ('FONTNAME', (0, 1), (-1, -1), self.hebrew_font),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [self.colors['tableStripeA'], self.colors['tableStripeB']]),
                # Borders
                ('BOX', (0, 0), (-1, -1), 1, self.colors['border']),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, self.colors['border'])
            ]))
            
            story.append(fault_table)
            story.append(Spacer(1, 25))
        
        return story
    
    def _create_summary_section(self, maintenance_records, styles):
        """Create summary section with cards"""
        story = []
        
        # Section title
        section_title = self._reverse_hebrew_text("סיכום כספי כולל")
        story.append(Paragraph(section_title, styles['large']))
        story.append(Spacer(1, 10))
        
        # Calculate summary data
        total_maintenance = len(maintenance_records)
        total_cost = sum(record.get('cost', 0) for record in maintenance_records)
        fault_count = len([r for r in maintenance_records if r.get('fault_type')])
        total_repair_cost = sum(record.get('repair_cost', 0) for record in maintenance_records)
        total_all_cost = total_cost + total_repair_cost
        
        # Create summary cards
        summary_data = [
            [self._reverse_hebrew_text("סה״כ טיפולים"), str(total_maintenance)],
            [self._reverse_hebrew_text("עלות טיפולים"), f"₪{total_cost:,.0f}"],
            [self._reverse_hebrew_text("סה״כ תקלות"), str(fault_count)],
            [self._reverse_hebrew_text("עלות תיקונים"), f"₪{total_repair_cost:,.0f}"],
            [self._reverse_hebrew_text("עלות כוללת"), f"₪{total_all_cost:,.0f}"]
        ]
        
        # Create summary table
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.colors['surface']),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['text']),
            ('FONTNAME', (0, 0), (-1, -1), self.hebrew_font),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            # Data styling
            ('BACKGROUND', (1, 0), (1, -1), self.colors['tableStripeA']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['text']),
            # Special styling for total cost
            ('BACKGROUND', (0, 4), (1, 4), self.colors['accent']),
            ('TEXTCOLOR', (0, 4), (1, 4), self.colors['text']),
            ('FONTWEIGHT', (0, 4), (1, 4), 'bold'),
            # Borders
            ('BOX', (0, 0), (-1, -1), 1, self.colors['border']),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, self.colors['border'])
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 25))
        
        return story
    
    def _create_approvals_section(self, styles):
        """Create approvals section with signature lines"""
        story = []
        
        # Section title
        section_title = self._reverse_hebrew_text("חתימות ואישורים")
        story.append(Paragraph(section_title, styles['large']))
        story.append(Spacer(1, 10))
        
        # Signature rows
        signature_data = [
            [self._reverse_hebrew_text("מאשר תחזוקה"), "", "", ""],
            [self._reverse_hebrew_text("אישור מנהל תפעול"), "", "", ""]
        ]
        
        signature_table = Table(signature_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), self.hebrew_font),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            # Borders
            ('BOX', (0, 0), (-1, -1), 1, self.colors['border']),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, self.colors['border'])
        ]))
        
        story.append(signature_table)
        story.append(Spacer(1, 25))
        
        return story
    
    def _create_footer(self, styles):
        """Create footer section"""
        story = []
        
        # Footer content
        footer_text = f"Confidential — Operations | עמוד 1 מתוך 1 | גרסה 1.0"
        story.append(Paragraph(self._reverse_hebrew_text(footer_text), styles['xs']))
        
        return story

def test_template_hebrew_pdf():
    """Test template-based Hebrew PDF generation"""
    generator = TemplateHebrewPDFGenerator()
    
    # Test data
    vehicle_data = {
        'license_plate': '10-600-42',
        'make': 'Mazda',
        'model': 'Mazda3',
        'year': 2022,
        'specifications': {
            'color': 'כסוף',
            'interior_color': 'אפור'
        },
        'location': 'Operations',
        'status': 'פעיל',
        'driver': {
            'name': 'אלון ישראלי',
            'phone': '+972-51-9268240',
            'email': 'alon.israeli@company.co.il'
        }
    }
    
    maintenance_records = [
        {
            'date': '25/08/2024',
            'type': 'שגרתית',
            'description': 'טיפול תקופתי מלא',
            'cost': 2458,
            'status': 'הושלם',
            'fault_type': 'צמיגים',
            'fault_severity': 'חמורה',
            'repair_cost': 2634,
            'repair_days': 5
        },
        {
            'date': '18/07/2024',
            'type': 'מנוע',
            'description': 'בדיקת מנוע ותיקון קל',
            'cost': 1070,
            'status': 'הושלם'
        },
        {
            'date': '23/02/2024',
            'type': 'פליטה',
            'description': 'בדיקת מערכת פליטה',
            'cost': 948,
            'status': 'מתוכנן',
            'fault_type': 'צמיגים',
            'fault_severity': 'קלה',
            'repair_cost': 876,
            'repair_days': 6
        }
    ]
    
    # Generate test PDF
    output_path = 'test_template_hebrew_report.pdf'
    generator.generate_maintenance_report(vehicle_data, maintenance_records, output_path)
    print(f"Test template PDF generated: {output_path}")

if __name__ == "__main__":
    test_template_hebrew_pdf()
