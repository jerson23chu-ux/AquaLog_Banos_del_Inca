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

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #043b8f 0%,
                #0875d1 52%,
                #00a6c9 100%
            );
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
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
        box-shadow: 0 18px 45px rgba(8,92,160,0.22);
        color: white;
    }

    .hero-title {
        font-size: 45px;
        font-weight: 900;
        color: white !important;
    }

    .hero-subtitle {
        font-size: 20px;
        font-weight: 700;
        color: white !important;
        margin-bottom: 9px;
    }

    .hero-text {
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
        box-shadow: 0 8px 23px rgba(0,70,120,0.06);
        color: #294e62 !important;
    }

    .card h3 {
        color: #07527f !important;
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
    }

    .footer {
        text-align: center;
        color: #557286 !important;
        padding: 18px 0 5px 0;
        font-size: 13px;
    }

    .welcome-container {
        max-width: 1050px;
        margin: 35px auto 18px auto;
        background:
            linear-gradient(
                135deg,
                #043a91 0%,
                #0875d1 52%,
                #12b7dc 100%
            );
        border-radius: 30px;
        padding: 52px 46px;
        text-align: center;
        box-shadow: 0 22px 55px rgba(8,92,160,0.24);
    }

    .welcome-title {
        font-size: 58px;
        font-weight: 900;
        color: white !important;
    }

    .welcome-subtitle {
        font-size: 22px;
        font-weight: 700;
        color: #effcff !important;
        margin-bottom: 20px;
    }

    .welcome-badge {
        display: inline-block;
        margin: 5px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.24);
        color: white !important;
        font-size: 13px;
        font-weight: 700;
    }

    .welcome-project {
        max-width: 820px;
        margin: 24px auto 8px auto;
        padding: 18px 22px;
        border-radius: 18px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        color: #f4fdff !important;
        font-size: 16px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PANTALLA DE BIENVENIDA
# ============================================================

if "iniciado" not in st.session_state:
    st.session_state.iniciado = False

if not st.session_state.iniciado:

    st.markdown(
        '<div class="welcome-container">'
        '<div class="welcome-title">💧 AquaLog BI</div>'
        '<div class="welcome-subtitle">'
        'Inteligencia matemática para la gestión eficiente del agua'
        '</div>'
        '<span class="welcome-badge">'
        '🎓 Universidad Nacional de Cajamarca'
        '</span>'
        '<span class="welcome-badge">'
        '🌱 Curso: Educación Ambiental'
        '</span>'
        '<div class="welcome-project">'
        '<b>Desarrollo de software basado en logaritmos matemáticos '
        'para la gestión eficiente del agua en el distrito de '
        'Baños del Inca, 2026.</b><br><br>'
        'Registra, analiza, compara y simula escenarios de consumo '
        'y ahorro de agua mediante indicadores matemáticos.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(
        [1, 1.4, 1]
    )

    with c2:

        if st.button(
            "🚀 EMPEZAR",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.iniciado = True
            st.rerun()

    st.caption(
        "Universidad Nacional de Cajamarca · "
        "Educación Ambiental · Cajamarca · 2026"
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
        'Registra, analiza, compara y proyecta el consumo de agua '
        'mediante indicadores matemáticos, seguimiento histórico, '
        'alertas y escenarios de ahorro.'
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
            )
        ],

        "Institucional": [
            (
                "📊 Indicadores",
                "Compara el consumo entre periodos."
            ),
            (
                "🔧 Mantenimiento preventivo",
                "Programa inspecciones de conexiones."
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
# CARGA DE DATOS
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

    st.title("💧 AquaLog BI")

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

    if df.empty:

        card(
            "AquaLog BI está listo",
            "Aún no existen registros. "
            "Ingresa el primer consumo desde "
            "<b>Nuevo registro</b>.",
            "🚀"
        )

    else:

        total_consumo = (
            df[
                "Consumo del periodo (m³)"
            ].sum()
        )

        promedio = (
            df[
                "Consumo del periodo (m³)"
            ].mean()
        )

        codigos = (
            df["Código"]
            .nunique()
        )

        costo_total = (
            df[
                "Costo del periodo (S/)"
            ].sum()
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


# ============================================================
# NUEVO REGISTRO
# ============================================================

elif opcion == "➕ Nuevo registro":

    st.title(
        "Nuevo registro"
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
                            resultado["nivel"],
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

            st.session_state.df = pd.concat(
                [
                    df,
                    nuevo
                ],
                ignore_index=True
            )

            guardar_datos(
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

        tendencia = (
            tendencia_consumo(
                hist
            )
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

    st.write(
        "AquaLog BI procesa los datos de consumo "
        "mediante las siguientes expresiones:"
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

    st.info(
        "El índice logarítmico forma parte del "
        "modelo propuesto para el prototipo AquaLog BI."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        volumen = st.number_input(
            "V — Volumen (m³)",
            min_value=0.01,
            value=18.0
        )

    with c2:

        personas_motor = st.number_input(
            "P — Personas / unidades",
            min_value=1,
            value=4
        )

    with c3:

        dias_motor = st.number_input(
            "D — Días",
            min_value=1,
            value=30
        )

    cp = (
        volumen /
        (
            personas_motor *
            dias_motor
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

    st.success(
        "DATOS → PROCESAMIENTO → MODELO MATEMÁTICO → "
        "INDICADORES → INTERPRETACIÓN → DECISIÓN"
    )


# ============================================================
# PROYECTO
# ============================================================

elif opcion == "ℹ️ Proyecto":

    # ESTA PARTE ESTÁ HECHA CON COMPONENTES NATIVOS
    # PARA EVITAR EL PROBLEMA DE LOS <div>

    st.title(
        "💧 Proyecto AquaLog BI"
    )

    st.success(
        "🎓 UNIVERSIDAD NACIONAL DE CAJAMARCA"
    )

    st.info(
        "🌱 **Curso: Educación Ambiental**"
    )

    st.subheader(
        "📘 Proyecto de investigación"
    )

    st.write(
        "**Desarrollo de software basado en logaritmos matemáticos "
        "para la gestión eficiente del agua en el distrito de "
        "Baños del Inca, 2026.**"
    )

    st.divider()

    st.subheader(
        "🎯 Propósito del sistema"
    )

    st.write(
        "AquaLog BI convierte datos de consumo de agua "
        "en indicadores matemáticos, análisis comparativos "
        "y escenarios de ahorro orientados al apoyo de "
        "la toma de decisiones."
    )

    st.success(
        "💧 MEDIR → 🧮 ANALIZAR → 📊 COMPARAR → "
        "🎯 PROYECTAR → ✅ DECIDIR"
    )

    st.divider()

    st.subheader(
        "🎓 Datos académicos"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "🏛️ **Universidad**\n\n"
            "Universidad Nacional de Cajamarca"
        )

    with col2:

        st.info(
            "🌱 **Curso**\n\n"
            "Educación Ambiental"
        )

    st.subheader(
        "👩‍🏫 Docente"
    )

    st.info(
        "**Paola Ponce**"
    )

    st.divider()

    st.subheader(
        "👥 Equipo de desarrollo"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "👤 **Chuquiruna Escobal, Jhersonn**"
        )

        st.write(
            "👤 **Vasquez Azañero, Diego**"
        )

    with col2:

        st.write(
            "👤 **Paz Muñoz, Vili**"
        )

        st.write(
            "👤 **Vasquez Bustamante, Nathan Lowell**"
        )

    st.divider()

    st.subheader(
        "💧 ¿Qué hace AquaLog BI?"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📝 **REGISTRO**\n\n"
            "Almacena información de consumo "
            "de agua por código y periodo."
        )

    with col2:

        st.info(
            "🧮 **ANÁLISIS**\n\n"
            "Calcula indicadores y procesa los datos "
            "mediante el modelo matemático."
        )

    with col3:

        st.info(
            "🎯 **DECISIÓN**\n\n"
            "Compara periodos y permite simular "
            "escenarios de ahorro."
        )

    st.divider()

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
        "El índice logarítmico corresponde al modelo "
        "propuesto dentro del prototipo AquaLog BI."
    )

    st.success(
        "DATOS → PROCESAMIENTO → MODELO MATEMÁTICO → "
        "INDICADORES → INTERPRETACIÓN → DECISIÓN"
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    '💧 <strong>AquaLog BI</strong><br>'
    'Inteligencia matemática para la gestión eficiente del agua<br>'
    'Universidad Nacional de Cajamarca · Educación Ambiental<br>'
    'Baños del Inca · Cajamarca · 2026'
    '</div>',
    unsafe_allow_html=True
)
