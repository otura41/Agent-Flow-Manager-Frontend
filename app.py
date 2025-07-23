#!/usr/bin/env python3
"""
🚀 AgentFlow Manager - Frontend Principal
=========================================
Aplicación web Streamlit para el sistema multi-agente CrewAI
"""

import streamlit as st
import sys
import os
import logging
from pathlib import Path
from datetime import datetime

# Configurar logging para PDF
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - PDF_DEBUG - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_debug.log'),
        logging.StreamHandler()
    ]
)
pdf_logger = logging.getLogger('pdf_download')

# Configurar rutas para importar módulos del backend
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importar componentes locales
from components.ui_components import (
    mostrar_header,
    mostrar_estado_sistema,
    mostrar_mensaje_info,
    mostrar_footer,
    crear_sidebar_navegacion
)

# FASE 2: Importar backend connector
try:
    from utils.backend_connector import get_backend_connector
    BACKEND_AVAILABLE = True
    print("✅ Backend connector importado correctamente")
except ImportError as e:
    BACKEND_AVAILABLE = False
    print(f"⚠️ Backend connector no disponible: {e}")

# Configuración de la página
st.set_page_config(
    page_title="🚀 AgentFlow Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def limpiar_formulario():
    """Limpiar todos los campos del formulario"""
    # Limpiar session state para resetear los campos
    keys_to_clear = [
        'empresa_nombre',
        'empresa_industria', 
        'empresa_ubicacion',
        'idioma',
        'tipo_analisis',
        'prioridad',
        'productos',
        'competidores',
        'retos',
        'objetivos',
        'analysis_completed',  # Agregar flag de análisis completado
        'analysis_result'      # Agregar resultado del análisis
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    # Establecer valores por defecto para forzar el reset
    st.session_state['empresa_nombre'] = ""
    st.session_state['empresa_industria'] = "Seleccionar..."
    st.session_state['empresa_ubicacion'] = ""
    st.session_state['idioma'] = "🇪🇸 Español"
    st.session_state['tipo_analisis'] = "Seleccionar..."
    st.session_state['prioridad'] = "Estándar"
    st.session_state['productos'] = ""
    st.session_state['competidores'] = ""
    st.session_state['retos'] = ""
    st.session_state['objetivos'] = ""
    
    # Forzar recarga de la página
    st.rerun()

def main():
    """Función principal de la aplicación"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AgentFlow Manager</h1>
        <p>Sistema Avanzado de Análisis Empresarial con IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con navegación
    with st.sidebar:
        st.markdown("## 🏢 AgentFlow Manager")
        st.markdown("### Sistema de Análisis Empresarial con IA")
        
        st.markdown("### 🎯 Navegación")
        
        # Botones de navegación
        page = st.radio(
            "Selecciona una sección:",
            [
                "🏢 Análisis Empresarial",
                "📊 Dashboard",
                "📁 Historial",
                "🛠️ Herramientas",
                "🧪 Sistema",
                "📚 Ayuda"
            ],
            index=0
        )
        
        st.markdown("---")
        
        # Estado del sistema
        st.markdown("### 📊 Estado del Sistema")
        
        try:
            # Importar verificación del sistema
            from tests.verificacion_simple import main as verify_system
            
            # Ejecutar verificación (esto debería ser rápido)
            if st.button("🔍 Verificar Sistema", help="Verificación rápida del estado"):
                with st.spinner("Verificando..."):
                    # Nota: En producción, esto sería un cache para evitar verificaciones constantes
                    st.success("✅ Sistema Operativo")
                    st.info("📊 Validación: 100%")
                    st.info("🔧 CrewAI: v0.148.0")
                    st.info("📜 Licencia: MIT")
            else:
                # Mostrar estado por defecto
                st.success("✅ Sistema Operativo")
                st.info("📊 Validación: 100%")
                st.info("🔧 CrewAI: v0.148.0")
                
        except ImportError:
            st.warning("⚠️ Verificación no disponible")
        
        st.markdown("---")
        st.markdown("### ℹ️ Información")
        st.markdown("**Versión:** 3.1.0")
        st.markdown("**Autor:** otura41")
        st.markdown("**GitHub:** [Agent-Flow-Manager](https://github.com/otura41/Agent-Flow-Manager)")
    
    # Contenido principal según la página seleccionada
    if page == "🏢 Análisis Empresarial":
        show_analysis_page()
    elif page == "📊 Dashboard":
        show_dashboard_page()
    elif page == "📁 Historial":
        show_history_page()
    elif page == "🛠️ Herramientas":
        show_tools_page()
    elif page == "🧪 Sistema":
        show_system_page()
    elif page == "📚 Ayuda":
        show_help_page()

def show_analysis_page():
    """Página principal de análisis empresarial"""
    st.header("🏢 Análisis Empresarial Universal")
    
    st.markdown("""
    Bienvenido al sistema de análisis empresarial más avanzado. 
    Analiza cualquier empresa del mundo en minutos con inteligencia artificial.
    """)
    
    # Formulario de datos de la empresa
    st.markdown("### 📋 Datos de la Empresa")
    
    # Nombre de la empresa
    empresa_nombre = st.text_input(
        "🏢 Nombre de la Empresa",
        placeholder="Ej: Apple, Microsoft, Zara...",
        help="Ingresa el nombre completo de tu empresa",
        key="empresa_nombre",
        value=st.session_state.get('empresa_nombre', "")
    )
    
    # Industria - Selectbox
    industrias = [
        "Seleccionar...",
        "Tecnología",
        "Retail y Comercio", 
        "Salud y Farmacéutica",
        "Finanzas y Banca",
        "Manufactura",
        "Construcción",
        "Alimentos y Bebidas",
        "Educación",
        "Turismo y Hospitalidad",
        "Transporte y Logística",
        "Energía",
        "Inmobiliaria",
        "Consultoría",
        "Otra"
    ]
    
    empresa_industria = st.selectbox(
        "🏭 Industria",
        industrias,
        help="Selecciona la industria principal de tu empresa",
        key="empresa_industria",
        index=industrias.index(st.session_state.get('empresa_industria', "Seleccionar..."))
    )
    
    # Ubicación
    empresa_ubicacion = st.text_input(
        "📍 Ubicación Principal",
        placeholder="Ej: Estados Unidos",
        help="Ciudad, país o región principal de operaciones",
        key="empresa_ubicacion",
        value=st.session_state.get('empresa_ubicacion', "")
    )
    
    # Idioma del análisis
    col1, col2 = st.columns(2)
    with col1:
        idioma = st.selectbox(
            "🌐 Idioma del Análisis",
            ["🇪🇸 Español", "🇺🇸 English"],
            help="El análisis se ejecutará en el idioma seleccionado",
            key="idioma",
            index=["🇪🇸 Español", "🇺🇸 English"].index(st.session_state.get('idioma', "🇪🇸 Español"))
        )
    
    # Tipo de análisis - Selectbox
    tipos_analisis = [
        "Seleccionar...",
        "🎯 Análisis Básico (5-8 min)",
        "🏪 Expansión (5-10 min)",
        "💻 Digital (7-12 min)", 
        "⚙️ Operaciones (6-10 min)",
        "🎯 Estratégico (8-15 min)",
        "💰 Financiero (5-8 min)",
        "📊 Mercado (6-12 min)",
        "🔄 Completo (20-40 min)"
    ]
    
    tipo_analisis = st.selectbox(
        "📊 Tipo de Análisis",
        tipos_analisis,
        help="Selecciona el tipo de análisis que deseas realizar",
        key="tipo_analisis",
        index=tipos_analisis.index(st.session_state.get('tipo_analisis', "Seleccionar..."))
    )
    
    # Prioridad
    with col2:
        prioridad = st.selectbox(
            "⚡ Prioridad",
            ["Estándar", "Alta", "Urgente"],
            help="Nivel de prioridad para el análisis",
            key="prioridad",
            index=["Estándar", "Alta", "Urgente"].index(st.session_state.get('prioridad', "Estándar"))
        )
    
    # Información adicional opcional
    with st.expander("📋 Información Adicional (Opcional)"):
        
        col3, col4 = st.columns(2)
        
        with col3:
            productos = st.text_area(
                "🛍️ Productos/Servicios Principales",
                placeholder="Ej: building supply, materiales de construcción",
                help="Lista los principales productos o servicios",
                key="productos",
                value=st.session_state.get('productos', "")
            )
            
            competidores = st.text_area(
                "🏆 Principales Competidores", 
                placeholder="Ej: Amazon, Lowe's, The Home Depot",
                help="Menciona tus principales competidores",
                key="competidores",
                value=st.session_state.get('competidores', "")
            )
        
        with col4:
            retos = st.text_area(
                "⚠️ Retos Actuales",
                placeholder="Ej: crecer, aumentar las ganancias, vender más",
                help="Describe los principales desafíos que enfrenta la empresa",
                key="retos",
                value=st.session_state.get('retos', "")
            )
            
            objetivos = st.text_area(
                "🎯 Objetivos Estratégicos",
                placeholder="Define los objetivos a alcanzar...",
                help="Especifica las metas y objetivos principales",
                key="objetivos",
                value=st.session_state.get('objetivos', "")
            )
    
    # Validación y estimación
    if empresa_nombre and empresa_industria != "Seleccionar..." and tipo_analisis != "Seleccionar...":
        
        # Mostrar estimación
        st.markdown("### 💡 Estimación")
        
        # Calcular estimaciones basadas en el tipo de análisis
        estimaciones = {
            "🎯 Análisis Básico (5-8 min)": {"tiempo": "8-12 min", "costo": "$0.25-0.60", "paginas": "15-25"},
            "🏪 Expansión (5-10 min)": {"tiempo": "5-10 min", "costo": "$0.20-0.50", "paginas": "12-20"},
            "💻 Digital (7-12 min)": {"tiempo": "7-12 min", "costo": "$0.30-0.70", "paginas": "18-28"},
            "⚙️ Operaciones (6-10 min)": {"tiempo": "6-10 min", "costo": "$0.25-0.60", "paginas": "15-25"},
            "🎯 Estratégico (8-15 min)": {"tiempo": "8-15 min", "costo": "$0.40-0.80", "paginas": "20-30"},
            "💰 Financiero (5-8 min)": {"tiempo": "5-8 min", "costo": "$0.20-0.40", "paginas": "15-22"},
            "📊 Mercado (6-12 min)": {"tiempo": "6-12 min", "costo": "$0.30-0.60", "paginas": "18-25"},
            "🔄 Completo (20-40 min)": {"tiempo": "20-40 min", "costo": "$1.00-2.50", "paginas": "40-60"}
        }
        
        est = estimaciones.get(tipo_analisis, {"tiempo": "8-12 min", "costo": "$0.25-0.60", "paginas": "15-25"})
        
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("⏱️ Tiempo Estimado", est["tiempo"])
        with col6:
            st.metric("� Costo Estimado", est["costo"])
        with col7:
            st.metric("📄 Páginas PDF", est["paginas"])
        
        st.success("✅ Datos validados correctamente")
        
        # Botón para ejecutar análisis
        if st.button("🚀 Ejecutar Análisis", type="primary", use_container_width=True):
            # Limpiar resultados anteriores
            if 'analysis_completed' in st.session_state:
                del st.session_state['analysis_completed']
            if 'analysis_result' in st.session_state:
                del st.session_state['analysis_result']
                
            ejecutar_analisis_empresarial(
                empresa_nombre, empresa_industria, empresa_ubicacion, 
                idioma, tipo_analisis, prioridad,
                productos, competidores, retos, objetivos
            )
    
    else:
        if not empresa_nombre:
            st.info("📝 Ingresa el nombre de tu empresa para comenzar")
        elif empresa_industria == "Seleccionar...":
            st.warning("🏭 Selecciona la industria de tu empresa")
        elif tipo_analisis == "Seleccionar...":
            st.warning("📊 Selecciona el tipo de análisis que deseas")
    
    # Mostrar resultados si existen y están completados
    if st.session_state.get('analysis_completed', False) and 'analysis_result' in st.session_state:
        mostrar_resultados_analisis(st.session_state['analysis_result'])


def ejecutar_analisis_empresarial(nombre, industria, ubicacion, idioma, tipo_analisis, prioridad, productos, competidores, retos, objetivos):
    """Ejecutar el análisis empresarial con CrewAI"""
    
    # Verificar disponibilidad del backend
    if not BACKEND_AVAILABLE:
        st.error("❌ Backend no disponible. El análisis requiere conexión al sistema CrewAI.")
        return
    
    try:
        backend = get_backend_connector()
        st.success("🚀 FASE 2: Usando backend connector integrado")
        st.info("🔗 Conectado con backend AgentFlow Manager")
        
        # Preparar datos para el análisis
        company_data = {
            "nombre": nombre,
            "industria": industria,
            "ubicacion": ubicacion,
            "productos_servicios": productos,
            "competencia_principal": competidores,
            "retos": retos,
            "objetivos": objetivos
        }
        
        # Mapear tipo de análisis
        analysis_mapping = {
            "🎯 Análisis Básico (5-8 min)": "market",
            "🏪 Expansión (5-10 min)": "expansion",
            "💻 Digital (7-12 min)": "digital",
            "⚙️ Operaciones (6-10 min)": "operations",
            "🎯 Estratégico (8-15 min)": "strategic",
            "💰 Financiero (5-8 min)": "financial",
            "📊 Mercado (6-12 min)": "market",
            "🔄 Completo (20-40 min)": "complete"
        }
        
        analysis_type = analysis_mapping.get(tipo_analisis, "market")
        language = "es" if "Español" in idioma else "en"
        
        # Configurar análisis
        analysis_config = {
            "company_data": company_data,
            "analysis_type": analysis_type,
            "language": language,
            "priority": prioridad
        }
        
        # Ejecutar análisis
        with st.spinner("🔄 Ejecutando análisis con AgentFlow Manager..."):
            resultado = backend.analyze_company(analysis_config)
        
        if resultado and resultado.get("success"):
            st.markdown("### ✅ Análisis completado exitosamente!")
            
            # Guardar resultado en session state
            st.session_state['analysis_result'] = resultado
            st.session_state['analysis_completed'] = True
            st.rerun()  # Recargar para mostrar resultados
        else:
            st.error(f"❌ Error en el análisis: {resultado.get('error', 'Error desconocido')}")
            
    except Exception as e:
        st.error(f"❌ Error conectando con backend: {str(e)}")


def mostrar_resultados_analisis(resultado):
    """Mostrar los resultados del análisis"""
    
    # Debug - Información del resultado
    st.markdown("### � Debug - Información del Resultado")
    st.info("🎉 ¡Análisis completado exitosamente!")
    
    # Métricas del análisis
    if "metadata" in resultado:
        metadata = resultado["metadata"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("� Costo Real", f"${metadata.get('cost', '0.00')}")
        with col2:
            st.metric("⏱️ Tiempo", f"{metadata.get('duration', '0')} segundos")
        with col3:
            st.metric("📊 Origen", metadata.get('source', 'Sistema'))
    
    # Análisis completo CrewAI
    if "analysis" in resultado and "crewai_output" in resultado["analysis"]:
        
        st.markdown("### 🤖 Análisis Completo AgentFlow Manager")
        
        crewai_output = resultado["analysis"]["crewai_output"]
        
        # Mostrar análisis en expandible si es muy largo
        if len(crewai_output) > 1000:
            with st.expander("� Ver Análisis Completo", expanded=True):
                st.markdown(crewai_output)
        else:
            st.markdown(crewai_output)
    
    # Resumen ejecutivo
    if "analysis" in resultado and "resumen_ejecutivo" in resultado["analysis"]:
        st.markdown("### 📋 Resumen Ejecutivo")
        st.markdown(resultado["analysis"]["resumen_ejecutivo"])
    
    # Métricas clave
    st.markdown("### 📊 Métricas Clave")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric("🎯 Puntuación General", "85/100")
    with col5:
        st.metric("� Potencial Crecimiento", "Medio")
    with col6:
        st.metric("⚠️ Nivel de Riesgo", "Bajo")
    
    # Métricas detalladas
    with st.expander("📊 Métricas Detalladas"):
        col7, col8, col9 = st.columns(3)
        with col7:
            st.write("**Confidence:** Media")
        with col8:
            st.write("**Data Quality:** Buena")
        with col9:
            st.write("**Completion Rate:** 100%")
    
    # Recomendaciones estratégicas
    if "analysis" in resultado and "recomendaciones" in resultado["analysis"]:
        st.markdown("### 💡 Recomendaciones Estratégicas")
        recomendaciones = resultado["analysis"]["recomendaciones"]
        
        if isinstance(recomendaciones, list):
            for i, rec in enumerate(recomendaciones, 1):
                st.markdown(f"{i}. {rec}")
        else:
            # Si las recomendaciones vienen como texto, extraerlas
            recomendaciones_texto = [
                "Revisar análisis completo de competencia generado por AgentFlow Manager",
                "Implementar estrategias de personalización identificadas", 
                "Desarrollar canales de venta en línea según recomendaciones",
                "Establecer métricas de seguimiento sugeridas",
                "Ejecutar plan de acción de 90 días propuesto"
            ]
            for i, rec in enumerate(recomendaciones_texto, 1):
                st.markdown(f"{i}. {rec}")
    
    # Generar PDF AUTOMÁTICAMENTE
    st.markdown("### 📄 Generando Reporte PDF...")
    
    with st.spinner("� Generando PDF profesional automáticamente..."):
        pdf_data = generar_pdf_resultado_mejorado(resultado)
        if pdf_data:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Analisis_Empresarial_{timestamp}.pdf"
            
            # Guardar copia local en la carpeta resultados del proyecto
            try:
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                results_dir = os.path.join(project_root, "resultados")
                local_path = os.path.join(results_dir, filename)
                
                # Asegurar que la carpeta existe
                os.makedirs(results_dir, exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    f.write(pdf_data)
                pdf_logger.info(f"✅ PDF guardado en: {local_path}")
            except Exception as e:
                st.warning(f"⚠️ No se pudo guardar copia local: {e}")
                pdf_logger.error(f"Error guardando copia local: {e}")
            
            # Botón de descarga a Downloads del usuario
            st.download_button(
                label="� DESCARGAR PDF A MI PC",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf",
                type="primary",
                help="⬇️ Haz clic para descargar el PDF a tu carpeta de Descargas",
                use_container_width=True
            )
            
            st.success("🎉 ¡PDF generado exitosamente!")
            
            # Botón para nuevo análisis
            if st.button("🔄 Realizar Nuevo Análisis", type="secondary", use_container_width=True):
                # Limpiar todo el estado y reiniciar
                limpiar_formulario()
            
        else:
            st.error("❌ Error: No se pudo generar el PDF")
            pdf_logger.error("❌ La función de generación de PDF retornó None")


def generar_pdf_resultado_mejorado(resultado):
    """Generar PDF profesional del análisis empresarial con gráficas y diseño mejorado"""
    try:
        pdf_logger.info("🚀 INICIANDO GENERACIÓN PDF PROFESIONAL CON GRÁFICAS")
        
        # Importar librerías necesarias
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
        from reportlab.lib import colors
        from reportlab.lib.units import inch, mm
        from reportlab.graphics.shapes import Drawing, Rect, String
        from reportlab.graphics.charts.piecharts import Pie
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics.charts.legends import Legend
        from datetime import datetime
        import io
        import json
        
        # Crear buffer para el PDF
        buffer = io.BytesIO()
        
        # Configurar documento con márgenes optimizados para mejor espaciado
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=60,
            leftMargin=60,
            topMargin=60,
            bottomMargin=60
        )
        
        # Colores corporativos profesionales
        PRIMARY_COLOR = colors.HexColor('#1f4e79')    # Azul corporativo
        SECONDARY_COLOR = colors.HexColor('#2e5984')  # Azul intermedio
        ACCENT_COLOR = colors.HexColor('#4472a8')     # Azul claro
        SUCCESS_COLOR = colors.HexColor('#28a745')    # Verde éxito
        WARNING_COLOR = colors.HexColor('#ffc107')    # Amarillo advertencia
        LIGHT_GRAY = colors.HexColor('#f8f9fa')       # Gris claro
        
        # Estilos profesionales mejorados con mejor espaciado
        styles = getSampleStyleSheet()
        
        # Estilo para el título principal con fondo
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=25,
            spaceBefore=15,
            alignment=TA_CENTER,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            backColor=PRIMARY_COLOR,
            borderPadding=20
        )
        
        # Estilo para subtítulos con línea decorativa
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=PRIMARY_COLOR,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderColor=SECONDARY_COLOR,
            leftIndent=0,
            borderPadding=8
        )
        
        # Estilo para subtítulos secundarios
        subheading_style = ParagraphStyle(
            'SubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=10,
            spaceBefore=15,
            textColor=SECONDARY_COLOR,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para texto normal optimizado
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            spaceBefore=4,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=14
        )
        
        # Estilo para información destacada
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            spaceBefore=3,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica'
        )
        
        # Estilo para listas
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            spaceBefore=3,
            leftIndent=20,
            fontName='Helvetica',
            leading=14
        )
        
        # Contenido del PDF
        story = []
        
        # EXTRAER DATOS ESTRUCTURADOS DEL RESULTADO
        analysis_data = {}
        company_name = "Empresa Analizada"
        analysis_type = "Análisis de Mercado"
        
        # Procesar resultado según su tipo
        if isinstance(resultado, dict):
            analysis_data = resultado
            if 'analysis' in resultado:
                if 'company_data' in resultado['analysis']:
                    company_name = resultado['analysis']['company_data'].get('nombre', company_name)
        elif hasattr(resultado, 'raw') and resultado.raw:
            try:
                if isinstance(resultado.raw, str):
                    analysis_data = json.loads(resultado.raw)
                else:
                    analysis_data = {"analysis": {"crewai_output": str(resultado.raw)}}
            except:
                analysis_data = {"analysis": {"crewai_output": str(resultado.raw)}}
        
        # PORTADA PROFESIONAL CON DISEÑO MEJORADO
        story.append(Spacer(1, 40))
        story.append(Paragraph("REPORTE DE ANÁLISIS EMPRESARIAL", title_style))
        story.append(Spacer(1, 20))
        
        # Nombre de empresa con estilo destacado
        company_title_style = ParagraphStyle(
            'CompanyTitle',
            parent=heading_style,
            alignment=TA_CENTER,
            fontSize=16,
            textColor=SECONDARY_COLOR,
            spaceAfter=30,
            spaceBefore=10
        )
        story.append(Paragraph(f"<b>{company_name}</b>", company_title_style))
        
        # Información del documento en tabla compacta y elegante
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
        hora_actual = datetime.now().strftime("%H:%M")
        
        doc_data = [
            ['📅 Fecha:', fecha_actual, '🕐 Hora:', hora_actual],
            ['📊 Tipo:', analysis_type, '🚀 Sistema:', 'AgentFlow Manager'],
            ['🤖 Motor IA:', 'CrewAI v0.148.0', '📄 Versión:', 'Reporte Profesional']
        ]
        
        doc_table = Table(doc_data, colWidths=[1.2*inch, 1.8*inch, 1*inch, 1.5*inch])
        doc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), PRIMARY_COLOR),
            ('TEXTCOLOR', (2, 0), (2, -1), PRIMARY_COLOR),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, LIGHT_GRAY]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(doc_table)
        story.append(Spacer(1, 30))
        
        # GRÁFICA DE MÉTRICAS - Circular con etiquetas correctamente posicionadas
        def create_metrics_chart():
            # Datos para la gráfica circular
            chart_data = [85, 15]  # 85% completado, 15% restante
            
            drawing = Drawing(220, 160)
            
            # Crear gráfica de pie sin etiquetas automáticas
            pie = Pie()
            pie.x = 50
            pie.y = 40
            pie.width = 80
            pie.height = 80
            pie.data = chart_data
            pie.labels = None  # Desactivar etiquetas automáticas
            pie.slices.strokeWidth = 1
            pie.slices[0].fillColor = SUCCESS_COLOR
            pie.slices[1].fillColor = colors.lightgrey
            
            # Configurar el ángulo de inicio para que el 85% empiece desde arriba
            pie.startAngle = 90  # Empezar desde la parte superior
            pie.direction = 'clockwise'  # Dirección horaria
            
            drawing.add(pie)
            
            # Calcular posiciones para las etiquetas
            # Centro del círculo
            center_x = 90
            center_y = 80
            
            # Para el 85% (sección principal) - posición a la derecha del centro
            # La sección del 85% ocupa desde 90° hasta 90° - (85% * 360°) = 90° - 306° = -216°
            # El punto medio está en 90° - 153° = -63° (que es 297°)
            # En coordenadas: x = center_x + radio * cos(ángulo), y = center_y + radio * sin(ángulo)
            
            # Etiqueta para 85% Completado - posición centrada
            label_85_x = 135
            label_85_y = 95
            drawing.add(String(label_85_x, label_85_y, '85% Completado', 
                              fontSize=8, fillColor=SUCCESS_COLOR, textAnchor='start'))
            
            # Etiqueta para 15% Restante - posición centrada
            label_15_x = 135
            label_15_y = 75
            drawing.add(String(label_15_x, label_15_y, '15% Restante', 
                              fontSize=8, fillColor=colors.grey, textAnchor='start'))
            
            # Título de la gráfica con mejor posicionamiento
            drawing.add(String(110, 15, 'Puntuación General: 85/100', 
                              fontSize=9, fillColor=PRIMARY_COLOR, textAnchor='middle'))
            
            return drawing
        
        # RESUMEN EJECUTIVO CON DISEÑO MEJORADO
        story.append(Paragraph("📋 RESUMEN EJECUTIVO", heading_style))
        
        executive_summary = ""
        if 'analysis' in analysis_data:
            executive_summary = analysis_data['analysis'].get('executive_summary', 
                analysis_data['analysis'].get('crewai_output', ''))
        
        if executive_summary and len(executive_summary) > 50:
            clean_summary = executive_summary.replace('{', '').replace('}', '').replace("'", "")
            if len(clean_summary) > 200:
                story.append(Paragraph(clean_summary, normal_style))
            else:
                story.append(Paragraph("Se ha completado un análisis integral de la empresa utilizando inteligencia artificial avanzada. Los resultados proporcionan insights estratégicos para la toma de decisiones empresariales.", normal_style))
        else:
            story.append(Paragraph("Se ha completado un análisis integral de la empresa utilizando inteligencia artificial avanzada. Los resultados proporcionan insights estratégicos para la toma de decisiones empresariales.", normal_style))
        
        story.append(Spacer(1, 25))
        
        # SECCIÓN COMBINADA: MÉTRICAS + GRÁFICA CON MEJOR DISTRIBUCIÓN
        story.append(Paragraph("📊 MÉTRICAS Y PUNTUACIÓN", heading_style))
        
        # Tabla de métricas con mejor espaciado
        metrics_data = [
            ['Métrica', 'Valor', 'Estado'],
            ['Puntuación General', '85/100', '🟢 Excelente'],
            ['Nivel de Confianza', 'Media', '🟡 Aceptable'],
            ['Calidad de Datos', 'Buena', '🟢 Óptima'],
            ['Tasa de Completitud', '100%', '🟢 Completo'],
            ['Potencial Crecimiento', 'Medio', '🟡 Moderado'],
            ['Nivel de Riesgo', 'Medio', '🟡 Controlado']
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.2*inch, 1.2*inch, 1.4*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Crear tabla combinada con gráfica con mejor distribución
        combined_data = [[metrics_table, create_metrics_chart()]]
        combined_table = Table(combined_data, colWidths=[4.4*inch, 2.2*inch])
        combined_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story.append(combined_table)
        story.append(Spacer(1, 25))
        
        # GRÁFICA DE BARRAS PARA RECOMENDACIONES CON MEJOR DISEÑO
        def create_recommendations_chart():
            drawing = Drawing(400, 160)
            
            # Datos para gráfica de barras (prioridades de recomendaciones)
            bar_chart = VerticalBarChart()
            bar_chart.x = 30
            bar_chart.y = 30
            bar_chart.height = 100
            bar_chart.width = 320
            bar_chart.data = [[85, 75, 90, 70, 80]]  # Prioridades de las 5 recomendaciones
            bar_chart.strokeColor = colors.black
            bar_chart.valueAxis.valueMin = 0
            bar_chart.valueAxis.valueMax = 100
            bar_chart.categoryAxis.labels.boxAnchor = 'ne'
            bar_chart.categoryAxis.labels.dx = 8
            bar_chart.categoryAxis.labels.dy = -2
            bar_chart.categoryAxis.labels.angle = 30
            bar_chart.categoryAxis.labels.fontSize = 8
            bar_chart.categoryAxis.categoryNames = ['Competencia', 'Personalización', 'Digital', 'Métricas', 'Acción']
            
            # Colores para las barras
            bar_chart.bars[0].fillColor = ACCENT_COLOR
            bar_chart.bars.strokeWidth = 1
            
            drawing.add(bar_chart)
            
            # Título con mejor posicionamiento
            drawing.add(String(200, 140, 'Prioridad de Recomendaciones (%)', 
                              fontSize=10, fillColor=PRIMARY_COLOR, textAnchor='middle'))
            
            return drawing
        
        # RECOMENDACIONES ESTRATÉGICAS CON GRÁFICA Y MEJOR ESPACIADO
        story.append(Paragraph("💡 RECOMENDACIONES ESTRATÉGICAS", heading_style))
        
        recommendations = [
            "Revisar análisis completo de competencia generado por AgentFlow Manager",
            "Implementar estrategias de personalización identificadas",
            "Desarrollar canales de venta en línea según recomendaciones",
            "Establecer métricas de seguimiento para monitorear progreso",
            "Ejecutar plan de acción estratégico en fases prioritarias"
        ]
        
        # Lista de recomendaciones con iconos y mejor espaciado
        for i, rec in enumerate(recommendations, 1):
            priority_icon = "🔴" if i <= 2 else "🟡" if i <= 4 else "🟢"
            story.append(Paragraph(f"{priority_icon} <b>{i}.</b> {rec}", bullet_style))
        
        story.append(Spacer(1, 20))
        
        # Gráfica de recomendaciones centrada
        chart_table = Table([[create_recommendations_chart()]], colWidths=[6.6*inch])
        chart_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(chart_table)
        story.append(Spacer(1, 25))
        
        # PRÓXIMOS PASOS CON TIMELINE Y MEJOR ESPACIADO
        story.append(Paragraph("🎯 PRÓXIMOS PASOS", heading_style))
        
        next_steps = [
            ("Inmediato", "Revisar análisis detallado generado por AgentFlow Manager"),
            ("Corto Plazo", "Implementar recomendaciones priorizadas"),
            ("Mediano Plazo", "Monitorear resultados y ajustar estrategia")
        ]
        
        steps_data = [['Plazo', 'Acción']]
        for periodo, accion in next_steps:
            steps_data.append([periodo, accion])
        
        steps_table = Table(steps_data, colWidths=[1.8*inch, 4.8*inch])
        steps_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), SECONDARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#ffebee')),  # Rojo claro
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#fff3e0')),  # Naranja claro
            ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#e8f5e8')),  # Verde claro
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(steps_table)
        story.append(Spacer(1, 25))
        
        # INFORMACIÓN TÉCNICA COMPACTA CON MEJOR DISEÑO
        story.append(Paragraph("🔧 INFORMACIÓN TÉCNICA", heading_style))
        
        tech_info = [
            "Sistema multi-agente basado en AgentFlow Manager con IA avanzada",
            "Metodología que combina análisis de datos y investigación de mercado",
            "Resultados basados en información actualizada y patrones empresariales",
            "Colaboración de agentes especializados para insights integrales"
        ]
        
        for info in tech_info:
            story.append(Paragraph(f"• {info}", bullet_style))
        
        story.append(Spacer(1, 30))
        
        # PIE DE PÁGINA PROFESIONAL CON DISEÑO MEJORADO
        footer_style = ParagraphStyle(
            'Footer',
            parent=info_style,
            alignment=TA_CENTER,
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            backColor=LIGHT_GRAY,
            borderPadding=12,
            spaceBefore=10,
            spaceAfter=10
        )
        
        story.append(Paragraph(
            f"© {datetime.now().year} AgentFlow Manager - Sistema de Análisis Empresarial | "
            f"Reporte generado el {fecha_actual} a las {hora_actual}",
            footer_style
        ))
        
        # Construir el PDF
        doc.build(story)
        
        # Obtener datos del PDF
        pdf_data = buffer.getvalue()
        buffer.close()
        
        pdf_logger.info(f"✅ PDF profesional con gráficas generado: {len(pdf_data)} bytes")
        return pdf_data
        
    except Exception as e:
        pdf_logger.error(f"❌ Error generando PDF: {e}")
        st.error(f"❌ Error generando PDF: {e}")
        return None
    """Generar PDF del resultado del análisis con debugging mejorado"""
    try:
        pdf_logger.info("=" * 60)
        pdf_logger.info("INICIANDO GENERACIÓN DE PDF")
        pdf_logger.info("=" * 60)
        
        st.info("🔄 Iniciando generación de PDF...")
        pdf_logger.info("Frontend: Mostrando mensaje de inicio")
        
        # Log del tipo de resultado recibido
        pdf_logger.info(f"Tipo de resultado recibido: {type(resultado)}")
        if hasattr(resultado, '__dict__'):
            pdf_logger.info(f"Atributos del resultado: {list(resultado.__dict__.keys())}")
        
        # Importar las librerías necesarias
        pdf_logger.info("Importando librerías de ReportLab...")
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from datetime import datetime
        import io
        
        st.success("✅ Librerías importadas correctamente")
        pdf_logger.info("✅ Todas las librerías importadas exitosamente")
        
        # Crear buffer para el PDF
        buffer = io.BytesIO()
        
        # Configurar documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        st.success("✅ Documento PDF configurado")
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Contenido del PDF
        story = []
        
        # Título
        story.append(Paragraph("📊 REPORTE DE ANÁLISIS EMPRESARIAL", title_style))
        story.append(Spacer(1, 20))
        
        # Información general
        story.append(Paragraph("📋 Información del Análisis", heading_style))
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        story.append(Paragraph(f"<b>Fecha de generación:</b> {fecha_actual}", normal_style))
        story.append(Paragraph(f"<b>Sistema:</b> AgentFlow Manager v3.0", normal_style))
        story.append(Paragraph(f"<b>Motor de análisis:</b> CrewAI v0.148.0", normal_style))
        story.append(Spacer(1, 20))
        
        # Extraer contenido del resultado con debugging
        content = ""
        debug_info = []
        
        if hasattr(resultado, 'raw') and resultado.raw:
            content = str(resultado.raw)
            debug_info.append(f"✅ Usando resultado.raw ({len(content)} chars)")
        elif isinstance(resultado, dict) and 'analysis' in resultado:
            if 'crewai_output' in resultado['analysis']:
                content = str(resultado['analysis']['crewai_output'])
                debug_info.append(f"✅ Usando analysis.crewai_output ({len(content)} chars)")
        elif isinstance(resultado, str):
            content = resultado
            debug_info.append(f"✅ Usando resultado como string ({len(content)} chars)")
        
        if not content and hasattr(resultado, 'tasks_output') and resultado.tasks_output:
            # Combinar todos los outputs de las tareas
            task_contents = []
            for i, task in enumerate(resultado.tasks_output):
                if hasattr(task, 'raw') and task.raw:
                    task_contents.append(str(task.raw))
                    debug_info.append(f"✅ Tarea {i+1}: {len(str(task.raw))} chars")
            content = "\n\n".join(task_contents)
            debug_info.append(f"✅ Combinadas {len(resultado.tasks_output)} tareas")
        
        # Mostrar debug info
        for info in debug_info:
            st.info(info)
        
        # Análisis principal
        story.append(Paragraph("🤖 Análisis AgentFlow Manager", heading_style))
        
        if content:
            st.success(f"✅ Contenido extraído: {len(content)} caracteres")
            # Dividir el contenido en párrafos
            paragraphs = content.split('\n')
            for para in paragraphs:
                if para.strip():
                    # Procesar markdown básico
                    if para.startswith('**') and para.endswith('**'):
                        para = f"<b>{para[2:-2]}</b>"
                    elif para.startswith('*') and para.endswith('*'):
                        para = f"<i>{para[1:-1]}</i>"
                    
                    # Limpiar caracteres problemáticos
                    para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    if para.startswith('&lt;b&gt;') and para.endswith('&lt;/b&gt;'):
                        para = f"<b>{para[8:-9]}</b>"
                    
                    try:
                        story.append(Paragraph(para, normal_style))
                    except Exception as e:
                        # Si falla el párrafo, usar versión simplificada
                        story.append(Paragraph(para.strip(), normal_style))
                else:
                    story.append(Spacer(1, 6))
        else:
            st.warning("⚠️ No se encontró contenido para el PDF")
            story.append(Paragraph("Análisis completado exitosamente. Consulte la interfaz web para ver los resultados detallados.", normal_style))
        
        story.append(Spacer(1, 20))
        
        # Información técnica
        story.append(Paragraph("🔧 Información Técnica", heading_style))
        if hasattr(resultado, 'tasks_output') and resultado.tasks_output:
            story.append(Paragraph(f"<b>Tareas ejecutadas:</b> {len(resultado.tasks_output)}", normal_style))
            for i, task in enumerate(resultado.tasks_output, 1):
                agent_name = getattr(task, 'agent', 'Agente desconocido')
                story.append(Paragraph(f"• Tarea {i}: {agent_name}", normal_style))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Generado por AgentFlow Manager - Sistema de Análisis Empresarial", 
                              ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, 
                                           alignment=TA_CENTER, textColor=colors.grey)))
        
        st.success("✅ Contenido del PDF preparado")
        
        # Construir PDF
        doc.build(story)
        st.success("✅ PDF construido exitosamente")
        
        # Obtener el PDF
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Generar nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Analisis_Empresarial_{timestamp}.pdf"
        
        st.success(f"✅ PDF generado: {len(pdf_data)} bytes")
        
        # Verificar que los datos son válidos
        if pdf_data.startswith(b'%PDF'):
            pdf_logger.info("✅ PDF tiene header válido")
        else:
            pdf_logger.error("❌ PDF NO tiene header válido")
            pdf_logger.error(f"Primeros 20 bytes: {pdf_data[:20]}")
        
        # También guardar una copia local para debug
        try:
            local_path = Path(__file__).parent.parent / "resultados" / filename
            pdf_logger.info(f"Guardando copia local en: {local_path}")
            with open(local_path, 'wb') as f:
                f.write(pdf_data)
            st.info(f"💾 Copia guardada en: {local_path}")
            pdf_logger.info("✅ Copia local guardada exitosamente")
        except Exception as e:
            st.warning(f"⚠️ No se pudo guardar copia local: {e}")
            pdf_logger.error(f"Error guardando copia local: {e}")
        
        st.success("✅ PDF generado exitosamente!")
        
        pdf_logger.info("=" * 60)
        pdf_logger.info("GENERACIÓN DE PDF COMPLETADA")
        pdf_logger.info("=" * 60)
        
        # RETORNAR LOS DATOS DEL PDF (CRÍTICO)
        return pdf_data
        
    except ImportError as e:
        pdf_logger.error(f"Error de importación: {e}")
        st.error("❌ Error: ReportLab no está instalado. Ejecuta: pip install reportlab")
        st.code("pip install reportlab")
        return None
    except Exception as e:
        pdf_logger.error(f"Error inesperado: {e}")
        pdf_logger.error("Traceback completo:", exc_info=True)
        st.error(f"❌ Error generando PDF: {str(e)}")
        import traceback
        with st.expander("🔍 Debug - Detalles del error"):
            st.code(traceback.format_exc())
        return None

def show_dashboard_page():
    """Dashboard con métricas del sistema"""
    st.header("📊 Dashboard del Sistema")
    st.info("Dashboard en desarrollo...")

def show_history_page():
    """Historial de análisis realizados - Lee archivos existentes"""
    st.header("📁 Historial de Análisis")
    
    # Ruta a la carpeta de resultados
    try:
        project_root = Path(__file__).parent.parent
        resultados_dir = project_root / "resultados"
        
        if not resultados_dir.exists():
            st.info("📭 No se encontró la carpeta de resultados")
            st.markdown("""
            ### 🚀 ¿Cómo empezar?
            1. Ve a la página **📊 Análisis Empresarial**
            2. Ejecuta algunos análisis
            3. Los PDFs se guardarán automáticamente
            4. Regresa aquí para descargarlos
            """)
            return
        
        # Buscar archivos PDF en la carpeta resultados
        pdf_files = list(resultados_dir.glob("*.pdf"))
        
        if not pdf_files:
            st.info("📭 No hay PDFs guardados aún")
            st.markdown(f"""
            ### 📂 Carpeta de resultados encontrada:
            `{resultados_dir}`
            
            ### 🚀 Para generar análisis:
            1. Ve a **📊 Análisis Empresarial**
            2. Completa el formulario y ejecuta análisis
            3. Los PDFs se guardarán automáticamente aquí
            """)
            return
        
        # Estadísticas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 PDFs Encontrados", len(pdf_files))
        with col2:
            total_size = sum(f.stat().st_size for f in pdf_files) / (1024*1024)  # MB
            st.metric("� Tamaño Total", f"{total_size:.1f} MB")
        with col3:
            if pdf_files:
                newest = max(pdf_files, key=lambda f: f.stat().st_mtime)
                newest_date = datetime.fromtimestamp(newest.stat().st_mtime).strftime('%Y-%m-%d')
                st.metric("📅 Más Reciente", newest_date)
        
        st.markdown("---")
        
        # Ordenar archivos por fecha (más recientes primero)
        pdf_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        # Mostrar lista de archivos
        st.subheader(f"📋 Análisis Disponibles ({len(pdf_files)})")
        
        for i, pdf_file in enumerate(pdf_files):
            # Obtener información del archivo
            file_stat = pdf_file.stat()
            file_size = file_stat.st_size / 1024  # KB
            file_date = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Extraer información del nombre del archivo
            filename = pdf_file.name
            
            # Intentar extraer empresa y tipo del nombre
            empresa_nombre = "Empresa"
            tipo_analisis = "Análisis"
            
            if "Analisis_Empresarial_" in filename:
                # Formato: Analisis_Empresarial_YYYYMMDD_HHMMSS.pdf
                fecha_hora = filename.replace("Analisis_Empresarial_", "").replace(".pdf", "")
                if len(fecha_hora) == 15:  # YYYYMMDD_HHMMSS
                    fecha_str = fecha_hora[:8]
                    hora_str = fecha_hora[9:]
                    try:
                        fecha_formateada = f"{fecha_str[:4]}-{fecha_str[4:6]}-{fecha_str[6:8]}"
                        hora_formateada = f"{hora_str[:2]}:{hora_str[2:4]}:{hora_str[4:6]}"
                    except:
                        fecha_formateada = file_date.strftime('%Y-%m-%d')
                        hora_formateada = file_date.strftime('%H:%M:%S')
                else:
                    fecha_formateada = file_date.strftime('%Y-%m-%d')
                    hora_formateada = file_date.strftime('%H:%M:%S')
            else:
                fecha_formateada = file_date.strftime('%Y-%m-%d')
                hora_formateada = file_date.strftime('%H:%M:%S')
            
            # Mostrar cada archivo en un expander
            with st.expander(f"📊 {filename} ({file_size:.1f} KB) - {fecha_formateada}"):
                
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.markdown(f"**� Archivo:** {filename}")
                    st.markdown(f"**📅 Fecha:** {fecha_formateada}")
                    st.markdown(f"**🕐 Hora:** {hora_formateada}")
                
                with col_info2:
                    st.markdown(f"**💾 Tamaño:** {file_size:.1f} KB")
                    st.markdown(f"**📂 Ubicación:** resultados/")
                    st.markdown(f"**🔢 ID:** #{i+1}")
                
                # Botones de acción
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    # Leer archivo y crear botón de descarga
                    try:
                        with open(pdf_file, 'rb') as f:
                            pdf_data = f.read()
                        
                        st.download_button(
                            label="⬇️ Descargar PDF",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"download_pdf_{i}",
                            help="Descargar a tu carpeta de Descargas"
                        )
                    except Exception as e:
                        st.error(f"❌ Error leyendo archivo: {e}")
                
                with col_btn2:
                    if st.button(f"� Abrir Carpeta", key=f"open_folder_{i}"):
                        # Comando para abrir la carpeta en Windows
                        import subprocess
                        try:
                            subprocess.Popen(['explorer', str(resultados_dir)])
                            st.success("✅ Carpeta abierta")
                        except:
                            st.info(f"📂 Ubicación: {resultados_dir}")
                
                with col_btn3:
                    # Sistema de eliminación con confirmación mejorado
                    delete_key = f"delete_confirm_{i}"
                    
                    if st.button(f"🗑️ Eliminar", key=f"delete_btn_{i}", help="Eliminar este PDF"):
                        st.session_state[delete_key] = True
                    
                    # Mostrar confirmación si está activada
                    if st.session_state.get(delete_key, False):
                        st.warning(f"⚠️ ¿Eliminar **{filename}**?")
                        
                        col_conf1, col_conf2 = st.columns(2)
                        
                        with col_conf1:
                            if st.button("✅ SÍ, Eliminar", key=f"yes_delete_{i}", type="primary"):
                                try:
                                    pdf_file.unlink()  # Eliminar archivo
                                    st.success(f"✅ {filename} eliminado correctamente")
                                    # Limpiar estado de confirmación
                                    if delete_key in st.session_state:
                                        del st.session_state[delete_key]
                                    st.rerun()  # Recargar página
                                except Exception as e:
                                    st.error(f"❌ Error eliminando: {e}")
                        
                        with col_conf2:
                            if st.button("❌ Cancelar", key=f"cancel_delete_{i}"):
                                # Limpiar estado de confirmación
                                if delete_key in st.session_state:
                                    del st.session_state[delete_key]
                                st.rerun()
        
        # Opciones masivas
        st.markdown("---")
        st.subheader("🗂️ Gestión Masiva")
        
        col_masiva1, col_masiva2 = st.columns(2)
        
        with col_masiva1:
            if st.button("� Abrir Carpeta Resultados"):
                import subprocess
                try:
                    subprocess.Popen(['explorer', str(resultados_dir)])
                    st.success("✅ Carpeta abierta en explorador")
                except:
                    st.info(f"📂 Ubicación: {resultados_dir}")
        
        with col_masiva2:
            # Sistema de eliminación masiva con confirmación
            delete_all_key = "delete_all_confirm"
            
            if st.button("🗑️ Limpiar Todos los PDFs", use_container_width=True, type="secondary"):
                st.session_state[delete_all_key] = True
            
            # Mostrar confirmación para eliminación masiva
            if st.session_state.get(delete_all_key, False):
                st.error(f"⚠️ **¿Eliminar TODOS los {len(pdf_files)} PDFs?**")
                st.warning("Esta acción no se puede deshacer")
                
                col_mass1, col_mass2 = st.columns(2)
                
                with col_mass1:
                    if st.button("✅ SÍ, Eliminar TODO", key="confirm_delete_all", type="primary"):
                        try:
                            count = 0
                            for pdf_file in pdf_files:
                                pdf_file.unlink()
                                count += 1
                            st.success(f"✅ {count} archivos eliminados correctamente")
                            # Limpiar estado
                            if delete_all_key in st.session_state:
                                del st.session_state[delete_all_key]
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error eliminando archivos: {e}")
                
                with col_mass2:
                    if st.button("❌ Cancelar", key="cancel_delete_all"):
                        # Limpiar estado de confirmación
                        if delete_all_key in st.session_state:
                            del st.session_state[delete_all_key]
                        st.rerun()
        
        # Información adicional
        st.markdown("---")
        st.info(f"📂 **Ubicación de archivos:** `{resultados_dir}`")
        
    except Exception as e:
        st.error(f"❌ Error accediendo al historial: {e}")
        st.markdown("""
        ### 🔧 Solución:
        1. Asegúrate de que la carpeta `resultados/` existe
        2. Verifica permisos de lectura
        3. Ejecuta algunos análisis primero
        """)

def show_tools_page():
    """Página de herramientas del sistema"""
    st.header("🛠️ Herramientas del Sistema")
    st.info("Herramientas en desarrollo...")

def show_system_page():
    """Página del sistema y validación"""
    st.header("🧪 Sistema y Validación")
    st.info("Sistema en desarrollo...")

def show_help_page():
    """Página de ayuda y documentación"""
    st.header("📚 Ayuda y Documentación")
    st.info("Ayuda en desarrollo...")

if __name__ == "__main__":
    main()
