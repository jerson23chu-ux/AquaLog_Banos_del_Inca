import streamlit as st
import pandas as pd
import math
import os
from datetime import date


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
# ESTILOS
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

    /* =======================================================
       BARRA LATERAL
       ======================================================= */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #043b8f 0%,
                #0875d1 52%,
                #00a6c9 100%
            );
        border-right: 1px solid rgba(255,255,255,0.14);
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

    /* =======================================================
       CONTROLES
       ======================================================= */

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

    /* =======================================================
       MÉTRICAS
       ======================================================= */

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

    /* =======================================================
       HERO PRINCIPAL
       ======================================================= */

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

    /* =======================================================
       TARJETAS
       ======================================================= */

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

    /* =======================================================
       ALERTAS
       ======================================================= */

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

    /* =======================================================
       PORTADA DE BIENVENIDA
       ======================================================= */

    .welcome-container {
        max-width: 1100px;
        margin: 20px auto 15px auto;

        background:
            linear-gradient(
                135deg,
                #043a91 0%,
                #076ec5 46%,
                #10aed5 100%
            );

        border-radius: 32px;
        padding: 52px 55px;

        box-shadow:
            0 25px 65px
            rgba(0,70,130,0.25);

        text-align: center;
        color: white;
    }

    .welcome-drop {
        font-size: 70px;
        margin-bottom: 5px;
    }

    .welcome-title {
        font-size: 60px;
        font-weight: 900;
        line-height: 1;
        color: white !important;
        margin-bottom: 12px;
    }

    .welcome-subtitle {
        font-size: 23px;
        font-weight: 700;
        color: #e7faff !important;
        margin-bottom: 26px;
    }

    .welcome-university {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 999px;
        padding: 9px 18px;
        margin: 5px;
        color: white !important;
        font-weight: 700;
        font-size: 14px;
    }

    .welcome-project {
        max-width: 850px;
        margin: 27px auto 10px auto;
        padding: 21px 25px;
        border-radius: 19px;
        background: rgba(255,255,255,0.11);
        border: 1px solid rgba(255,255,255,0.18);
        color: #f2fcff !important;
        font-size: 16px;
        line-height: 1.65;
    }

    .welcome-year {
        margin-top: 20px;
        color: #dff7ff !important;
        font-size: 14px;
        font-weight: 600;
    }

    /* Botón empezar */

    div[data-testid="stButton"] > button {
        border-radius: 14px;
        font-weight: 800;
        min-height: 48px;
    }

    .footer {
        text-align: center;
        color: #557286 !important;
        padding: 18px 0 5px 0;
        font-size: 13px;
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
# ESTADO DE LA PANTALLA DE BIENVENIDA
# ============================================================

if "iniciado" not in st.session_state:
    st.session_state.iniciado = False


# ============================================================
# PANTALLA DE BIENVENIDA
# ============================================================

if not st.session_state.iniciado:

    # Ocultamos el sidebar mientras se muestra la portada
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-container">'
        '<div class="welcome-drop">💧</div>'
        '<div class="welcome-title">AquaLog BI</div>'
        '<div class="welcome-subtitle">'
        'Inteligencia matemática para la gestión eficiente del agua'
        '</div>'
        '<span class="welcome-university">🎓 Universidad Nacional de Cajamarca</span>'
        '<span class="welcome-university">🌱 Curso: Educación Ambiental</span>'
        '<div class="welcome-project">'
        '<b>Desarrollo de software basado en logaritmos matemáticos para la '
        'gestión eficiente del agua en el distrito de Baños del Inca, 2026.</b>'
        '<br><br>'
        'Una herramienta digital orientada al registro, análisis, comparación '
        'y simulación del consumo de agua mediante indicadores matemáticos.'
        '</div>'
        '<div class="welcome-year">'
        'Baños del Inca · Cajamarca · 2026'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    izquierda, centro, derecha = st.columns([2, 2, 2])

    with centro:

        if st.button(
            "🚀 EMPEZAR",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.iniciado = True
            st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:25px;
            color:#557286;
            font-size:13px;
        ">
            Universidad Nacional de Cajamarca · Educación Ambiental
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# COMPONENTES VISUALES
# ============================================================

def hero():

    st.markdown(
        '<div class="hero">'
        '<div class="hero-title">💧 AquaLog BI</div>'
        '<div class="hero-subtitle">'
        'Inteligencia matemática para la gestión eficiente del agua'
        '</div>'
        '<div class="hero-text">'
        'Registra, analiza, compara y proyecta el consumo de agua mediante '
        'indicadores matemáticos, seguimiento histórico, alertas y escenarios '
        'de ahorro.'
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
# MOTOR MATEMÁTICO
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
        (
            personas *
            dias
        )
    )

    litros_persona_dia = (
        cp * 1000
    )

    indice_log = math.log10(
        1 + cp
    )

    costo = (
        consumo *
        tarifa
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
        "consumo_diario":
            consumo_diario,

        "cp":
            cp,

        "litros_persona_dia":
            litros_persona_dia,

        "indice_log":
            indice_log,

        "nivel":
            nivel,

        "costo":
            costo
    }


# ============================================================
# HISTORIAL
# ============================================================

def historial_codigo(
    df,
    codigo
):

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


def variacion_ultimo_periodo(
    historial
):

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
        (
            actual -
            anterior
        )
        /
        anterior
    ) * 100


def tendencia_consumo(
    historial
):

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

def generar_alertas(
    df
):

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

        variacion = (
            variacion_ultimo_periodo(
                hist
            )
        )

        if variacion is None:

            continue

        if variacion >= 20:

            alertas.append(
                {
                    "tipo": "rojo",
                    "titulo":
                        f"🔴 Aumento importante — {codigo}",
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
                    "titulo":
                        f"🟢 Reducción detectada — {codigo}",
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
                    "titulo":
                        f"🟡 Tendencia creciente — {codigo}",
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
                "Evita mantener los caños abiertos "
                "cuando el agua no sea necesaria."
            ),

            (
                "🚿 Duchas más eficientes",
                "Reducir algunos minutos de ducha "
                "puede disminuir el consumo acumulado."
            ),

            (
                "🔧 Revisión de fugas",
                "Inspecciona conexiones, inodoros, "
                "tanques y grifos."
            ),

            (
                "📊 Seguimiento",
                "Compara cada nuevo registro con "
                "el periodo anterior."
            )
        ],

        "Comercial": [

            (
                "📋 Control por actividad",
                "Identifica cuáles actividades "
                "concentran el mayor consumo."
            ),

            (
                "🔧 Mantenimiento",
                "Revisa instalaciones y equipos "
                "que utilizan agua."
            ),

            (
                "🎯 Metas de ahorro",
                "Establece reducciones graduales "
                "y compara resultados."
            )
        ],

        "Educativo": [

            (
                "🏫 Sensibilización",
                "Promueve hábitos responsables "
                "entre estudiantes y trabajadores."
            ),

            (
                "🚰 Servicios higiénicos",
                "Controla fugas y consumos innecesarios."
            ),

            (
                "📈 Seguimiento periódico",
                "Analiza la evolución del consumo "
                "de cada periodo."
            )
        ],

        "Institucional": [

            (
                "📊 Indicadores",
                "Compara consumo entre periodos "
                "y áreas."
            ),

            (
                "🔧 Mantenimiento preventivo",
                "Programa inspecciones de conexiones "
                "e instalaciones."
            ),

            (
                "🎯 Objetivos de reducción",
                "Define metas de consumo medibles."
            )
        ],

        "Riego": [

            (
                "🌅 Horario",
                "Realiza el riego en horarios "
                "de menor evaporación."
            ),

            (
                "💧 Dosificación",
                "Evita aplicar más agua de la necesaria."
            ),

            (
                "🔍 Inspección",
                "Revisa mangueras, uniones y "
                "sistemas de distribución."
            )
        ],

        "Otro": [

            (
                "📊 Medición",
                "Registra el consumo periódicamente."
            ),

            (
                "🔍 Identificación de pérdidas",
                "Revisa posibles usos innecesarios "
                "o fugas."
            ),

            (
                "🎯 Proyección",
                "Utiliza el simulador para establecer "
                "metas de reducción."
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
                "El valor calculado se encuentra "
                "en el nivel alto según los criterios "
                "referenciales del prototipo."
            )
        )

    return lista


# ============================================================
# CARGAR DATOS
# ============================================================

if "df" not in st.session_state:

    st.session_state.df = (
        cargar_datos()
    )

df = normalizar_df(
    st.session_state.df
)


# ============================================================
# MENÚ LATERAL
# ============================================================

with st.sidebar:

    st.title(
        "💧 AquaLog BI"
    )

    st.caption(
        "Gestión inteligente del agua"
    )

    st.caption(
        "Universidad Nacional de Cajamarca"
    )

    st.caption(
        "Curso: Educación Ambiental"
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
            "ℹ️ Proyecto"
        ]
    )

    st.divider()

    st.caption(
        "Sistema adaptable a distintos "
        "sectores, comunidades y tipos de uso."
    )

    st.divider()

    if st.button(
        "← Volver al inicio",
        use_container_width=True
    ):

        st.session_state.iniciado = False

        st.rerun()


# ============================================================
# ENCABEZADO
# ============================================================

hero()


# ============================================================
# CENTRO DE CONTROL
# ============================================================

if opcion == "🏠 Centro de control":

    st.title(
        "Centro de control"
    )

    st.caption(
        "Vista general del comportamiento "
        "de los registros almacenados en AquaLog BI."
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

        total_consumo = (
            df[
                "Consumo del periodo (m³)"
            ]
            .sum()
        )

        promedio = (
            df[
                "Consumo del periodo (m³)"
            ]
            .mean()
        )

        codigos = (
            df["Código"]
            .nunique()
        )

        costo_total = (
            df[
                "Costo del periodo (S/)"
            ]
            .sum()
        )

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

        c1, c2, c3, c4 = (
            st.columns(4)
        )

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
            "🏆 Mayores consumos registrados"
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

            personas = (
                st.number_input(
                    "👥 Personas o unidades de referencia",
                    min_value=1,
                    max_value=100000,
                    value=4
                )
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

            tarifa = (
                st.number_input(
                    "💰 Tarifa (S/ por m³)",
                    min_value=0.0,
                    value=0.0,
                    step=0.1
                )
            )

        observaciones = (
            st.text_area(
                "📝 Observaciones"
            )
        )

        enviar = (
            st.form_submit_button(
                "💧 ANALIZAR Y GUARDAR",
                use_container_width=True
            )
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
                        "Código":
                            codigo,

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

            df = normalizar_df(
                st.session_state.df
            )

            st.success(
                "✅ Registro guardado correctamente."
            )

            r1, r2, r3, r4 = (
                st.columns(4)
            )

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
                "Costo estimado",
                f'S/ {resultado["costo"]:.2f}'
            )

            if tipo_uso == "Doméstico":

                st.subheader(
                    "🚦 Clasificación"
                )

                if resultado["nivel"] == "BAJO":

                    st.success(
                        "🟢 NIVEL BAJO"
                    )

                elif resultado["nivel"] == "MODERADO":

                    st.warning(
                        "🟡 NIVEL MODERADO"
                    )

                else:

                    st.error(
                        "🔴 NIVEL ALTO"
                    )

                st.caption(
                    "Clasificación referencial utilizada "
                    "por el prototipo AquaLog BI."
                )

            else:

                st.info(
                    "Para usos no domésticos se realiza "
                    "un análisis general sin aplicar los "
                    "rangos domésticos."
                )


# ============================================================
# FICHA INDIVIDUAL
# ============================================================

elif opcion == "👤 Ficha individual":

    st.title(
        "Ficha individual"
    )

    st.caption(
        "Consulta la evolución histórica "
        "de un código registrado."
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

        ultimo = (
            hist.iloc[-1]
        )

        variacion = (
            variacion_ultimo_periodo(
                hist
            )
        )

        tendencia = (
            tendencia_consumo(
                hist
            )
        )

        st.subheader(
            f"💧 Código {codigo}"
        )

        st.write(
            f"**Sector / comunidad:** "
            f"{ultimo['Sector / comunidad']}"
        )

        st.write(
            f"**Zona / referencia:** "
            f"{ultimo['Zona / referencia']}"
        )

        st.write(
            f"**Tipo de uso:** "
            f"{ultimo['Tipo de uso']}"
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

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

        grafico = (
            grafico.dropna()
        )

        if not grafico.empty:

            grafico = (
                grafico.set_index(
                    "Fecha_dt"
                )
            )

            st.line_chart(
                grafico
            )

        st.subheader(
            "🔎 Interpretación"
        )

        if variacion is None:

            st.info(
                "Se necesitan al menos dos registros "
                "para realizar una comparación entre periodos."
            )

        elif variacion > 0:

            st.warning(
                f"📈 El consumo aumentó "
                f"{variacion:.2f}% respecto "
                f"al periodo anterior."
            )

        elif variacion < 0:

            st.success(
                f"📉 El consumo disminuyó "
                f"{abs(variacion):.2f}% respecto "
                f"al periodo anterior."
            )

        else:

            st.info(
                "El consumo se mantuvo sin variación."
            )

        st.write(
            f"**Tendencia reciente:** {tendencia}"
        )

        st.subheader(
            "📋 Historial"
        )

        st.dataframe(
            hist.drop(
                columns=[
                    "Fecha_dt"
                ]
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

    st.caption(
        "Consulta y descarga los registros "
        "almacenados en AquaLog BI."
    )

    if df.empty:

        st.info(
            "No existen registros."
        )

    else:

        c1, c2 = st.columns(2)

        with c1:

            tipos_disponibles = [
                "Todos"
            ] + sorted(
                df["Tipo de uso"]
                .astype(str)
                .unique()
                .tolist()
            )

            filtro_tipo = st.selectbox(
                "Tipo de uso",
                tipos_disponibles
            )

        with c2:

            sectores_disponibles = [
                "Todos"
            ] + sorted(
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

            filtro_sector = st.selectbox(
                "Sector / comunidad",
                sectores_disponibles
            )

        filtrado = df.copy()

        if filtro_tipo != "Todos":

            filtrado = filtrado[
                filtrado["Tipo de uso"] ==
                filtro_tipo
            ]

        if filtro_sector != "Todos":

            filtrado = filtrado[
                filtrado[
                    "Sector / comunidad"
                ] ==
                filtro_sector
            ]

        st.metric(
            "Registros encontrados",
            len(filtrado)
        )

        st.dataframe(
            filtrado,
            use_container_width=True,
            hide_index=True
        )

        csv = filtrado.to_csv(
            index=False
        ).encode(
            "utf-8-sig"
        )

        st.download_button(
            "📥 DESCARGAR DATOS CSV",
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

    st.caption(
        "Evalúa posibles escenarios de reducción "
        "del consumo sin modificar los registros guardados."
    )

    tab1, tab2 = st.tabs(
        [
            "👤 Escenario individual",
            "🌎 Escenario colectivo"
        ]
    )

    with tab1:

        consumo_base = (
            st.number_input(
                "💧 Consumo actual por periodo (m³)",
                min_value=0.01,
                value=20.0,
                step=0.1
            )
        )

        tarifa_sim = (
            st.number_input(
                "💰 Tarifa estimada (S/ por m³)",
                min_value=0.0,
                value=1.5,
                step=0.1
            )
        )

        reduccion = (
            st.slider(
                "🎯 Meta de reducción",
                0,
                50,
                15,
                1,
                format="%d%%"
            )
        )

        nuevo = (
            consumo_base *
            (
                1 -
                reduccion / 100
            )
        )

        ahorro = (
            consumo_base -
            nuevo
        )

        ahorro_economico = (
            ahorro *
            tarifa_sim
        )

        c1, c2, c3, c4 = (
            st.columns(4)
        )

        c1.metric(
            "Consumo actual",
            f"{consumo_base:.2f} m³"
        )

        c2.metric(
            "Consumo proyectado",
            f"{nuevo:.2f} m³"
        )

        c3.metric(
            "Agua ahorrada",
            f"{ahorro:.2f} m³"
        )

        c4.metric(
            "Ahorro económico",
            f"S/ {ahorro_economico:.2f}"
        )

        escenarios = pd.DataFrame(
            {
                "Escenario": [
                    "Actual",
                    "Ahorro 5%",
                    "Ahorro 10%",
                    "Ahorro 15%",
                    "Ahorro 20%",
                    "Ahorro 25%",
                    f"Meta {reduccion}%"
                ],

                "Consumo (m³)": [
                    consumo_base,
                    consumo_base * 0.95,
                    consumo_base * 0.90,
                    consumo_base * 0.85,
                    consumo_base * 0.80,
                    consumo_base * 0.75,
                    nuevo
                ]
            }
        )

        st.subheader(
            "📊 Comparación de escenarios"
        )

        st.bar_chart(
            escenarios.set_index(
                "Escenario"
            )
        )

    with tab2:

        unidades = (
            st.number_input(
                "👥 Número de unidades o puntos",
                min_value=1,
                value=10
            )
        )

        consumo_promedio = (
            st.number_input(
                "💧 Consumo promedio por unidad",
                min_value=0.01,
                value=18.0,
                step=0.1
            )
        )

        meta = (
            st.slider(
                "🎯 Meta colectiva",
                0,
                50,
                15,
                1,
                format="%d%%"
            )
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

        proyectado_total = (
            consumo_total -
            ahorro_total
        )

        c1, c2, c3 = (
            st.columns(3)
        )

        c1.metric(
            "Consumo total actual",
            f"{consumo_total:.2f} m³"
        )

        c2.metric(
            "Consumo proyectado",
            f"{proyectado_total:.2f} m³"
        )

        c3.metric(
            "Ahorro colectivo",
            f"{ahorro_total:.2f} m³"
        )


# ============================================================
# ANÁLISIS
# ============================================================

elif opcion == "📈 Análisis":

    st.title(
        "Análisis dinámico"
    )

    st.caption(
        "Explora patrones generales de consumo "
        "a partir de los registros almacenados."
    )

    if df.empty:

        st.info(
            "No existen registros."
        )

    else:

        st.subheader(
            "📊 Consumo por tipo de uso"
        )

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

        st.bar_chart(
            por_tipo
        )

        if len(por_tipo) > 0:

            mayor_tipo = (
                por_tipo.index[0]
            )

            mayor_valor = (
                por_tipo.iloc[0]
            )

            st.info(
                f"💧 El tipo de uso con mayor "
                f"consumo acumulado es "
                f"**{mayor_tipo}**, con "
                f"**{mayor_valor:.2f} m³**."
            )

        st.subheader(
            "🗓️ Evolución temporal"
        )

        temporal = df.copy()

        temporal["Fecha"] = (
            pd.to_datetime(
                temporal["Fecha"],
                errors="coerce"
            )
        )

        evolucion = (
            temporal.dropna(
                subset=[
                    "Fecha"
                ]
            )
            .groupby(
                "Fecha"
            )[
                "Consumo del periodo (m³)"
            ]
            .sum()
            .sort_index()
        )

        st.line_chart(
            evolucion
        )

        st.subheader(
            "📍 Promedio por sector o comunidad"
        )

        sectores = df.copy()

        sectores[
            "Sector / comunidad"
        ] = sectores[
            "Sector / comunidad"
        ].replace(
            "",
            "Sin especificar"
        )

        promedio_sector = (
            sectores.groupby(
                "Sector / comunidad"
            )[
                "Consumo del periodo (m³)"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            promedio_sector
        )


# ============================================================
# ALERTAS
# ============================================================

elif opcion == "🚨 Alertas":

    st.title(
        "Centro de alertas"
    )

    st.caption(
        "Las alertas se basan en reglas "
        "operativas del prototipo AquaLog BI."
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

            st.metric(
                "Alertas detectadas",
                len(alertas)
            )

            for alerta in alertas:

                alerta_html(
                    alerta["tipo"],
                    alerta["titulo"],
                    alerta["texto"]
                )

        st.caption(
            "Reglas utilizadas: incremento igual "
            "o superior al 20 %, reducción igual "
            "o superior al 10 % y tendencia "
            "creciente en tres registros consecutivos."
        )


# ============================================================
# RECOMENDACIONES
# ============================================================

elif opcion == "💡 Recomendaciones":

    st.title(
        "Recomendaciones"
    )

    st.caption(
        "Selecciona el tipo de uso para "
        "consultar acciones orientativas."
    )

    tipo = st.selectbox(
        "Tipo de uso",
        TIPOS_USO
    )

    nivel = None

    if tipo == "Doméstico":

        nivel = st.selectbox(
            "Nivel de consumo",
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

    st.caption(
        "Visualiza cómo AquaLog BI transforma "
        "los datos registrados en indicadores."
    )

    card(
        "Etapa 1 — Consumo unitario diario",
        "El volumen registrado se relaciona "
        "con el número de personas o unidades "
        "de referencia y los días del periodo.",
        "1️⃣"
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

    card(
        "Etapa 2 — Transformación logarítmica",
        "AquaLog BI transforma el valor "
        "calculado mediante un logaritmo "
        "decimal.",
        "2️⃣"
    )

    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )

    st.info(
        "El índice logarítmico forma parte "
        "del modelo propuesto para el prototipo "
        "AquaLog BI."
    )

    st.subheader(
        "🧪 Prueba del modelo"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        volumen = (
            st.number_input(
                "V — Volumen (m³)",
                min_value=0.01,
                value=18.0
            )
        )

    with c2:

        personas_motor = (
            st.number_input(
                "P — Personas / unidades",
                min_value=1,
                value=4
            )
        )

    with c3:

        dias_motor = (
            st.number_input(
                "D — Días",
                min_value=1,
                value=30
            )
        )

    cp = (
        volumen /
        (
            personas_motor *
            dias_motor
        )
    )

    il = math.log10(
        1 +
        cp
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

    st.success(
        "DATOS → PROCESAMIENTO → "
        "MODELO MATEMÁTICO → INDICADORES "
        "→ INTERPRETACIÓN → DECISIÓN"
    )


# ============================================================
# PROYECTO
# ============================================================

elif opcion == "ℹ️ Proyecto":

    st.title(
        "Proyecto AquaLog BI"
    )

    st.markdown(
        """
        <div style="
            background: linear-gradient(
                120deg,
                #043a91,
                #0796ce
            );
            padding: 25px 28px;
            border-radius: 22px;
            margin-bottom: 20px;
            color: white;
            box-shadow: 0 10px 30px rgba(0,80,150,0.15);
        ">
            <div style="
                font-size: 14px;
                font-weight: 700;
                opacity: 0.9;
            ">
                UNIVERSIDAD NACIONAL DE CAJAMARCA
            </div>

            <div style="
                font-size: 27px;
                font-weight: 900;
                margin-top: 5px;
                color: white;
            ">
                💧 AquaLog BI
            </div>

            <div style="
                font-size: 16px;
                margin-top: 9px;
                color: #ecfbff;
            ">
                Curso: Educación Ambiental
            </div>
        </div>
        """,
        unsafe_allow_html=True
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
        "🎓 Datos académicos"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            "🏛️ **Universidad:** "
            "Universidad Nacional de Cajamarca"
        )

    with c2:

        st.info(
            "🌱 **Curso:** Educación Ambiental"
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
        "**Paola Ponce**"
    )

    st.subheader(
        "👥 Equipo de desarrollo"
    )

    c1, c2 = st.columns(2)

    with c1:

        card(
            "Chuquiruna Escobal, Jhersonn",
            "Integrante del equipo AquaLog BI.",
            "👤"
        )

        card(
            "Vasquez Azañero, Diego",
            "Integrante del equipo AquaLog BI.",
            "👤"
        )

    with c2:

        card(
            "Paz Muñoz, Vili",
            "Integrante del equipo AquaLog BI.",
            "👤"
        )

        card(
            "Vasquez Bustamante, Nathan Lowell",
            "Integrante del equipo AquaLog BI.",
            "👤"
        )

    st.subheader(
        "💧 ¿Qué hace AquaLog BI?"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        card(
            "Registro",
            "Almacena información de consumo "
            "de agua por código y periodo.",
            "📝"
        )

    with c2:

        card(
            "Análisis",
            "Calcula indicadores y transforma "
            "los datos mediante el modelo matemático.",
            "🧮"
        )

    with c3:

        card(
            "Decisión",
            "Permite comparar periodos, detectar "
            "cambios y simular escenarios de ahorro.",
            "🎯"
        )

    st.subheader(
        "🧮 Fundamento matemático"
    )

    st.latex(
        r"C_p=\frac{V}{P\times D}"
    )

    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )

    st.caption(
        "El índice logarítmico corresponde "
        "al modelo propuesto dentro del prototipo "
        "AquaLog BI."
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    '💧 <strong>AquaLog BI</strong><br>'
    'Universidad Nacional de Cajamarca · '
    'Curso de Educación Ambiental<br>'
    'Baños del Inca · Cajamarca · 2026'
    '</div>',
    unsafe_allow_html=True
)
