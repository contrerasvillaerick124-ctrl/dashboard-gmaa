import pandas as pd

KPIS = {
    "productividad_actual": 12.5,
    "productividad_anterior": 11.8,
    "produccion_actual": 35992.7,
    "produccion_anterior": 33937.5,
    "beneficio_mensual": 126827,
    "relacion_bc": 1.26
}

PARETO_CAUSAS = [
    "Falta de control y optimización en la producción",
    "Paradas en la producción y ciclos",
    "Falta de mantenimiento",
    "Falta de inspección y control",
    "Mermas y exceso de abastecimiento",
    "Recepción y entregas fuera de tiempo",
    "Materia prima en mal estado",
    "Ausencia de gestión de cadena de suministro",
    "Entregas de productos fuera de tiempo",
    "Falta de capacitaciones a los trabajadores"
]

PARETO_FRECUENCIAS = [16, 16, 14, 14, 12, 12, 12, 8, 8, 8]
PARETO_TOTAL = 120

PARETO_M_CATEGORIES = {
    "Métodos": [
        "Falta de control y optimización en la producción",
        "Falta de inspección y control",
        "Falta de capacitaciones a los trabajadores"
    ],
    "Máquinas": [
        "Paradas en la producción y ciclos",
        "Falta de mantenimiento"
    ],
    "Materiales": [
        "Mermas y exceso de abastecimiento",
        "Materia prima en mal estado"
    ],
    "Personas": [
        "Recepción y entregas fuera de tiempo",
        "Ausencia de gestión de cadena de suministro",
        "Entregas de productos fuera de tiempo"
    ]
}

def get_pareto_dataframe():
    df = pd.DataFrame({
        "Causa": PARETO_CAUSAS,
        "Frecuencia": PARETO_FRECUENCIAS
    })
    df["Porcentaje"] = (df["Frecuencia"] / PARETO_TOTAL * 100).round(2)
    df["Porcentaje_Acumulado"] = df["Porcentaje"].cumsum().round(2)
    df["Categoria_M"] = df["Causa"].apply(get_categoria_m)
    return df

def get_categoria_m(causa):
    for categoria, causas in PARETO_M_CATEGORIES.items():
        if causa in causas:
            return categoria
    return "Sin categoría"

ISHikawa_DATA = {
    "Métodos": [
        "Falta de control",
        "Falta de inspección",
        "Falta de capacitación"
    ],
    "Máquinas": [
        "Paradas de producción",
        "Falta de mantenimiento"
    ],
    "Materiales": [
        "Mermas",
        "Materia prima en mal estado"
    ],
    "Personas": [
        "Recepción tardía",
        "Falta de gestión de suministro",
        "Entregas tardías"
    ]
}

PHVA_DETALLADO = {
    "Planificar (P)": {
        "texto": (
            "**Diagnóstico y Estrategia.** "
            "Se definió implementar el sistema de gestión de calidad NTP ISO 9001:2015, "
            "capacitar al personal en control de calidad y establecer políticas para reducir los defectos "
            "desde la recepción de materia prima."
        ),
        "color": "#2E86C1",
        "icon": "📋"
    },
    "Hacer (D)": {
        "texto": (
            "**Ejecución de Mejoras.** "
            "Se implementó la metodología 5S en el área de producción, "
            "se rediseñó el DOP (7 operaciones + 3 inspecciones) y se mejoró el proceso de diseño y corte "
            "para evitar paradas de máquina."
        ),
        "color": "#52BE80",
        "icon": "⚙️"
    },
    "Verificar (V)": {
        "texto": (
            "**Medición de Resultados.** "
            "Se compararon los indicadores y se comprobó que la productividad subió de 11.8 a 12.5 unid/hora. "
            "La producción mensual se incrementó en 2,179.7 pares, generando un beneficio de S/ 126,827."
        ),
        "color": "#F5B041",
        "icon": "📊"
    },
    "Actuar (A)": {
        "texto": (
            "**Estandarización y Sostenibilidad.** "
            "Se documentaron los nuevos procesos en el Sistema de Gestión de Calidad (SGC) y se estableció "
            "la capacitación continua para que las mejoras no se pierdan con el tiempo (mejora continua)."
        ),
        "color": "#AF7AC5",
        "icon": "🔄"
    }
}

PHVA_PHASES = list(PHVA_DETALLADO.keys())
PHVA_COLORS = [PHVA_DETALLADO[p]["color"] for p in PHVA_PHASES]
PHVA_VALUES = [1, 1, 1, 1]

PHVA_TEXTOS = {
    "Planificar (P)": "Planificar (P): Acción: Capacitación e ISO 9001. Meta: Reducir defectos.",
    "Hacer (D)": "Hacer (D): Acción: 5S y mejora del DOP. Meta: Evitar paradas de máquina.",
    "Verificar (V)": "Verificar (V): Acción: Medición de indicadores. Resultado: Productividad subió de 11.8 a 12.5.",
    "Actuar (A)": "Actuar (A): Acción: Estandarización. Resultado: Beneficio de S/ 126,827 (B/C 1.26)."
}