import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use('Agg')

from datos import (
    KPIS, get_pareto_dataframe, PARETO_M_CATEGORIES,
    PHVA_DETALLADO, PHVA_PHASES, PHVA_TEXTOS
)
from graficos import generar_ishikawa, generar_phva_donut, generar_kpi_barras

st.set_page_config(
    layout="wide",
    page_title="Dashboard GMAA SAC - Mejora Continua",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# CSS Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #1F4E78;
        --secondary: #2C3E50;
        --success: #27AE60;
        --warning: #ED7D31;
        --danger: #E74C3C;
        --purple: #7030A0;
        --green: #70AD47;
        --bg: #FFFFFF;
        --card-bg: #FFFFFF;
        --border: #E8ECEF;
        --text: #2C3E50;
        --text-muted: #6C757D;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    .stApp {
        background-color: var(--bg);
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--primary) !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 20px rgba(31, 78, 120, 0.08);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 8px 30px rgba(31, 78, 120, 0.12);
        transform: translateY(-2px);
    }
    [data-testid="stMetric"] label {
        color: var(--text-muted) !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: transparent;
        padding: 0 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F8F9FA;
        border-radius: 10px 10px 0 0;
        padding: 14px 28px;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid var(--border);
        border-bottom: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #EFF3F7;
        color: var(--primary);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--primary);
        font-size: 1.1rem;
        font-weight: 700;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
    }
    .stTable {
        border-radius: 12px;
        overflow: hidden;
    }

    .stRadio > div {
        flex-direction: row;
        gap: 12px;
        flex-wrap: wrap;
    }
    .stRadio label {
        background: #F8F9FA;
        border: 2px solid var(--border);
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .stRadio label:hover {
        border-color: var(--primary);
        background: #EFF3F7;
    }

    .phase-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        height: 100%;
    }
    .phase-card h4 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
    }
    .phase-card p {
        margin: 0;
        line-height: 1.7;
        font-size: 1.05rem;
        color: var(--text);
    }
    .phase-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
    }
    .section-header::before {
        content: "";
        width: 4px;
        height: 28px;
        background: var(--primary);
        border-radius: 2px;
    }

    .dashboard-footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-muted);
        font-size: 0.85rem;
        border-top: 1px solid var(--border);
        margin-top: 2rem;
    }

    .info-box {
        background: #EFF3F7;
        border-left: 4px solid var(--primary);
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    .info-box.success {
        background: #E8F8F0;
        border-left-color: var(--success);
    }
    .info-box.warning {
        background: #FFF3E0;
        border-left-color: var(--warning);
    }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1F4E78 0%, #2C3E50 100%); 
                border-radius: 12px; padding: 1rem; text-align: center; color: white;
                box-shadow: 0 4px 15px rgba(31, 78, 120, 0.3);">
        <div style="font-size: 2.5rem;">🏭</div>
        <div style="font-weight: 700; font-size: 0.85rem; margin-top: 0.25rem;">GMAA SAC</div>
    </div>
    """, unsafe_allow_html=True)
with col_title:
    st.markdown("""
    <div style="padding-top: 0.5rem;">
        <h1 style="margin: 0; font-size: 2.2rem; background: linear-gradient(90deg, #1F4E78, #2C3E50); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Dashboard de Mejora Continua
        </h1>
        <p style="margin: 0.25rem 0 0 0; color: #6C757D; font-size: 1.1rem; font-weight: 400;">
            Calzado GMAA SAC — Análisis 5W2H, Pareto, Ishikawa, PHVA & KPIs
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Productividad",
        value=f"{KPIS['productividad_actual']:.1f}",
        delta=f"+{KPIS['productividad_actual'] - KPIS['productividad_anterior']:.1f} unid/hr",
        delta_color="normal"
    )

with kpi2:
    st.metric(
        label="Producción Mensual",
        value=f"{KPIS['produccion_actual']:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."),
        delta=f"+{KPIS['produccion_actual'] - KPIS['produccion_anterior']:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."),
        delta_color="normal"
    )

with kpi3:
    st.metric(
        label="Beneficio Mensual",
        value=f"S/ {KPIS['beneficio_mensual']:,}".replace(",", ".")
    )

with kpi4:
    st.metric(
        label="Relación B/C",
        value=f"{KPIS['relacion_bc']:.2f}",
        help="Beneficio / Costo = 1.26 (Rentable)"
    )

st.sidebar.markdown("### 🔍 Filtros de Análisis")
categoria_seleccionada = st.sidebar.selectbox(
    "Filtrar Pareto por Categoría (4M):",
    options=["Todas"] + list(PARETO_M_CATEGORIES.keys()),
    index=0,
    help="Selecciona una categoría para filtrar el diagrama de Pareto"
)

df_pareto = get_pareto_dataframe()
if categoria_seleccionada != "Todas":
    df_filtrado = df_pareto[df_pareto["Categoria_M"] == categoria_seleccionada].copy()
else:
    df_filtrado = df_pareto.copy()

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Contexto (5W2H)",
    "2. Análisis (Pareto & Ishikawa)",
    "3. Solución (Ciclo PHVA)",
    "4. KPIs & Resultados"
])

with tab1:
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0;">Definición del Problema — Metodología 5W2H</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="background: linear-gradient(135deg, #E8F0FE 0%, #EFF3F7 100%); border-left-color: #1F4E78; font-size: 1.05rem; line-height: 1.8;">
        <strong>🎯 PLANTEAMIENTO DEL PROBLEMA</strong><br><br>
        <strong>Calzado GMAA SAC</strong>, empresa dedicada a la fabricación de calzado en <strong>Trujillo, Perú</strong>, presenta una <strong>baja productividad en su línea de producción (11.8 unid/hora)</strong>. 
        Esta situación genera <strong>pérdidas estimadas en S/ 126,827 mensuales</strong> debido a fallas en el control de producción, paradas de máquina y falta de mantenimiento. 
        Para resolverlo, se aplican herramientas de calidad como <strong>Pareto, Ishikawa y el ciclo PHVA</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong>📋 Herramientas de Calidad Utilizadas:</strong><br>
        • <strong>Recolección:</strong> DOP (Diario de Operaciones de Producción)<br>
        • <strong>Análisis:</strong> Diagrama de Pareto (Principio 80/20) + Diagrama de Ishikawa (4M)<br>
        • <strong>Mejora:</strong> Ciclo PHVA (Planificar-Hacer-Verificar-Actuar)
    </div>
    """, unsafe_allow_html=True)

    w2h_data = {
        "Pregunta": [
            "**WHAT** (¿Qué se mejora?)",
            "**WHERE** (¿Dónde ocurre?)",
            "**WHEN** (¿Cuándo ocurre?)",
            "**WHO** (¿Quiénes participan?)",
            "**WHY** (¿Por qué mejorar?)",
            "**HOW** (¿Cómo se mejora?)",
            "**HOW MUCH** (¿Cuánto cuesta/beneficio?)"
        ],
        "Respuesta": [
            "Productividad y calidad en la línea de producción de calzado (pares/hora, defectos, paradas)",
            "Planta de producción Calzado GMAA SAC — Líneas de corte, cosido, armado y acabado",
            "Turnos de producción diarios; mayor incidencia en horas pico y cambios de modelo",
            "Operarios de línea, jefes de turno, mantenimiento, calidad, logística, gerencia de producción",
            "Baja productividad (11.8 unid/h), paradas frecuentes, defectos, mermas, entregas tardías → pérdidas económicas",
            "Capacitación ISO 9001, implementación 5S, mejora DOP, mantenimiento preventivo, estandarización, indicadores",
            "Inversión en capacitación y 5S → Beneficio mensual S/ 126,827 | Relación B/C = 1.26 | Productividad +5.9%"
        ]
    }

    df_w2h = pd.DataFrame(w2h_data)
    st.table(df_w2h.style.set_properties(**{
        'background-color': '#FFFFFF',
        'color': '#2C3E50',
        'border-color': '#E8ECEF',
        'font-family': 'Inter, Arial, sans-serif',
        'font-size': '0.95rem'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#1F4E78'), ('color', 'white'), 
                                     ('font-weight', '700'), ('font-size', '1rem'),
                                     ('padding', '12px'), ('text-align', 'left')]},
        {'selector': 'td', 'props': [('padding', '12px'), ('border', '1px solid #E8ECEF'),
                                     ('vertical-align', 'top'), ('line-height', '1.6')]},
        {'selector': 'tr:nth-of-type(odd)', 'props': [('background-color', '#F8F9FA')]},
        {'selector': 'tr:hover', 'props': [('background-color', '#EFF3F7')]}
    ]))

with tab2:
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0;">Análisis de Causas — Pareto & Ishikawa</h2>
    </div>
    """, unsafe_allow_html=True)

    col_pareto, col_ishikawa = st.columns([1, 1], gap="large")

    with col_pareto:
        st.markdown("#### 📊 Diagrama de Pareto - Causas de Baja Productividad")

        if len(df_filtrado) > 0:
            from plotly.subplots import make_subplots
            fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])

            fig_pareto.add_trace(
                go.Bar(
                    x=df_filtrado["Causa"],
                    y=df_filtrado["Frecuencia"],
                    name="Frecuencia",
                    marker_color="#1F4E78",
                    text=df_filtrado["Frecuencia"],
                    textposition="outside",
                    textfont=dict(size=12, color="#1F4E78", family="Arial Black"),
                    width=0.55,
                    hovertemplate="<b>%{x}</b><br>Frecuencia: %{y}<br>%{customdata:.1f}%<extra></extra>",
                    customdata=df_filtrado["Porcentaje"]
                ),
                secondary_y=False
            )

            fig_pareto.add_trace(
                go.Scatter(
                    x=df_filtrado["Causa"],
                    y=df_filtrado["Porcentaje_Acumulado"],
                    name="% Acumulado",
                    mode="lines+markers+text",
                    line=dict(color="#C0392B", width=3),
                    marker=dict(size=10, color="#C0392B", symbol="circle", line=dict(width=2, color="#FFFFFF")),
                    text=df_filtrado["Porcentaje_Acumulado"].apply(lambda x: f"{x:.1f}%"),
                    textposition="top center",
                    textfont=dict(size=11, color="#C0392B", family="Arial Black"),
                    hovertemplate="<b>%{x}</b><br>% Acumulado: %{y:.1f}%<extra></extra>"
                ),
                secondary_y=True
            )

            fig_pareto.add_hline(
                y=80, line_dash="dot", line_color="#C0392B", line_width=2.5,
                secondary_y=True
            )

            fig_pareto.update_xaxes(
                tickangle=-30,
                tickfont=dict(size=10, family="Arial"),
                title_text="",
                showgrid=False
            )
            fig_pareto.update_yaxes(
                title_text="<b>Frecuencia</b>", secondary_y=False,
                showgrid=True, gridcolor="#F0F0F0",
                title_font=dict(size=12, color="#1F4E78"),
                rangemode="tozero"
            )
            fig_pareto.update_yaxes(
                title_text="<b>% Acumulado</b>", secondary_y=True,
                range=[0, 105], showgrid=False,
                title_font=dict(size=12, color="#C0392B"),
                tickfont=dict(size=10, color="#C0392B"),
                ticksuffix="%"
            )

            fig_pareto.update_layout(
                height=540,
                template="plotly_white",
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=11, family="Arial"),
                    bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#E0E0E0",
                    borderwidth=1
                ),
                margin=dict(t=50, b=150, l=60, r=60),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                hovermode="x unified",
                title=dict(
                    text="<b>Diagrama de Pareto - Causas de Baja Productividad</b>",
                    font=dict(size=16, color="#1F4E78", family="Arial"),
                    x=0.5,
                    y=0.97
                )
            )

            st.plotly_chart(fig_pareto, width='stretch')

            st.info("""
            📌 **Análisis Pareto (Regla 80/20):** Las primeras 6 causas (Falta de control, Paradas, Mantenimiento, Inspección, Mermas y Recepción) acumulan el 80% del problema. Esto nos indica que si concentramos los esfuerzos en resolver estos 6 puntos críticos, eliminaremos la mayor parte de la baja productividad.
            """)

        else:
            st.warning("No hay datos para la categoría seleccionada.")

    with col_ishikawa:
        st.markdown("#### 🐟 Diagrama de Ishikawa (Espina de Pescado) — 4M")
        
        fig_ishikawa = generar_ishikawa()
        st.pyplot(fig_ishikawa, width='stretch')
        
        st.success("""
        🐟 **Causa Raíz (Ishikawa 4M):** Identificamos que el problema no es solo de máquinas. La 'Falta de control' (Métodos) y las 'Entregas tardías' (Personas) son igual de graves. La causa raíz principal es la ausencia de un sistema de gestión de calidad que estandarice los procesos.
        """)

with tab3:
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0;">Ciclo PHVA — Mejora Continua</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **El Problema:** Línea de producción con fallas constantes, sin inspección y con máquinas paradas. **La Solución:** Aplicar el ciclo PHVA para ordenar la empresa.
    """)

    fase_seleccionada = st.radio(
        "Selecciona una fase para ver el detalle:",
        options=list(PHVA_DETALLADO.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )

    col_donut, col_info = st.columns([1, 1], gap="large")

    with col_donut:
        fig_phva = generar_phva_donut(fase_seleccionada)
        st.plotly_chart(fig_phva, width='stretch')

    with col_info:
        data = PHVA_DETALLADO[fase_seleccionada]
        color = data["color"]
        icon = data["icon"]

        badge_styles = {
            '#2E86C1': 'background:#2E86C1; color:white;',
            '#52BE80': 'background:#52BE80; color:white;',
            '#F5B041': 'background:#F5B041; color:white;',
            '#AF7AC5': 'background:#AF7AC5; color:white;'
        }

        st.markdown(f"""
        <div class="phase-card" style="border-left: 6px solid {color}; background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span style="font-size: 1.8rem;">{icon}</span>
                <span class="phase-badge" style="{badge_styles.get(color, 'background:#6C757D; color:white;')}">{fase_seleccionada}</span>
            </div>
            <p style="font-size: 1.15rem; line-height: 1.9; color: #2C3E50; margin: 0;">
                {data["texto"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.warning("""
        🚨 **Lo que hacíamos mal:** No teníamos métricas, no había mantenimiento preventivo y los operarios no estaban capacitados. 
        ✅ **Lo que hacemos ahora:** Implementamos 5S, medimos la productividad a diario y estandarizamos el proceso. Resultado: Pasamos de 11.8 a 12.5 unidades por hora.
        """)

        st.success("""
        **Cierre del ciclo:** Aplicando el PHVA logramos el objetivo principal (**12.5 unid/hora**). 
        El siguiente paso es mantener este estándar mediante **auditorías mensuales** y la mejora continua institucionalizada.
        """)

with tab4:
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0;">Indicadores Clave — Comparativo Antes vs Después</h2>
    </div>
    """, unsafe_allow_html=True)

    col_table, col_chart = st.columns([1, 1], gap="large")

    with col_table:
        st.markdown("#### 📋 Tabla Comparativa de KPIs")

        kpi_table = pd.DataFrame({
            "Indicador": [
                "Productividad (unid/hora)",
                "Producción Mensual (pares)",
                "Beneficio Mensual (S/)",
                "Relación Beneficio/Costo",
                "Defectos / Calidad",
                "Paradas de Máquina",
                "Entregas a Tiempo"
            ],
            "Antes (Situación Inicial)": [
                "11.8",
                "33,938",
                "— (Pérdida)",
                "< 1.0 (Déficit)",
                "Alto (Sin control)",
                "Frecuentes (Sin mantenimiento)",
                "Bajo cumplimiento"
            ],
            "Meta (Objetivo)": [
                "≥ 12.5",
                "≥ 35,000",
                "> 0",
                "≥ 1.2",
                "Reducir 50%",
                "Reducir 70%",
                "≥ 95%"
            ],
            "Después (Post-Mejora)": [
                "**12.5** ✅",
                "**35,993** ✅",
                "**126,827** ✅",
                "**1.26** ✅",
                "Controlado (ISO 9001)",
                "Mantenimiento preventivo",
                "Estandarizado (DOP/5S)"
            ]
        })

        st.dataframe(
            kpi_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Indicador": st.column_config.TextColumn(width="medium"),
                "Antes (Situación Inicial)": st.column_config.TextColumn(width="medium"),
                "Meta (Objetivo)": st.column_config.TextColumn(width="medium"),
                "Después (Post-Mejora)": st.column_config.TextColumn(width="large")
            }
        )

    with col_chart:
        st.markdown("#### 📈 Gráfico Comparativo: Antes vs Después")
        fig_kpi = generar_kpi_barras()
        st.plotly_chart(fig_kpi, width='stretch')

    st.success("""
    💰 **Impacto en el Negocio:** La mejora en la productividad no solo nos hizo cumplir la meta técnica, sino que generó un aumento en la producción de +2,179.7 pares al mes. Esto se traduce en un beneficio económico real de **S/ 126,827 mensuales** y una relación Beneficio/Costo de 1.26 (por cada sol invertido, ganamos 0.26 soles).
    """)

st.markdown("""
<div class="dashboard-footer">
    <strong>Dashboard de Mejora Continua — Calzado GMAA SAC</strong><br>
    Desarrollado con Streamlit, Plotly & Matplotlib | Metodología: 5W2H · Pareto · Ishikawa · PHVA<br>
    Datos basados en caso real de optimización de producción de calzado
</div>
""", unsafe_allow_html=True)