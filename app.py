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
                circle at 10% 10%,
                rgba(0, 174, 239, 0.10),
                transparent 24%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(0, 92, 230, 0.09),
                transparent 26%
            ),
            linear-gradient(
                135deg,
                #f6fcff 0%,
                #eaf7ff 55%,
                #ffffff 100%
            );

        color: #17384d;
    }


    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }


    h1,
    h2,
    h3 {
        color: #0b4f7c !important;
    }


    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #063d9d 0%,
                #0875d1 55%,
                #00a7cf 100%
            );

        border-right:
            1px solid
            rgba(255,255,255,0.15);
    }


    [data-testid="stSidebar"] * {
        color: white !important;
    }


    [data-testid="stSidebar"]
    [data-testid="stRadio"] label {
        padding: 0.35rem 0.5rem;
        border-radius: 10px;
    }


    [data-testid="stSidebar"]
    [data-testid="stRadio"] label:hover {
        background:
            rgba(255,255,255,0.10);
    }


    div[data-testid="stMetric"] {
        background:
            rgba(255,255,255,0.96);

        border:
            1px solid
            rgba(10, 100, 160, 0.10);

        padding:
            18px 18px;

        border-radius:
            18px;

        box-shadow:
            0 8px 24px
            rgba(0, 70, 120, 0.07);
    }


    [data-testid="stMetricValue"] {
        color:
            #0b63ce !important;

        font-weight:
            800;
    }


    [data-testid="stMetricLabel"] {
        color:
            #3f6277 !important;

        font-weight:
            700;
    }


    .hero {
        background:
            linear-gradient(
                120deg,
                #063d9d 0%,
                #0875d1 52%,
                #12b9dc 100%
            );

        border-radius:
            28px;

        padding:
            30px 34px;

        margin-bottom:
            24px;

        box-shadow:
            0 18px 45px
            rgba(8, 92, 160, 0.22);

        color:
            white;

        position:
            relative;

        overflow:
            hidden;
    }


    .hero-title {
        font-size:
            46px;

        line-height:
            1.05;

        font-weight:
            850;

        margin-bottom:
            8px;

        color:
            white !important;
    }


    .hero-subtitle {
        font-size:
            19px;

        font-weight:
            650;

        color:
            white !important;

        margin-bottom:
            8px;
    }


    .hero-text {
        font-size:
            15px;

        color:
            #eefbff !important;

        max-width:
            900px;

        line-height:
            1.55;
    }


    .hero-chip {
        display:
            inline-block;

        margin:
            10px 6px 0 0;

        padding:
            7px 12px;

        border-radius:
            999px;

        border:
            1px solid
            rgba(255,255,255,0.25);

        background:
            rgba(255,255,255,0.13);

        color:
            white !important;

        font-size:
            12px;

        font-weight:
            700;
    }


    .info-card {
        background:
            rgba(255,255,255,0.96);

        border:
            1px solid
            rgba(10, 100, 160, 0.10);

        border-radius:
            18px;

        padding:
            18px 20px;

        box-shadow:
            0 8px 24px
            rgba(0, 70, 120, 0.06);

        margin:
            8px 0 14px 0;
    }


    .tip-card {
        background:
            white;

        border-left:
            6px solid #0b8fe3;

        border-radius:
            14px;

        padding:
            15px 18px;

        margin:
            9px 0;

        box-shadow:
            0 5px 16px
            rgba(0,0,0,0.05);
    }


    .credit-card {
        background:
            linear-gradient(
                135deg,
                #ffffff,
                #eef9ff
            );

        border:
            1px solid #d1edf9;

        border-radius:
            15px;

        padding:
            14px 16px;

        margin:
            8px 0;
    }


    .footer {
        text-align:
            center;

        color:
            #557286;

        padding:
            18px 0 4px 0;

        font-size:
            13px;
    }


    .stButton button {
        border:
            none;

        border-radius:
            12px;

        font-weight:
            700;
    }


    .stDownloadButton button {
        border-radius:
            12px;

        font-weight:
            700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DE INTERFAZ
# ============================================================

def hero():

    contenido = (
        '<div class="hero">'
        '<div class="hero-title">💧 AquaLog BI</div>'
        '<div class="hero-subtitle">'
        'Analiza, compara y proyecta el consumo de agua'
        '</div>'
        '<div class="hero-text">'
        'Sistema interactivo para registrar consumos, '
        'explorar patrones, simular escenarios de ahorro '
        'y apoyar decisiones para un uso más eficiente del agua.'
        '</div>'
        '<span class="hero-chip">📍 Ubicación configurable</span>'
        '<span class="hero-chip">🏠 Múltiples tipos de uso</span>'
        '<span class="hero-chip">📊 Análisis dinámico</span>'
        '<span class="hero-chip">🧮 Modelo matemático</span>'
        '</div>'
    )

    st.markdown(
        contenido,
        unsafe_allow_html=True
    )


def info_card(
    titulo,
    texto,
    icono="💧"
):

    st.markdown(
        f'<div class="info-card">'
        f'<h3>{icono} {titulo}</h3>'
        f'<p>{texto}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def tip_card(
    titulo,
    texto
):

    st.markdown(
        f'<div class="tip-card">'
        f'<strong>{titulo}</strong>'
        f'<br>{texto}'
        f'</div>',
        unsafe_allow_html=True
    )


def credit_card(
    texto,
    icono="👤"
):

    st.markdown(
        f'<div class="credit-card">'
        f'{icono} '
        f'<strong>{texto}</strong>'
        f'</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FUNCIONES DE DATOS
# ============================================================

def dataframe_vacio():

    return pd.DataFrame(
        columns=COLUMNAS
    )


def normalizar_df(df):

    if df is None or df.empty:

        return dataframe_vacio()


    df = df.copy()


    # --------------------------------------------------------
    # COMPATIBILIDAD CON TU APP ANTERIOR
    # --------------------------------------------------------

    equivalencias = {

        "Hogar":
            "Código",

        "Sector":
            "Sector / comunidad",

        "CAS":
            "Zona / referencia",

        "Habitantes":
            "Personas",

        "Consumo mensual (m³)":
            "Consumo del periodo (m³)",

        "Costo mensual (S/)":
            "Costo del periodo (S/)"

    }


    for antigua, nueva in (
        equivalencias.items()
    ):

        if (
            antigua in df.columns
            and
            nueva not in df.columns
        ):

            df[nueva] = (
                df[antigua]
            )


    # --------------------------------------------------------
    # VALORES POR DEFECTO
    # --------------------------------------------------------

    defaults = {

        "Código":
            "",

        "Fecha":
            pd.Timestamp
            .today()
            .strftime(
                "%Y-%m-%d"
            ),

        "Sector / comunidad":
            "",

        "Zona / referencia":
            "",

        "Tipo de uso":
            "Doméstico",

        "Personas":
            1,

        "Consumo del periodo (m³)":
            0.0,

        "Días":
            30,

        "Tarifa (S/ por m³)":
            0.0,

        "Consumo diario (m³)":
            0.0,

        "Consumo por persona (L/día)":
            0.0,

        "Índice logarítmico":
            0.0,

        "Nivel":
            "SIN CLASIFICAR",

        "Costo del periodo (S/)":
            0.0,

        "Observaciones":
            ""

    }


    for columna, valor in (
        defaults.items()
    ):

        if columna not in df.columns:

            df[columna] = valor


    # --------------------------------------------------------
    # CONVERTIR DATOS NUMÉRICOS
    # --------------------------------------------------------

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

        df[columna] = (

            pd.to_numeric(

                df[columna],

                errors="coerce"

            )

            .fillna(0)

        )


    df["Personas"] = (

        df["Personas"]

        .replace(
            0,
            1
        )

        .astype(int)

    )


    df["Días"] = (

        df["Días"]

        .replace(
            0,
            30
        )

        .astype(int)

    )


    df["Tipo de uso"] = (

        df["Tipo de uso"]

        .replace(
            "",
            "Doméstico"
        )

    )


    fecha_actual = (

        pd.Timestamp

        .today()

        .strftime(
            "%Y-%m-%d"
        )

    )


    df["Fecha"] = (

        df["Fecha"]

        .astype(str)

        .replace(

            {

                "":
                    fecha_actual,

                "nan":
                    fecha_actual

            }

        )

    )


    return df[COLUMNAS]


# ============================================================
# CARGAR DATOS
# ============================================================

def cargar_datos():

    if os.path.exists(
        ARCHIVO_DATOS
    ):

        try:

            df = pd.read_csv(
                ARCHIVO_DATOS
            )

            return normalizar_df(
                df
            )

        except Exception:

            return dataframe_vacio()


    return dataframe_vacio()


# ============================================================
# GUARDAR DATOS
# ============================================================

def guardar_datos(df):

    df = normalizar_df(
        df
    )


    df.to_csv(

        ARCHIVO_DATOS,

        index=False,

        encoding=
        "utf-8-sig"

    )


# ============================================================
# MODELO MATEMÁTICO
# ============================================================

def analizar_consumo(
    personas,
    consumo_m3,
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

        consumo_m3 /
        dias

    )


    consumo_persona_m3_dia = (

        consumo_m3 /

        (
            personas *
            dias
        )

    )


    litros_persona_dia = (

        consumo_persona_m3_dia *
        1000

    )


    indice_log = (

        math.log10(

            1 +
            consumo_persona_m3_dia

        )

    )


    costo = (

        consumo_m3 *
        tarifa

    )


    # --------------------------------------------------------
    # CLASIFICACIÓN DOMÉSTICA
    # --------------------------------------------------------

    if tipo_uso == "Doméstico":

        if litros_persona_dia < 100:

            nivel = "BAJO"


        elif litros_persona_dia <= 170:

            nivel = "MODERADO"


        else:

            nivel = "ALTO"


    else:

        nivel = (
            "ANÁLISIS GENERAL"
        )


    return {

        "consumo_diario":
            consumo_diario,

        "consumo_persona_m3_dia":
            consumo_persona_m3_dia,

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
# RECOMENDACIONES
# ============================================================

def recomendaciones(
    tipo_uso,
    nivel=None
):

    base = {


        "Doméstico": [

            (
                "🚰 Cierra los caños",

                "Evita mantener el agua "
                "corriendo cuando no "
                "sea necesaria."
            ),

            (
                "🚿 Reduce el tiempo de ducha",

                "Disminuye algunos minutos "
                "y corta el agua mientras "
                "aplicas jabón o champú."
            ),

            (
                "🔧 Revisa fugas",

                "Inspecciona caños, "
                "tanques, conexiones "
                "e inodoros."
            ),

            (
                "🧺 Optimiza la lavadora",

                "Usa cargas completas "
                "y evita ciclos "
                "innecesarios."
            ),

            (
                "📊 Controla tu consumo",

                "Compara distintos periodos "
                "para detectar aumentos "
                "anormales."
            )

        ],


        "Comercial": [

            (
                "📋 Control por actividad",

                "Registra el consumo "
                "por turno, área o "
                "actividad comercial."
            ),

            (
                "🔧 Mantén equipos y conexiones",

                "Revisa periódicamente "
                "los puntos donde "
                "se utiliza agua."
            ),

            (
                "🧹 Optimiza la limpieza",

                "Evita dejar correr agua "
                "cuando un recipiente "
                "o sistema dosificado "
                "sea suficiente."
            ),

            (
                "🎯 Define metas",

                "Usa el simulador "
                "para establecer "
                "reducciones realistas."
            )

        ],


        "Educativo": [

            (
                "🏫 Promueve hábitos",

                "Desarrolla campañas "
                "de uso responsable "
                "entre estudiantes "
                "y personal."
            ),

            (
                "🚰 Revisa servicios higiénicos",

                "Controla pérdidas "
                "en lavatorios, "
                "inodoros y conexiones."
            ),

            (
                "📈 Monitorea mensualmente",

                "Relaciona el consumo "
                "con asistencia "
                "y actividades institucionales."
            ),

            (
                "🌱 Optimiza el riego",

                "Prefiere horarios "
                "de menor evaporación."
            )

        ],


        "Institucional": [

            (
                "📊 Usa indicadores",

                "Compara consumo por área, "
                "trabajador o periodo."
            ),

            (
                "🔧 Programa mantenimiento",

                "Realiza revisiones "
                "preventivas "
                "de instalaciones."
            ),

            (
                "🚻 Prioriza zonas críticas",

                "Supervisa servicios "
                "higiénicos y puntos "
                "de alto uso."
            ),

            (
                "🎯 Establece metas",

                "Define reducciones "
                "progresivas y "
                "evalúa resultados."
            )

        ],


        "Riego": [

            (
                "🌅 Elige el horario adecuado",

                "Riega temprano "
                "o al final "
                "de la tarde."
            ),

            (
                "💧 Ajusta el volumen",

                "Evita aplicar más agua "
                "de la necesaria."
            ),

            (
                "🔍 Revisa pérdidas",

                "Inspecciona mangueras, "
                "uniones y conexiones."
            ),

            (
                "📅 Registra cada jornada",

                "Compara volumen, "
                "frecuencia "
                "y área irrigada."
            )

        ],


        "Otro": [

            (
                "📊 Mide primero",

                "Registra el consumo "
                "de forma periódica."
            ),

            (
                "🔧 Revisa pérdidas",

                "Identifica fugas "
                "o usos innecesarios."
            ),

            (
                "🎯 Define una meta",

                "Usa el simulador "
                "para evaluar reducciones."
            ),

            (
                "📈 Evalúa resultados",

                "Compara periodos "
                "antes y después "
                "de aplicar mejoras."
            )

        ]

    }


    lista = list(

        base.get(

            tipo_uso,

            base["Otro"]

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

                "El consumo por persona "
                "es alto dentro de "
                "los criterios referenciales "
                "del prototipo. "
                "Revisa primero posibles "
                "fugas y hábitos de "
                "mayor consumo."
            )

        )


    return lista


# ============================================================
# INICIAR SESIÓN
# ============================================================

if "df" not in st.session_state:

    st.session_state.df = (
        cargar_datos()
    )


df = normalizar_df(
    st.session_state.df
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "💧 AquaLog BI"
)


st.sidebar.caption(
    "Gestión interactiva del agua"
)


st.sidebar.divider()


opcion = st.sidebar.radio(

    "MENÚ PRINCIPAL",

    [

        "🏠 Inicio",

        "➕ Nuevo registro",

        "🔎 Explorador",

        "🎯 Simulador de ahorro",

        "📈 Análisis",

        "💡 Recomendaciones",

        "🧮 Modelo matemático",

        "ℹ️ Proyecto"

    ]

)


st.sidebar.divider()


st.sidebar.caption(

    "Sistema de uso general. "
    "La muestra de 75 usuarios "
    "corresponde a la investigación, "
    "no al límite del software."

)


# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================

hero()


# ============================================================
# INICIO
# ============================================================

if opcion == "🏠 Inicio":

    st.title(
        "Panel general"
    )


    if df.empty:

        info_card(

            "Bienvenido a AquaLog BI",

            "Todavía no existen registros. "
            "Empieza desde la opción "
            "<b>Nuevo registro</b>. "
            "El sistema puede utilizarse "
            "con diferentes sectores, "
            "comunidades, usuarios "
            "y tipos de consumo.",

            "👋"

        )


        c1, c2, c3 = (
            st.columns(3)
        )


        with c1:

            info_card(

                "Registra",

                "Guarda información "
                "del consumo "
                "y su contexto.",

                "📝"

            )


        with c2:

            info_card(

                "Analiza",

                "Calcula indicadores "
                "y compara distintos "
                "registros.",

                "📊"

            )


        with c3:

            info_card(

                "Proyecta",

                "Simula escenarios "
                "de ahorro de agua "
                "y dinero.",

                "🎯"

            )


    else:

        # ----------------------------------------------------
        # INDICADORES
        # ----------------------------------------------------

        total_registros = (
            len(df)
        )


        usuarios_unicos = (

            df["Código"]

            .astype(str)

            .nunique()

        )


        consumo_total = (

            df[
                "Consumo del periodo (m³)"
            ]

            .sum()

        )


        consumo_promedio = (

            df[
                "Consumo del periodo (m³)"
            ]

            .mean()

        )


        costo_total = (

            df[
                "Costo del periodo (S/)"
            ]

            .sum()

        )


        c1, c2, c3, c4, c5 = (
            st.columns(5)
        )


        c1.metric(

            "🧾 Registros",

            total_registros

        )


        c2.metric(

            "👥 Usuarios/puntos",

            usuarios_unicos

        )


        c3.metric(

            "💧 Consumo total",

            f"{consumo_total:.1f} m³"

        )


        c4.metric(

            "📊 Promedio",

            f"{consumo_promedio:.1f} m³"

        )


        c5.metric(

            "💰 Costo estimado",

            f"S/ {costo_total:.2f}"

        )


        st.subheader(
            "Vista rápida"
        )


        g1, g2 = (
            st.columns(2)
        )


        # ----------------------------------------------------
        # CONSUMO POR TIPO
        # ----------------------------------------------------

        with g1:

            st.markdown(
                "#### Consumo por tipo de uso"
            )


            por_tipo = (

                df

                .groupby(

                    "Tipo de uso",

                    as_index=False

                )

                [
                    "Consumo del periodo (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo del periodo (m³)",

                    ascending=False

                )

            )


            st.bar_chart(

                por_tipo,

                x=
                    "Tipo de uso",

                y=
                    "Consumo del periodo (m³)",

                use_container_width=True

            )


        # ----------------------------------------------------
        # CONSUMO POR SECTOR
        # ----------------------------------------------------

        with g2:

            st.markdown(
                "#### Consumo por sector/comunidad"
            )


            sectores = (
                df.copy()
            )


            sectores[
                "Sector / comunidad"
            ] = (

                sectores[
                    "Sector / comunidad"
                ]

                .replace(

                    "",

                    "Sin especificar"

                )

            )


            por_sector = (

                sectores

                .groupby(

                    "Sector / comunidad",

                    as_index=False

                )

                [
                    "Consumo del periodo (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo del periodo (m³)",

                    ascending=False

                )

                .head(8)

            )


            st.bar_chart(

                por_sector,

                x=
                    "Sector / comunidad",

                y=
                    "Consumo del periodo (m³)",

                use_container_width=True

            )


        # ----------------------------------------------------
        # ALERTAS
        # ----------------------------------------------------

        st.subheader(
            "🚨 Alertas"
        )


        domesticos = (

            df[

                df[
                    "Tipo de uso"
                ]

                ==
                "Doméstico"

            ]

        )


        altos = int(

            (

                domesticos[
                    "Nivel"
                ]

                ==
                "ALTO"

            )

            .sum()

        )


        if altos > 0:

            st.warning(

                f"Se detectaron "
                f"{altos} registro(s) "
                f"domésticos clasificados "
                f"como consumo alto "
                f"dentro de los criterios "
                f"referenciales "
                f"del prototipo."

            )


        else:

            st.success(

                "No existen registros "
                "domésticos clasificados "
                "actualmente como "
                "consumo alto."

            )


        # ----------------------------------------------------
        # MAYORES CONSUMOS
        # ----------------------------------------------------

        st.subheader(
            "🔥 Mayores consumos registrados"
        )


        top = (

            df

            .sort_values(

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

            .head(7)

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

        "Registra hogares, comercios, "
        "instituciones, centros educativos, "
        "riego u otros tipos de uso."

    )


    with st.form(

        "form_registro",

        clear_on_submit=False

    ):


        c1, c2, c3 = (
            st.columns(3)
        )


        # ----------------------------------------------------
        # COLUMNA 1
        # ----------------------------------------------------

        with c1:

            codigo = st.text_input(

                "🆔 Código o identificador",

                placeholder=
                    "Ejemplo: U001"

            )


            fecha_registro = (
                st.date_input(

                    "📅 Fecha",

                    value=
                        date.today()

                )
            )


            tipo_uso = (
                st.selectbox(

                    "🏷️ Tipo de uso",

                    TIPOS_USO

                )
            )


        # ----------------------------------------------------
        # COLUMNA 2
        # ----------------------------------------------------

        with c2:

            sector = st.text_input(

                "📍 Sector / comunidad",

                placeholder=

                    "Ej.: Centro, "
                    "La Esperanza, "
                    "Shaullo..."

            )


            zona = st.text_input(

                "🧭 Zona / referencia",

                placeholder=
                    "Dato opcional"

            )


            personas = (
                st.number_input(

                    "👥 Personas o usuarios "
                    "de referencia",

                    min_value=1,

                    max_value=5000,

                    value=4,

                    help=

                        "En uso doméstico "
                        "corresponde al número "
                        "de habitantes."

                )
            )


        # ----------------------------------------------------
        # COLUMNA 3
        # ----------------------------------------------------

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

                "💰 Tarifa referencial "
                "(S/ por m³)",

                min_value=0.0,

                value=0.0,

                step=0.1,

                help=

                    "Déjalo en cero "
                    "si no deseas "
                    "estimar costos."

            )


        observaciones = (
            st.text_area(

                "📝 Observaciones",

                placeholder=

                    "Ej.: presencia de fugas, "
                    "condiciones particulares, "
                    "notas de campo..."

            )
        )


        guardar = (
            st.form_submit_button(

                "💧 ANALIZAR Y GUARDAR",

                use_container_width=True

            )
        )


    # --------------------------------------------------------
    # PROCESAR
    # --------------------------------------------------------

    if guardar:

        codigo_limpio = (

            codigo

            .strip()

            .upper()

        )


        if not codigo_limpio:

            st.error(

                "Ingresa un código "
                "o identificador."

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
                            codigo_limpio,

                        "Fecha":

                            fecha_registro

                            .strftime(
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

                                4

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

                                5

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


            # ------------------------------------------------
            # RESULTADOS
            # ------------------------------------------------

            r1, r2, r3, r4 = (
                st.columns(4)
            )


            r1.metric(

                "💧 Consumo diario",

                f'{resultado["consumo_diario"]:.3f} m³'

            )


            r2.metric(

                "👤 Referencia individual",

                f'{resultado["litros_persona_dia"]:.1f} L/día'

            )


            r3.metric(

                "🔢 Índice logarítmico",

                f'{resultado["indice_log"]:.5f}'

            )


            r4.metric(

                "💰 Costo estimado",

                f'S/ {resultado["costo"]:.2f}'

            )


            # ------------------------------------------------
            # NIVEL
            # ------------------------------------------------

            if tipo_uso == "Doméstico":

                if (
                    resultado[
                        "nivel"
                    ]
                    ==
                    "BAJO"
                ):

                    st.success(

                        "🟢 Clasificación "
                        "doméstica: BAJO"

                    )


                elif (
                    resultado[
                        "nivel"
                    ]
                    ==
                    "MODERADO"
                ):

                    st.warning(

                        "🟡 Clasificación "
                        "doméstica: MODERADO"

                    )


                else:

                    st.error(

                        "🔴 Clasificación "
                        "doméstica: ALTO"

                    )


            else:

                st.info(

                    "En usos no domésticos "
                    "el sistema muestra "
                    "los indicadores, "
                    "pero no aplica "
                    "los rangos domésticos "
                    "por persona."

                )


            # ------------------------------------------------
            # DESARROLLO MATEMÁTICO
            # ------------------------------------------------

            with st.expander(
                "🧮 Ver desarrollo matemático"
            ):

                st.latex(
                    r"C_p=\frac{V}{P\times D}"
                )


                st.write(

                    f'**Cₚ = '
                    f'{consumo:.2f} / '
                    f'({personas} × {dias}) '
                    f'= '
                    f'{resultado["consumo_persona_m3_dia"]:.5f} '
                    f'm³/persona/día**'

                )


                st.latex(
                    r"I_L=\log_{10}(1+C_p)"
                )


                st.write(

                    f'**Iₗ = '
                    f'{resultado["indice_log"]:.5f}**'

                )


            # ------------------------------------------------
            # RECOMENDACIONES
            # ------------------------------------------------

            st.subheader(
                "💡 Recomendaciones para este registro"
            )


            for titulo, texto in (
                recomendaciones(

                    tipo_uso,

                    resultado[
                        "nivel"
                    ]

                )
            ):

                tip_card(
                    titulo,
                    texto
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
            "No existen datos para explorar."
        )


    else:

        # ----------------------------------------------------
        # FILTROS
        # ----------------------------------------------------

        f1, f2, f3 = (
            st.columns(3)
        )


        sectores_disponibles = (

            sorted(

                [

                    x

                    for x in (

                        df[
                            "Sector / comunidad"
                        ]

                        .astype(str)

                        .unique()

                        .tolist()

                    )

                    if x.strip()

                ]

            )

        )


        tipos_disponibles = (

            sorted(

                df[
                    "Tipo de uso"
                ]

                .astype(str)

                .unique()

                .tolist()

            )

        )


        niveles_disponibles = (

            sorted(

                df[
                    "Nivel"
                ]

                .astype(str)

                .unique()

                .tolist()

            )

        )


        with f1:

            sector_filtro = (
                st.selectbox(

                    "📍 Sector",

                    [
                        "Todos"
                    ]
                    +
                    sectores_disponibles

                )
            )


        with f2:

            tipo_filtro = (
                st.selectbox(

                    "🏷️ Tipo de uso",

                    [
                        "Todos"
                    ]
                    +
                    tipos_disponibles

                )
            )


        with f3:

            nivel_filtro = (
                st.selectbox(

                    "🚦 Nivel",

                    [
                        "Todos"
                    ]
                    +
                    niveles_disponibles

                )
            )


        consulta = (
            st.text_input(

                "🔍 Buscar por código, "
                "sector o zona",

                placeholder=
                    "Escribe una palabra..."

            )
        )


        filtrado = (
            df.copy()
        )


        if (
            sector_filtro
            !=
            "Todos"
        ):

            filtrado = filtrado[

                filtrado[
                    "Sector / comunidad"
                ]

                ==
                sector_filtro

            ]


        if (
            tipo_filtro
            !=
            "Todos"
        ):

            filtrado = filtrado[

                filtrado[
                    "Tipo de uso"
                ]

                ==
                tipo_filtro

            ]


        if (
            nivel_filtro
            !=
            "Todos"
        ):

            filtrado = filtrado[

                filtrado[
                    "Nivel"
                ]

                ==
                nivel_filtro

            ]


        if consulta.strip():

            palabra = (
                consulta.strip()
            )


            mascara = (

                filtrado[
                    "Código"
                ]

                .astype(str)

                .str.contains(

                    palabra,

                    case=False,

                    na=False

                )

                |

                filtrado[
                    "Sector / comunidad"
                ]

                .astype(str)

                .str.contains(

                    palabra,

                    case=False,

                    na=False

                )

                |

                filtrado[
                    "Zona / referencia"
                ]

                .astype(str)

                .str.contains(

                    palabra,

                    case=False,

                    na=False

                )

            )


            filtrado = (
                filtrado[
                    mascara
                ]
            )


        st.caption(

            f"{len(filtrado)} "
            f"registro(s) encontrado(s)."

        )


        st.dataframe(

            filtrado

            .sort_values(

                "Fecha",

                ascending=False

            ),

            use_container_width=True,

            hide_index=True

        )


        # ----------------------------------------------------
        # DESCARGAR CSV
        # ----------------------------------------------------

        csv = (

            filtrado

            .to_csv(
                index=False
            )

            .encode(
                "utf-8-sig"
            )

        )


        st.download_button(

            "📥 Descargar selección en CSV",

            data=csv,

            file_name=
                "AquaLog_BI_datos.csv",

            mime=
                "text/csv",

            use_container_width=True

        )


        # ----------------------------------------------------
        # HISTORIAL
        # ----------------------------------------------------

        st.divider()


        st.subheader(
            "👤 Historial por código"
        )


        codigos = (

            sorted(

                df[
                    "Código"
                ]

                .astype(str)

                .unique()

                .tolist()

            )

        )


        codigo_seleccionado = (
            st.selectbox(

                "Selecciona un código",

                codigos

            )
        )


        historial = (

            df[

                df[
                    "Código"
                ]

                .astype(str)

                ==
                codigo_seleccionado

            ]

            .copy()

        )


        historial[
            "Fecha"
        ] = (

            pd.to_datetime(

                historial[
                    "Fecha"
                ],

                errors=
                    "coerce"

            )

        )


        historial = (

            historial

            .sort_values(
                "Fecha"
            )

        )


        h1, h2, h3 = (
            st.columns(3)
        )


        h1.metric(

            "Registros",

            len(historial)

        )


        h2.metric(

            "Consumo promedio",

            f'{historial["Consumo del periodo (m³)"].mean():.2f} m³'

        )


        h3.metric(

            "Último consumo",

            f'{historial["Consumo del periodo (m³)"].iloc[-1]:.2f} m³'

        )


        if len(historial) > 1:

            st.line_chart(

                historial,

                x=
                    "Fecha",

                y=
                    "Consumo del periodo (m³)",

                use_container_width=True

            )


        else:

            st.info(

                "Este código todavía "
                "tiene un solo registro."

            )


        st.dataframe(

            historial,

            use_container_width=True,

            hide_index=True

        )


        # ----------------------------------------------------
        # IMPORTAR CSV
        # ----------------------------------------------------

        st.divider()


        st.subheader(
            "📤 Importar CSV"
        )


        archivo_subido = (
            st.file_uploader(

                "Selecciona un archivo CSV "
                "compatible con AquaLog BI",

                type=[
                    "csv"
                ]

            )
        )


        if archivo_subido is not None:

            try:

                base_importada = (

                    normalizar_df(

                        pd.read_csv(
                            archivo_subido
                        )

                    )

                )


                st.success(

                    f"Archivo leído correctamente: "
                    f"{len(base_importada)} registros."

                )


                if st.button(

                    "✅ USAR ESTA BASE DE DATOS",

                    use_container_width=True

                ):

                    st.session_state.df = (
                        base_importada
                    )


                    guardar_datos(
                        base_importada
                    )


                    st.rerun()


            except Exception as error:

                st.error(

                    f"No se pudo importar "
                    f"el archivo: {error}"

                )


        # ----------------------------------------------------
        # ELIMINAR REGISTRO
        # ----------------------------------------------------

        st.divider()


        st.subheader(
            "🗑️ Eliminar un registro"
        )


        opciones_borrado = (

            df

            .reset_index()

            .apply(

                lambda fila:

                    f'{fila["index"]} | '
                    f'{fila["Código"]} | '
                    f'{fila["Fecha"]} | '
                    f'{fila["Consumo del periodo (m³)"]:.2f} m³',

                axis=1

            )

            .tolist()

        )


        registro_borrar = (
            st.selectbox(

                "Selecciona el registro",

                [
                    "Seleccionar..."
                ]
                +
                opciones_borrado

            )
        )


        if st.button(

            "🗑️ ELIMINAR REGISTRO",

            use_container_width=True

        ):


            if (
                registro_borrar
                ==
                "Seleccionar..."
            ):

                st.warning(

                    "Selecciona "
                    "un registro."

                )


            else:

                indice_real = int(

                    registro_borrar

                    .split(
                        " | "
                    )[0]

                )


                nuevo_df = (

                    df

                    .drop(
                        index=
                            indice_real
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

                    "✅ Registro eliminado."

                )


                st.rerun()


# ============================================================
# SIMULADOR DE AHORRO
# ============================================================

elif opcion == "🎯 Simulador de ahorro":

    st.title(
        "Simulador de ahorro"
    )


    st.write(

        "Prueba metas de reducción "
        "y observa el posible ahorro "
        "de agua y dinero."

    )


    modo = st.radio(

        "Origen del consumo",

        [

            "Ingresar manualmente",

            "Usar un registro existente"

        ],

        horizontal=True

    )


    consumo_base = 20.0

    tarifa_base = 0.0

    etiqueta = (
        "Escenario manual"
    )


    # --------------------------------------------------------
    # USAR REGISTRO EXISTENTE
    # --------------------------------------------------------

    if (
        modo
        ==
        "Usar un registro existente"
        and
        not df.empty
    ):


        opciones_df = (

            df

            .reset_index(
                drop=True
            )

        )


        opciones = (

            opciones_df

            .apply(

                lambda fila:

                    f'{fila["Código"]} | '
                    f'{fila["Fecha"]} | '
                    f'{fila["Consumo del periodo (m³)"]:.2f} m³',

                axis=1

            )

            .tolist()

        )


        seleccion = (
            st.selectbox(

                "Selecciona un registro",

                opciones

            )
        )


        posicion = (

            opciones

            .index(
                seleccion
            )

        )


        fila = (

            opciones_df

            .iloc[
                posicion
            ]

        )


        consumo_base = float(

            fila[
                "Consumo del periodo (m³)"
            ]

        )


        tarifa_base = float(

            fila[
                "Tarifa (S/ por m³)"
            ]

        )


        etiqueta = str(

            fila[
                "Código"
            ]

        )


    # --------------------------------------------------------
    # MANUAL
    # --------------------------------------------------------

    else:

        s1, s2 = (
            st.columns(2)
        )


        with s1:

            consumo_base = (
                st.number_input(

                    "💧 Consumo actual (m³)",

                    min_value=0.01,

                    value=20.0,

                    step=0.1

                )
            )


        with s2:

            tarifa_base = (
                st.number_input(

                    "💰 Tarifa (S/ por m³)",

                    min_value=0.0,

                    value=0.0,

                    step=0.1,

                    key=
                        "tarifa_sim"

                )
            )


    # --------------------------------------------------------
    # META
    # --------------------------------------------------------

    reduccion = (
        st.slider(

            "🎯 Meta de reducción",

            min_value=0,

            max_value=50,

            value=15,

            step=1,

            format="%d%%"

        )
    )


    nuevo_consumo = (

        consumo_base *

        (
            1 -
            reduccion / 100
        )

    )


    ahorro_m3 = (

        consumo_base -
        nuevo_consumo

    )


    ahorro_anual = (

        ahorro_m3 *
        12

    )


    ahorro_soles = (

        ahorro_m3 *
        tarifa_base

    )


    ahorro_soles_anual = (

        ahorro_soles *
        12

    )


    # --------------------------------------------------------
    # MÉTRICAS
    # --------------------------------------------------------

    c1, c2, c3, c4 = (
        st.columns(4)
    )


    c1.metric(

        "💧 Consumo actual",

        f"{consumo_base:.2f} m³"

    )


    c2.metric(

        "🎯 Nuevo consumo",

        f"{nuevo_consumo:.2f} m³",

        delta=
            f"-{ahorro_m3:.2f} m³"

    )


    c3.metric(

        "💙 Ahorro/periodo",

        f"{ahorro_m3:.2f} m³"

    )


    c4.metric(

        "🌎 Ahorro anual",

        f"{ahorro_anual:.2f} m³"

    )


    if tarifa_base > 0:

        st.success(

            f"Con una reducción del "
            f"{reduccion}% en {etiqueta}, "
            f"el ahorro económico estimado "
            f"sería S/ {ahorro_soles:.2f} "
            f"por periodo y aproximadamente "
            f"S/ {ahorro_soles_anual:.2f} "
            f"al año."

        )


    else:

        st.info(

            f"Con una reducción del "
            f"{reduccion}% podrías ahorrar "
            f"aproximadamente "
            f"{ahorro_anual:.2f} m³ "
            f"al año."

        )


    # --------------------------------------------------------
    # ESCENARIOS
    # --------------------------------------------------------

    st.subheader(
        "📊 Comparación de escenarios"
    )


    porcentajes = [

        0,

        5,

        10,

        15,

        20,

        25,

        reduccion

    ]


    etiquetas = [

        "Actual",

        "Ahorro 5%",

        "Ahorro 10%",

        "Ahorro 15%",

        "Ahorro 20%",

        "Ahorro 25%",

        f"Meta {reduccion}%"

    ]


    escenarios = pd.DataFrame(

        {

            "Escenario":
                etiquetas,

            "Consumo (m³)":

                [

                    consumo_base *

                    (
                        1 -
                        porcentaje / 100
                    )

                    for porcentaje
                    in porcentajes

                ]

        }

    )


    st.bar_chart(

        escenarios,

        x=
            "Escenario",

        y=
            "Consumo (m³)",

        use_container_width=True

    )


    st.dataframe(

        escenarios,

        use_container_width=True,

        hide_index=True

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

            "Registra información "
            "para generar análisis."

        )


    else:

        a1, a2 = (
            st.columns(2)
        )


        tipos_disponibles = (

            sorted(

                df[
                    "Tipo de uso"
                ]

                .astype(str)

                .unique()

                .tolist()

            )

        )


        sectores_disponibles = (

            sorted(

                [

                    x

                    for x in (

                        df[
                            "Sector / comunidad"
                        ]

                        .astype(str)

                        .unique()

                        .tolist()

                    )

                    if x.strip()

                ]

            )

        )


        with a1:

            tipos_seleccionados = (
                st.multiselect(

                    "🏷️ Tipos de uso",

                    options=
                        tipos_disponibles,

                    default=
                        tipos_disponibles

                )
            )


        with a2:

            sectores_seleccionados = (
                st.multiselect(

                    "📍 Sectores",

                    options=
                        sectores_disponibles,

                    default=
                        sectores_disponibles

                )
            )


        analisis = (

            df[

                df[
                    "Tipo de uso"
                ]

                .isin(
                    tipos_seleccionados
                )

            ]

            .copy()

        )


        if (
            sectores_disponibles
            and
            sectores_seleccionados
        ):

            analisis = analisis[

                analisis[
                    "Sector / comunidad"
                ]

                .isin(
                    sectores_seleccionados
                )

            ]


        if analisis.empty:

            st.warning(

                "Los filtros seleccionados "
                "no contienen registros."

            )


        else:

            # ------------------------------------------------
            # KPIs
            # ------------------------------------------------

            k1, k2, k3, k4 = (
                st.columns(4)
            )


            k1.metric(

                "Registros analizados",

                len(analisis)

            )


            k2.metric(

                "Consumo total",

                f'{analisis["Consumo del periodo (m³)"].sum():.2f} m³'

            )


            k3.metric(

                "Promedio",

                f'{analisis["Consumo del periodo (m³)"].mean():.2f} m³'

            )


            k4.metric(

                "Costo total",

                f'S/ {analisis["Costo del periodo (S/)"].sum():.2f}'

            )


            # ------------------------------------------------
            # POR TIPO
            # ------------------------------------------------

            st.subheader(
                "📊 Consumo por tipo de uso"
            )


            consumo_tipo = (

                analisis

                .groupby(

                    "Tipo de uso",

                    as_index=False

                )

                [
                    "Consumo del periodo (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo del periodo (m³)",

                    ascending=False

                )

            )


            st.bar_chart(

                consumo_tipo,

                x=
                    "Tipo de uso",

                y=
                    "Consumo del periodo (m³)",

                use_container_width=True

            )


            # ------------------------------------------------
            # POR SECTOR
            # ------------------------------------------------

            st.subheader(
                "📍 Consumo por sector/comunidad"
            )


            temporal_sector = (
                analisis.copy()
            )


            temporal_sector[
                "Sector / comunidad"
            ] = (

                temporal_sector[
                    "Sector / comunidad"
                ]

                .replace(

                    "",

                    "Sin especificar"

                )

            )


            consumo_sector = (

                temporal_sector

                .groupby(

                    "Sector / comunidad",

                    as_index=False

                )

                [
                    "Consumo del periodo (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo del periodo (m³)",

                    ascending=False

                )

            )


            st.bar_chart(

                consumo_sector,

                x=
                    "Sector / comunidad",

                y=
                    "Consumo del periodo (m³)",

                use_container_width=True

            )


            # ------------------------------------------------
            # EVOLUCIÓN TEMPORAL
            # ------------------------------------------------

            st.subheader(
                "🗓️ Evolución temporal"
            )


            evolucion = (
                analisis.copy()
            )


            evolucion[
                "Fecha"
            ] = (

                pd.to_datetime(

                    evolucion[
                        "Fecha"
                    ],

                    errors=
                        "coerce"

                )

            )


            evolucion = (

                evolucion

                .dropna(
                    subset=[
                        "Fecha"
                    ]
                )

                .groupby(

                    "Fecha",

                    as_index=False

                )

                [
                    "Consumo del periodo (m³)"
                ]

                .sum()

                .sort_values(
                    "Fecha"
                )

            )


            if not evolucion.empty:

                st.line_chart(

                    evolucion,

                    x=
                        "Fecha",

                    y=
                        "Consumo del periodo (m³)",

                    use_container_width=True

                )


            # ------------------------------------------------
            # RANKING
            # ------------------------------------------------

            st.subheader(
                "🏆 Ranking de consumo"
            )


            ranking = (

                analisis

                .sort_values(

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

                        "Consumo por persona (L/día)",

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
# RECOMENDACIONES
# ============================================================

elif opcion == "💡 Recomendaciones":

    st.title(
        "Recomendaciones inteligentes"
    )


    st.write(

        "Selecciona el tipo de uso "
        "para obtener recomendaciones "
        "más apropiadas."

    )


    tipo_rec = (
        st.selectbox(

            "🏷️ Tipo de uso",

            TIPOS_USO

        )
    )


    nivel_rec = None


    if tipo_rec == "Doméstico":

        nivel_rec = (
            st.selectbox(

                "🚦 Nivel de consumo",

                [

                    "BAJO",

                    "MODERADO",

                    "ALTO"

                ]

            )
        )


    for titulo, texto in (
        recomendaciones(

            tipo_rec,

            nivel_rec

        )
    ):

        tip_card(
            titulo,
            texto
        )


# ============================================================
# MODELO MATEMÁTICO
# ============================================================

elif opcion == "🧮 Modelo matemático":

    st.title(
        "Modelo matemático"
    )


    info_card(

        "Consumo diario por persona",

        "Para el análisis doméstico, "
        "AquaLog BI distribuye el volumen "
        "consumido entre las personas "
        "y los días del periodo.",

        "1️⃣"

    )


    st.latex(
        r"C_p=\frac{V}{P\times D}"
    )


    st.write(
        "**V** = volumen consumido en m³."
    )


    st.write(
        "**P** = número de personas."
    )


    st.write(
        "**D** = días del periodo."
    )


    st.write(
        "**Cₚ** = consumo "
        "en m³/persona/día."
    )


    st.divider()


    info_card(

        "Índice logarítmico",

        "AquaLog BI transforma "
        "el consumo diario por persona "
        "a una escala logarítmica "
        "para facilitar la comparación "
        "de valores.",

        "2️⃣"

    )


    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )


    st.warning(

        "Los rangos BAJO, MODERADO "
        "y ALTO son criterios "
        "referenciales del prototipo "
        "para uso doméstico y deberán "
        "quedar sustentados "
        "metodológicamente "
        "en la investigación."

    )


    # --------------------------------------------------------
    # CALCULADORA
    # --------------------------------------------------------

    st.subheader(
        "🧪 Calculadora interactiva"
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    with c1:

        volumen_demo = (
            st.number_input(

                "V: volumen (m³)",

                min_value=0.01,

                value=18.0,

                key=
                    "vol_demo"

            )
        )


    with c2:

        personas_demo = (
            st.number_input(

                "P: personas",

                min_value=1,

                value=4,

                key=
                    "per_demo"

            )
        )


    with c3:

        dias_demo = (
            st.number_input(

                "D: días",

                min_value=1,

                value=30,

                key=
                    "dias_demo"

            )
        )


    cp_demo = (

        volumen_demo /

        (
            personas_demo *
            dias_demo
        )

    )


    il_demo = (

        math.log10(

            1 +
            cp_demo

        )

    )


    c1, c2 = (
        st.columns(2)
    )


    c1.metric(

        "Cₚ",

        f"{cp_demo * 1000:.2f} "
        f"L/persona/día"

    )


    c2.metric(

        "Iₗ",

        f"{il_demo:.5f}"

    )


# ============================================================
# PROYECTO
# ============================================================

elif opcion == "ℹ️ Proyecto":

    st.title(
        "Acerca del proyecto"
    )


    info_card(

        "Proyecto de investigación",

        "<b>"
        "Desarrollo de software basado "
        "en logaritmos matemáticos para "
        "la gestión eficiente del agua "
        "en el distrito de Baños del Inca, "
        "2026."
        "</b>"
        "<br><br>"
        "AquaLog BI está diseñado como "
        "un sistema de uso general. "
        "La ubicación, el sector, "
        "la zona y el tipo de uso "
        "se determinan en cada registro.",

        "📘"

    )


    st.subheader(
        "👩‍🏫 Docente"
    )


    credit_card(

        "Paola Ponce",

        "👩‍🏫"

    )


    st.subheader(
        "👥 Integrantes"
    )


    credit_card(
        "Chuquiruna Escobal, Jhersonn"
    )


    credit_card(
        "Paz Muñoz, Vili"
    )


    credit_card(
        "Vasquez Azañero, Diego"
    )


    credit_card(
        "Vasquez Bustamante, Nathan Lowell"
    )


    st.subheader(
        "✨ ¿Qué puede hacer AquaLog BI?"
    )


    funciones = [

        "📝 Registrar diferentes tipos "
        "de usuarios y consumos.",

        "📍 Trabajar con diferentes "
        "sectores y comunidades.",

        "💧 Analizar el consumo de agua.",

        "🧮 Aplicar un modelo logarítmico.",

        "🔎 Buscar y filtrar información.",

        "👤 Consultar el historial "
        "de un usuario o punto.",

        "🎯 Simular escenarios de ahorro.",

        "💰 Estimar costos cuando "
        "se ingresa una tarifa.",

        "📈 Analizar la evolución temporal.",

        "🏆 Identificar los mayores consumos.",

        "💡 Mostrar recomendaciones "
        "según el tipo de uso.",

        "📥 Descargar los datos registrados."

    ]


    for funcion in funciones:

        st.write(
            funcion
        )


    st.info(

        "La muestra de 75 usuarios "
        "pertenece al estudio académico. "
        "No es un límite del software: "
        "AquaLog BI puede registrar "
        "más o menos usuarios "
        "según la aplicación."

    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()


st.markdown(

    '<div class="footer">'
    '💧 <strong>AquaLog BI</strong>'
    '<br>'
    'Sistema interactivo para el análisis '
    'y gestión eficiente del agua'
    '<br>'
    'Baños del Inca · Cajamarca · 2026'
    '</div>',

    unsafe_allow_html=True

)
