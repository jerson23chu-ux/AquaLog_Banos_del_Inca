import streamlit as st
import pandas as pd
import math
import os
from datetime import date, datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# ============================================================
# AQUAlog BI
# Inteligencia matemática para la gestión eficiente del agua
# ============================================================


# ============================================================
# 1. CONFIGURACIÓN
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
# 2. DISEÑO Y CONTRASTE
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       FONDO GENERAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 12% 8%,
                rgba(0, 174, 239, 0.10),
                transparent 23%
            ),
            radial-gradient(
                circle at 88% 12%,
                rgba(0, 92, 230, 0.08),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #f4fbff 0%,
                #edf8ff 55%,
                #ffffff 100%
            );
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }


    /* =====================================================
       TEXTO DEL CONTENIDO PRINCIPAL
       ===================================================== */

    h1, h2, h3 {
        color: #064c78 !important;
    }

    .main p {
        color: #294e62;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #294e62;
    }


    /* =====================================================
       SIDEBAR
       IMPORTANTE: YA NO SE OBLIGA TODO A SER BLANCO
       ===================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #043783 0%,
                #0870c8 52%,
                #00a2c6 100%
            );
        border-right:
            1px solid rgba(255,255,255,0.18);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    [data-testid="stSidebar"] p {
        color: #e8f8ff !important;
    }

    [data-testid="stSidebar"] label {
        color: white !important;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label p {
        color: white !important;
        font-weight: 650;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25);
    }


    /* =====================================================
       INPUTS - TEXTO OSCURO SOBRE FONDO BLANCO
       ===================================================== */

    input {
        color: #102f40 !important;
        background-color: white !important;
    }

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

    [data-baseweb="popover"] {
        color: #102f40 !important;
    }

    [role="option"] {
        color: #102f40 !important;
        background-color: white !important;
    }

    [role="option"]:hover {
        background-color: #e8f6ff !important;
    }


    /* =====================================================
       ETIQUETAS DE FORMULARIOS
       ===================================================== */

    [data-testid="stWidgetLabel"] p {
        color: #234b61 !important;
        font-weight: 700 !important;
    }


    /* =====================================================
       MÉTRICAS
       ===================================================== */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.97);
        border: 1px solid rgba(0,100,160,0.12);
        padding: 16px 18px;
        border-radius: 18px;
        box-shadow:
            0 8px 24px
            rgba(0,70,120,0.07);
    }

    [data-testid="stMetricValue"] {
        color: #0867c8 !important;
        font-weight: 850;
    }

    [data-testid="stMetricLabel"] {
        color: #496a7d !important;
        font-weight: 700;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        background:
            linear-gradient(
                120deg,
                #043783 0%,
                #0875d1 50%,
                #12b8da 100%
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
        font-size: 46px;
        font-weight: 900;
        color: white !important;
        line-height: 1.05;
    }

    .hero-subtitle {
        color: white !important;
        font-size: 20px;
        font-weight: 700;
        margin-top: 7px;
    }

    .hero-text {
        color: #effcff !important;
        font-size: 15px;
        line-height: 1.55;
        margin-top: 8px;
        max-width: 1000px;
    }

    .chip {
        display: inline-block;
        margin: 12px 7px 0 0;
        padding: 7px 12px;

        background:
            rgba(255,255,255,0.14);

        border:
            1px solid
            rgba(255,255,255,0.25);

        border-radius: 999px;

        color: white !important;
        font-size: 12px;
        font-weight: 750;
    }


    /* =====================================================
       TARJETAS
       ===================================================== */

    .card {
        background: white;
        border: 1px solid #d7ebf5;
        border-radius: 18px;

        padding: 18px 20px;
        margin: 8px 0 14px 0;

        box-shadow:
            0 8px 22px
            rgba(0,70,120,0.06);

        color: #294e62 !important;
    }

    .card h3 {
        color: #07527f !important;
    }

    .card p {
        color: #294e62 !important;
    }


    /* =====================================================
       ALERTAS PERSONALIZADAS
       ===================================================== */

    .alert-red {
        background: #fff1f1;
        color: #71272d !important;
        border-left: 6px solid #d93645;
        border-radius: 13px;
        padding: 14px 17px;
        margin-bottom: 9px;
    }

    .alert-green {
        background: #ecfff4;
        color: #155c3a !important;
        border-left: 6px solid #18a568;
        border-radius: 13px;
        padding: 14px 17px;
        margin-bottom: 9px;
    }

    .alert-yellow {
        background: #fff9df;
        color: #6f5810 !important;
        border-left: 6px solid #e5ad17;
        border-radius: 13px;
        padding: 14px 17px;
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


    /* =====================================================
       BOTONES
       ===================================================== */

    .stButton button {
        border-radius: 12px;
        font-weight: 750;
    }

    .stDownloadButton button {
        border-radius: 12px;
        font-weight: 750;
    }


    /* =====================================================
       TABLAS
       ===================================================== */

    [data-testid="stDataFrame"] {
        background-color: white;
        border-radius: 14px;
    }


    /* =====================================================
       PESTAÑAS
       ===================================================== */

    button[data-baseweb="tab"] {
        color: #184c68 !important;
        font-weight: 700 !important;
    }


    /* =====================================================
       PIE DE PÁGINA
       ===================================================== */

    .footer {
        text-align: center;
        color: #557286 !important;
        padding: 18px 0 5px 0;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. ELEMENTOS VISUALES
# ============================================================

def hero():

    st.markdown(
        '<div class="hero">'
        '<div class="hero-title">💧 AquaLog BI</div>'
        '<div class="hero-subtitle">'
        'Inteligencia matemática para la gestión eficiente del agua'
        '</div>'
        '<div class="hero-text">'
        'Sistema interactivo para registrar, analizar, comparar '
        'y proyectar el consumo de agua mediante indicadores matemáticos, '
        'seguimiento histórico, alertas automáticas y escenarios de ahorro.'
        '</div>'
        '<span class="chip">💧 Consumo</span>'
        '<span class="chip">🧮 Matemática</span>'
        '<span class="chip">📊 Analítica</span>'
        '<span class="chip">🚨 Alertas</span>'
        '<span class="chip">🎯 Proyección</span>'
        '<span class="chip">📄 Reportes</span>'
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


def mostrar_alerta(tipo, titulo, texto):

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
# 4. BASE DE DATOS
# ============================================================

def dataframe_vacio():

    return pd.DataFrame(
        columns=COLUMNAS
    )


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

    for columna in numericas:

        df[columna] = pd.to_numeric(
            df[columna],
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

    fecha_convertida = pd.to_datetime(
        df["Fecha"],
        errors="coerce"
    )

    fecha_convertida = (
        fecha_convertida
        .fillna(pd.Timestamp.today())
    )

    df["Fecha"] = (
        fecha_convertida
        .dt.strftime("%Y-%m-%d")
    )

    return df[COLUMNAS]


def cargar_datos():

    if not os.path.exists(
        ARCHIVO_DATOS
    ):
        return dataframe_vacio()

    try:

        return normalizar_df(
            pd.read_csv(
                ARCHIVO_DATOS
            )
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
# 5. MOTOR MATEMÁTICO
# ============================================================

def analizar_consumo(
    personas,
    consumo,
    dias,
    tipo_uso,
    tarifa
):

    personas = max(
        int(personas),
        1
    )

    dias = max(
        int(dias),
        1
    )

    consumo_diario = (
        consumo / dias
    )

    cp = (
        consumo /
        (personas * dias)
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
# 6. HISTORIAL Y COMPARACIÓN
# ============================================================

def historial_codigo(df, codigo):

    historial = df[
        df["Código"].astype(str) ==
        str(codigo)
    ].copy()

    historial["Fecha_dt"] = pd.to_datetime(
        historial["Fecha"],
        errors="coerce"
    )

    historial = historial.sort_values(
        "Fecha_dt"
    )

    return historial


def calcular_variacion(historial):

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

    variacion = (
        (actual - anterior) /
        anterior
    ) * 100

    return variacion


def calcular_tendencia(historial):

    if len(historial) < 3:
        return "SIN DATOS SUFICIENTES"

    valores = (
        historial[
            "Consumo del periodo (m³)"
        ]
        .tail(3)
        .tolist()
    )

    if (
        valores[0] <
        valores[1] <
        valores[2]
    ):
        return "CRECIENTE"

    elif (
        valores[0] >
        valores[1] >
        valores[2]
    ):
        return "DECRECIENTE"

    return "VARIABLE"


# ============================================================
# 7. ALERTAS
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

        variacion = calcular_variacion(
            hist
        )

        if variacion is None:
            continue

        if variacion >= 20:

            alertas.append({
                "tipo": "rojo",
                "titulo":
                    f"🔴 Incremento importante — {codigo}",
                "texto":
                    f"El consumo aumentó "
                    f"{variacion:.1f}% respecto "
                    f"al registro anterior."
            })

        elif variacion <= -10:

            alertas.append({
                "tipo": "verde",
                "titulo":
                    f"🟢 Reducción detectada — {codigo}",
                "texto":
                    f"El consumo disminuyó "
                    f"{abs(variacion):.1f}% respecto "
                    f"al registro anterior."
            })

        tendencia = calcular_tendencia(
            hist
        )

        if tendencia == "CRECIENTE":

            alertas.append({
                "tipo": "amarillo",
                "titulo":
                    f"🟡 Tendencia creciente — {codigo}",
                "texto":
                    "Los tres últimos registros "
                    "presentan incrementos consecutivos."
            })

    return alertas


# ============================================================
# 8. RECOMENDACIONES
# ============================================================

def obtener_recomendaciones(
    tipo_uso,
    nivel=None
):

    datos = {

        "Doméstico": [
            (
                "🚰 Evita desperdicios",
                "Cierra los caños cuando el agua no sea necesaria."
            ),
            (
                "🚿 Optimiza las duchas",
                "Reducir algunos minutos puede generar un ahorro acumulado importante."
            ),
            (
                "🔧 Busca posibles fugas",
                "Revisa tanques, grifos, conexiones e inodoros."
            ),
            (
                "📊 Compara tus periodos",
                "Utiliza el historial de AquaLog BI para identificar cambios."
            )
        ],

        "Comercial": [
            (
                "📋 Control por actividad",
                "Identifica las operaciones que demandan mayor cantidad de agua."
            ),
            (
                "🔧 Mantenimiento preventivo",
                "Revisa instalaciones y equipos relacionados con el agua."
            ),
            (
                "🎯 Define metas",
                "Establece objetivos progresivos de reducción."
            )
        ],

        "Educativo": [
            (
                "🏫 Educación y sensibilización",
                "Promueve prácticas responsables entre estudiantes y personal."
            ),
            (
                "🚰 Revisión de instalaciones",
                "Supervisa servicios higiénicos y puntos de consumo."
            ),
            (
                "📈 Seguimiento periódico",
                "Compara consumos entre diferentes periodos."
            )
        ],

        "Institucional": [
            (
                "📊 Monitoreo",
                "Controla los consumos de manera periódica."
            ),
            (
                "🔧 Mantenimiento",
                "Programa inspecciones preventivas."
            ),
            (
                "🎯 Metas de gestión",
                "Utiliza indicadores para establecer objetivos de reducción."
            )
        ],

        "Riego": [
            (
                "🌅 Horarios de riego",
                "Prefiere periodos de menor evaporación."
            ),
            (
                "💧 Dosificación",
                "Evita aplicar más agua de la necesaria."
            ),
            (
                "🔍 Revisión del sistema",
                "Comprueba mangueras, tuberías y conexiones."
            )
        ],

        "Otro": [
            (
                "📊 Medición periódica",
                "Mantén registros comparables de consumo."
            ),
            (
                "🔍 Identificación de pérdidas",
                "Evalúa posibles usos innecesarios."
            ),
            (
                "🎯 Simulación",
                "Estudia distintos escenarios mediante AquaLog BI."
            )
        ]
    }

    lista = list(
        datos.get(
            tipo_uso,
            datos["Otro"]
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
                "El resultado se encuentra en el nivel alto "
                "de acuerdo con los criterios referenciales "
                "implementados en el prototipo."
            )
        )

    return lista


# ============================================================
# 9. GENERADOR DE PDF
# ============================================================

def crear_pdf(
    fila,
    historial
):

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
        textColor=colors.HexColor(
            "#075A8F"
        ),
        spaceAfter=8
    )

    subtitulo = ParagraphStyle(
        "SubtituloAqua",
        parent=estilos["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor(
            "#4A6B7C"
        ),
        spaceAfter=18
    )

    seccion = ParagraphStyle(
        "SeccionAqua",
        parent=estilos["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor(
            "#075A8F"
        ),
        spaceBefore=10,
        spaceAfter=8
    )

    texto = ParagraphStyle(
        "TextoAqua",
        parent=estilos["BodyText"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor(
            "#273F4B"
        )
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
        Spacer(
            1,
            10
        )
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
        [
            "Sector / comunidad",
            str(fila["Sector / comunidad"])
        ],
        [
            "Zona / referencia",
            str(fila["Zona / referencia"])
        ],
        [
            "Tipo de uso",
            str(fila["Tipo de uso"])
        ]
    ]

    tabla = Table(
        tabla_identificacion,
        colWidths=[
            150,
            340
        ]
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
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#203A49")
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
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
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
        Spacer(
            1,
            14
        )
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
        colWidths=[
            220,
            270
        ]
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
            "Clasificación",
            str(fila["Nivel"])
        ],
        [
            "Costo estimado",
            f'S/ {fila["Costo del periodo (S/)"]:.2f}'
        ]
    ]

    tabla3 = Table(
        resultados,
        colWidths=[
            220,
            270
        ]
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
            "Consumo unitario diario: "
            "Cₚ = V / (P × D)",
            texto
        )
    )

    elementos.append(
        Spacer(
            1,
            5
        )
    )

    elementos.append(
        Paragraph(
            "Índice logarítmico: "
            "Iₗ = log10(1 + Cₚ)",
            texto
        )
    )

    variacion = calcular_variacion(
        historial
    )

    tendencia = calcular_tendencia(
        historial
    )

    elementos.append(
        Paragraph(
            "5. Análisis histórico",
            seccion
        )
    )

    if variacion is None:

        texto_variacion = (
            "No existe información suficiente "
            "para comparar con un periodo anterior."
        )

    elif variacion > 0:

        texto_variacion = (
            f"El consumo aumentó "
            f"{variacion:.2f}% respecto "
            f"al periodo anterior."
        )

    elif variacion < 0:

        texto_variacion = (
            f"El consumo disminuyó "
            f"{abs(variacion):.2f}% respecto "
            f"al periodo anterior."
        )

    else:

        texto_variacion = (
            "El consumo no presentó variación "
            "respecto al periodo anterior."
        )

    elementos.append(
        Paragraph(
            texto_variacion,
            texto
        )
    )

    elementos.append(
        Spacer(
            1,
            7
        )
    )

    elementos.append(
        Paragraph(
            f"Tendencia reciente: "
            f"<b>{tendencia}</b>",
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
                f"<b>{titulo_rec}</b>: "
                f"{texto_rec}",
                texto
            )
        )

        elementos.append(
            Spacer(
                1,
                5
            )
        )

    elementos.append(
        Paragraph(
            "7. Observaciones",
            seccion
        )
    )

    observacion = str(
        fila["Observaciones"]
    ).strip()

    if not observacion:
        observacion = (
            "No se registraron observaciones."
        )

    elementos.append(
        Paragraph(
            observacion,
            texto
        )
    )

    elementos.append(
        Spacer(
            1,
            25
        )
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
# 10. ESTADO DE LA APLICACIÓN
# ============================================================

if "df" not in st.session_state:

    st.session_state.df = (
        cargar_datos()
    )

df = normalizar_df(
    st.session_state.df
)


# ============================================================
# 11. MENÚ
# ============================================================

with st.sidebar:

    st.title(
        "💧 AquaLog BI"
    )

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
# 12. CENTRO DE CONTROL
# ============================================================

if opcion == "🏠 Centro de control":

    st.title(
        "Centro de control"
    )

    if df.empty:

        card(
            "AquaLog BI está listo",
            "Todavía no existen registros. "
            "Ingresa el primero desde "
            "<b>Nuevo registro</b>.",
            "🚀"
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        with c1:

            card(
                "Medir",
                "Registra información.",
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
                "Estudia cambios.",
                "📈"
            )

        with c4:

            card(
                "Decidir",
                "Proyecta mejoras.",
                "🎯"
            )

    else:

        consumo_total = (
            df[
                "Consumo del periodo (m³)"
            ].sum()
        )

        promedio = (
            df[
                "Consumo del periodo (m³)"
            ].mean()
        )

        puntos = (
            df["Código"]
            .astype(str)
            .nunique()
        )

        costo = (
            df[
                "Costo del periodo (S/)"
            ].sum()
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "💧 Consumo acumulado",
            f"{consumo_total:.2f} m³"
        )

        c2.metric(
            "📊 Promedio",
            f"{promedio:.2f} m³"
        )

        c3.metric(
            "🆔 Puntos registrados",
            puntos
        )

        c4.metric(
            "💰 Costo acumulado",
            f"S/ {costo:.2f}"
        )

        alertas = generar_alertas(
            df
        )

        aumentos = sum(
            alerta["tipo"] == "rojo"
            for alerta in alertas
        )

        reducciones = sum(
            alerta["tipo"] == "verde"
            for alerta in alertas
        )

        c1, c2 = (
            st.columns(2)
        )

        c1.metric(
            "📈 Incrementos importantes",
            aumentos
        )

        c2.metric(
            "📉 Reducciones detectadas",
            reducciones
        )

        st.subheader(
            "🚨 Resumen de alertas"
        )

        if not alertas:

            st.success(
                "No se detectaron alertas "
                "comparativas relevantes."
            )

        else:

            for alerta in alertas[:6]:

                mostrar_alerta(
                    alerta["tipo"],
                    alerta["titulo"],
                    alerta["texto"]
                )

        st.subheader(
            "📊 Consumo por tipo de uso"
        )

        consumo_tipo = (
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
            consumo_tipo
        )

        st.subheader(
            "📍 Consumo por sector/comunidad"
        )

        sectores_df = df.copy()

        sectores_df[
            "Sector / comunidad"
        ] = (
            sectores_df[
                "Sector / comunidad"
            ]
            .replace(
                "",
                "Sin especificar"
            )
        )

        consumo_sector = (
            sectores_df.groupby(
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
            consumo_sector
        )

        st.subheader(
            "🏆 Mayores consumos"
        )

        ranking = (
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
            ranking,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 13. NUEVO REGISTRO
# ============================================================

elif opcion == "➕ Nuevo registro":

    st.title(
        "Nuevo registro"
    )

    st.caption(
        "Un mismo código puede tener diferentes "
        "registros a lo largo del tiempo."
    )

    with st.form(
        "registro"
    ):

        c1, c2, c3 = (
            st.columns(3)
        )

        with c1:

            codigo = st.text_input(
                "🆔 Código",
                placeholder="Ejemplo: U001"
            )

            fecha_registro = (
                st.date_input(
                    "📅 Fecha",
                    value=date.today()
                )
            )

            tipo_uso = (
                st.selectbox(
                    "🏷️ Tipo de uso",
                    TIPOS_USO
                )
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

        guardar = (
            st.form_submit_button(
                "💧 ANALIZAR Y GUARDAR",
                use_container_width=True
            )
        )

    if guardar:

        codigo = (
            codigo.strip().upper()
        )

        if not codigo:

            st.error(
                "Debes ingresar un código."
            )

        else:

            resultado = (
                analizar_consumo(
                    personas,
                    consumo,
                    dias,
                    tipo_uso,
                    tarifa
                )
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

            c1, c2, c3, c4 = (
                st.columns(4)
            )

            c1.metric(
                "Consumo diario",
                f'{resultado["consumo_diario"]:.3f} m³'
            )

            c2.metric(
                "Consumo individual",
                f'{resultado["litros_persona_dia"]:.1f} L/día'
            )

            c3.metric(
                "Índice logarítmico",
                f'{resultado["indice_log"]:.6f}'
            )

            c4.metric(
                "Costo estimado",
                f'S/ {resultado["costo"]:.2f}'
            )

            if tipo_uso == "Doméstico":

                if resultado["nivel"] == "BAJO":

                    st.success(
                        "🟢 Nivel referencial: BAJO"
                    )

                elif resultado["nivel"] == "MODERADO":

                    st.warning(
                        "🟡 Nivel referencial: MODERADO"
                    )

                else:

                    st.error(
                        "🔴 Nivel referencial: ALTO"
                    )

            else:

                st.info(
                    "Para usos no domésticos "
                    "el sistema analiza los indicadores "
                    "sin aplicar la clasificación "
                    "doméstica."
                )

            historial = historial_codigo(
                st.session_state.df,
                codigo
            )

            variacion = calcular_variacion(
                historial
            )

            if variacion is not None:

                if variacion > 0:

                    st.warning(
                        f"📈 El consumo aumentó "
                        f"{variacion:.1f}% respecto "
                        f"al registro anterior."
                    )

                elif variacion < 0:

                    st.success(
                        f"📉 El consumo disminuyó "
                        f"{abs(variacion):.1f}% respecto "
                        f"al registro anterior."
                    )

            with st.expander(
                "🧮 Ver desarrollo matemático"
            ):

                st.latex(
                    r"C_p=\frac{V}{P\times D}"
                )

                st.write(
                    f"Cₚ = {consumo:.2f} / "
                    f"({personas} × {dias})"
                )

                st.write(
                    f"Cₚ = "
                    f"{resultado['cp']:.6f} "
                    f"m³/unidad/día"
                )

                st.latex(
                    r"I_L=\log_{10}(1+C_p)"
                )

                st.write(
                    f"Iₗ = "
                    f"{resultado['indice_log']:.6f}"
                )


# ============================================================
# 14. FICHA INDIVIDUAL
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
            df[
                "Código"
            ]
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

        variacion = calcular_variacion(
            historial
        )

        tendencia = calcular_tendencia(
            historial
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "Registros",
            len(historial)
        )

        c2.metric(
            "Último consumo",
            f'{ultimo["Consumo del periodo (m³)"]:.2f} m³'
        )

        c3.metric(
            "Promedio",
            f'{historial["Consumo del periodo (m³)"].mean():.2f} m³'
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

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Máximo",
            f'{historial["Consumo del periodo (m³)"].max():.2f} m³'
        )

        c2.metric(
            "Mínimo",
            f'{historial["Consumo del periodo (m³)"].min():.2f} m³'
        )

        c3.metric(
            "Tendencia",
            tendencia
        )

        st.subheader(
            "📈 Evolución histórica"
        )

        grafico = historial[
            [
                "Fecha_dt",
                "Consumo del periodo (m³)"
            ]
        ].dropna()

        if not grafico.empty:

            grafico = (
                grafico
                .set_index("Fecha_dt")
            )

            st.line_chart(
                grafico
            )

        st.subheader(
            "🔍 Interpretación"
        )

        if variacion is None:

            st.info(
                "Se necesita un segundo registro "
                "para calcular variaciones."
            )

        elif variacion >= 20:

            mostrar_alerta(
                "rojo",
                "Incremento importante",
                f"El consumo aumentó "
                f"{variacion:.1f}%."
            )

        elif variacion <= -10:

            mostrar_alerta(
                "verde",
                "Reducción detectada",
                f"El consumo disminuyó "
                f"{abs(variacion):.1f}%."
            )

        else:

            mostrar_alerta(
                "amarillo",
                "Variación moderada",
                f"El cambio fue de "
                f"{variacion:+.1f}%."
            )

        if tendencia == "CRECIENTE":

            st.warning(
                "⚠️ Los tres últimos registros "
                "presentan una tendencia creciente."
            )

        elif tendencia == "DECRECIENTE":

            st.success(
                "✅ Los tres últimos registros "
                "presentan una tendencia decreciente."
            )

        st.subheader(
            "📋 Historial completo"
        )

        mostrar = historial.drop(
            columns=["Fecha_dt"]
        )

        st.dataframe(
            mostrar,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# 15. EXPLORADOR
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

        sectores = sorted(
            [
                x
                for x in
                df["Sector / comunidad"]
                .astype(str)
                .unique()
                .tolist()
                if x.strip()
            ]
        )

        tipos = sorted(
            df["Tipo de uso"]
            .astype(str)
            .unique()
            .tolist()
        )

        niveles = sorted(
            df["Nivel"]
            .astype(str)
            .unique()
            .tolist()
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        with c1:

            filtro_sector = (
                st.selectbox(
                    "📍 Sector",
                    ["Todos"] + sectores
                )
            )

        with c2:

            filtro_tipo = (
                st.selectbox(
                    "🏷️ Tipo de uso",
                    ["Todos"] + tipos
                )
            )

        with c3:

            filtro_nivel = (
                st.selectbox(
                    "🚦 Nivel",
                    ["Todos"] + niveles
                )
            )

        busqueda = st.text_input(
            "🔍 Buscar código, sector o zona"
        )

        filtrado = df.copy()

        if filtro_sector != "Todos":

            filtrado = filtrado[
                filtrado[
                    "Sector / comunidad"
                ] == filtro_sector
            ]

        if filtro_tipo != "Todos":

            filtrado = filtrado[
                filtrado[
                    "Tipo de uso"
                ] == filtro_tipo
            ]

        if filtro_nivel != "Todos":

            filtrado = filtrado[
                filtrado[
                    "Nivel"
                ] == filtro_nivel
            ]

        if busqueda.strip():

            palabra = (
                busqueda.strip()
            )

            mascara = (
                filtrado["Código"]
                .astype(str)
                .str.contains(
                    palabra,
                    case=False,
                    na=False
                )
                |
                filtrado["Sector / comunidad"]
                .astype(str)
                .str.contains(
                    palabra,
                    case=False,
                    na=False
                )
                |
                filtrado["Zona / referencia"]
                .astype(str)
                .str.contains(
                    palabra,
                    case=False,
                    na=False
                )
            )

            filtrado = (
                filtrado[mascara]
            )

        st.caption(
            f"{len(filtrado)} registro(s) encontrados."
        )

        st.dataframe(
            filtrado,
            use_container_width=True,
            hide_index=True
        )

        csv = (
            filtrado
            .to_csv(index=False)
            .encode("utf-8-sig")
        )

        st.download_button(
            "📥 DESCARGAR DATOS CSV",
            data=csv,
            file_name="AquaLog_BI_datos.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "📤 Importar base CSV"
        )

        archivo = st.file_uploader(
            "Selecciona un archivo CSV",
            type=["csv"]
        )

        if archivo is not None:

            try:

                importado = normalizar_df(
                    pd.read_csv(
                        archivo
                    )
                )

                st.success(
                    f"Se detectaron "
                    f"{len(importado)} registros."
                )

                if st.button(
                    "✅ USAR ESTA BASE",
                    use_container_width=True
                ):

                    st.session_state.df = (
                        importado
                    )

                    guardar_datos(
                        importado
                    )

                    st.rerun()

            except Exception as error:

                st.error(
                    f"No se pudo importar: "
                    f"{error}"
                )

        st.divider()

        st.subheader(
            "🗑️ Eliminar registro"
        )

        temporal = (
            df.reset_index()
        )

        opciones = temporal.apply(
            lambda fila:
                f'{fila["index"]} | '
                f'{fila["Código"]} | '
                f'{fila["Fecha"]} | '
                f'{fila["Consumo del periodo (m³)"]:.2f} m³',
            axis=1
        ).tolist()

        seleccion = st.selectbox(
            "Selecciona el registro",
            ["Seleccionar..."] + opciones
        )

        if st.button(
            "🗑️ ELIMINAR",
            use_container_width=True
        ):

            if seleccion == "Seleccionar...":

                st.warning(
                    "Primero selecciona un registro."
                )

            else:

                indice = int(
                    seleccion.split(
                        " | "
                    )[0]
                )

                nuevo_df = (
                    df.drop(
                        index=indice
                    )
                    .reset_index(
                        drop=True
                    )
                )

                st.session_state.df = (
                    nuevo_df
                )

                guardar_datos(
                    nuevo_df
                )

                st.success(
                    "Registro eliminado."
                )

                st.rerun()


# ============================================================
# 16. SIMULADOR
# ============================================================

elif opcion == "🎯 Simulador":

    st.title(
        "Simulador AquaLog"
    )

    st.write(
        "Explora escenarios hipotéticos "
        "de reducción del consumo."
    )

    tab1, tab2 = st.tabs(
        [
            "👤 Escenario individual",
            "🌎 Escenario colectivo"
        ]
    )

    with tab1:

        consumo_actual = st.number_input(
            "💧 Consumo actual por periodo (m³)",
            min_value=0.01,
            value=20.0,
            step=0.1,
            key="individual_consumo"
        )

        tarifa_sim = st.number_input(
            "💰 Tarifa (S/ por m³)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            key="individual_tarifa"
        )

        meta = st.slider(
            "🎯 Meta de reducción",
            0,
            50,
            15,
            1,
            format="%d%%",
            key="individual_meta"
        )

        consumo_proyectado = (
            consumo_actual *
            (1 - meta / 100)
        )

        ahorro = (
            consumo_actual -
            consumo_proyectado
        )

        ahorro_12_periodos = (
            ahorro * 12
        )

        ahorro_dinero = (
            ahorro *
            tarifa_sim
        )

        ahorro_dinero_12 = (
            ahorro_dinero *
            12
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "Consumo actual",
            f"{consumo_actual:.2f} m³"
        )

        c2.metric(
            "Consumo proyectado",
            f"{consumo_proyectado:.2f} m³"
        )

        c3.metric(
            "Ahorro por periodo",
            f"{ahorro:.2f} m³"
        )

        c4.metric(
            "Ahorro en 12 periodos",
            f"{ahorro_12_periodos:.2f} m³"
        )

        if tarifa_sim > 0:

            st.success(
                f"💰 Ahorro económico estimado: "
                f"S/ {ahorro_dinero:.2f} por periodo "
                f"y S/ {ahorro_dinero_12:.2f} "
                f"en 12 periodos."
            )

        escenarios = pd.Series(
            {
                "Actual":
                    consumo_actual,

                "Reducción 5%":
                    consumo_actual * 0.95,

                "Reducción 10%":
                    consumo_actual * 0.90,

                "Reducción 15%":
                    consumo_actual * 0.85,

                "Reducción 20%":
                    consumo_actual * 0.80,

                "Reducción 25%":
                    consumo_actual * 0.75,

                f"Meta {meta}%":
                    consumo_proyectado
            }
        )

        st.subheader(
            "📊 Comparación de escenarios"
        )

        st.bar_chart(
            escenarios
        )

    with tab2:

        st.subheader(
            "Proyección colectiva"
        )

        cantidad = st.number_input(
            "🔢 Número de unidades o puntos",
            min_value=1,
            value=10
        )

        consumo_promedio = st.number_input(
            "💧 Consumo promedio por unidad (m³)",
            min_value=0.01,
            value=18.0,
            step=0.1
        )

        meta_colectiva = st.slider(
            "🎯 Meta colectiva",
            0,
            50,
            15,
            1,
            format="%d%%"
        )

        actual_total = (
            cantidad *
            consumo_promedio
        )

        ahorro_total = (
            actual_total *
            meta_colectiva /
            100
        )

        proyectado_total = (
            actual_total -
            ahorro_total
        )

        ahorro_12 = (
            ahorro_total *
            12
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "Consumo colectivo",
            f"{actual_total:.2f} m³"
        )

        c2.metric(
            "Escenario proyectado",
            f"{proyectado_total:.2f} m³"
        )

        c3.metric(
            "Ahorro por periodo",
            f"{ahorro_total:.2f} m³"
        )

        c4.metric(
            "Ahorro en 12 periodos",
            f"{ahorro_12:.2f} m³"
        )

        st.info(
            f"Con una reducción del "
            f"{meta_colectiva}% aplicada a "
            f"{cantidad} unidades, "
            f"el ahorro proyectado sería "
            f"{ahorro_total:.2f} m³ por periodo."
        )


# ============================================================
# 17. ANÁLISIS
# ============================================================

elif opcion == "📈 Análisis":

    st.title(
        "Análisis dinámico"
    )

    if df.empty:

        st.info(
            "No existen datos disponibles."
        )

    else:

        tipos = sorted(
            df["Tipo de uso"]
            .astype(str)
            .unique()
            .tolist()
        )

        sectores = sorted(
            [
                x
                for x in
                df["Sector / comunidad"]
                .astype(str)
                .unique()
                .tolist()
                if x.strip()
            ]
        )

        c1, c2 = (
            st.columns(2)
        )

        with c1:

            tipos_sel = st.multiselect(
                "🏷️ Tipos de uso",
                tipos,
                default=tipos
            )

        with c2:

            sectores_sel = st.multiselect(
                "📍 Sectores",
                sectores,
                default=sectores
            )

        analisis = df[
            df["Tipo de uso"]
            .isin(tipos_sel)
        ].copy()

        if sectores and sectores_sel:

            analisis = analisis[
                analisis[
                    "Sector / comunidad"
                ].isin(sectores_sel)
            ]

        if analisis.empty:

            st.warning(
                "No existen datos para "
                "los filtros seleccionados."
            )

        else:

            c1, c2, c3, c4 = (
                st.columns(4)
            )

            c1.metric(
                "Registros",
                len(analisis)
            )

            c2.metric(
                "Consumo total",
                f'{analisis["Consumo del periodo (m³)"].sum():.2f} m³'
            )

            c3.metric(
                "Promedio",
                f'{analisis["Consumo del periodo (m³)"].mean():.2f} m³'
            )

            c4.metric(
                "Costo",
                f'S/ {analisis["Costo del periodo (S/)"].sum():.2f}'
            )

            st.subheader(
                "📊 Consumo por tipo de uso"
            )

            por_tipo = (
                analisis.groupby(
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
                por_tipo
            )

            st.subheader(
                "📍 Consumo por sector"
            )

            temp = analisis.copy()

            temp[
                "Sector / comunidad"
            ] = (
                temp[
                    "Sector / comunidad"
                ]
                .replace(
                    "",
                    "Sin especificar"
                )
            )

            por_sector = (
                temp.groupby(
                    "Sector / comunidad"
                )[
                    "Consumo del periodo (m³)"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                por_sector
            )

            st.subheader(
                "🗓️ Evolución temporal"
            )

            temporal = analisis.copy()

            temporal["Fecha"] = (
                pd.to_datetime(
                    temporal["Fecha"],
                    errors="coerce"
                )
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

            st.subheader(
                "🏆 Ranking de consumo"
            )

            ranking = (
                analisis.sort_values(
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
                .head(15)
            )

            st.dataframe(
                ranking,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# 18. ALERTAS
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
                "✅ No se detectaron alertas "
                "con los criterios actuales."
            )

        else:

            st.metric(
                "Alertas detectadas",
                len(alertas)
            )

            for alerta in alertas:

                mostrar_alerta(
                    alerta["tipo"],
                    alerta["titulo"],
                    alerta["texto"]
                )

        st.caption(
            "Las alertas se generan comparando "
            "el historial disponible de cada código."
        )


# ============================================================
# 19. RECOMENDACIONES
# ============================================================

elif opcion == "💡 Recomendaciones":

    st.title(
        "Recomendaciones AquaLog"
    )

    tipo = st.selectbox(
        "🏷️ Tipo de uso",
        TIPOS_USO
    )

    nivel = None

    if tipo == "Doméstico":

        nivel = st.selectbox(
            "🚦 Nivel",
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

    for titulo_rec, texto_rec in recomendaciones:

        tip(
            titulo_rec,
            texto_rec
        )


# ============================================================
# 20. MOTOR MATEMÁTICO
# ============================================================

elif opcion == "🧮 Motor matemático":

    st.title(
        "Motor matemático AquaLog"
    )

    card(
        "1. Datos",
        "AquaLog BI recibe el volumen de agua, "
        "el número de unidades de referencia "
        "y la duración del periodo.",
        "📥"
    )

    st.latex(
        r"C_p=\frac{V}{P\times D}"
    )

    st.write(
        "**V** = volumen consumido en m³."
    )

    st.write(
        "**P** = personas o unidades de referencia."
    )

    st.write(
        "**D** = días del periodo."
    )

    st.write(
        "**Cₚ** = consumo unitario diario."
    )

    card(
        "2. Transformación logarítmica",
        "El indicador calculado pasa por "
        "una transformación logarítmica.",
        "🧮"
    )

    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )

    st.info(
        "La transformación permite representar "
        "el indicador en una escala logarítmica."
    )

    card(
        "3. Comparación histórica",
        "Los nuevos resultados pueden compararse "
        "con los registros anteriores del mismo código.",
        "📈"
    )

    st.latex(
        r"\Delta C(\%)="
        r"\frac{C_{actual}-C_{anterior}}{C_{anterior}}"
        r"\times100"
    )

    card(
        "4. Interpretación",
        "AquaLog BI integra resultados matemáticos, "
        "variaciones y tendencias para facilitar "
        "la interpretación de los registros.",
        "🔍"
    )

    st.warning(
        "Las categorías domésticas BAJO, MODERADO "
        "y ALTO son criterios referenciales del prototipo "
        "y deben estar debidamente sustentadas "
        "en la investigación."
    )

    st.subheader(
        "🧪 Laboratorio matemático"
    )

    c1, c2, c3 = (
        st.columns(3)
    )

    with c1:

        volumen_demo = st.number_input(
            "V — Volumen (m³)",
            min_value=0.01,
            value=18.0
        )

    with c2:

        unidades_demo = st.number_input(
            "P — Unidades",
            min_value=1,
            value=4
        )

    with c3:

        dias_demo = st.number_input(
            "D — Días",
            min_value=1,
            value=30
        )

    cp_demo = (
        volumen_demo /
        (
            unidades_demo *
            dias_demo
        )
    )

    il_demo = math.log10(
        1 + cp_demo
    )

    c1, c2, c3 = (
        st.columns(3)
    )

    c1.metric(
        "Cₚ",
        f"{cp_demo:.6f} m³/unidad/día"
    )

    c2.metric(
        "Equivalencia",
        f"{cp_demo * 1000:.2f} L/unidad/día"
    )

    c3.metric(
        "Índice Iₗ",
        f"{il_demo:.6f}"
    )

    st.subheader(
        "🔄 Arquitectura conceptual"
    )

    st.success(
        "DATOS → PROCESAMIENTO → "
        "MODELO MATEMÁTICO → INDICADORES → "
        "COMPARACIÓN → INTERPRETACIÓN → DECISIÓN"
    )


# ============================================================
# 21. REPORTES PDF
# ============================================================

elif opcion == "📄 Reportes PDF":

    st.title(
        "Reportes PDF"
    )

    st.write(
        "Genera un reporte profesional "
        "a partir del último registro "
        "y del historial de un código."
    )

    if df.empty:

        st.info(
            "Primero debes registrar información."
        )

    else:

        codigos = sorted(
            df[
                "Código"
            ]
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

        variacion = calcular_variacion(
            historial
        )

        tendencia = calcular_tendencia(
            historial
        )

        st.subheader(
            "Vista previa"
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "Código",
            codigo
        )

        c2.metric(
            "Último consumo",
            f'{ultimo["Consumo del periodo (m³)"]:.2f} m³'
        )

        c3.metric(
            "Índice",
            f'{ultimo["Índice logarítmico"]:.6f}'
        )

        c4.metric(
            "Nivel",
            ultimo["Nivel"]
        )

        st.write(
            f"**Sector / comunidad:** "
            f"{ultimo['Sector / comunidad']}"
        )

        st.write(
            f"**Tipo de uso:** "
            f"{ultimo['Tipo de uso']}"
        )

        if variacion is None:

            st.info(
                "No existe un registro anterior "
                "para calcular la variación."
            )

        elif variacion > 0:

            st.warning(
                f"📈 Variación respecto "
                f"al periodo anterior: "
                f"+{variacion:.2f}%"
            )

        elif variacion < 0:

            st.success(
                f"📉 Variación respecto "
                f"al periodo anterior: "
                f"{variacion:.2f}%"
            )

        st.write(
            f"**Tendencia reciente:** "
            f"{tendencia}"
        )

        pdf = crear_pdf(
            ultimo,
            historial
        )

        st.download_button(
            "📄 DESCARGAR REPORTE PDF",
            data=pdf,
            file_name=
                f"AquaLog_BI_{codigo}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        historial_csv = (
            historial
            .drop(
                columns=["Fecha_dt"]
            )
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

        st.download_button(
            "📊 DESCARGAR HISTORIAL CSV",
            data=historial_csv,
            file_name=
                f"AquaLog_Historial_{codigo}.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# 22. PROYECTO
# ============================================================

elif opcion == "ℹ️ Proyecto":

    st.title(
        "Proyecto AquaLog BI"
    )

    card(
        "Título del proyecto",
        "<b>Desarrollo de software basado "
        "en logaritmos matemáticos para "
        "la gestión eficiente del agua "
        "en el distrito de Baños del Inca, "
        "2026.</b>",
        "📘"
    )

    st.subheader(
        "🎯 Propósito"
    )

    st.write(
        "AquaLog BI busca convertir datos "
        "de consumo de agua en información "
        "útil mediante procesamiento matemático, "
        "análisis histórico, comparación de periodos "
        "y simulación de escenarios."
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

    st.subheader(
        "🚀 Capacidades del sistema"
    )

    funciones = [
        "Registro de información de consumo.",
        "Uso de diferentes sectores y contextos.",
        "Múltiples tipos de uso del agua.",
        "Cálculo del consumo diario.",
        "Cálculo de consumo unitario.",
        "Transformación logarítmica.",
        "Historial por código.",
        "Comparación entre periodos.",
        "Detección de variaciones.",
        "Análisis de tendencias.",
        "Centro de alertas.",
        "Simulación individual.",
        "Simulación colectiva.",
        "Proyección de ahorro.",
        "Estimación económica.",
        "Análisis por sectores.",
        "Ranking de consumo.",
        "Exportación CSV.",
        "Reportes PDF."
    ]

    for funcion in funciones:

        st.write(
            f"✅ {funcion}"
        )


# ============================================================
# 23. PIE DE PÁGINA
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
