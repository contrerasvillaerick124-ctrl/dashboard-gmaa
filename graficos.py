import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import plotly.graph_objects as go


def generar_ishikawa():
    """
    Diagrama de Ishikawa con forma de PESCADO real.
    Espina central horizontal + 4 espinas diagonales (2 arriba, 2 abajo).
    Causas horizontales saliendo de las diagonales.
    Lienzo: 100x100.
    Diseño premium: fondo blanco puro, colores suaves, sin cuadrícula.
    """
    fig, ax = plt.subplots(figsize=(18, 11))
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.axis('off')
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')

    COLOR_PRINCIPAL = '#1F4E78'
    COLOR_PRINCIPAL_SUAVE = '#2E86C1'
    COLOR_CAUSAS = '#85929E'
    COLOR_CAJA_BORDE = '#1F4E78'
    COLOR_CAJA_FONDO = '#FDFEFE'

    # ============================================================
    # 1. ESPINA CENTRAL (flecha horizontal gruesa)
    # ============================================================
    ax.annotate('',
                xy=(95, 50), xycoords='data',
                xytext=(5, 50), textcoords='data',
                arrowprops=dict(
                    arrowstyle='->',
                    color=COLOR_PRINCIPAL,
                    lw=6,
                    mutation_scale=50
                ))

    # Cabeza del pescado - Problema central
    ax.text(97, 50, 'BAJA PRODUCTIVIDAD',
            fontsize=15, fontweight='bold', color='white',
            ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.6", facecolor=COLOR_PRINCIPAL, edgecolor='none'))

    # ============================================================
    # 2. ESPINA DIAGONAL SUPERIOR - MÉTODOS (de 30,50 a 15,80)
    # ============================================================
    ax.plot([30, 15], [50, 80], color=COLOR_PRINCIPAL_SUAVE, linewidth=4, solid_capstyle='round', zorder=3)

    ax.text(15, 83, 'MÉTODOS',
            fontsize=13, fontweight='bold', color=COLOR_PRINCIPAL_SUAVE,
            ha='center', va='bottom',
            bbox=dict(boxstyle="round,pad=0.4", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=2.5),
            zorder=4)

    # Causas horizontales hacia la IZQUIERDA de la diagonal
    causas_metodos = [
        (28, 54, "Falta de control y optimización\nen la producción"),
        (24, 62, "Falta de inspección\ny control de calidad"),
        (20, 70, "Falta de capacitaciones\na los trabajadores")
    ]
    for x_diag, y_diag, texto in causas_metodos:
        ax.plot([x_diag, 2], [y_diag, y_diag], color=COLOR_CAUSAS, linewidth=2.5, alpha=0.9, solid_capstyle='round', zorder=2)
        ax.text(0.5, y_diag, texto,
                fontsize=10, color='#2C3E50',
                ha='left', va='center',
                bbox=dict(boxstyle="round,pad=0.35", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=1.5),
                zorder=4)

    # ============================================================
    # 3. ESPINA DIAGONAL SUPERIOR - MÁQUINAS (de 50,50 a 35,80)
    # ============================================================
    ax.plot([50, 35], [50, 80], color=COLOR_PRINCIPAL_SUAVE, linewidth=4, solid_capstyle='round', zorder=3)

    ax.text(35, 83, 'MÁQUINAS',
            fontsize=13, fontweight='bold', color=COLOR_PRINCIPAL_SUAVE,
            ha='center', va='bottom',
            bbox=dict(boxstyle="round,pad=0.4", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=2.5),
            zorder=4)

    # Causas horizontales hacia la DERECHA
    causas_maquinas = [
        (47, 56, "Paradas en la producción\ny ciclos improductivos"),
        (42, 66, "Falta de mantenimiento\npreventivo y correctivo")
    ]
    for x_diag, y_diag, texto in causas_maquinas:
        ax.plot([x_diag, 75], [y_diag, y_diag], color=COLOR_CAUSAS, linewidth=2.5, alpha=0.9, solid_capstyle='round', zorder=2)
        ax.text(76.5, y_diag, texto,
                fontsize=10, color='#2C3E50',
                ha='left', va='center',
                bbox=dict(boxstyle="round,pad=0.35", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=1.5),
                zorder=4)

    # ============================================================
    # 4. ESPINA DIAGONAL INFERIOR - MATERIALES (de 30,50 a 15,20)
    # ============================================================
    ax.plot([30, 15], [50, 20], color=COLOR_PRINCIPAL_SUAVE, linewidth=4, solid_capstyle='round', zorder=3)

    ax.text(15, 17, 'MATERIALES',
            fontsize=13, fontweight='bold', color=COLOR_PRINCIPAL_SUAVE,
            ha='center', va='top',
            bbox=dict(boxstyle="round,pad=0.4", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=2.5),
            zorder=4)

    # Causas horizontales hacia la IZQUIERDA
    causas_materiales = [
        (28, 46, "Mermas y exceso\nde abastecimiento"),
        (23, 36, "Materia prima\nen mal estado"),
        (19, 28, "Mal manejo de\ninventarios")
    ]
    for x_diag, y_diag, texto in causas_materiales:
        ax.plot([x_diag, 2], [y_diag, y_diag], color=COLOR_CAUSAS, linewidth=2.5, alpha=0.9, solid_capstyle='round', zorder=2)
        ax.text(0.5, y_diag, texto,
                fontsize=10, color='#2C3E50',
                ha='left', va='center',
                bbox=dict(boxstyle="round,pad=0.35", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=1.5),
                zorder=4)

    # ============================================================
    # 5. ESPINA DIAGONAL INFERIOR - PERSONAS (de 50,50 a 35,20)
    # ============================================================
    ax.plot([50, 35], [50, 20], color=COLOR_PRINCIPAL_SUAVE, linewidth=4, solid_capstyle='round', zorder=3)

    ax.text(35, 17, 'PERSONAS',
            fontsize=13, fontweight='bold', color=COLOR_PRINCIPAL_SUAVE,
            ha='center', va='top',
            bbox=dict(boxstyle="round,pad=0.4", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=2.5),
            zorder=4)

    # Causas horizontales hacia la DERECHA
    causas_personas = [
        (47, 44, "Recepción y entregas\nfuera de tiempo"),
        (43, 34, "Ausencia de gestión\nde cadena de suministro"),
        (39, 26, "Entregas de productos\nfuera de tiempo")
    ]
    for x_diag, y_diag, texto in causas_personas:
        ax.plot([x_diag, 75], [y_diag, y_diag], color=COLOR_CAUSAS, linewidth=2.5, alpha=0.9, solid_capstyle='round', zorder=2)
        ax.text(76.5, y_diag, texto,
                fontsize=10, color='#2C3E50',
                ha='left', va='center',
                bbox=dict(boxstyle="round,pad=0.35", fc=COLOR_CAJA_FONDO, ec=COLOR_CAJA_BORDE, lw=1.5),
                zorder=4)

    # ============================================================
    # TÍTULO
    # ============================================================
    ax.text(50, 98, 'DIAGRAMA DE ISHIKAWA (CAUSA-EFECTO) — ESTRUCTURA 4M',
            fontsize=18, fontweight='bold', color=COLOR_PRINCIPAL,
            ha='center', va='top')

    # Leyenda
    legend_elements = [
        Line2D([0], [0], color=COLOR_PRINCIPAL_SUAVE, lw=5, label='Espina central y principales (4M)'),
        Line2D([0], [0], color=COLOR_CAUSAS, lw=2.5, alpha=0.9, label='Causas específicas'),
        mpatches.Patch(facecolor=COLOR_CAJA_FONDO, edgecolor=COLOR_CAJA_BORDE, linewidth=2, label='Cajas de texto')
    ]
    ax.legend(handles=legend_elements, loc='lower right',
              fontsize=11, framealpha=0.95, edgecolor='#E0E0E0',
              title="Leyenda", title_fontsize=12)

    plt.tight_layout()
    return fig


def generar_phva_donut(fase_seleccionada='Planificar'):
    """Gráfico Donut PHVA premium - etiquetas DENTRO, centro con texto, colores pastel"""
    fases = ['Planificar', 'Hacer', 'Verificar', 'Actuar']
    colores = ['#2E86C1', '#52BE80', '#F5B041', '#AF7AC5']
    valores = [1, 1, 1, 1]

    pull = [0.08 if f == fase_seleccionada else 0 for f in fases]

    fig = go.Figure(data=[go.Pie(
        labels=fases,
        values=valores,
        hole=0.6,
        marker=dict(
            colors=colores,
            line=dict(color='#FFFFFF', width=5)
        ),
        textinfo='label',
        textfont=dict(size=16, color='#FFFFFF', family='Arial Black'),
        hoverinfo='label+percent',
        pull=pull,
        direction='clockwise',
        sort=False,
        rotation=45,
        textposition='inside'
    )])

    fig.add_annotation(
        text="Ciclo de<br>Mejora<br>Continua",
        x=0.5, y=0.5,
        font=dict(size=22, color='#1F4E78', family='Arial Black'),
        showarrow=False,
        align='center',
        xanchor='center',
        yanchor='middle'
    )

    fig.update_layout(
        height=540,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.08,
            font=dict(size=13, family='Arial'),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#E0E0E0",
            borderwidth=1,
            itemsizing='constant'
        ),
        margin=dict(t=30, b=30, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def generar_kpi_barras():
    """Gráfico de barras agrupadas: Antes vs Después - estilo premium"""
    categorias = ['Productividad\n(unid/hora)', 'Producción Mensual\n(miles de pares)']
    antes = [11.8, 33.9]
    despues = [12.5, 36.0]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Antes (Situación Inicial)',
        x=categorias,
        y=antes,
        marker_color='#E74C3C',
        text=[f'{v:.1f}' for v in antes],
        textposition='outside',
        textfont=dict(size=14, color='#E74C3C', family='Arial Black'),
        width=0.35,
        offsetgroup=0
    ))

    fig.add_trace(go.Bar(
        name='Después (Post-Mejoras)',
        x=categorias,
        y=despues,
        marker_color='#52BE80',
        text=[f'{v:.1f}' for v in despues],
        textposition='outside',
        textfont=dict(size=14, color='#52BE80', family='Arial Black'),
        width=0.35,
        offsetgroup=1
    ))

    fig.update_layout(
        title=dict(
            text='<b>COMPARATIVO KPIs: ANTES vs DESPUÉS</b>',
            font=dict(size=16, color='#1F4E78', family='Arial'),
            x=0.5
        ),
        barmode='group',
        height=420,
        template='plotly_white',
        yaxis=dict(title='Valor', showgrid=True, gridcolor='#F0F0F0', zeroline=False),
        xaxis=dict(showgrid=False),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=11), bgcolor="rgba(255,255,255,0.9)", bordercolor="#E0E0E0", borderwidth=1
        ),
        margin=dict(t=60, b=60, l=50, r=30),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig


def generar_pareto(df_filtrado):
    """Gráfico de Pareto con estilo premium y transparent background"""
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Barras - Azul corporativo, valores encima
    fig.add_trace(
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

    # Línea acumulada - Rojo, puntos gruesos, valores encima
    fig.add_trace(
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

    # Línea del 80% - Punteada roja horizontal
    fig.add_hline(
        y=80, line_dash="dot", line_color="#C0392B", line_width=2.5,
        secondary_y=True
    )

    # Ejes
    fig.update_xaxes(
        tickangle=-30,
        tickfont=dict(size=10, family="Arial"),
        title_text="",
        showgrid=False
    )
    fig.update_yaxes(
        title_text="<b>Frecuencia</b>", secondary_y=False,
        showgrid=True, gridcolor="#F0F0F0",
        title_font=dict(size=12, color="#1F4E78"),
        rangemode="tozero"
    )
    fig.update_yaxes(
        title_text="<b>% Acumulado</b>", secondary_y=True,
        range=[0, 105], showgrid=False,
        title_font=dict(size=12, color="#C0392B"),
        tickfont=dict(size=10, color="#C0392B"),
        ticksuffix="%"
    )

    fig.update_layout(
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
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        title=dict(
            text="<b>Diagrama de Pareto - Causas de Baja Productividad</b>",
            font=dict(size=16, color="#1F4E78", family="Arial"),
            x=0.5,
            y=0.97
        )
    )

    return fig