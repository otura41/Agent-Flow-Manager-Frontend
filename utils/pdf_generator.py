#!/usr/bin/env python3
"""
[PDF] PDF Generator para AgentFlow Manager
🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹==
Generador de PDFs profesionales para reportes de análisis empresarial
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
import streamlit as st

class BusinessAnalysisPDFGenerator:
    """Generador de PDFs para análisis empresariales"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurar estilos personalizados"""
        # Estilo para títulos principales
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f4e79'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#2e5984'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para texto normal
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Estilo para métricas
        self.styles.add(ParagraphStyle(
            name='MetricStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1f4e79')
        ))

    def generate_analysis_pdf(self, company_name, analysis_data, result_data):
        """Generar PDF completo del análisis empresarial"""
        
        # Crear buffer en memoria
        buffer = BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Contenido del documento
        story = []
        
        # Portada
        self.add_cover_page(story, company_name, analysis_data, result_data)
        
        # Contenido principal
        self.add_main_content(story, company_name, analysis_data, result_data)
        
        # Construir PDF
        doc.build(story)
        
        # Obtener bytes del PDF
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def add_cover_page(self, story, company_name, analysis_data, result_data):
        """Agregar página de portada"""
        
        # Título principal
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("REPORTE DE ANÁLISIS EMPRESARIAL", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Nombre de la empresa
        story.append(Paragraph(f"<b>{company_name}</b>", self.styles['CustomTitle']))
        story.append(Spacer(1, 1*inch))
        
        # Información básica
        info_data = [
            ['Empresa:', company_name],
            ['Industria:', analysis_data.get('industry', 'N/A')],
            ['Ubicación:', analysis_data.get('location', 'N/A')],
            ['Tipo de Análisis:', analysis_data.get('analysis_type', 'N/A')],
            ['Fecha de Análisis:', datetime.now().strftime('%d/%m/%Y')],
            ['Costo del Análisis:', f"${result_data.get('estimated_cost', 0):.2f}"],
            ['Tiempo de Procesamiento:', result_data.get('processing_time', 'N/A')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 1*inch))
        
        # Footer de portada
        story.append(Paragraph("Generado por AgentFlow Manager", self.styles['CustomNormal']))
        story.append(Paragraph("Sistema CrewAI v0.148.0", self.styles['CustomNormal']))
        story.append(Paragraph("© 2025 AgentFlow Manager - Todos los derechos reservados", self.styles['CustomNormal']))
        
        story.append(PageBreak())
    
    def add_main_content(self, story, company_name, analysis_data, result_data):
        """Agregar contenido principal del análisis"""
        
        analysis = result_data.get('analysis', {})
        
        # Resumen Ejecutivo
        story.append(Paragraph("RESUMEN EJECUTIVO", self.styles['CustomHeading']))
        if 'executive_summary' in analysis:
            # Limpiar y formatear el texto del resumen
            summary_text = analysis['executive_summary'].strip()
            # Dividir en párrafos
            paragraphs = summary_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    clean_para = para.strip().replace('\n', ' ')
                    if clean_para:
                        story.append(Paragraph(clean_para, self.styles['CustomNormal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Métricas Principales
        if 'metrics' in analysis:
            story.append(Paragraph("MÉTRICAS PRINCIPALES", self.styles['CustomHeading']))
            
            metrics = analysis['metrics']
            
            # Crear tabla de métricas principales
            main_metrics = []
            if 'overall_score' in metrics:
                main_metrics.append(['Puntuación General', f"{metrics['overall_score']}/100"])
            if 'growth_potential' in metrics:
                main_metrics.append(['Potencial de Crecimiento', str(metrics['growth_potential'])])
            if 'risk_level' in metrics:
                main_metrics.append(['Nivel de Riesgo', str(metrics['risk_level'])])
            
            if main_metrics:
                metrics_table = Table(main_metrics, colWidths=[2.5*inch, 2*inch])
                metrics_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(metrics_table)
            
            # Métricas adicionales
            additional_metrics = []
            for key, value in metrics.items():
                if key not in ['overall_score', 'growth_potential', 'risk_level']:
                    metric_name = key.replace('_', ' ').title()
                    additional_metrics.append([metric_name, str(value)])
            
            if additional_metrics:
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph("Métricas Detalladas:", self.styles['MetricStyle']))
                
                detailed_table = Table(additional_metrics, colWidths=[2.5*inch, 2*inch])
                detailed_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(detailed_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Recomendaciones Estratégicas
        if 'recommendations' in analysis:
            story.append(Paragraph("RECOMENDACIONES ESTRATÉGICAS", self.styles['CustomHeading']))
            
            for i, rec in enumerate(analysis['recommendations'], 1):
                recommendation_text = f"{i}. {rec}"
                story.append(Paragraph(recommendation_text, self.styles['CustomNormal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Análisis SWOT
        if 'swot_analysis' in analysis:
            story.append(Paragraph("ANÁLISIS SWOT", self.styles['CustomHeading']))
            
            swot = analysis['swot_analysis']
            
            # Crear tabla SWOT
            swot_data = []
            
            # Fortalezas
            if 'strengths' in swot:
                swot_data.append(['FORTALEZAS', ''])
                for strength in swot['strengths'][:5]:  # Máximo 5
                    swot_data.append(['', f"• {strength}"])
            
            # Debilidades
            if 'weaknesses' in swot:
                swot_data.append(['DEBILIDADES', ''])
                for weakness in swot['weaknesses'][:5]:
                    swot_data.append(['', f"• {weakness}"])
            
            # Oportunidades
            if 'opportunities' in swot:
                swot_data.append(['OPORTUNIDADES', ''])
                for opportunity in swot['opportunities'][:5]:
                    swot_data.append(['', f"• {opportunity}"])
            
            # Amenazas
            if 'threats' in swot:
                swot_data.append(['AMENAZAS', ''])
                for threat in swot['threats'][:5]:
                    swot_data.append(['', f"• {threat}"])
            
            if swot_data:
                swot_table = Table(swot_data, colWidths=[1.5*inch, 4*inch])
                swot_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#d5e6f2')),
                    ('BACKGROUND', (0, 6), (0, 6), colors.HexColor('#f2e6d5')),
                    ('BACKGROUND', (0, 11), (0, 11), colors.HexColor('#e6f2d5')),
                    ('BACKGROUND', (0, 16), (0, 16), colors.HexColor('#f2d5d5')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                story.append(swot_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Próximos Pasos
        if 'next_steps' in analysis:
            story.append(Paragraph("PRÓXIMOS PASOS", self.styles['CustomHeading']))
            
            for i, step in enumerate(analysis['next_steps'], 1):
                step_text = f"{i}. {step}"
                story.append(Paragraph(step_text, self.styles['CustomNormal']))

def generate_pdf_for_streamlit(company_name, analysis_data, result_data):
    """Función auxiliar para generar PDF para Streamlit"""
    try:
        generator = BusinessAnalysisPDFGenerator()
        pdf_bytes = generator.generate_analysis_pdf(company_name, analysis_data, result_data)
        return pdf_bytes
    except Exception as e:
        st.error(f"Error generando PDF: {e}")
        return None
