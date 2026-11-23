import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datos import (
    KPIS, get_pareto_dataframe, PARETO_M_CATEGORIES,
    PHVA_DETALLADO, PHVA_PHASES
)
from graficos import (
    generar_ishikawa, generar_phva_donut, generar_kpi_barras, generar_pareto
)

st.set_page_config(
    layout="wide",
    page_title="Dashboard GMAA SAC - Mejora Continua",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ==================== CSS PREMIUM ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #1F4E78;
        --primary-dark: #15406E;
        --secondary: #2C3E50;
        --success: #52BE80;
        --success-dark: #45A056;
        --warning: #F5B041;
        --warning-dark: #D68910;
        --danger: #E74C3C;
        --info: #2E86C1;
        --info-light: #E8F4FD;
        --bg: #F4F6F9;
        --card-bg: #FFFFFF;
        --border: #E8ECEF;
        --text: #2C3E50;
        --text-muted: #6C757D;
        --pastel-blue: #E8F4FD;
        --pastel-green: #E9F7EF;
        --pastel-orange: #FDF3E7;
        --pastel-purple: #F4EEFA;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 100%;
    }

    /* Ocultar elementos de Streamlit para aspecto nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stAppHeader {display: none;}

    /* Fondo general */
    .stApp {
        background-color: var(--bg);
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary) !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        font-weight: 700 !important;
    }

    /* ===== HEADER PREMIUM ===== */
    .premium-header {
        background: linear-gradient(135deg, #1F4E78 0%, #15406E 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(31, 78, 120, 0.3);
        position: relative;
        overflow: hidden;
    }
    .premium-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
        transform: translate(50%, -50%);
    }
    .premium-header h1 {
        color: white !important;
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .premium-header p {
        color: rgba(255,255,255,0.9) !important;
        margin: 0;
        font-size: 1.1rem;
        font-weight: 400;
    }
    .premium-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
        backdrop-filter: blur(4px);
    }

    /* ===== TARJETAS KPI PREMIUM ===== */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.75rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid var(--border);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--primary);
    }
    .kpi-card.success::before { background: var(--success); }
    .kpi-card.warning::before { background: var(--warning); }
    .kpi-card.info::before { background: var(--info); }
    .kpi-label {
        color: var(--text-muted);
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
        display: block;
    }
    .kpi-value {
        color: var(--primary);
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
    }
    .kpi-delta {
        display: inline-block;
        background: var(--pastel-green);
        color: var(--success-dark);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-top: 0.5rem;
        border: 1px solid var(--success);
    }
    .kpi-delta.warning {
        background: var(--pastel-orange);
        color: var(--warning-dark);
        border-color: var(--warning);
    }

    /* ===== TABS PREMIUM ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0 4px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: var(--card-bg);
        border-radius: 12px 12px 0 0;
        padding: 14px 28px;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.95rem;
        border: 1px solid var(--border);
        border-bottom: none;
        transition: all 0.2s ease;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #F0F4F8;
        color: var(--primary);
        border-color: var(--primary);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--card-bg) !important;
        color: var(--primary) !important;
        border-color: var(--primary) !important;
        border-bottom: 2px solid var(--primary);
        box-shadow: 0 -2px 10px rgba(31, 78, 120, 0.1);
    }

    /* ===== SIDEBAR PREMIUM ===== */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--primary);
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* ===== DATA TABLE ===== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .stTable {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ===== RADIO BUTTONS PREMIUM ===== */
    .stRadio > div {
        flex-direction: row;
        gap: 12px;
        flex-wrap: wrap;
    }
    .stRadio label {
        background: var(--card-bg);
        border: 2px solid var(--border);
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    }
    .stRadio label:hover {
        border-color: var(--primary);
        background: var(--pastel-blue);
    }

    /* ===== CALLOUTS / ANOTACIONES ===== */
    .callout {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid var(--border);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }
    .callout::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    .callout.info::before { background: var(--info); }
    .callout.success::before { background: var(--success); }
    .callout.warning::before { background: var(--warning); }
    .callout .callout-icon {
        font-size: 1.5rem;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .callout .callout-content {
        flex: 1;
    }
    .callout-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        color: var(--text);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .callout-body {
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.7;
        margin: 0;
    }
    .callout.info .callout-title { color: var(--info); }
    .callout.success .callout-title { color: var(--success); }
    .callout.warning .callout-title { color: var(--warning); }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 2rem 0 1.5rem 0;
    }
    .section-header::before {
        content: "";
        width: 4px;
        height: 28px;
        background: var(--primary);
        border-radius: 2px;
    }
    .section-header h2 {
        margin: 0;
        font-size: 1.4rem;
    }

    /* ===== PHVA PHASE CARD ===== */
    .phase-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 16px;
        padding: 1.75rem;
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
        line-height: 1.8;
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

    /* ===== FOOTER ===== */
    .dashboard-footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-muted);
        font-size: 0.85rem;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
    }

    /* Ocultar warnings de deprecación */
    .stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="premium-header">
    <div class="premium-badge">🏭 GMAA S.A.C. | Sistema de Gestión de Calidad</div>
    <h1>Dashboard de Mejora Continua</h1>
    <p>Análisis de productividad, PHVA y KPIs — Calzado GMAA SAC, Trujillo, Perú</p>
</div>
""", unsafe_allow_html=True)

# ==================== KPI ROW ====================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
    <div class="kpi-card info">
        <span class="kpi-label">Productividad (unid/hora)</span>
        <p class="kpi-value">12.5</p>
        <span class="kpi-delta">+0.7 vs anterior</span>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="kpi-card success">
        <span class="kpi-label">Producción Mensual (pares)</span>
        <p class="kpi-value">35,992.7</p>
        <span class="kpi-delta warning">+2,179.7 pares</span>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="kpi-card success">
        <span class="kpi-label">Beneficio Mensual</span>
        <p class="kpi-value">S/ 126,827</p>
        <span class="kpi-delta">Rentable</span>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class="kpi-card info">
        <span class="kpi-label">Relación B/C</span>
        <p class="kpi-value">1.26</p>
        <span class="kpi-delta">1.26 : 1</span>
    </div>
    """, unsafe_allow_html=True)

# ==================== SIDEBAR FILTER ====================
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

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Contexto (5W2H)",
    "2. Análisis (Pareto & Ishikawa)",
    "3. Solución (Ciclo PHVA)",
    "4. KPIs & Resultados"
])

# ==================== TAB 1: 5W2H ====================
with tab1:
    st.markdown("""
    <div class="section-header">
        <h2>Definición del Problema — Metodología 5W2H</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="callout info">
        <span class="callout-icon">🎯</span>
        <div class="callout-content">
            <div class="callout-title">Planteamiento del Problema</div>
            <p class="callout-body">
                <strong>Calzado GMAA SAC</strong>, empresa dedicada a la fabricación de calzado en
                <strong>Trujillo, Perú</strong>, presenta una <strong>baja productividad en su línea de
                producción (11.8 unid/hora)</strong>. Esta situación genera
                <strong>pérdidas estimadas en S/ 126,827 mensuales</strong> debido a fallas en el control
                de producción, paradas de máquina y falta de mantenimiento. Para resolverlo, se aplican
                herramientas de calidad como <strong>Pareto, Ishikawa y el ciclo PHVA</strong>.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="callout info">
        <span class="callout-icon">📋</span>
        <div class="callout-content">
            <div class="callout-title">Herramientas de Calidad Utilizadas</div>
            <p class="callout-body">
                • <strong>Recolección:</strong> DOP (Diario de Operaciones de Producción)<br>
                • <strong>Análisis:</strong> Diagrama de Pareto (Principio 80/20) + Diagrama de Ishikawa (4M)<br>
                • <strong>Mejora:</strong> Ciclo PHVA (Planificar-Hacer-Verificar-Actuar)
            </p>
        </div>
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

# ==================== TAB 2: ANÁLISIS ====================
with tab2:
    st.markdown("""
    <div class="section-header">
        <h2>Análisis de Causas — Pareto & Ishikawa</h2>
    </div>
    """, unsafe_allow_html=True)

    col_pareto, col_ishikawa = st.columns([1, 1], gap="large")

    # --- PARETO ---
    with col_pareto:
        st.markdown("#### 📊 Diagrama de Pareto - Causas de Baja Productividad")

        if len(df_filtrado) > 0:
            fig_pareto = generar_pareto(df_filtrado)
            st.plotly_chart(fig_pareto, width='stretch')

            st.markdown("""
            <div class="callout info">
                <span class="callout-icon">📌</span>
                <div class="callout-content">
                    <div class="callout-title">Análisis Pareto (Regla 80/20)</div>
                    <p class="callout-body">
                        Las primeras 6 causas (Falta de control, Paradas, Mantenimiento, Inspección, Mermas y
                        Recepción) acumulan el 80% del problema. Esto nos indica que si concentramos los
                        esfuerzos en resolver estos 6 puntos críticos, eliminaremos la mayor parte de la
                        baja productividad.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No hay datos para la categoría seleccionada.")

    # --- ISHIKAWA ---
    with col_ishikawa:
        st.markdown("#### 🐟 Diagrama de Ishikawa (Espina de Pescado) — 4M")

        fig_ishikawa = generar_ishikawa()
        st.pyplot(fig_ishikawa, width='stretch')

        st.markdown("""
        <div class="callout success">
            <span class="callout-icon">🐟</span>
            <div class="callout-content">
                <div class="callout-title">Causa Raíz (Ishikawa 4M)</div>
                <p class="callout-body">
                    Identificamos que el problema no es solo de máquinas. La <strong>'Falta de control'</strong>
                    (Métodos) y las <strong>'Entregas tardías'</strong> (Personas) son igual de graves. La causa
                    raíz principal es la ausencia de un sistema de gestión de calidad que estandarice los procesos.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3: PHVA ====================
with tab3:
    st.markdown("""
    <div class="section-header">
        <h2>Ciclo PHVA — Mejora Continua</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="callout info">
        <span class="callout-icon">🔄</span>
        <div class="callout-content">
            <div class="callout-title">El Problema y la Solución</div>
            <p class="callout-body">
                <strong>El Problema:</strong> Línea de producción con fallas constantes, sin inspección y con
                máquinas paradas.<br>
                <strong>La Solución:</strong> Aplicar el ciclo PHVA para ordenar la empresa.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Selector de fase
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
        <div class="phase-card" style="border-left: 6px solid {color};">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span style="font-size: 1.8rem;">{icon}</span>
                <span class="phase-badge" style="{badge_styles.get(color, 'background:#6C757D; color:white;')}">{fase_seleccionada}</span>
            </div>
            <p style="font-size: 1.15rem; line-height: 1.9; color: #2C3E50; margin: 0;">
                {data["texto"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="callout warning">
            <span class="callout-icon">🚨</span>
            <div class="callout-content">
                <div class="callout-title">Lo que hacíamos mal vs. Lo que hacemos ahora</div>
                <p class="callout-body">
                    <strong>Lo que hacíamos mal:</strong> No teníamos métricas, no había mantenimiento
                    preventivo y los operarios no estaban capacitados.<br>
                    <strong>Lo que hacemos ahora:</strong> Implementamos 5S, medimos la productividad a
                    diario y estandarizamos el proceso. Resultado: Pasamos de 11.8 a 12.5 unidades por hora.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="callout success">
            <span class="callout-icon">✅</span>
            <div class="callout-content">
                <div class="callout-title">Cierre del ciclo PHVA</div>
                <p class="callout-body">
                    Aplicando el PHVA logramos el objetivo principal (<strong>12.5 unid/hora</strong>).
                    El siguiente paso es mantener este estándar mediante <strong>auditorías mensuales</strong>
                    y la mejora continua institucionalizada.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 4: KPIs ====================
with tab4:
    st.markdown("""
    <div class="section-header">
        <h2>Indicadores Clave — Comparativo Antes vs Después</h2>
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

    st.markdown("""
    <div class="callout success">
        <span class="callout-icon">💰</span>
        <div class="callout-content">
            <div class="callout-title">Impacto en el Negocio</div>
            <p class="callout-body">
                La mejora en la productividad no solo nos hizo cumplir la meta técnica, sino que
                generó un aumento en la producción de <strong>+2,179.7 pares al mes</strong>.
                Esto se traduce en un beneficio económico real de <strong>S/ 126,827 mensuales</strong>
                y una relación Beneficio/Costo de <strong>1.26</strong> (por cada sol invertido,
                ganamos 0.26 soles).
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="dashboard-footer">
    <strong>Dashboard de Mejora Continua — Calzado GMAA SAC</strong><br>
    Desarrollado con Streamlit, Plotly & Matplotlib | Metodología: 5W2H · Pareto · Ishikawa · PHVA<br>
    Datos basados en caso real de optimización de producción de calzado
</div>
""", unsafe_allow_html=True)