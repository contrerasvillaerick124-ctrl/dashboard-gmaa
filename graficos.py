import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import plotly.graph_objects as go


def generar_ishikawa():
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # 1. Espina Central
    ax.annotate('', xy=(85, 50), xytext=(5, 50), arrowprops=dict(arrowstyle='->', color='black', lw=3))
    ax.text(86, 50, 'Baja\nproductividad', ha='left', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", fc="#f0f0f0", ec="black"))

    # 2. Definir las 4 Espinas (Coordenadas de inicio y fin)
    espinas = {
        'Mano de obra': {'start': (25, 50), 'end': (15, 85)},
        'Método':      {'start': (35, 50), 'end': (45, 85)},
        'Materia prima': {'start': (65, 50), 'end': (55, 15)},
        'Maquinaria':  {'start': (75, 50), 'end': (85, 15)}
    }

    for nombre, coords in espinas.items():
        ax.plot([coords['start'][0], coords['end'][0]], [coords['start'][1], coords['end'][1]], color='black', lw=2)
        # Caja del nombre de la categoría
        ax.text(coords['end'][0], coords['end'][1] + (3 if coords['end'][1] > 50 else -3), nombre, 
                ha='center', va='center', fontsize=12, fontweight='bold', 
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black"))

    # 3. Función para calcular la intersección y dibujar la causa
    def dibujar_causa(categoria, y_target, texto, lado='izq'):
        start = espinas[categoria]['start']
        end = espinas[categoria]['end']
        
        # Interpolación para encontrar el punto exacto (x, y) en la diagonal
        t = (y_target - start[1]) / (end[1] - start[1])
        x_interseccion = start[0] + t * (end[0] - start[0])
        
        # Dibujar la línea horizontal desde la intersección
        if lado == 'izq':
            x_texto = x_interseccion - 15
            ax.plot([x_texto, x_interseccion], [y_target, y_target], color='black', lw=1.5)
            ax.text(x_texto - 1, y_target, texto, ha='right', va='center', fontsize=10, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray"))
        else:
            x_texto = x_interseccion + 15
            ax.plot([x_interseccion, x_texto], [y_target, y_target], color='black', lw=1.5)
            ax.text(x_texto + 1, y_target, texto, ha='left', va='center', fontsize=10, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray"))

    # 4. Colocar las causas (Usando y_target para que se conecten solas)
    # Mano de obra
    dibujar_causa('Mano de obra', 75, 'Entregas de productos\nfuera de tiempo', 'izq')
    dibujar_causa('Mano de obra', 60, 'Falta de capacitaciones\na los trabajadores', 'izq')

    # Método
    dibujar_causa('Método', 75, 'Falta de una gestión de calidad,\ninspección y control en los productos', 'der')
    dibujar_causa('Método', 62, 'Falta de una optimización en\nla calidad y producción del producto', 'der')
    dibujar_causa('Método', 55, 'Falta de orden, limpieza y\nobstrucciones en las líneas de producción', 'der')

    # Materia prima
    dibujar_causa('Materia prima', 35, 'Materia prima de mala calidad', 'izq')
    dibujar_causa('Materia prima', 20, 'Desperdicios de M.P y acumulación\npara el abastecimiento en proceso', 'izq')

    # Maquinaria
    dibujar_causa('Maquinaria', 35, 'Fallas y paradas en\nla producción de calzados', 'der')
    dibujar_causa('Maquinaria', 20, 'Falta de mantenimiento en\nla fabricación del producto', 'der')

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