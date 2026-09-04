import streamlit as st
import pandas as pd
import math
import os

from datetime import date
from textwrap import dedent


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
    "Consumo mensual (m³)",
    "Días",
    "Tarifa (S/ por m³)",
    "Consumo diario (m³)",
    "Consumo por persona (L/día)",
    "Índice logarítmico",
    "Nivel",
    "Costo mensual (S/)",
    "Observaciones"
]


# ============================================================
# FUNCIÓN PARA MOSTRAR HTML CORRECTAMENTE
# ============================================================

def html(contenido):

    st.markdown(
        dedent(contenido).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# DISEÑO VISUAL
# ============================================================

st.markdown(
    """
<style>

/* =========================================
FONDO GENERAL
========================================= */

.stApp {

    background:

        radial-gradient(
            circle at 12% 8%,
            rgba(32,196,232,0.13),
            transparent 24%
        ),

        radial-gradient(
            circle at 90% 18%,
            rgba(11,99,206,0.11),
            transparent 26%
        ),

        linear-gradient(
            135deg,
            #f4fbff 0%,
            #eaf7ff 55%,
            #ffffff 100%
        );

    color: #123047;

}


.block-container {

    padding-top: 1.6rem;

    padding-bottom: 2rem;

    max-width: 1500px;

}


h1,
h2,
h3,
h4 {

    color: #0a4f82 !important;

}


p,
span,
label {

    color: #16384f;

}


/* =========================================
ENCABEZADO PRINCIPAL
========================================= */

.hero {

    position: relative;

    overflow: hidden;

    background:

        linear-gradient(
            120deg,
            #073d9e 0%,
            #0b72d8 48%,
            #17b9dd 100%
        );

    border-radius: 30px;

    padding: 38px 42px;

    margin-bottom: 26px;

    box-shadow:

        0 18px 45px
        rgba(8,92,160,0.22);

}


.hero::before {

    content: "";

    position: absolute;

    width: 360px;

    height: 360px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.08);

    right: -140px;

    top: -175px;

}


.hero::after {

    content: "";

    position: absolute;

    width: 220px;

    height: 220px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.06);

    right: 130px;

    bottom: -165px;

}


.hero-grid {

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 24px;

    position: relative;

    z-index: 2;

}


.hero-copy {

    max-width: 900px;

}


.hero-badge {

    display: inline-block;

    background:
        rgba(255,255,255,0.14);

    border:
        1px solid
        rgba(255,255,255,0.28);

    color:
        white !important;

    border-radius: 999px;

    padding: 7px 13px;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 0.8px;

    margin-bottom: 13px;

}


.hero h1 {

    color:
        white !important;

    font-size: 50px;

    line-height: 1.05;

    margin: 0;

    font-weight: 850;

}


.hero h1 span {

    color:
        #85ecff !important;

}


.hero h3 {

    color:
        white !important;

    margin: 11px 0 8px 0;

    font-size: 21px;

}


.hero p {

    color:
        #edfaff !important;

    font-size: 16px;

    line-height: 1.55;

    margin: 0;

}


.hero-tags {

    display: flex;

    flex-wrap: wrap;

    gap: 8px;

    margin-top: 18px;

}


.hero-tag {

    color:
        white !important;

    background:
        rgba(255,255,255,0.13);

    border:
        1px solid
        rgba(255,255,255,0.20);

    padding: 7px 12px;

    border-radius: 999px;

    font-weight: 650;

    font-size: 13px;

}


.hero-drop {

    min-width: 125px;

    min-height: 125px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 67px;

    background:
        rgba(255,255,255,0.13);

    border:
        1px solid
        rgba(255,255,255,0.30);

    box-shadow:

        inset 0 0 30px
        rgba(255,255,255,0.10);

}


/* =========================================
TARJETAS DE INDICADORES
========================================= */

.kpi {

    background:
        rgba(255,255,255,0.96);

    border:
        1px solid
        rgba(11,99,206,0.09);

    border-radius: 20px;

    padding: 20px 18px;

    text-align: center;

    box-shadow:

        0 8px 24px
        rgba(19,84,128,0.08);

    min-height: 140px;

}


.kpi .icon {

    font-size: 28px;

}


.kpi .value {

    font-size: 29px;

    font-weight: 850;

    color:
        #0b63ce !important;

    margin-top: 4px;

}


.kpi .label {

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 0.35px;

    color:
        #496a7e !important;

}


/* =========================================
TARJETAS GENERALES
========================================= */

.card {

    background:
        rgba(255,255,255,0.95);

    border:
        1px solid
        rgba(11,99,206,0.09);

    border-radius: 20px;

    padding: 21px;

    margin:
        8px 0 16px 0;

    box-shadow:

        0 7px 22px
        rgba(19,84,128,0.07);

}


.card h3 {

    margin-top: 0;

}


/* =========================================
RECOMENDACIONES
========================================= */

.tip {

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


.tip p {

    margin: 0;

}


/* =========================================
CRÉDITOS
========================================= */

.credit {

    background:

        linear-gradient(
            135deg,
            #ffffff,
            #eef9ff
        );

    border:
        1px solid #d1edf9;

    border-radius:
        16px;

    padding:
        15px 17px;

    margin:
        8px 0;

}


/* =========================================
SIDEBAR
========================================= */

section[data-testid="stSidebar"] {

    background:

        linear-gradient(
            180deg,
            #0647a8 0%,
            #087bd2 52%,
            #0ca5cf 100%
        );

    border-right:

        1px solid
        rgba(255,255,255,0.15);

}


section[data-testid="stSidebar"] * {

    color:
        white !important;

}


section[data-testid="stSidebar"]
div[role="radiogroup"] > label {

    background:
        rgba(255,255,255,0.04);

    padding:
        8px 10px;

    margin:
        3px 0;

    border-radius:
        11px;

}


section[data-testid="stSidebar"]
div[role="radiogroup"] > label:hover {

    background:
        rgba(255,255,255,0.13);

}


/* =========================================
BOTONES
========================================= */

.stButton button {

    border:
        none;

    border-radius:
        13px;

    font-weight:
        750;

    background:

        linear-gradient(
            90deg,
            #0b63ce,
            #0b9bdc
        );

    color:
        white !important;

}


.stDownloadButton button {

    border-radius:
        13px;

    font-weight:
        700;

}


/* =========================================
MÉTRICAS NATIVAS
========================================= */

[data-testid="stMetricValue"] {

    color:
        #0a568d !important;

    font-weight:
        800;

}


[data-testid="stMetricLabel"] {

    color:
        #234a62 !important;

}


/* =========================================
PIE
========================================= */

.footer {

    text-align:
        center;

    color:
        #507184;

    padding:
        18px 0 4px 0;

    font-size:
        13px;

}


/* =========================================
CELULARES
========================================= */

@media (max-width: 850px) {

    .hero-grid {

        display:
            block;

    }

    .hero-drop {

        display:
            none;

    }

    .hero h1 {

        font-size:
            40px;

    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DE DATOS
# ============================================================

def dataframe_vacio():

    return pd.DataFrame(
        columns=COLUMNAS
    )


# ============================================================
# ANÁLISIS MATEMÁTICO
# ============================================================

def analizar_consumo(
    personas,
    consumo_m3,
    dias,
    tipo_uso,
    tarifa
):

    consumo_diario = (
        consumo_m3 /
        dias
    )


    personas_seguras = max(
        int(personas),
        1
    )


    consumo_persona_m3_dia = (

        consumo_m3 /

        (
            personas_seguras *
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


    # Clasificación únicamente para uso doméstico

    if tipo_uso == "Doméstico":

        if litros_persona_dia < 100:

            nivel = "BAJO"

        elif litros_persona_dia <= 170:

            nivel = "MODERADO"

        else:

            nivel = "ALTO"

    else:

        nivel = "ANÁLISIS GENERAL"


    return (

        consumo_diario,

        litros_persona_dia,

        indice_log,

        nivel,

        costo

    )


# ============================================================
# COMPATIBILIDAD CON TU VERSIÓN ANTERIOR
# ============================================================

def normalizar_df(df):

    if df is None or df.empty:

        return dataframe_vacio()


    df = df.copy()


    # -----------------------------------------
    # CONVERTIR CAMPOS DE LA VERSIÓN ANTERIOR
    # -----------------------------------------

    mapa = {

        "Hogar":
            "Código",

        "Sector":
            "Sector / comunidad",

        "CAS":
            "Zona / referencia",

        "Habitantes":
            "Personas"

    }


    for antigua, nueva in mapa.items():

        if (
            antigua in df.columns
            and
            nueva not in df.columns
        ):

            df[nueva] = (
                df[antigua]
            )


    # -----------------------------------------
    # CREAR COLUMNAS FALTANTES
    # -----------------------------------------

    for columna in COLUMNAS:

        if columna not in df.columns:

            if columna == "Tipo de uso":

                df[columna] = (
                    "Doméstico"
                )

            elif columna == "Personas":

                df[columna] = 1

            elif columna == "Días":

                df[columna] = 30

            elif columna in [

                "Tarifa (S/ por m³)",

                "Costo mensual (S/)"

            ]:

                df[columna] = 0.0

            else:

                df[columna] = ""


    # -----------------------------------------
    # DATOS NUMÉRICOS
    # -----------------------------------------

    numericas = [

        "Personas",

        "Consumo mensual (m³)",

        "Días",

        "Tarifa (S/ por m³)",

        "Consumo diario (m³)",

        "Consumo por persona (L/día)",

        "Índice logarítmico",

        "Costo mensual (S/)"

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


    hoy = (

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
                    hoy,

                "nan":
                    hoy,

                "NaT":
                    hoy

            }

        )

    )


    return df[COLUMNAS]


# ============================================================
# CARGAR Y GUARDAR
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


if "df" not in st.session_state:

    st.session_state.df = (
        cargar_datos()
    )


# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================

html(
    """
    <div class="hero">

        <div class="hero-grid">

            <div class="hero-copy">

                <div class="hero-badge">
                    💧 SISTEMA INTELIGENTE DE GESTIÓN DEL AGUA
                </div>

                <h1>
                    AquaLog <span>BI</span>
                </h1>

                <h3>
                    Analiza, compara y proyecta
                    el consumo de agua
                </h3>

                <p>

                    Una plataforma interactiva
                    para registrar consumos,
                    explorar patrones,
                    simular escenarios de ahorro
                    y apoyar decisiones para
                    el uso responsable del agua.

                </p>

                <div class="hero-tags">

                    <div class="hero-tag">
                        📍 Ubicación configurable
                    </div>

                    <div class="hero-tag">
                        🏠 Múltiples tipos de uso
                    </div>

                    <div class="hero-tag">
                        📊 Análisis dinámico
                    </div>

                    <div class="hero-tag">
                        🧮 Modelo matemático
                    </div>

                </div>

            </div>

            <div class="hero-drop">
                💧
            </div>

        </div>

    </div>
    """
)


# ============================================================
# MENÚ LATERAL
# ============================================================

st.sidebar.markdown(

    dedent(
        """
        <div style="
            text-align:center;
            padding:8px 0 18px 0;
        ">

            <div style="
                font-size:54px;
            ">
                💧
            </div>

            <div style="
                font-size:24px;
                font-weight:850;
                color:white;
            ">
                AquaLog BI
            </div>

            <div style="
                font-size:13px;
                color:#dff7ff;
                margin-top:4px;
            ">
                Gestión interactiva del agua
            </div>

        </div>
        """
    ).strip(),

    unsafe_allow_html=True

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


df = normalizar_df(
    st.session_state.df
)


# ============================================================
# INICIO
# ============================================================

if opcion == "🏠 Inicio":

    st.header(
        "🏠 Panel general"
    )


    if df.empty:

        html(
            """
            <div class="card">

                <h3>
                    👋 Bienvenido a AquaLog BI
                </h3>

                <p>

                    Todavía no existen registros.

                    Empieza ingresando información
                    desde la sección

                    <b>
                    ➕ Nuevo registro
                    </b>.

                </p>

                <p>

                    AquaLog BI no está limitado
                    a una comunidad ni a un
                    número determinado de usuarios.

                </p>

            </div>
            """
        )


    else:

        total_registros = len(
            df
        )


        usuarios_unicos = (

            df["Código"]

            .astype(str)

            .nunique()

        )


        consumo_total = (

            df[
                "Consumo mensual (m³)"
            ]

            .sum()

        )


        consumo_promedio = (

            df[
                "Consumo mensual (m³)"
            ]

            .mean()

        )


        costo_total = (

            df[
                "Costo mensual (S/)"
            ]

            .sum()

        )


        # =====================================
        # KPIs
        # =====================================

        columnas = st.columns(5)


        tarjetas = [

            (
                "🧾",
                total_registros,
                "REGISTROS"
            ),

            (
                "👥",
                usuarios_unicos,
                "USUARIOS / PUNTOS"
            ),

            (
                "💧",
                f"{consumo_total:.1f}",
                "CONSUMO TOTAL m³"
            ),

            (
                "📊",
                f"{consumo_promedio:.1f}",
                "PROMEDIO m³"
            ),

            (
                "💰",
                f"S/ {costo_total:.2f}",
                "COSTO ESTIMADO"
            )

        ]


        for columna, tarjeta in zip(
            columnas,
            tarjetas
        ):

            icono, valor, texto = (
                tarjeta
            )


            with columna:

                html(
                    f"""
                    <div class="kpi">

                        <div class="icon">
                            {icono}
                        </div>

                        <div class="value">
                            {valor}
                        </div>

                        <div class="label">
                            {texto}
                        </div>

                    </div>
                    """
                )


        st.write("")


        # =====================================
        # GRÁFICOS RÁPIDOS
        # =====================================

        c1, c2 = st.columns(
            [1.15, 1]
        )


        with c1:

            st.subheader(
                "📊 Consumo por tipo de uso"
            )


            por_tipo = (

                df

                .groupby(
                    "Tipo de uso",
                    as_index=False
                )

                [
                    "Consumo mensual (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo mensual (m³)",

                    ascending=False

                )

            )


            st.bar_chart(

                por_tipo,

                x="Tipo de uso",

                y="Consumo mensual (m³)",

                use_container_width=True

            )


        with c2:

            st.subheader(
                "📍 Sectores con mayor consumo"
            )


            temp = df.copy()


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

                temp

                .groupby(
                    "Sector / comunidad",
                    as_index=False
                )

                [
                    "Consumo mensual (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo mensual (m³)",

                    ascending=False

                )

                .head(8)

            )


            st.bar_chart(

                por_sector,

                x="Sector / comunidad",

                y="Consumo mensual (m³)",

                use_container_width=True

            )


        # =====================================
        # ALERTA DEL SISTEMA
        # =====================================

        st.subheader(
            "🚨 Lectura rápida del sistema"
        )


        domesticos = df[

            df[
                "Tipo de uso"
            ]

            ==
            "Doméstico"

        ]


        altos = int(

            (
                domesticos[
                    "Nivel"
                ]

                ==
                "ALTO"

            ).sum()

        )


        if altos > 0:

            st.warning(

                f"Se detectaron {altos} "
                f"registro(s) domésticos "
                f"con consumo alto. "

                "Puedes revisarlos desde "
                "el Explorador."

            )

        else:

            st.success(

                "No existen registros domésticos "
                "clasificados actualmente "
                "como consumo alto."

            )


        # =====================================
        # MAYORES CONSUMOS
        # =====================================

        st.subheader(
            "🔥 Mayores consumos registrados"
        )


        top = (

            df

            .sort_values(

                "Consumo mensual (m³)",

                ascending=False

            )

            [

                [

                    "Código",

                    "Sector / comunidad",

                    "Tipo de uso",

                    "Consumo mensual (m³)",

                    "Nivel"

                ]

            ]

            .head(5)

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

    st.header(
        "➕ Nuevo registro"
    )


    st.caption(

        "Puedes registrar hogares, comercios, "
        "instituciones, centros educativos, "
        "riego u otros tipos de uso."

    )


    with st.form(
        "registro_form",
        clear_on_submit=False
    ):


        c1, c2, c3 = (
            st.columns(3)
        )


        # -------------------------------------
        # COLUMNA 1
        # -------------------------------------

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


        # -------------------------------------
        # COLUMNA 2
        # -------------------------------------

        with c2:

            sector = st.text_input(

                "📍 Sector / comunidad",

                placeholder=
                "Ej.: Centro, La Esperanza, Shaullo..."

            )


            zona = st.text_input(

                "🧭 Zona / referencia",

                placeholder=
                "Dato opcional"

            )


            personas = st.number_input(

                "👥 Personas o usuarios de referencia",

                min_value=1,

                max_value=5000,

                value=4,

                help=

                "Para uso doméstico corresponde "
                "al número de habitantes."

            )


        # -------------------------------------
        # COLUMNA 3
        # -------------------------------------

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

                "💰 Tarifa referencial (S/ por m³)",

                min_value=0.0,

                value=0.0,

                step=0.1,

                help=

                "Puedes dejarlo en cero "
                "si no deseas calcular costos."

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


    # =========================================
    # PROCESAR
    # =========================================

    if guardar:

        codigo_limpio = (

            codigo

            .strip()

            .upper()

        )


        if not codigo_limpio:

            st.error(

                "⚠️ Ingresa un código "
                "o identificador."

            )


        else:

            (

                consumo_diario,

                litros_persona,

                indice_log,

                nivel,

                costo

            ) = analizar_consumo(

                personas,

                consumo,

                dias,

                tipo_uso,

                tarifa

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

                        "Consumo mensual (m³)":
                            float(consumo),

                        "Días":
                            int(dias),

                        "Tarifa (S/ por m³)":
                            float(tarifa),

                        "Consumo diario (m³)":
                            round(
                                consumo_diario,
                                4
                            ),

                        "Consumo por persona (L/día)":
                            round(
                                litros_persona,
                                2
                            ),

                        "Índice logarítmico":
                            round(
                                indice_log,
                                5
                            ),

                        "Nivel":
                            nivel,

                        "Costo mensual (S/)":
                            round(
                                costo,
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

                "✅ Registro guardado "
                "correctamente."

            )


            # =================================
            # RESULTADOS
            # =================================

            r1, r2, r3, r4 = (
                st.columns(4)
            )


            r1.metric(

                "💧 Consumo diario",

                f"{consumo_diario:.3f} m³"

            )


            r2.metric(

                "👤 Referencia individual",

                f"{litros_persona:.1f} L/día"

            )


            r3.metric(

                "🔢 Índice logarítmico",

                f"{indice_log:.5f}"

            )


            r4.metric(

                "💰 Costo estimado",

                f"S/ {costo:.2f}"

            )


            if tipo_uso == "Doméstico":

                if nivel == "BAJO":

                    st.success(

                        "🟢 Clasificación doméstica: "
                        "CONSUMO BAJO"

                    )


                elif nivel == "MODERADO":

                    st.warning(

                        "🟡 Clasificación doméstica: "
                        "CONSUMO MODERADO"

                    )


                else:

                    st.error(

                        "🔴 Clasificación doméstica: "
                        "CONSUMO ALTO"

                    )


            else:

                st.info(

                    "ℹ️ En usos no domésticos "
                    "AquaLog BI presenta los "
                    "indicadores matemáticos, "
                    "pero no aplica los rangos "
                    "domésticos de consumo "
                    "por persona."

                )


            st.divider()


            # =================================
            # DESARROLLO MATEMÁTICO
            # =================================

            st.subheader(
                "🧮 Análisis matemático"
            )


            st.latex(
                r"C_p=\frac{V}{P\times D}"
            )


            consumo_persona_m3 = (

                consumo /

                (
                    personas *
                    dias
                )

            )


            st.write(

                f"**Cₚ = "
                f"{consumo:.2f} / "
                f"({personas} × {dias}) "
                f"= "
                f"{consumo_persona_m3:.5f} "
                f"m³/persona/día**"

            )


            st.latex(
                r"I_L=\log_{10}(1+C_p)"
            )


            st.write(

                f"**Iₗ = "
                f"{indice_log:.5f}**"

            )


# ============================================================
# EXPLORADOR
# ============================================================

elif opcion == "🔎 Explorador":

    st.header(
        "🔎 Explorador de registros"
    )


    if df.empty:

        st.info(

            "No existen datos "
            "para explorar."

        )


    else:

        # =====================================
        # FILTROS
        # =====================================

        f1, f2, f3 = (
            st.columns(3)
        )


        sectores = (

            ["Todos"]

            +

            sorted(

                [

                    valor

                    for valor in (

                        df[
                            "Sector / comunidad"
                        ]

                        .astype(str)

                        .unique()

                    )

                    if valor.strip()

                ]

            )

        )


        tipos = (

            ["Todos"]

            +

            sorted(

                df[
                    "Tipo de uso"
                ]

                .astype(str)

                .unique()

                .tolist()

            )

        )


        niveles = (

            ["Todos"]

            +

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

                    sectores

                )
            )


        with f2:

            tipo_filtro = (
                st.selectbox(

                    "🏷️ Tipo de uso",

                    tipos

                )
            )


        with f3:

            nivel_filtro = (
                st.selectbox(

                    "🚦 Nivel",

                    niveles

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


        if sector_filtro != "Todos":

            filtrado = filtrado[

                filtrado[
                    "Sector / comunidad"
                ]

                ==
                sector_filtro

            ]


        if tipo_filtro != "Todos":

            filtrado = filtrado[

                filtrado[
                    "Tipo de uso"
                ]

                ==
                tipo_filtro

            ]


        if nivel_filtro != "Todos":

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


        # =====================================
        # DESCARGAR
        # =====================================

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


        st.divider()


        # =====================================
        # HISTORIAL
        # =====================================

        st.subheader(
            "👤 Historial de un usuario o punto"
        )


        codigos = sorted(

            df[
                "Código"
            ]

            .astype(str)

            .unique()

            .tolist()

        )


        codigo_seleccionado = (
            st.selectbox(

                "Selecciona un código",

                codigos

            )
        )


        historial = df[

            df[
                "Código"
            ]

            .astype(str)

            ==
            codigo_seleccionado

        ].copy()


        historial[
            "Fecha"
        ] = pd.to_datetime(

            historial[
                "Fecha"
            ],

            errors="coerce"

        )


        historial = (
            historial

            .sort_values(
                "Fecha"
            )
        )


        if len(historial) > 1:

            st.line_chart(

                historial,

                x="Fecha",

                y="Consumo mensual (m³)",

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


        # =====================================
        # IMPORTAR DATOS
        # =====================================

        st.divider()


        st.subheader(
            "📤 Importar base de datos"
        )


        archivo_subido = (
            st.file_uploader(

                "Selecciona un archivo CSV",

                type=[
                    "csv"
                ]

            )
        )


        if archivo_subido is not None:

            try:

                base_importada = (
                    pd.read_csv(
                        archivo_subido
                    )
                )


                base_importada = (
                    normalizar_df(
                        base_importada
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


                    st.success(

                        "Base de datos "
                        "actualizada correctamente."

                    )


                    st.rerun()


            except Exception as error:

                st.error(

                    f"No se pudo importar "
                    f"el archivo: {error}"

                )


        # =====================================
        # ELIMINAR
        # =====================================

        st.divider()


        st.subheader(
            "🗑️ Eliminar registro"
        )


        codigo_borrar = (
            st.selectbox(

                "Código",

                [
                    "Seleccionar..."
                ]

                +
                codigos,

                key=
                    "codigo_borrar"

            )
        )


        if st.button(

            "🗑️ Eliminar último registro "
            "guardado de ese código",

            use_container_width=True

        ):


            if (
                codigo_borrar
                ==
                "Seleccionar..."
            ):

                st.warning(

                    "Selecciona "
                    "un código."

                )


            else:

                candidatos = df[

                    df[
                        "Código"
                    ]

                    .astype(str)

                    ==
                    codigo_borrar

                ]


                indice = (
                    candidatos
                    .index[-1]
                )


                nuevo_df = (

                    df

                    .drop(
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

                    "✅ Registro eliminado."

                )


                st.rerun()


# ============================================================
# SIMULADOR DE AHORRO
# ============================================================

elif opcion == "🎯 Simulador de ahorro":

    st.header(
        "🎯 Simulador de ahorro"
    )


    st.write(

        "Prueba diferentes escenarios "
        "de reducción del consumo y "
        "observa cuánto agua y dinero "
        "podrían ahorrarse."

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


    # =========================================
    # REGISTRO EXISTENTE
    # =========================================

    if (
        modo
        ==
        "Usar un registro existente"
        and
        not df.empty
    ):


        opciones_df = (
            df.reset_index(
                drop=True
            )
        )


        opciones = (

            opciones_df

            .apply(

                lambda fila:

                f'{fila["Código"]} | '
                f'{fila["Fecha"]} | '
                f'{fila["Consumo mensual (m³)"]:.2f} m³',

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
                "Consumo mensual (m³)"
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


    # =========================================
    # MANUAL
    # =========================================

    else:

        c1, c2 = (
            st.columns(2)
        )


        with c1:

            consumo_base = (
                st.number_input(

                    "💧 Consumo actual (m³)",

                    min_value=0.01,

                    value=20.0,

                    step=0.1

                )
            )


        with c2:

            tarifa_base = (
                st.number_input(

                    "💰 Tarifa (S/ por m³)",

                    min_value=0.0,

                    value=0.0,

                    step=0.1,

                    key=
                        "tarifa_simulador"

                )
            )


    # =========================================
    # META
    # =========================================

    reduccion = st.slider(

        "🎯 Meta de reducción",

        min_value=0,

        max_value=50,

        value=15,

        step=1,

        format="%d%%"

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


    # =========================================
    # RESULTADOS
    # =========================================

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

        "💙 Ahorro por periodo",

        f"{ahorro_m3:.2f} m³"

    )


    c4.metric(

        "🌎 Ahorro anual estimado",

        f"{ahorro_anual:.2f} m³"

    )


    if tarifa_base > 0:

        st.success(

            f"💰 Con una reducción del "
            f"{reduccion}% en {etiqueta}, "
            f"el ahorro económico estimado "
            f"sería de S/ {ahorro_soles:.2f} "
            f"por periodo y aproximadamente "
            f"S/ {ahorro_soles_anual:.2f} "
            f"al año."

        )


    else:

        st.info(

            f"💧 Con una reducción del "
            f"{reduccion}%, podrías ahorrar "
            f"aproximadamente "
            f"{ahorro_anual:.2f} m³ "
            f"de agua al año."

        )


    # =========================================
    # ESCENARIOS
    # =========================================

    st.subheader(
        "📊 Comparación de escenarios"
    )


    escenarios = pd.DataFrame(

        {

            "Escenario": [

                "Actual",

                "Ahorro 5%",

                "Ahorro 10%",

                "Ahorro 15%",

                "Ahorro 20%",

                f"Meta {reduccion}%"

            ],

            "Consumo (m³)": [

                consumo_base,

                consumo_base *
                0.95,

                consumo_base *
                0.90,

                consumo_base *
                0.85,

                consumo_base *
                0.80,

                nuevo_consumo

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


# ============================================================
# ANÁLISIS
# ============================================================

elif opcion == "📈 Análisis":

    st.header(
        "📈 Análisis dinámico"
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

                .unique()

                .tolist()

            )

        )


        sectores_disponibles = (

            sorted(

                [

                    valor

                    for valor in (

                        df[
                            "Sector / comunidad"
                        ]

                        .astype(str)

                        .unique()

                    )

                    if valor.strip()

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


        analisis = df[

            df[
                "Tipo de uso"
            ]

            .isin(
                tipos_seleccionados
            )

        ].copy()


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

            # =================================
            # TIPO DE USO
            # =================================

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
                    "Consumo mensual (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo mensual (m³)",

                    ascending=False

                )

            )


            st.bar_chart(

                consumo_tipo,

                x=
                    "Tipo de uso",

                y=
                    "Consumo mensual (m³)",

                use_container_width=True

            )


            # =================================
            # SECTOR
            # =================================

            st.subheader(
                "📍 Consumo por sector / comunidad"
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
                    "Consumo mensual (m³)"
                ]

                .sum()

                .sort_values(

                    "Consumo mensual (m³)",

                    ascending=False

                )

            )


            st.bar_chart(

                consumo_sector,

                x=
                    "Sector / comunidad",

                y=
                    "Consumo mensual (m³)",

                use_container_width=True

            )


            # =================================
            # EVOLUCIÓN
            # =================================

            st.subheader(
                "🗓️ Evolución temporal"
            )


            evolucion = (
                analisis.copy()
            )


            evolucion[
                "Fecha"
            ] = pd.to_datetime(

                evolucion[
                    "Fecha"
                ],

                errors="coerce"

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
                    "Consumo mensual (m³)"
                ]

                .sum()

                .sort_values(
                    "Fecha"
                )

            )


            if not evolucion.empty:

                st.line_chart(

                    evolucion,

                    x="Fecha",

                    y="Consumo mensual (m³)",

                    use_container_width=True

                )


            # =================================
            # RANKING
            # =================================

            st.subheader(
                "🏆 Ranking de consumo"
            )


            ranking = (

                analisis

                .sort_values(

                    "Consumo mensual (m³)",

                    ascending=False

                )

                [

                    [

                        "Código",

                        "Fecha",

                        "Sector / comunidad",

                        "Tipo de uso",

                        "Consumo mensual (m³)",

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

    st.header(
        "💡 Recomendaciones inteligentes"
    )


    st.write(

        "Selecciona el tipo de uso "
        "para recibir recomendaciones "
        "más apropiadas."

    )


    tipo_recomendacion = (
        st.selectbox(

            "🏷️ Tipo de uso",

            TIPOS_USO

        )
    )


    recomendaciones = {


        "Doméstico": [

            (
                "🚰 Cierra los caños",

                "Evita mantener el agua "
                "corriendo cuando no sea necesaria."
            ),

            (
                "🚿 Reduce el tiempo de ducha",

                "Disminuye algunos minutos "
                "y cierra el agua mientras "
                "aplicas jabón o champú."
            ),

            (
                "🔧 Revisa fugas",

                "Inspecciona caños, tanques, "
                "inodoros y conexiones."
            ),

            (
                "🧺 Optimiza la lavadora",

                "Usa cargas completas y "
                "evita ciclos innecesarios."
            ),

            (
                "📊 Controla tu consumo",

                "Compara diferentes periodos "
                "para detectar aumentos anormales."
            )

        ],


        "Comercial": [

            (
                "📋 Control por actividad",

                "Registra el consumo por turno, "
                "área o actividad comercial."
            ),

            (
                "🔧 Mantén los equipos",

                "Revisa grifos, tuberías "
                "y equipos que utilizan agua."
            ),

            (
                "🧹 Mejora las rutinas de limpieza",

                "Evita utilizar agua corriente "
                "cuando no sea necesaria."
            ),

            (
                "📊 Compara periodos",

                "Relaciona el consumo con "
                "el nivel de actividad."
            )

        ],


        "Educativo": [

            (
                "🏫 Sensibiliza a los estudiantes",

                "Promueve hábitos y campañas "
                "para el uso responsable del agua."
            ),

            (
                "🚰 Revisa servicios higiénicos",

                "Controla fugas en inodoros, "
                "lavatorios y conexiones."
            ),

            (
                "📈 Monitorea mensualmente",

                "Compara consumo, asistencia "
                "y actividades institucionales."
            ),

            (
                "🌱 Optimiza el riego",

                "Utiliza horarios con "
                "menor evaporación."
            )

        ],


        "Institucional": [

            (
                "📊 Usa indicadores",

                "Compara el consumo por área, "
                "trabajador o periodo."
            ),

            (
                "🔧 Programa mantenimiento",

                "Realiza inspecciones "
                "preventivas."
            ),

            (
                "🚻 Revisa servicios higiénicos",

                "Prioriza zonas de uso frecuente."
            ),

            (
                "🎯 Establece metas",

                "Define reducciones progresivas "
                "y monitorea resultados."
            )

        ],


        "Riego": [

            (
                "🌅 Elige el horario adecuado",

                "Prefiere primeras horas "
                "de la mañana o final de la tarde."
            ),

            (
                "💧 Evita el exceso de riego",

                "Ajusta el volumen a las "
                "necesidades del área."
            ),

            (
                "🔍 Revisa pérdidas",

                "Inspecciona mangueras, "
                "uniones y conexiones."
            ),

            (
                "📅 Registra cada jornada",

                "Compara volumen, frecuencia "
                "y área irrigada."
            )

        ],


        "Otro": [

            (
                "📊 Mide antes de decidir",

                "Registra el consumo "
                "de forma constante."
            ),

            (
                "🔧 Revisa pérdidas",

                "Identifica fugas o usos "
                "innecesarios."
            ),

            (
                "🎯 Define una meta",

                "Utiliza el simulador "
                "para evaluar reducciones."
            ),

            (
                "📈 Evalúa resultados",

                "Compara los periodos "
                "antes y después de los cambios."
            )

        ]

    }


    for titulo, descripcion in (
        recomendaciones[
            tipo_recomendacion
        ]
    ):

        html(
            f"""
            <div class="tip">

                <h4>
                    {titulo}
                </h4>

                <p>
                    {descripcion}
                </p>

            </div>
            """
        )


# ============================================================
# MODELO MATEMÁTICO
# ============================================================

elif opcion == "🧮 Modelo matemático":

    st.header(
        "🧮 Modelo matemático"
    )


    html(
        """
        <div class="card">

            <h3>
                1. Consumo diario por persona
            </h3>

            <p>

                Para el análisis doméstico,
                AquaLog BI distribuye el
                volumen consumido entre
                las personas y los días
                correspondientes al periodo.

            </p>

        </div>
        """
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


    html(
        """
        <div class="card">

            <h3>
                2. Índice logarítmico
            </h3>

            <p>

                AquaLog BI transforma el
                consumo diario por persona
                a una escala logarítmica,
                permitiendo representar
                y comparar los valores
                de forma más compacta.

            </p>

        </div>
        """
    )


    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )


    st.warning(

        "⚠️ Los rangos BAJO, MODERADO "
        "y ALTO se aplican únicamente "
        "al análisis doméstico dentro "
        "del prototipo y deberán estar "
        "sustentados metodológicamente "
        "en el proyecto."

    )


    # =========================================
    # CALCULADORA
    # =========================================

    st.subheader(
        "🧪 Calculadora matemática"
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
                    "volumen_demo"

            )
        )


    with c2:

        personas_demo = (
            st.number_input(

                "P: personas",

                min_value=1,

                value=4,

                key=
                    "personas_demo"

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


    st.success(

        f"💧 Cₚ = "
        f"{cp_demo:.5f} m³/persona/día "
        f"= "
        f"{cp_demo * 1000:.2f} "
        f"L/persona/día | "

        f"🔢 Iₗ = "
        f"{il_demo:.5f}"

    )


# ============================================================
# PROYECTO
# ============================================================

elif opcion == "ℹ️ Proyecto":

    st.header(
        "ℹ️ Acerca del proyecto"
    )


    html(
        """
        <div class="card">

            <h3>
                📘 AquaLog BI
            </h3>

            <p>

                <b>

                Desarrollo de software basado
                en logaritmos matemáticos para
                la gestión eficiente del agua
                en el distrito de Baños del Inca,
                2026.

                </b>

            </p>

            <p>

                AquaLog BI está diseñado como
                un sistema de uso general.

                La ubicación, sector, zona y
                tipo de uso se determinan
                en cada registro.

            </p>

        </div>
        """
    )


    # =========================================
    # DOCENTE
    # =========================================

    st.subheader(
        "👩‍🏫 Docente"
    )


    html(
        """
        <div class="credit">

            👩‍🏫
            <b>
                Paola Ponce
            </b>

        </div>
        """
    )


    # =========================================
    # INTEGRANTES
    # =========================================

    st.subheader(
        "👥 Integrantes"
    )


    integrantes = [

        "Chuquiruna Escobal, Jhersonn",

        "Paz Muñoz, Vili",

        "Vasquez Azañero, Diego",

        "Vasquez Bustamante, Nathan Lowell"

    ]


    for integrante in integrantes:

        html(
            f"""
            <div class="credit">

                👤
                <b>
                    {integrante}
                </b>

            </div>
            """
        )


    # =========================================
    # FUNCIONALIDADES
    # =========================================

    st.subheader(
        "✨ ¿Qué puede hacer AquaLog BI?"
    )


    html(
        """
        <div class="card">

            <p>
                📝 Registrar diferentes tipos
                de usuarios y consumos.
            </p>

            <p>
                📍 Trabajar con diferentes
                sectores y comunidades.
            </p>

            <p>
                💧 Analizar el consumo de agua.
            </p>

            <p>
                🧮 Aplicar un modelo
                logarítmico.
            </p>

            <p>
                🔎 Buscar y filtrar información.
            </p>

            <p>
                👤 Consultar el historial
                de un usuario.
            </p>

            <p>
                🎯 Simular escenarios
                de ahorro.
            </p>

            <p>
                💰 Estimar posibles costos
                de consumo.
            </p>

            <p>
                📈 Analizar la evolución
                del consumo.
            </p>

            <p>
                🏆 Identificar los mayores
                consumos.
            </p>

            <p>
                💡 Generar recomendaciones
                según el tipo de uso.
            </p>

            <p>
                📥 Descargar la información
                registrada.
            </p>

        </div>
        """
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()


html(
    """
    <div class="footer">

        💧
        <b>
            AquaLog BI
        </b>

        <br>

        Sistema interactivo para el análisis
        y gestión eficiente del agua

        <br>

        Baños del Inca · Cajamarca · 2026

    </div>
    """
)
