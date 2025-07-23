"""
Componentes UI reutilizables para el frontend de AgentFlow Manager
"""

import streamlit as st
from typing import Dict, Any, Optional, List
import plotly.graph_objects as go
import plotly.express as px

def mostrar_header(titulo: str, subtitulo: Optional[str] = None) -> None:
    """
    Muestra un header estilizado para las páginas
    
    Args:
        titulo: Título principal
        subtitulo: Subtítulo opcional
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #1f77b4, #17becf);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    ">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">
            [RUN] {titulo}
        </h1>
        {f'<p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;">{subtitulo}</p>' if subtitulo else ''}
    </div>
    """, unsafe_allow_html=True)

def mostrar_metrica_card(
    titulo: str, 
    valor: str, 
    icono: str = "📊",
    color: str = "#1f77b4"
) -> None:
    """
    Muestra una tarjeta de métrica estilizada
    
    Args:
        titulo: Título de la métrica
        valor: Valor a mostrar
        icono: Icono para la tarjeta
        color: Color de acento
    """
    st.markdown(f"""
    <div style="
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid {color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    ">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">{icono}</div>
            <div>
                <h3 style="margin: 0; color: #333;">{titulo}</h3>
                <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: {color};">{valor}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def crear_sidebar_navegacion() -> str:
    """
    Crea un sidebar de navegación
    
    Returns:
        La página seleccionada
    """
    with st.sidebar:
        st.markdown("## 🧭 Navegación")
        
        paginas = {
            "🏠 Inicio": "inicio",
            "📊 Análisis": "analisis", 
            "[RUN] Agentes": "agentes",
            "⚙️ Configuración": "configuracion"
        }
        
        pagina_seleccionada = st.selectbox(
            "Seleccionar página:",
            options=list(paginas.keys()),
            key="navegacion"
        )
        
        return paginas[pagina_seleccionada]

def mostrar_estado_sistema(estado: Dict[str, Any]) -> None:
    """
    Muestra el estado del sistema en formato visual
    
    Args:
        estado: Diccionario con información del estado
    """
    st.markdown("### 🔍 Estado del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_color = "#28a745" if estado.get("activo", False) else "#dc3545"
        status_text = "Activo" if estado.get("activo", False) else "Inactivo"
        mostrar_metrica_card("Estado", status_text, "🔋", status_color)
    
    with col2:
        agentes_count = estado.get("agentes_activos", 0)
        mostrar_metrica_card("Agentes", str(agentes_count), "[RUN]", "#17a2b8")
    
    with col3:
        tareas_count = estado.get("tareas_completadas", 0)
        mostrar_metrica_card("Tareas", str(tareas_count), "✅", "#ffc107")

def crear_grafico_metricas(datos: List[Dict[str, Any]]) -> go.Figure:
    """
    Crea un gráfico de métricas usando Plotly
    
    Args:
        datos: Lista de datos para el gráfico
        
    Returns:
        Figura de Plotly
    """
    if not datos:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title="Métricas del Sistema",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    # Extraer datos para el gráfico
    labels = [item.get("nombre", f"Item {i}") for i, item in enumerate(datos)]
    values = [item.get("valor", 0) for item in datos]
    
    fig = px.bar(
        x=labels,
        y=values,
        title="Métricas del Sistema",
        labels={"x": "Componentes", "y": "Valores"}
    )
    
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def mostrar_mensaje_info(mensaje: str, tipo: str = "info") -> None:
    """
    Muestra un mensaje informativo estilizado
    
    Args:
        mensaje: Texto del mensaje
        tipo: Tipo de mensaje (info, success, warning, error)
    """
    colores = {
        "info": "#17a2b8",
        "success": "#28a745", 
        "warning": "#ffc107",
        "error": "#dc3545"
    }
    
    iconos = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️", 
        "error": "❌"
    }
    
    color = colores.get(tipo, "#17a2b8")
    icono = iconos.get(tipo, "ℹ️")
    
    st.markdown(f"""
    <div style="
        background: {color}15;
        border: 1px solid {color};
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    ">
        <div style="font-size: 1.5rem;">{icono}</div>
        <div style="color: {color}; font-weight: 500;">{mensaje}</div>
    </div>
    """, unsafe_allow_html=True)

def crear_formulario_configuracion() -> Dict[str, Any]:
    """
    Crea un formulario de configuración básico
    
    Returns:
        Diccionario con la configuración
    """
    st.markdown("### ⚙️ Configuración del Sistema")
    
    with st.form("configuracion_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            modo_debug = st.checkbox("Modo Debug", value=False)
            max_agentes = st.number_input("Máx. Agentes", min_value=1, max_value=10, value=3)
        
        with col2:
            timeout = st.number_input("Timeout (seg)", min_value=30, max_value=300, value=120)
            auto_save = st.checkbox("Auto-guardar", value=True)
        
        submit = st.form_submit_button("💾 Guardar Configuración")
        
        if submit:
            config = {
                "modo_debug": modo_debug,
                "max_agentes": max_agentes,
                "timeout": timeout,
                "auto_save": auto_save
            }
            mostrar_mensaje_info("✅ Configuración guardada exitosamente", "success")
            return config
    
    return {}

# Función para mostrar el footer
def mostrar_footer() -> None:
    """Muestra el footer de la aplicación"""
    st.markdown("➖")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>[RUN] <strong>AgentFlow Manager</strong> - Powered by CrewAI & Streamlit</p>
        <p>Desarrollado para gestión inteligente de agentes empresariales</p>
    </div>
    """, unsafe_allow_html=True)
