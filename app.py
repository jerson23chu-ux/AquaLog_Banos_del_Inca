import streamlit as st
import pandas as pd
import math
import os
from datetime import date, datetime
from io import BytesIO


# ============================================================
# IMPORTACIÓN SEGURA DE REPORTLAB
# ============================================================

REPORTLAB_DISPONIBLE = True

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle
    )

except ModuleNotFoundError:
    REPORTLAB_DISPONIBLE = False


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="AquaLog BI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

ARCHIVO_DATOS = "hogares.csv"

TIPOS_USO = [
    "Doméstico",
    "Comercial",
    "Educativo",
    "Institucional",
    "Riego",
    "Otro"
]

COLUMNAS = [
    "Código",
    "Fecha",
    "Sector / comunidad",
    "Zona / referencia",
    "Tipo de uso",
    "Personas",
    "Consumo del periodo (m³)",
    "Días",
    "Tarifa (S/ por m³)",
    "Consumo diario (m³)",
    "Consumo por persona (L/día)",
    "Índice logarítmico",
    "Nivel",
    "Costo del periodo (S/)",
    "Observaciones"
]


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 8%,
                rgba(0,174,239,0.10),
                transparent 22%
            ),
            radial-gradient(
                circle at 90% 12%,
                rgba(0,87,230,0.08),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #f6fcff 0%,
                #edf8ff 52%,
                #ffffff 100%
            );
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.3rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #0b4f7c !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #294e62;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #043b8f 0%,
                #0875d1 52%,
                #00a6c9 100%
            );
        border-right:
            1px solid rgba(255,255,255,0.14);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: white !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label p {
        color: white !important;
        font-weight: 650;
    }

    input,
    textarea {
        color: #102f40 !important;
        background-color: white !important;
    }

    [data-baseweb="input"] {
        background-color: white !important;
    }

    [data-baseweb="input"] input {
        color: #102f40 !important;
    }

    [data-baseweb="textarea"] {
        background-color: white !important;
    }

    [data-baseweb="textarea"] textarea {
        color: #102f40 !important;
    }

    [data-baseweb="select"] > div {
        background-color: white !important;
        color: #102f40 !important;
    }

    [data-baseweb="select"] span {
        color: #102f40 !important;
    }

    [role="option"] {
        color: #102f40 !important;
        background-color: white !important;
    }

    [role="option"]:hover {
        background-color: #e8f6ff !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #234b61 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.97);
        border: 1px solid rgba(0,100,160,0.11);
        padding: 16px 17px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,70,120,0.07);
    }

    [data-testid="stMetricValue"] {
        color: #0869ce !important;
        font-weight: 850;
    }

    [data-testid="stMetricLabel"] {
        color: #45677d !important;
        font-weight: 700;
    }

    .hero {
        background:
            linear-gradient(
                120deg,
                #043a91 0%,
                #0875d1 50%,
                #12b7dc 100%
            );
        border-radius: 28px;
        padding: 30px 34px;
        margin-bottom: 24px;
        box-shadow:
            0 18px 45px
            rgba(8,92,160,0.22);
        color: white;
    }

    .hero-title {
        font-size: 45px;
        font-weight: 900;
        line-height: 1.05;
        margin-bottom: 8px;
        color: white !important;
    }

    .hero-subtitle {
        font-size: 20px;
        font-weight: 700;
        color: white !important;
        margin-bottom: 9px;
    }

    .hero-text {
        max-width: 950px;
        line-height: 1.6;
        font-size: 15px;
        color: #effcff !important;
    }

    .chip {
        display: inline-block;
        margin: 11px 7px 0 0;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.24);
        color: white !important;
        font-size: 12px;
        font-weight: 700;
    }

    .card {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(0,100,160,0.11);
        border-radius: 18px;
        padding: 18px 20px;
        margin: 8px 0 14px 0;
        box-shadow:
            0 8px 23px
            rgba(0,70,120,0.06);
        color: #294e62 !important;
    }

    .card h3 {
        color: #07527f !important;
    }

    .card p {
        color: #294e62 !important;
    }

    .alert-red {
        background: #fff4f4;
        color: #71272d !important;
        border-left: 6px solid #dc3545;
        padding: 14px 17px;
        border-radius: 13px;
        margin-bottom: 9px;
    }

    .alert-green {
        background: #f0fff7;
        color: #155c3a !important;
        border-left: 6px solid #18a568;
        padding: 14px 17px;
        border-radius: 13px;
        margin-bottom: 9px;
    }

    .alert-yellow {
        background: #fffbea;
        color: #6f5810 !important;
        border-left: 6px solid #e5ad17;
        padding: 14px 17px;
        border-radius: 13px;
        margin-bottom: 9px;
    }

    .tip {
        background: white;
        color: #294e62 !important;
        border-left: 6px solid #0b8fe3;
        border-radius: 14px;
        padding: 15px 18px;
        margin: 9px 0;
        box-shadow: 0 5px 16px rgba(0,0,0,0.05);
    }

    .footer {
        text-align: center;
        color: #557286 !important;
        padding: 18px 0 5px 0;
        font-size: 13px;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 12px;
        font-weight: 750;
    }

    button[data-baseweb="tab"] {
        color: #184c68 !important;
        font-weight: 700 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# COMPONENTES VISUALES
# ============================================================

def hero():

    st.markdown(
        '<div class="hero">'
        '<div class="hero-title">💧 AquaLog BI</div>'
        '<div class="hero-subtitle">Inteligencia matemática para la gestión eficiente del agua</div>'
        '<div class="hero-text">'
        'Registra, analiza, compara y proyecta el consumo de agua mediante indicadores matemáticos, '
        'seguimiento histórico, alertas y escenarios de ahorro.'
        '</div>'
        '<span class="chip">📊 Analítica</span>'
        '<span class="chip">🧮 Modelo matemático</span>'
        '<span class="chip">🚨 Alertas</span>'
        '<span class="chip">🎯 Simulación</span>'
        '<span class="chip">📈 Seguimiento</span>'
        '</div>',
        unsafe_allow_html=True
    )


def card(titulo, texto, icono="💧"):

    st.markdown(
        f'<div class="card">'
        f'<h3>{icono} {titulo}</h3>'
        f'<p>{texto}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def alerta_html(tipo, titulo, texto):

    clase = {
        "rojo": "alert-red",
        "verde": "alert-green",
        "amarillo": "alert-yellow"
    }.get(tipo, "alert-yellow")

    st.markdown(
        f'<div class="{clase}">'
        f'<strong>{titulo}</strong><br>'
        f'{texto}'
        f'</div>',
        unsafe_allow_html=True
    )


def tip(titulo, texto):

    st.markdown(
        f'<div class="tip">'
        f'<strong>{titulo}</strong><br>'
        f'{texto}'
        f'</div>',
        unsafe_allow_html=True
    )


# ============================================================
# BASE DE DATOS
# ============================================================

def dataframe_vacio():

    return pd.DataFrame(columns=COLUMNAS)


def normalizar_df(df):

    if df is None or df.empty:
        return dataframe_vacio()

    df = df.copy()

    equivalencias = {
        "Hogar": "Código",
        "Sector": "Sector / comunidad",
        "CAS": "Zona / referencia",
        "Habitantes": "Personas",
        "Consumo mensual (m³)": "Consumo del periodo (m³)",
        "Costo mensual (S/)": "Costo del periodo (S/)"
    }

    for antigua, nueva in equivalencias.items():
        if antigua in df.columns and nueva not in df.columns:
            df[nueva] = df[antigua]

    defaults = {
        "Código": "",
        "Fecha": date.today().strftime("%Y-%m-%d"),
        "Sector / comunidad": "",
        "Zona / referencia": "",
        "Tipo de uso": "Doméstico",
        "Personas": 1,
        "Consumo del periodo (m³)": 0.0,
        "Días": 30,
        "Tarifa (S/ por m³)": 0.0,
        "Consumo diario (m³)": 0.0,
        "Consumo por persona (L/día)": 0.0,
        "Índice logarítmico": 0.0,
        "Nivel": "SIN CLASIFICAR",
        "Costo del periodo (S/)": 0.0,
        "Observaciones": ""
    }

    for columna, valor in defaults.items():
        if columna not in df.columns:
            df[columna] = valor

    numericas = [
        "Personas",
        "Consumo del periodo (m³)",
        "Días",
        "Tarifa (S/ por m³)",
        "Consumo diario (m³)",
        "Consumo por persona (L/día)",
        "Índice logarítmico",
        "Costo del periodo (S/)"
    ]

    for col in numericas:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    df["Personas"] = (
        df["Personas"]
        .replace(0, 1)
        .astype(int)
    )

    df["Días"] = (
        df["Días"]
        .replace(0, 30)
        .astype(int)
    )

    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        errors="coerce"
    )

    df["Fecha"] = df["Fecha"].fillna(
        pd.Timestamp.today()
    )

    df["Fecha"] = df["Fecha"].dt.strftime(
        "%Y-%m-%d"
    )

    return df[COLUMNAS]


def cargar_datos():

    if not os.path.exists(ARCHIVO_DATOS):
        return dataframe_vacio()

    try:
        return normalizar_df(
            pd.read_csv(ARCHIVO_DATOS)
        )

    except Exception:
        return dataframe_vacio()


def guardar_datos(df):

    df = normalizar_df(df)

    df.to_csv(
        ARCHIVO_DATOS,
        index=False,
        encoding="utf-8-sig"
    )


# ============================================================
# MOTOR MATEMÁTICO
# ============================================================

def analizar_consumo(
    personas,
    consumo,
    dias,
    tipo_uso,
    tarifa
):

    personas = max(int(personas), 1)
    dias = max(int(dias), 1)

    consumo_diario = consumo / dias

    cp = consumo / (
        personas * dias
    )

    litros_persona_dia = (
        cp * 1000
    )

    indice_log = math.log10(
        1 + cp
    )

    costo = (
        consumo * tarifa
    )

    if tipo_uso == "Doméstico":

        if litros_persona_dia < 100:
            nivel = "BAJO"

        elif litros_persona_dia <= 170:
            nivel = "MODERADO"

        else:
            nivel = "ALTO"

    else:
        nivel = "ANÁLISIS GENERAL"

    return {
        "consumo_diario": consumo_diario,
        "cp": cp,
        "litros_persona_dia": litros_persona_dia,
        "indice_log": indice_log,
        "nivel": nivel,
        "costo": costo
    }


# ============================================================
# HISTORIAL
# ============================================================

def historial_codigo(df, codigo):

    temporal = df[
        df["Código"].astype(str) ==
        str(codigo)
    ].copy()

    temporal["Fecha_dt"] = pd.to_datetime(
        temporal["Fecha"],
        errors="coerce"
    )

    return temporal.sort_values(
        "Fecha_dt"
    )


def variacion_ultimo_periodo(historial):

    if len(historial) < 2:
        return None

    actual = float(
        historial[
            "Consumo del periodo (m³)"
        ].iloc[-1]
    )

    anterior = float(
        historial[
            "Consumo del periodo (m³)"
        ].iloc[-2]
    )

    if anterior == 0:
        return None

    return (
        (actual - anterior) /
        anterior
    ) * 100


def tendencia_consumo(historial):

    if len(historial) < 3:
        return "SIN DATOS SUFICIENTES"

    ultimos = (
        historial[
            "Consumo del periodo (m³)"
        ]
        .tail(3)
        .tolist()
    )

    if (
        ultimos[0] <
        ultimos[1] <
        ultimos[2]
    ):
        return "CRECIENTE"

    if (
        ultimos[0] >
        ultimos[1] >
        ultimos[2]
    ):
        return "DECRECIENTE"

    return "VARIABLE"


# ============================================================
# ALERTAS
# ============================================================

def generar_alertas(df):

    alertas = []

    if df.empty:
        return alertas

    codigos = (
        df["Código"]
        .astype(str)
        .unique()
    )

    for codigo in codigos:

        hist = historial_codigo(
            df,
            codigo
        )

        if len(hist) < 2:
            continue

        variacion = variacion_ultimo_periodo(
            hist
        )

        if variacion is None:
            continue

        if variacion >= 20:

            alertas.append(
                {
                    "tipo": "rojo",
                    "titulo": f"🔴 Aumento importante — {codigo}",
                    "texto":
                        f"El consumo aumentó "
                        f"{variacion:.1f}% respecto "
                        f"al periodo anterior."
                }
            )

        elif variacion <= -10:

            alertas.append(
                {
                    "tipo": "verde",
                    "titulo": f"🟢 Reducción detectada — {codigo}",
                    "texto":
                        f"El consumo disminuyó "
                        f"{abs(variacion):.1f}% respecto "
                        f"al periodo anterior."
                }
            )

        tendencia = tendencia_consumo(
            hist
        )

        if tendencia == "CRECIENTE":

            alertas.append(
                {
                    "tipo": "amarillo",
                    "titulo": f"🟡 Tendencia creciente — {codigo}",
                    "texto":
                        "Los tres últimos registros "
                        "muestran incrementos consecutivos."
                }
            )

    return alertas


# ============================================================
# RECOMENDACIONES
# ============================================================

def obtener_recomendaciones(
    tipo_uso,
    nivel=None
):

    recomendaciones = {

        "Doméstico": [
            (
                "🚰 Control de caños",
                "Evita mantener los caños abiertos cuando el agua no sea necesaria."
            ),
            (
                "🚿 Duchas más eficientes",
                "Reducir algunos minutos de ducha puede disminuir el consumo acumulado."
            ),
            (
                "🔧 Revisión de fugas",
                "Inspecciona conexiones, inodoros, tanques y grifos."
            ),
            (
                "📊 Seguimiento",
                "Compara cada nuevo registro con el periodo anterior."
            )
        ],

        "Comercial": [
            (
                "📋 Control por actividad",
                "Identifica cuáles actividades concentran el mayor consumo."
            ),
            (
                "🔧 Mantenimiento",
                "Revisa instalaciones y equipos que utilizan agua."
            ),
            (
                "🎯 Metas de ahorro",
                "Establece reducciones graduales y compara resultados."
            )
        ],

        "Educativo": [
            (
                "🏫 Sensibilización",
                "Promueve hábitos responsables entre estudiantes y trabajadores."
            ),
            (
                "🚰 Servicios higiénicos",
                "Controla fugas y consumos innecesarios."
            ),
            (
                "📈 Seguimiento periódico",
                "Analiza la evolución del consumo de cada periodo."
            )
        ],

        "Institucional": [
            (
                "📊 Indicadores",
                "Compara consumo entre periodos y áreas."
            ),
            (
                "🔧 Mantenimiento preventivo",
                "Programa inspecciones de conexiones e instalaciones."
            ),
            (
                "🎯 Objetivos de reducción",
                "Define metas de consumo medibles."
            )
        ],

        "Riego": [
            (
                "🌅 Horario",
                "Realiza el riego en horarios de menor evaporación."
            ),
            (
                "💧 Dosificación",
                "Evita aplicar más agua de la necesaria."
            ),
            (
                "🔍 Inspección",
                "Revisa mangueras, uniones y sistemas de distribución."
            )
        ],

        "Otro": [
            (
                "📊 Medición",
                "Registra el consumo periódicamente."
            ),
            (
                "🔍 Identificación de pérdidas",
                "Revisa posibles usos innecesarios o fugas."
            ),
            (
                "🎯 Proyección",
                "Utiliza el simulador para establecer metas de reducción."
            )
        ]
    }

    lista = list(
        recomendaciones.get(
            tipo_uso,
            recomendaciones["Otro"]
        )
    )

    if (
        tipo_uso == "Doméstico"
        and
        nivel == "ALTO"
    ):

        lista.insert(
            0,
            (
                "🚨 Atención prioritaria",
                "El valor calculado se encuentra en el nivel alto "
                "según los criterios referenciales del prototipo."
            )
        )

    return lista


# ============================================================
# PDF
# ============================================================

def crear_pdf(
    fila,
    historial
):

    if not REPORTLAB_DISPONIBLE:
        return None

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloAqua",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#075A8F"),
        spaceAfter=8
    )

    subtitulo = ParagraphStyle(
        "SubtituloAqua",
        parent=estilos["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4A6B7C"),
        spaceAfter=18
    )

    seccion = ParagraphStyle(
        "SeccionAqua",
        parent=estilos["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#075A8F"),
        spaceBefore=10,
        spaceAfter=8
    )

    texto = ParagraphStyle(
        "TextoAqua",
        parent=estilos["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#273F4B")
    )

    elementos = []

    elementos.append(
        Paragraph(
            "AquaLog BI",
            titulo
        )
    )

    elementos.append(
        Paragraph(
            "Reporte de análisis del consumo de agua",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            "Inteligencia matemática para la gestión eficiente del agua",
            subtitulo
        )
    )

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Paragraph(
            "1. Identificación",
            seccion
        )
    )

    tabla_identificacion = [
        ["Código", str(fila["Código"])],
        ["Fecha", str(fila["Fecha"])],
        ["Sector / comunidad", str(fila["Sector / comunidad"])],
        ["Zona / referencia", str(fila["Zona / referencia"])],
        ["Tipo de uso", str(fila["Tipo de uso"])]
    ]

    tabla = Table(
        tabla_identificacion,
        colWidths=[150, 340]
    )

    tabla.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF7FD")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#C8DFEA")
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    elementos.append(tabla)

    elementos.append(
        Spacer(1, 14)
    )

    elementos.append(
        Paragraph(
            "2. Datos registrados",
            seccion
        )
    )

    datos_registrados = [
        [
            "Personas o unidades de referencia",
            str(fila["Personas"])
        ],
        [
            "Consumo del periodo",
            f'{fila["Consumo del periodo (m³)"]:.2f} m³'
        ],
        [
            "Duración del periodo",
            f'{fila["Días"]} días'
        ],
        [
            "Tarifa",
            f'S/ {fila["Tarifa (S/ por m³)"]:.2f} por m³'
        ]
    ]

    tabla2 = Table(
        datos_registrados,
        colWidths=[220, 270]
    )

    tabla2.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#F1F8FB")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#C8DFEA")
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    elementos.append(
        tabla2
    )

    elementos.append(
        Paragraph(
            "3. Resultados matemáticos",
            seccion
        )
    )

    resultados = [
        [
            "Consumo diario",
            f'{fila["Consumo diario (m³)"]:.4f} m³/día'
        ],
        [
            "Consumo individual de referencia",
            f'{fila["Consumo por persona (L/día)"]:.2f} L/día'
        ],
        [
            "Índice logarítmico",
            f'{fila["Índice logarítmico"]:.6f}'
        ],
        [
            "Nivel",
            str(fila["Nivel"])
        ],
        [
            "Costo estimado",
            f'S/ {fila["Costo del periodo (S/)"]:.2f}'
        ]
    ]

    tabla3 = Table(
        resultados,
        colWidths=[220, 270]
    )

    tabla3.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF7FD")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#C8DFEA")
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    elementos.append(
        tabla3
    )

    elementos.append(
        Paragraph(
            "4. Modelo matemático",
            seccion
        )
    )

    elementos.append(
        Paragraph(
            "Consumo unitario diario: Cₚ = V / (P × D)",
            texto
        )
    )

    elementos.append(
        Spacer(1, 5)
    )

    elementos.append(
        Paragraph(
            "Índice logarítmico: Iₗ = log10(1 + Cₚ)",
            texto
        )
    )

    variacion = variacion_ultimo_periodo(
        historial
    )

    tendencia = tendencia_consumo(
        historial
    )

    elementos.append(
        Paragraph(
            "5. Análisis histórico",
            seccion
        )
    )

    if variacion is None:

        analisis = (
            "No existen registros suficientes "
            "para comparar periodos."
        )

    elif variacion > 0:

        analisis = (
            f"El consumo aumentó "
            f"{variacion:.2f}% respecto "
            f"al periodo anterior."
        )

    elif variacion < 0:

        analisis = (
            f"El consumo disminuyó "
            f"{abs(variacion):.2f}% respecto "
            f"al periodo anterior."
        )

    else:

        analisis = (
            "El consumo no presentó variación."
        )

    elementos.append(
        Paragraph(
            analisis,
            texto
        )
    )

    elementos.append(
        Spacer(1, 7)
    )

    elementos.append(
        Paragraph(
            f"Tendencia reciente: <b>{tendencia}</b>",
            texto
        )
    )

    elementos.append(
        Paragraph(
            "6. Recomendaciones",
            seccion
        )
    )

    recomendaciones = obtener_recomendaciones(
        fila["Tipo de uso"],
        fila["Nivel"]
    )

    for titulo_rec, texto_rec in recomendaciones:

        elementos.append(
            Paragraph(
                f"<b>{titulo_rec}</b>: {texto_rec}",
                texto
            )
        )

        elementos.append(
            Spacer(1, 5)
        )

    elementos.append(
        Spacer(1, 20)
    )

    elementos.append(
        Paragraph(
            "AquaLog BI · Baños del Inca · Cajamarca · 2026",
            subtitulo
        )
    )

    documento.build(
        elementos
    )

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# ESTADO
# ============================================================

if "df" not in st.session_state:

    st.session_state.df = cargar_datos()

df = normalizar_df(
    st.session_state.df
)


# ============================================================
# MENÚ
# ============================================================

with st.sidebar:

    st.title("💧 AquaLog BI")

    st.caption(
        "Gestión inteligente del agua"
    )

    st.divider()

    opcion = st.radio(
        "MENÚ PRINCIPAL",
        [
            "🏠 Centro de control",
            "➕ Nuevo registro",
            "👤 Ficha individual",
            "🔎 Explorador",
            "🎯 Simulador",
            "📈 Análisis",
            "🚨 Alertas",
            "💡 Recomendaciones",
            "🧮 Motor matemático",
            "📄 Reportes PDF",
            "ℹ️ Proyecto"
        ]
    )

    st.divider()

    st.caption(
        "Sistema adaptable a distintos "
        "sectores, comunidades y tipos de uso."
    )


hero()


# ============================================================
# CENTRO DE CONTROL
# ============================================================

if opcion == "🏠 Centro de control":

    st.title(
        "Centro de control"
    )

    if df.empty:

        card(
            "AquaLog BI está listo",
            "Aún no existen registros. "
            "Ingresa el primer consumo desde "
            "<b>Nuevo registro</b>.",
            "🚀"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            card(
                "Medir",
                "Registra el consumo.",
                "💧"
            )

        with c2:
            card(
                "Analizar",
                "Obtén indicadores.",
                "🧮"
            )

        with c3:
            card(
                "Comparar",
                "Observa cambios históricos.",
                "📈"
            )

        with c4:
            card(
                "Decidir",
                "Simula y proyecta mejoras.",
                "🎯"
            )

    else:

        total_consumo = df[
            "Consumo del periodo (m³)"
        ].sum()

        promedio = df[
            "Consumo del periodo (m³)"
        ].mean()

        codigos = df[
            "Código"
        ].nunique()

        costo_total = df[
            "Costo del periodo (S/)"
        ].sum()

        alertas = generar_alertas(
            df
        )

        incrementos = sum(
            1
            for alerta in alertas
            if alerta["tipo"] == "rojo"
        )

        reducciones = sum(
            1
            for alerta in alertas
            if alerta["tipo"] == "verde"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "💧 Consumo acumulado",
            f"{total_consumo:.2f} m³"
        )

        c2.metric(
            "📊 Promedio por registro",
            f"{promedio:.2f} m³"
        )

        c3.metric(
            "🆔 Puntos registrados",
            codigos
        )

        c4.metric(
            "💰 Costo acumulado",
            f"S/ {costo_total:.2f}"
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "📈 Aumentos importantes",
            incrementos
        )

        c2.metric(
            "📉 Reducciones detectadas",
            reducciones
        )

        st.subheader(
            "🚨 Centro de alertas"
        )

        if not alertas:

            st.success(
                "No se detectaron alertas "
                "comparativas relevantes."
            )

        else:

            for alerta in alertas[:8]:

                alerta_html(
                    alerta["tipo"],
                    alerta["titulo"],
                    alerta["texto"]
                )

        st.subheader(
            "📊 Consumo por tipo de uso"
        )

        resumen_tipo = (
            df.groupby(
                "Tipo de uso"
            )[
                "Consumo del periodo (m³)"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            resumen_tipo
        )

        st.subheader(
            "📍 Consumo por sector o comunidad"
        )

        temp_sector = df.copy()

        temp_sector[
            "Sector / comunidad"
        ] = (
            temp_sector[
                "Sector / comunidad"
            ]
            .replace(
                "",
                "Sin especificar"
            )
        )

        resumen_sector = (
            temp_sector.groupby(
                "Sector / comunidad"
            )[
                "Consumo del periodo (m³)"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(12)
        )

        st.bar_chart(
            resumen_sector
        )

        st.subheader(
            "🏆 Mayores consumos"
        )

        top = (
            df.sort_values(
                "Consumo del periodo (m³)",
                ascending=False
            )
            [
                [
                    "Código",
                    "Fecha",
                    "Sector / comunidad",
                    "Tipo de uso",
                    "Consumo del periodo (m³)",
                    "Nivel"
                ]
            ]
            .head(10)
        )

        st.dataframe(
            top,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# NUEVO REGISTRO
# ============================================================

elif opcion == "➕ Nuevo registro":

    st.title(
        "Nuevo registro"
    )

    st.caption(
        "Los registros pueden repetirse "
        "para un mismo código en diferentes fechas."
    )

    with st.form(
        "nuevo_registro"
    ):

        c1, c2, c3 = st.columns(3)

        with c1:

            codigo = st.text_input(
                "🆔 Código",
                placeholder="Ejemplo: U001"
            )

            fecha_registro = st.date_input(
                "📅 Fecha",
                value=date.today()
            )

            tipo_uso = st.selectbox(
                "🏷️ Tipo de uso",
                TIPOS_USO
            )

        with c2:

            sector = st.text_input(
                "📍 Sector / comunidad"
            )

            zona = st.text_input(
                "🧭 Zona / referencia"
            )

            personas = st.number_input(
                "👥 Personas o unidades de referencia",
                min_value=1,
                max_value=100000,
                value=4
            )

        with c3:

            consumo = st.number_input(
                "💧 Consumo del periodo (m³)",
                min_value=0.01,
                value=18.0,
                step=0.1
            )

            dias = st.number_input(
                "📆 Días del periodo",
                min_value=1,
                max_value=366,
                value=30
            )

            tarifa = st.number_input(
                "💰 Tarifa (S/ por m³)",
                min_value=0.0,
                value=0.0,
                step=0.1
            )

        observaciones = st.text_area(
            "📝 Observaciones"
        )

        enviar = st.form_submit_button(
            "💧 ANALIZAR Y GUARDAR",
            use_container_width=True
        )

    if enviar:

        codigo = (
            codigo
            .strip()
            .upper()
        )

        if not codigo:

            st.error(
                "Ingresa un código."
            )

        else:

            resultado = analizar_consumo(
                personas,
                consumo,
                dias,
                tipo_uso,
                tarifa
            )

            nuevo = pd.DataFrame(
                [
                    {
                        "Código": codigo,
                        "Fecha":
                            fecha_registro.strftime(
                                "%Y-%m-%d"
                            ),
                        "Sector / comunidad":
                            sector.strip(),
                        "Zona / referencia":
                            zona.strip(),
                        "Tipo de uso":
                            tipo_uso,
                        "Personas":
                            int(personas),
                        "Consumo del periodo (m³)":
                            float(consumo),
                        "Días":
                            int(dias),
                        "Tarifa (S/ por m³)":
                            float(tarifa),
                        "Consumo diario (m³)":
                            round(
                                resultado[
                                    "consumo_diario"
                                ],
                                5
                            ),
                        "Consumo por persona (L/día)":
                            round(
                                resultado[
                                    "litros_persona_dia"
                                ],
                                2
                            ),
                        "Índice logarítmico":
                            round(
                                resultado[
                                    "indice_log"
                                ],
                                6
                            ),
                        "Nivel":
                            resultado[
                                "nivel"
                            ],
                        "Costo del periodo (S/)":
                            round(
                                resultado[
                                    "costo"
                                ],
                                2
                            ),
                        "Observaciones":
                            observaciones.strip()
                    }
                ]
            )

            st.session_state.df = (
                pd.concat(
                    [
                        df,
                        nuevo
                    ],
                    ignore_index=True
                )
            )

            guardar_datos(
                st.session_state.df
            )

            st.success(
                "✅ Registro guardado correctamente."
            )

            r1, r2, r3, r4 = st.columns(4)

            r1.metric(
                "Consumo diario",
                f'{resultado["consumo_diario"]:.3f} m³'
            )

            r2.metric(
                "Consumo individual",
                f'{resultado["litros_persona_dia"]:.1f} L/día'
            )

            r3.metric(
                "Índice logarítmico",
                f'{resultado["indice_log"]:.5f}'
            )

            r4.metric(
                "Costo",
                f'S/ {resultado["costo"]:.2f}'
            )


# ============================================================
# FICHA INDIVIDUAL
# ============================================================

elif opcion == "👤 Ficha individual":

    st.title(
        "Ficha individual"
    )

    if df.empty:

        st.info(
            "No existen registros."
        )

    else:

        codigos = sorted(
            df["Código"]
            .astype(str)
            .unique()
            .tolist()
        )

        codigo = st.selectbox(
            "🆔 Selecciona un código",
            codigos
        )

        hist = historial_codigo(
            df,
            codigo
        )

        ultimo = hist.iloc[-1]

        variacion = (
            variacion_ultimo_periodo(
                hist
            )
        )

        tendencia = tendencia_consumo(
            hist
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Registros",
            len(hist)
        )

        c2.metric(
            "Último consumo",
            f'{ultimo["Consumo del periodo (m³)"]:.2f} m³'
        )

        c3.metric(
            "Promedio",
            f'{hist["Consumo del periodo (m³)"].mean():.2f} m³'
        )

        if variacion is None:

            c4.metric(
                "Variación",
                "Sin comparación"
            )

        else:

            c4.metric(
                "Variación",
                f"{variacion:+.1f}%"
            )

        st.subheader(
            "📈 Evolución"
        )

        grafico = hist[
            [
                "Fecha_dt",
                "Consumo del periodo (m³)"
            ]
        ].copy()

        grafico = grafico.dropna()

        if not grafico.empty:

            grafico = grafico.set_index(
                "Fecha_dt"
            )

            st.line_chart(
                grafico
            )

        st.write(
            f"**Tendencia reciente:** {tendencia}"
        )

        st.dataframe(
            hist.drop(
                columns=["Fecha_dt"]
            ),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# EXPLORADOR
# ============================================================

elif opcion == "🔎 Explorador":

    st.title(
        "Explorador de registros"
    )

    if df.empty:

        st.info(
            "No existen registros."
        )

    else:

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode(
            "utf-8-sig"
        )

        st.download_button(
            "📥 Descargar datos CSV",
            data=csv,
            file_name="AquaLog_BI_datos.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# SIMULADOR
# ============================================================

elif opcion == "🎯 Simulador":

    st.title(
        "Simulador AquaLog"
    )

    tab1, tab2 = st.tabs(
        [
            "👤 Escenario individual",
            "🌎 Escenario colectivo"
        ]
    )

    with tab1:

        consumo_base = st.number_input(
            "💧 Consumo actual por periodo (m³)",
            min_value=0.01,
            value=20.0,
            step=0.1
        )

        reduccion = st.slider(
            "🎯 Meta de reducción",
            0,
            50,
            15,
            1,
            format="%d%%"
        )

        nuevo = consumo_base * (
            1 - reduccion / 100
        )

        ahorro = (
            consumo_base - nuevo
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Actual",
            f"{consumo_base:.2f} m³"
        )

        c2.metric(
            "Proyectado",
            f"{nuevo:.2f} m³"
        )

        c3.metric(
            "Ahorro",
            f"{ahorro:.2f} m³"
        )

    with tab2:

        unidades = st.number_input(
            "👥 Número de unidades o puntos",
            min_value=1,
            value=10
        )

        consumo_promedio = st.number_input(
            "💧 Consumo promedio por unidad",
            min_value=0.01,
            value=18.0,
            step=0.1
        )

        meta = st.slider(
            "🎯 Meta colectiva",
            0,
            50,
            15,
            1,
            format="%d%%"
        )

        consumo_total = (
            unidades *
            consumo_promedio
        )

        ahorro_total = (
            consumo_total *
            meta /
            100
        )

        st.metric(
            "Ahorro colectivo estimado",
            f"{ahorro_total:.2f} m³"
        )


# ============================================================
# ANÁLISIS
# ============================================================

elif opcion == "📈 Análisis":

    st.title(
        "Análisis dinámico"
    )

    if df.empty:

        st.info(
            "No existen registros."
        )

    else:

        por_tipo = (
            df.groupby(
                "Tipo de uso"
            )[
                "Consumo del periodo (m³)"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.subheader(
            "📊 Consumo por tipo de uso"
        )

        st.bar_chart(
            por_tipo
        )

        st.subheader(
            "🗓️ Evolución temporal"
        )

        temporal = df.copy()

        temporal["Fecha"] = pd.to_datetime(
            temporal["Fecha"],
            errors="coerce"
        )

        evolucion = (
            temporal.dropna(
                subset=["Fecha"]
            )
            .groupby("Fecha")
            [
                "Consumo del periodo (m³)"
            ]
            .sum()
            .sort_index()
        )

        st.line_chart(
            evolucion
        )


# ============================================================
# ALERTAS
# ============================================================

elif opcion == "🚨 Alertas":

    st.title(
        "Centro de alertas"
    )

    if df.empty:

        st.info(
            "No existen registros."
        )

    else:

        alertas = generar_alertas(
            df
        )

        if not alertas:

            st.success(
                "✅ No se detectaron alertas."
            )

        else:

            for alerta in alertas:

                alerta_html(
                    alerta["tipo"],
                    alerta["titulo"],
                    alerta["texto"]
                )


# ============================================================
# RECOMENDACIONES
# ============================================================

elif opcion == "💡 Recomendaciones":

    st.title(
        "Recomendaciones"
    )

    tipo = st.selectbox(
        "Tipo de uso",
        TIPOS_USO
    )

    nivel = None

    if tipo == "Doméstico":

        nivel = st.selectbox(
            "Nivel",
            [
                "BAJO",
                "MODERADO",
                "ALTO"
            ]
        )

    recomendaciones = (
        obtener_recomendaciones(
            tipo,
            nivel
        )
    )

    for titulo, texto in recomendaciones:

        tip(
            titulo,
            texto
        )


# ============================================================
# MOTOR MATEMÁTICO
# ============================================================

elif opcion == "🧮 Motor matemático":

    st.title(
        "Motor matemático AquaLog"
    )

    st.latex(
        r"C_p=\frac{V}{P\times D}"
    )

    st.write(
        "**V:** volumen consumido en m³."
    )

    st.write(
        "**P:** personas o unidades de referencia."
    )

    st.write(
        "**D:** duración del periodo en días."
    )

    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        volumen = st.number_input(
            "V — Volumen (m³)",
            min_value=0.01,
            value=18.0
        )

    with c2:

        personas = st.number_input(
            "P — Unidades",
            min_value=1,
            value=4
        )

    with c3:

        dias = st.number_input(
            "D — Días",
            min_value=1,
            value=30
        )

    cp = (
        volumen /
        (
            personas *
            dias
        )
    )

    il = math.log10(
        1 + cp
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Cₚ",
        f"{cp:.6f}"
    )

    c2.metric(
        "L/unidad/día",
        f"{cp * 1000:.2f}"
    )

    c3.metric(
        "Iₗ",
        f"{il:.6f}"
    )


# ============================================================
# REPORTES
# ============================================================

elif opcion == "📄 Reportes PDF":

    st.title(
        "Reportes AquaLog BI"
    )

    if df.empty:

        st.info(
            "Primero debes registrar información."
        )

    else:

        codigos = sorted(
            df["Código"]
            .astype(str)
            .unique()
            .tolist()
        )

        codigo = st.selectbox(
            "🆔 Selecciona un código",
            codigos
        )

        historial = historial_codigo(
            df,
            codigo
        )

        ultimo = historial.iloc[-1]

        variacion = variacion_ultimo_periodo(
            historial
        )

        tendencia = tendencia_consumo(
            historial
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Código",
            codigo
        )

        c2.metric(
            "Último consumo",
            f'{ultimo["Consumo del periodo (m³)"]:.2f} m³'
        )

        c3.metric(
            "Índice logarítmico",
            f'{ultimo["Índice logarítmico"]:.6f}'
        )

        c4.metric(
            "Nivel",
            ultimo["Nivel"]
        )

        st.write(
            f"**Tendencia:** {tendencia}"
        )

        if REPORTLAB_DISPONIBLE:

            pdf = crear_pdf(
                ultimo,
                historial
            )

            st.success(
                "✅ Generador PDF disponible."
            )

            st.download_button(
                "📄 DESCARGAR REPORTE PDF",
                data=pdf,
                file_name=f"AquaLog_BI_{codigo}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        else:

            st.warning(
                "⚠️ ReportLab no está instalado "
                "en el servidor. AquaLog BI seguirá "
                "funcionando normalmente."
            )

            if variacion is None:
                variacion_txt = "No disponible"
            else:
                variacion_txt = (
                    f"{variacion:+.2f}%"
                )

            reporte_txt = f"""
AQUALOG BI
REPORTE DE ANÁLISIS DEL CONSUMO DE AGUA

Código:
{codigo}

Fecha:
{ultimo["Fecha"]}

Sector / comunidad:
{ultimo["Sector / comunidad"]}

Zona / referencia:
{ultimo["Zona / referencia"]}

Tipo de uso:
{ultimo["Tipo de uso"]}

Consumo:
{ultimo["Consumo del periodo (m³)"]:.2f} m³

Consumo diario:
{ultimo["Consumo diario (m³)"]:.4f} m³/día

Consumo unitario:
{ultimo["Consumo por persona (L/día)"]:.2f} L/día

Índice logarítmico:
{ultimo["Índice logarítmico"]:.6f}

Nivel:
{ultimo["Nivel"]}

Variación:
{variacion_txt}

Tendencia:
{tendencia}

AquaLog BI
Baños del Inca - Cajamarca - 2026
"""

            st.download_button(
                "📄 DESCARGAR REPORTE TEMPORAL",
                data=reporte_txt.encode(
                    "utf-8"
                ),
                file_name=f"AquaLog_BI_{codigo}.txt",
                mime="text/plain",
                use_container_width=True
            )


# ============================================================
# PROYECTO
# ============================================================

elif opcion == "ℹ️ Proyecto":

    st.title(
        "Proyecto AquaLog BI"
    )

    card(
        "Proyecto de investigación",
        "<b>Desarrollo de software basado "
        "en logaritmos matemáticos para "
        "la gestión eficiente del agua "
        "en el distrito de Baños del Inca, "
        "2026.</b>",
        "📘"
    )

    st.subheader(
        "🎯 Propósito del sistema"
    )

    st.write(
        "AquaLog BI convierte datos de consumo "
        "en indicadores matemáticos, análisis "
        "comparativos y escenarios de ahorro "
        "orientados al apoyo de la toma de decisiones."
    )

    st.success(
        "MEDIR → ANALIZAR → COMPARAR → "
        "PROYECTAR → DECIDIR"
    )

    st.subheader(
        "👩‍🏫 Docente"
    )

    st.info(
        "Paola Ponce"
    )

    st.subheader(
        "👥 Equipo de desarrollo"
    )

    st.write(
        "👤 **Chuquiruna Escobal, Jhersonn**"
    )

    st.write(
        "👤 **Paz Muñoz, Vili**"
    )

    st.write(
        "👤 **Vasquez Azañero, Diego**"
    )

    st.write(
        "👤 **Vasquez Bustamante, Nathan Lowell**"
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    '💧 <strong>AquaLog BI</strong><br>'
    'Inteligencia matemática para la gestión eficiente del agua<br>'
    'Baños del Inca · Cajamarca · 2026'
    '</div>',
    unsafe_allow_html=True
)
