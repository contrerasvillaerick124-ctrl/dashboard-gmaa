import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import plotly.graph_objects as go


def generar_ishikawa():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')

    # Espina central
    ax.annotate('', xy=(85, 50), xytext=(5, 50),
                arrowprops=dict(arrowstyle='->', color='black', lw=4, mutation_scale=30))

    # Recuadro problema en la punta
    ax.text(85, 50, 'Baja productividad',
            fontsize=11, fontweight='bold', color='white',
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#D3D3D3', edgecolor='none'))

    # Espinas diagonales y cajas de categoría
    espinas = [
        {'cat': 'Método', 'start': (30, 50), 'end': (20, 85)},
        {'cat': 'Mano de obra', 'start': (30, 50), 'end': (10, 85)},
        {'cat': 'Maquinaria', 'start': (50, 50), 'end': (40, 15)},
        {'cat': 'Materia prima', 'start': (50, 50), 'end': (20, 15)}
    ]

    for espina in espinas:
        sx, sy = espina['start']
        ex, ey = espina['end']
        ax.plot([sx, ex], [sy, ey], color='black', linewidth=2.5, solid_capstyle='round')
        ax.text(ex, ey, espina['cat'],
                fontsize=10, fontweight='bold', color='black',
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black', linewidth=1))

    # Causas horizontales (línea + texto)
    causas = [
        # Método (espina de 30,50 a 20,85) - causas hacia la izquierda
        (75, "Falta de una gestión de calidad, inspección y control en los productos terminados", 'Método'),
        (65, "Falta de una optimización en la calidad y producción del producto", 'Método'),
        (55, "Falta de orden, limpieza y obstrucciones en las líneas de producción", 'Método'),
        # Mano de obra (espina de 30,50 a 10,85)
        (75, "Entregas de productos fuera de tiempo", 'Mano de obra'),
        (65, "Falta de capacitaciones a los trabajadores", 'Mano de obra'),
        # Maquinaria (espina de 50,50 a 40,15)
        (35, "Fallas y paradas en la producción de calzados", 'Maquinaria'),
        (25, "Falta de mantenimiento en la fabricación del producto", 'Maquinaria'),
        # Materia prima (espina de 50,50 a 20,15)
        (35, "Materia prima de mala calidad", 'Materia prima'),
        (25, "Desperdicios de M.P y acumulación para el abastecimiento en proceso", 'Materia prima')
    ]

    # Coordenadas de inicio en cada espina para las causas horizontales
    # Método: espina va de (30,50) a (20,85). Puntos a lo largo de la diagonal
    # Mano de obra: espina va de (30,50) a (10,85)
    # Maquinaria: espina va de (50,50) a (40,15)
    # Materia prima: espina va de (50,50) a (20,15)

    # Para cada causa, calcular punto en la espina y dibujar línea horizontal
    espina_points = {
        'Método': {
            75: (23, 72.5),
            65: (24, 67.5),
            55: (25, 62.5)
        },
        'Mano de obra': {
            75: (13, 77.5),
            65: (12, 72.5)
        },
        'Maquinaria': {
            35: (43, 37.5),
            25: (41, 27.5)
        },
        'Materia prima': {
            35: (23, 32.5),
            25: (22, 22.5)
        }
    }

    for y_causa, texto, categoria in causas:
        cx, cy = espina_points[categoria][y_causa]
        # Línea horizontal hacia la izquierda
        ax.plot([cx - 15, cx], [cy, cy], color='black', linewidth=2, solid_capstyle='round')
        # Texto a la izquierda de la línea
        ax.text(cx - 16, cy, texto,
                fontsize=8, color='black',
                ha='right', va='center',
                bbox=dict(boxstyle="round,pad=0.25", facecolor='white', edgecolor='black', linewidth=0.5))

    plt.tight_layout()
    return fig


def generar_phva_donut(fase_seleccionada='Planificar'):
    fases = ['Planificar', 'Hacer', 'Verificar', 'Actuar']
    colores = ['#1F4E78', '#70AD47', '#ED7D31', '#7030A0']
    valores = [1, 1, 1, 1]

    pull = [0.08 if f == fase_seleccionada else 0 for f in fases]

    fig = go.Figure(data=[go.Pie(
        labels=fases,
        values=valores,
        hole=0.6,
        marker=dict(colors=colores, line=dict(color='#FFFFFF', width=3)),
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
        font=dict(size=20, color='#1F4E78', family='Arial Black'),
        showarrow=False, align='center', xanchor='center', yanchor='middle'
    )

    fig.update_layout(
        height=520,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5,
                    xanchor="left", x=1.08,
                    font=dict(size=13, family='Arial'),
                    bgcolor="rgba(255,255,255,0.95)",
                    bordercolor="#E0E0E0", borderwidth=1),
        margin=dict(t=30, b=30, l=30, r=30),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF"
    )

    return fig


def generar_kpi_barras():
    categorias = ['Productividad\n(unid/hora)', 'Producción Mensual\n(miles de pares)']
    antes = [11.8, 33.9]
    despues = [12.5, 36.0]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Antes (Situación Inicial)',
        x=categorias, y=antes,
        marker_color='#E74C3C',
        text=[f'{v:.1f}' for v in antes],
        textposition='outside',
        textfont=dict(size=14, color='#E74C3C', family='Arial Black'),
        width=0.35, offsetgroup=0
    ))

    fig.add_trace(go.Bar(
        name='Después (Post-Mejoras)',
        x=categorias, y=despues,
        marker_color='#52BE80',
        text=[f'{v:.1f}' for v in despues],
        textposition='outside',
        textfont=dict(size=14, color='#52BE80', family='Arial Black'),
        width=0.35, offsetgroup=1
    ))

    fig.update_layout(
        title=dict(text='<b>COMPARATIVO KPIs: ANTES vs DESPUÉS</b>',
                   font=dict(size=16, color='#1F4E78', family='Arial'), x=0.5),
        barmode='group', height=420, template='plotly_white',
        yaxis=dict(title='Valor', showgrid=True, gridcolor='#F0F0F0', zeroline=False),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=11),
                    bgcolor="rgba(255,255,255,0.9)", bordercolor="#E0E0E0", borderwidth=1),
        margin=dict(t=60, b=60, l=50, r=30),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF"
    )

    return fig


def generar_pareto(df_filtrado):
    from plotly.subplots import make_subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df_filtrado["Causa"], y=df_filtrado["Frecuencia"],
            name="Frecuencia", marker_color="#1F4E78",
            text=df_filtrado["Frecuencia"], textposition="outside",
            textfont=dict(size=12, color="#1F4E78", family="Arial Black"),
            width=0.55,
            hovertemplate="<b>%{x}</b><br>Frecuencia: %{y}<br>%{customdata:.1f}%<extra></extra>",
            customdata=df_filtrado["Porcentaje"]
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df_filtrado["Causa"], y=df_filtrado["Porcentaje_Acumulado"],
            name="% Acumulado", mode="lines+markers+text",
            line=dict(color="#C0392B", width=3),
            marker=dict(size=10, color="#C0392B", symbol="circle", line=dict(width=2, color="#FFFFFF")),
            text=df_filtrado["Porcentaje_Acumulado"].apply(lambda x: f"{x:.1f}%"),
            textposition="top center",
            textfont=dict(size=11, color="#C0392B", family="Arial Black"),
            hovertemplate="<b>%{x}</b><br>% Acumulado: %{y:.1f}%<extra></extra>"
        ),
        secondary_y=True
    )

    fig.add_hline(y=80, line_dash="dot", line_color="#C0392B", line_width=2.5, secondary_y=True)

    fig.update_xaxes(tickangle=-30, tickfont=dict(size=10, family="Arial"),
                     title_text="", showgrid=False)
    fig.update_yaxes(title_text="<b>Frecuencia</b>", secondary_y=False,
                     showgrid=True, gridcolor="#F0F0F0",
                     title_font=dict(size=12, color="#1F4E78"), rangemode="tozero")
    fig.update_yaxes(title_text="<b>% Acumulado</b>", secondary_y=True,
                     range=[0, 105], showgrid=False,
                     title_font=dict(size=12, color="#C0392B"),
                     tickfont=dict(size=10, color="#C0392B"), ticksuffix="%")

    fig.update_layout(
        height=540, template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=11, family="Arial"),
                    bgcolor="rgba(255,255,255,0.95)", bordercolor="#E0E0E0", borderwidth=1),
        margin=dict(t=50, b=150, l=60, r=60),
        plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        hovermode="x unified",
        title=dict(text="<b>Diagrama de Pareto - Causas de Baja Productividad</b>",
                   font=dict(size=16, color="#1F4E78", family="Arial"), x=0.5, y=0.97)
    )

    return fig