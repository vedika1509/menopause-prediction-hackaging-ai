"""
PDF Generator for MenoBalance AI
Generates health summaries and reports using reportlab library.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import streamlit as st


class MenoBalancePDFGenerator:
    """PDF generator for MenoBalance AI health reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom styles for the PDF."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#9B59B6'),
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=HexColor('#9B59B6'),
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            textColor=black,
            fontName='Helvetica'
        ))
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=15,
            textColor=HexColor('#9B59B6'),
            fontName='Helvetica-Bold'
        ))

    def generate_health_summary_pdf(self, user_data, predictions=None, wellness_data=None):
        """Generate a comprehensive health summary PDF."""
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"menobalance_health_summary_{timestamp}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build the story (content)
        story = []
        
        # Add title page
        story.extend(self._create_title_page())
        
        # Add user information
        if user_data:
            story.extend(self._create_user_info_section(user_data))
        
        # Add predictions section
        if predictions:
            story.extend(self._create_predictions_section(predictions))
        
        # Add wellness data section
        if wellness_data:
            story.extend(self._create_wellness_section(wellness_data))
        
        # Add recommendations section
        story.extend(self._create_recommendations_section())
        
        # Add disclaimer
        story.extend(self._create_disclaimer_section())
        
        # Build PDF
        doc.build(story)
        
        return filename

    def _create_title_page(self):
        """Create the title page content."""
        story = []
        
        # Add title
        story.append(Paragraph("🌸 MenoBalance AI", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("Health Summary Report", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 30))
        
        # Add current date
        current_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"Generated on: {current_date}", self.styles['CustomBody']))
        story.append(Spacer(1, 40))
        
        # Add description
        description = """
        This comprehensive health summary provides insights into your menopause journey,
        wellness metrics, and personalized recommendations based on AI analysis.
        """
        story.append(Paragraph(description, self.styles['CustomBody']))
        
        story.append(PageBreak())
        return story

    def _create_user_info_section(self, user_data):
        """Create user information section."""
        story = []
        
        story.append(Paragraph("Personal Information", self.styles['CustomHeader']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=HexColor('#9B59B6')))
        story.append(Spacer(1, 12))
        
        # Create user info table
        user_info_data = [
            ["Age", str(user_data.get('age', 'Not specified'))],
            ["BMI", str(user_data.get('bmi', 'Not specified'))],
            ["Menopause Stage", user_data.get('menopause_stage', 'Not specified')],
            ["Last Period", user_data.get('last_period', 'Not specified')],
        ]
        
        user_table = Table(user_info_data, colWidths=[2*inch, 3*inch])
        user_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#E8DAEF')),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(user_table)
        story.append(Spacer(1, 20))
        
        return story

    def _create_predictions_section(self, predictions):
        """Create predictions section."""
        story = []
        
        story.append(Paragraph("AI Predictions & Insights", self.styles['CustomHeader']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=HexColor('#9B59B6')))
        story.append(Spacer(1, 12))
        
        if isinstance(predictions, dict):
            for prediction_type, data in predictions.items():
                story.append(Paragraph(f"{prediction_type.replace('_', ' ').title()}", self.styles['CustomSubtitle']))
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        story.append(Paragraph(f"• {key}: {value}", self.styles['CustomBody']))
                else:
                    story.append(Paragraph(f"• {data}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 10))
        
        return story

    def _create_wellness_section(self, wellness_data):
        """Create wellness data section."""
        story = []
        
        story.append(Paragraph("Wellness Metrics", self.styles['CustomHeader']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=HexColor('#9B59B6')))
        story.append(Spacer(1, 12))
        
        # Create wellness metrics table
        wellness_metrics = [
            ["Metric", "Score", "Status"],
            ["Overall Wellness", f"{wellness_data.get('wellness_score', 0)}/100", self._get_status(wellness_data.get('wellness_score', 0), 100)],
            ["Sleep Quality", f"{wellness_data.get('sleep_quality', 0)}/10", self._get_status(wellness_data.get('sleep_quality', 0), 10)],
            ["Stress Level", f"{wellness_data.get('stress_level', 0)}/10", self._get_status(wellness_data.get('stress_level', 0), 10, reverse=True)],
            ["Activity Level", f"{wellness_data.get('activity_level', 0)}/10", self._get_status(wellness_data.get('activity_level', 0), 10)],
            ["Mood Score", f"{wellness_data.get('mood_score', 0)}/10", self._get_status(wellness_data.get('mood_score', 0), 10)],
            ["Energy Level", f"{wellness_data.get('energy_level', 0)}/10", self._get_status(wellness_data.get('energy_level', 0), 10)],
        ]
        
        wellness_table = Table(wellness_metrics, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        wellness_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#9B59B6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(wellness_table)
        story.append(Spacer(1, 20))
        
        return story

    def _create_recommendations_section(self):
        """Create recommendations section."""
        story = []
        
        story.append(Paragraph("Personalized Recommendations", self.styles['CustomHeader']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=HexColor('#9B59B6')))
        story.append(Spacer(1, 12))
        
        recommendations = [
            "• Maintain regular sleep schedule (7-9 hours per night)",
            "• Practice stress management techniques like meditation or yoga",
            "• Stay physically active with moderate exercise",
            "• Eat a balanced diet rich in calcium and vitamin D",
            "• Stay hydrated and limit caffeine intake",
            "• Consider hormone therapy options with your healthcare provider",
            "• Join support groups for emotional support during menopause",
            "• Track your symptoms and discuss patterns with your doctor"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, self.styles['CustomBody']))
            story.append(Spacer(1, 8))
        
        return story

    def _create_disclaimer_section(self):
        """Create disclaimer section."""
        story = []
        
        story.append(Paragraph("Important Disclaimer", self.styles['CustomHeader']))
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=HexColor('#FF6B6B')))
        story.append(Spacer(1, 12))
        
        disclaimer = """
        This health summary is generated by MenoBalance AI for educational and informational purposes only. 
        It is not intended to replace professional medical advice, diagnosis, or treatment. 
        Always consult with your healthcare provider before making any health-related decisions.
        
        The predictions and recommendations provided are based on general patterns and should not be 
        considered as definitive medical advice. Individual results may vary.
        """
        
        story.append(Paragraph(disclaimer, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        return story

    def _get_status(self, score, max_score, reverse=False):
        """Get status based on score."""
        percentage = (score / max_score) * 100
        
        if reverse:  # For stress level (lower is better)
            if percentage <= 30:
                return "Excellent"
            elif percentage <= 50:
                return "Good"
            elif percentage <= 70:
                return "Fair"
            else:
                return "Needs Attention"
        else:  # For other metrics (higher is better)
            if percentage >= 80:
                return "Excellent"
            elif percentage >= 60:
                return "Good"
            elif percentage >= 40:
                return "Fair"
            else:
                return "Needs Attention"


def generate_health_summary_pdf(user_data=None, predictions=None, wellness_data=None):
    """Convenience function to generate health summary PDF."""
    generator = MenoBalancePDFGenerator()
    return generator.generate_health_summary_pdf(user_data, predictions, wellness_data)


# Example usage function for Streamlit
def create_download_button(filename, button_text="📄 Download Health Summary PDF"):
    """Create a download button for the generated PDF."""
    if os.path.exists(filename):
        with open(filename, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label=button_text,
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf"
            )
