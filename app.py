import streamlit as st
import math
import os
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt


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

META_MUESTRA = 75

SECTOR_ESTUDIO = "La Esperanza"
CAS_ESTUDIO = "Los Berros"


COLUMNAS = [
    "Hogar",
    "Fecha",
    "Sector",
    "CAS",
    "Tipo de vivienda",
    "Habitantes",
    "Consumo mensual (m³)",
    "Días",
    "Consumo diario (m³)",
    "Consumo por persona (L/día)",
    "Índice logarítmico",
    "Nivel"
]


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

/* ===============================
FONDO GENERAL
================================ */

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0,168,232,0.10),
            transparent 22%
        ),

        radial-gradient(
            circle at 90% 20%,
            rgba(0,91,234,0.10),
            transparent 24%
        ),

        linear-gradient(
            135deg,
            #eefbff 0%,
            #dff5ff 50%,
            #f8fdff 100%
        );

    color: #123047;
}


.stApp p,
.stApp label,
.stApp span {

    color: #123047;

}


/* ===============================
TÍTULOS
================================ */

h1,
h2,
h3,
h4 {

    color: #064b75 !important;

}


/* ===============================
ENCABEZADO PRINCIPAL
================================ */

.hero {

    background: linear-gradient(
        135deg,
        #004fc4 0%,
        #007fe8 50%,
        #00b7df 100%
    );

    border-radius: 26px;

    padding: 32px;

    color: white;

    box-shadow:
        0 10px 30px
        rgba(0,80,150,0.25);

    position: relative;

    overflow: hidden;

    margin-bottom: 24px;

}


.hero:before {

    content: "💧";

    position: absolute;

    right: 35px;

    top: 6px;

    font-size: 105px;

    opacity: 0.12;

}


.hero h1,
.hero h2,
.hero p {

    color: white !important;

    margin: 0;

}


.hero h1 {

    font-size: 46px;

    font-weight: 800;

}


.hero p {

    font-size: 17px;

    margin-top: 8px;

}


/* ===============================
TARJETAS
================================ */

.glass {

    background:
        rgba(255,255,255,0.94);

    border:
        1px solid
        rgba(0,110,180,0.10);

    border-radius: 20px;

    padding: 22px;

    box-shadow:
        0 7px 22px
        rgba(0,80,130,0.08);

    margin-bottom: 16px;

}


/* ===============================
MÉTRICAS
================================ */

.metric-card {

    background: white;

    border-radius: 18px;

    padding: 20px;

    text-align: center;

    box-shadow:
        0 6px 20px
        rgba(0,70,120,0.09);

    min-height: 140px;

}


.metric-card .ico {

    font-size: 30px;

}


.metric-card .val {

    font-size: 30px;

    font-weight: 800;

    color: #005bea !important;

}


.metric-card .lab {

    font-size: 13px;

    font-weight: 700;

    color: #31566b !important;

}


/* ===============================
NIVELES DE CONSUMO
================================ */

.level-low,
.level-mid,
.level-high {

    border-radius: 17px;

    padding: 19px;

    text-align: center;

    background: white;

    box-shadow:
        0 5px 16px
        rgba(0,0,0,0.07);

}


.level-low {

    border-top:
        5px solid #1f9d55;

}


.level-mid {

    border-top:
        5px solid #d99b00;

}


.level-high {

    border-top:
        5px solid #d93636;

}


/* ===============================
RECOMENDACIONES
================================ */

.tip {

    background: white;

    border-left:
        6px solid #008ed6;

    border-radius: 14px;

    padding: 17px 20px;

    margin: 10px 0;

    box-shadow:
        0 4px 14px
        rgba(0,0,0,0.06);

}


.tip h4 {

    margin: 0 0 5px 0;

}


.tip p {

    margin: 0;

}


/* ===============================
CRÉDITOS
================================ */

.credit {

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #eef9ff
        );

    border:
        1px solid #cfeefe;

    border-radius: 18px;

    padding: 18px;

    margin: 8px 0;

}


/* ===============================
ETIQUETAS
================================ */

.badge {

    display: inline-block;

    background: #e7f6ff;

    color: #045b8f !important;

    padding: 7px 12px;

    border-radius: 999px;

    font-weight: 700;

    margin-right: 6px;

    margin-bottom: 6px;

}


/* ===============================
SIDEBAR
================================ */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #004fc4,
            #007ddd,
            #00a8d8
        );

}


section[data-testid="stSidebar"] * {

    color: white !important;

}


/* ===============================
BOTONES
================================ */

.stButton button {

    background:
        linear-gradient(
            90deg,
            #005bea,
            #00a6d6
        );

    color: white !important;

    border: none;

    border-radius: 13px;

    font-weight: 700;

}


.stButton button:hover {

    transform:
        translateY(-1px);

}


/* ===============================
MÉTRICAS STREAMLIT
================================ */

[data-testid="stMetricValue"] {

    color: #064b75 !important;

    font-weight: 800;

}


[data-testid="stMetricLabel"] {

    color: #123047 !important;

}


/* ===============================
PIE DE PÁGINA
================================ */

.footer {

    text-align: center;

    color: #31566b;

    padding: 22px;

    font-size: 14px;

}

</style>
""", unsafe_allow_html=True)


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

    for columna in COLUMNAS:

        if columna not in df.columns:

            df[columna] = ""

    df["Sector"] = (
        df["Sector"]
        .replace(
            "",
            SECTOR_ESTUDIO
        )
    )

    df["CAS"] = (
        df["CAS"]
        .replace(
            "",
            CAS_ESTUDIO
        )
    )

    df["Días"] = (
        pd.to_numeric(
            df["Días"],
            errors="coerce"
        )
        .fillna(30)
        .astype(int)
    )

    df["Fecha"] = (
        df["Fecha"]
        .replace(
            "",
            pd.Timestamp.today().strftime(
                "%Y-%m-%d"
            )
        )
    )

    df["Tipo de vivienda"] = (
        df["Tipo de vivienda"]
        .replace(
            "",
            "No especificado"
        )
    )

    return df[COLUMNAS]


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
        encoding="utf-8-sig"
    )


if "df" not in st.session_state:

    st.session_state.df = (
        cargar_datos()
    )


# ============================================================
# MODELO MATEMÁTICO
# ============================================================

def analizar_consumo(
    habitantes,
    consumo_m3,
    dias
):

    consumo_diario_m3 = (
        consumo_m3 /
        dias
    )

    consumo_persona_m3_dia = (
        consumo_m3 /
        (
            habitantes *
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

    if litros_persona_dia < 100:

        nivel = "BAJO"

    elif litros_persona_dia <= 170:

        nivel = "MODERADO"

    else:

        nivel = "ALTO"

    return (
        consumo_diario_m3,
        consumo_persona_m3_dia,
        litros_persona_dia,
        indice_log,
        nivel
    )


# ============================================================
# RECOMENDACIONES
# ============================================================

def recomendaciones_por_nivel(
    nivel
):

    recomendaciones = [

        (
            "🚰 Cerrar los caños",

            "Cierra el caño mientras te cepillas "
            "los dientes, te enjabonas las manos "
            "o cuando no necesites agua corriendo."
        ),

        (
            "🚿 Reducir el tiempo de ducha",

            "Disminuye el tiempo de ducha y "
            "cierra el agua mientras aplicas "
            "jabón o champú."
        ),

        (
            "🔧 Revisar fugas",

            "Inspecciona caños, conexiones, "
            "tuberías e inodoros. Una fuga "
            "pequeña puede generar desperdicio "
            "constante."
        ),

        (
            "🪣 Usar recipientes",

            "Para algunas actividades de limpieza "
            "utiliza un balde o recipiente en lugar "
            "de mantener abierto el caño."
        ),

        (
            "🧺 Usar cargas completas",

            "Procura utilizar la lavadora con "
            "cargas completas y evita ciclos "
            "innecesarios."
        ),

        (
            "🌱 Riego responsable",

            "Riega durante las primeras horas "
            "de la mañana o al finalizar la tarde "
            "para reducir la evaporación."
        ),

        (
            "🚽 Revisar el inodoro",

            "Verifica que el tanque y las válvulas "
            "del inodoro no presenten pérdidas."
        ),

        (
            "♻️ Reutilizar agua",

            "Cuando sea apropiado y seguro, "
            "reutiliza agua para actividades "
            "como limpieza o riego."
        ),

        (
            "📊 Monitorear el consumo",

            "Compara periódicamente tu consumo "
            "para detectar incrementos y evaluar "
            "si las medidas de ahorro funcionan."
        )

    ]

    if nivel == "BAJO":

        return [
            recomendaciones[0],
            recomendaciones[1],
            recomendaciones[2],
            recomendaciones[5],
            recomendaciones[8]
        ]

    elif nivel == "MODERADO":

        return recomendaciones

    else:

        return [

            (
                "🚨 Acción prioritaria",

                "El consumo registrado es elevado. "
                "Se recomienda revisar primero "
                "posibles fugas en caños, tanques, "
                "inodoros y tuberías."
            ),

            *recomendaciones

        ]


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    f"""
    <div class="hero">

        <h1>
        💧 AquaLog BI
        </h1>

        <p>
        Inteligencia matemática para la gestión
        eficiente del agua
        </p>

        <p>
        📍 Sector {SECTOR_ESTUDIO}
        · CAS {CAS_ESTUDIO}
        · Baños del Inca
        · 2026
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MENÚ LATERAL
# ============================================================

st.sidebar.markdown(
    """
    <h1 style="
        text-align:center;
        color:white!important;">
        💧
    </h1>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
    <h2 style="
        text-align:center;
        color:white!important;">
        AquaLog BI
    </h2>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
    <p style="
        text-align:center;
        color:white!important;">
        Gestión inteligente del agua
    </p>
    """,
    unsafe_allow_html=True
)


st.sidebar.divider()


opcion = st.sidebar.radio(

    "MENÚ PRINCIPAL",

    [

        "🏠 Dashboard",

        "📝 Registrar usuario",

        "📊 Base de datos",

        "📈 Análisis y gráficos",

        "💡 Recomendaciones",

        "🧮 Modelo matemático",

        "ℹ️ Acerca del proyecto"

    ]

)


st.sidebar.divider()


st.sidebar.caption(
    f"Muestra objetivo: "
    f"{META_MUESTRA} usuarios"
)


# ============================================================
# DASHBOARD
# ============================================================

if opcion == "🏠 Dashboard":

    st.header(
        "🌊 Dashboard general"
    )

    df = normalizar_df(
        st.session_state.df
    )

    if df.empty:

        st.info(
            "💧 Aún no existen usuarios registrados. "
            "Ingresa el primer registro desde "
            "📝 Registrar usuario."
        )

    else:

        total = len(df)

        avance = min(
            total /
            META_MUESTRA,
            1.0
        )

        consumo_promedio = (
            pd.to_numeric(
                df[
                    "Consumo mensual (m³)"
                ],
                errors="coerce"
            )
            .mean()
        )

        litros_promedio = (
            pd.to_numeric(
                df[
                    "Consumo por persona (L/día)"
                ],
                errors="coerce"
            )
            .mean()
        )

        indice_promedio = (
            pd.to_numeric(
                df[
                    "Índice logarítmico"
                ],
                errors="coerce"
            )
            .mean()
        )


        # MÉTRICAS

        columnas = st.columns(4)


        tarjetas = [

            (
                "👥",
                f"{total}/{META_MUESTRA}",
                "USUARIOS REGISTRADOS"
            ),

            (
                "💧",
                f"{consumo_promedio:.2f}",
                "CONSUMO PROMEDIO m³"
            ),

            (
                "👤",
                f"{litros_promedio:.1f}",
                "L/PERSONA/DÍA"
            ),

            (
                "🔢",
                f"{indice_promedio:.4f}",
                "ÍNDICE LOGARÍTMICO"
            )

        ]


        for columna, tarjeta in zip(
            columnas,
            tarjetas
        ):

            icono, valor, titulo = (
                tarjeta
            )

            with columna:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="ico">
                        {icono}
                        </div>

                        <div class="val">
                        {valor}
                        </div>

                        <div class="lab">
                        {titulo}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        st.write("")


        # AVANCE DE LA MUESTRA

        st.subheader(
            "🎯 Avance de la muestra"
        )

        st.progress(
            avance
        )

        st.caption(
            f"{total} de {META_MUESTRA} "
            f"usuarios registrados "
            f"({avance * 100:.1f}%)."
        )


        # NIVELES

        bajos = int(
            (
                df["Nivel"]
                == "BAJO"
            ).sum()
        )

        moderados = int(
            (
                df["Nivel"]
                == "MODERADO"
            ).sum()
        )

        altos = int(
            (
                df["Nivel"]
                == "ALTO"
            ).sum()
        )


        st.subheader(
            "📊 Clasificación del consumo"
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            st.markdown(
                f"""
                <div class="level-low">

                    <h2>🟢</h2>

                    <h3>
                    Bajo
                    </h3>

                    <h1>
                    {bajos}
                    </h1>

                    <p>
                    usuarios
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:

            st.markdown(
                f"""
                <div class="level-mid">

                    <h2>🟡</h2>

                    <h3>
                    Moderado
                    </h3>

                    <h1>
                    {moderados}
                    </h1>

                    <p>
                    usuarios
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c3:

            st.markdown(
                f"""
                <div class="level-high">

                    <h2>🔴</h2>

                    <h3>
                    Alto
                    </h3>

                    <h1>
                    {altos}
                    </h1>

                    <p>
                    usuarios
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.write("")


        # MAYOR Y MENOR CONSUMO

        consumo_numerico = (
            pd.to_numeric(
                df[
                    "Consumo mensual (m³)"
                ],
                errors="coerce"
            )
        )


        indice_mayor = (
            consumo_numerico
            .idxmax()
        )


        indice_menor = (
            consumo_numerico
            .idxmin()
        )


        mayor = df.loc[
            indice_mayor
        ]


        menor = df.loc[
            indice_menor
        ]


        c1, c2 = st.columns(2)


        with c1:

            st.markdown(
                f"""
                <div class="glass">

                    <h3>
                    🔴 Mayor consumo mensual
                    </h3>

                    <p>
                    <b>
                    {mayor["Hogar"]}
                    </b>
                    ·
                    {float(
                        mayor[
                            "Consumo mensual (m³)"
                        ]
                    ):.2f}
                    m³
                    </p>

                    <p>
                    {mayor["Habitantes"]}
                    habitantes
                    ·
                    {mayor["Nivel"]}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with c2:

            st.markdown(
                f"""
                <div class="glass">

                    <h3>
                    🟢 Menor consumo mensual
                    </h3>

                    <p>
                    <b>
                    {menor["Hogar"]}
                    </b>
                    ·
                    {float(
                        menor[
                            "Consumo mensual (m³)"
                        ]
                    ):.2f}
                    m³
                    </p>

                    <p>
                    {menor["Habitantes"]}
                    habitantes
                    ·
                    {menor["Nivel"]}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# REGISTRAR USUARIO
# ============================================================

elif opcion == "📝 Registrar usuario":

    st.header(
        "📝 Registro de consumo"
    )


    st.write(
        "Registra un usuario del sector de estudio. "
        "AquaLog BI calculará automáticamente "
        "los indicadores matemáticos."
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        codigo = st.text_input(

            "🆔 Código del usuario",

            placeholder="Ejemplo: U001"

        )


        fecha_registro = st.date_input(

            "📅 Fecha del registro",

            value=date.today()

        )


    with c2:

        habitantes = st.number_input(

            "👥 Número de habitantes",

            min_value=1,

            max_value=20,

            value=4

        )


        vivienda = st.selectbox(

            "🏠 Tipo de vivienda",

            [

                "Casa independiente",

                "Vivienda multifamiliar",

                "Departamento",

                "Otro"

            ]

        )


    with c3:

        consumo = st.number_input(

            "💧 Consumo mensual (m³)",

            min_value=0.1,

            value=18.0,

            step=0.1

        )


        dias = st.number_input(

            "📆 Días del periodo",

            min_value=1,

            max_value=31,

            value=30

        )


    st.markdown(

        f"""
        <span class="badge">
        📍 {SECTOR_ESTUDIO}
        </span>

        <span class="badge">
        CAS {CAS_ESTUDIO}
        </span>
        """,

        unsafe_allow_html=True

    )


    st.write("")


    if st.button(

        "💧 ANALIZAR Y REGISTRAR",

        use_container_width=True

    ):


        codigo_limpio = (
            codigo
            .strip()
            .upper()
        )


        if (
            not st.session_state.df.empty
        ):

            codigos = (

                st.session_state.df[
                    "Hogar"
                ]

                .astype(str)

                .str.upper()

                .tolist()

            )

        else:

            codigos = []


        if not codigo_limpio:

            st.error(
                "⚠️ Ingresa un código de usuario."
            )


        elif codigo_limpio in codigos:

            st.error(
                "⚠️ Ese código ya existe. "
                "Utiliza un código diferente."
            )


        else:

            (
                consumo_diario,

                consumo_persona_m3,

                litros_persona,

                indice_log,

                nivel

            ) = analizar_consumo(

                habitantes,

                consumo,

                dias

            )


            nuevo_registro = pd.DataFrame(

                [

                    {

                        "Hogar":
                        codigo_limpio,

                        "Fecha":
                        fecha_registro.strftime(
                            "%Y-%m-%d"
                        ),

                        "Sector":
                        SECTOR_ESTUDIO,

                        "CAS":
                        CAS_ESTUDIO,

                        "Tipo de vivienda":
                        vivienda,

                        "Habitantes":
                        habitantes,

                        "Consumo mensual (m³)":
                        consumo,

                        "Días":
                        dias,

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
                            4
                        ),

                        "Nivel":
                        nivel

                    }

                ]

            )


            st.session_state.df = (
                pd.concat(

                    [

                        normalizar_df(
                            st.session_state.df
                        ),

                        nuevo_registro

                    ],

                    ignore_index=True

                )
            )


            guardar_datos(
                st.session_state.df
            )


            st.success(
                "✅ Usuario registrado correctamente."
            )


            st.divider()


            # RESULTADOS

            st.subheader(
                "📊 Resultado del análisis"
            )


            c1, c2, c3, c4 = (
                st.columns(4)
            )


            c1.metric(

                "💧 Consumo diario",

                f"{consumo_diario:.3f} m³"

            )


            c2.metric(

                "👤 Por persona",

                f"{litros_persona:.1f} L/día"

            )


            c3.metric(

                "🔢 Índice log.",

                f"{indice_log:.4f}"

            )


            c4.metric(

                "📊 Nivel",

                nivel

            )


            if nivel == "BAJO":

                st.success(
                    "🟢 CONSUMO BAJO"
                )


            elif nivel == "MODERADO":

                st.warning(
                    "🟡 CONSUMO MODERADO"
                )


            else:

                st.error(
                    "🔴 CONSUMO ALTO"
                )


            # MODELO MATEMÁTICO

            st.divider()


            st.subheader(
                "🧮 Desarrollo matemático"
            )


            st.write(
                "Primero se calcula el "
                "consumo diario por persona:"
            )


            st.latex(
                r"C_p=\frac{V}{P\times D}"
            )


            st.write(

                f"**Cₚ = "
                f"{consumo:.2f} / "
                f"({habitantes} × {dias}) "
                f"= "
                f"{consumo_persona_m3:.5f} "
                f"m³/persona/día**"

            )


            st.write(
                "Posteriormente se aplica "
                "el modelo logarítmico:"
            )


            st.latex(
                r"I_L=\log_{10}(1+C_p)"
            )


            st.write(

                f"**Iₗ = log₁₀"
                f"(1 + "
                f"{consumo_persona_m3:.5f}) "
                f"= {indice_log:.4f}**"

            )


            # RECOMENDACIONES

            st.divider()


            st.subheader(
                "💡 Recomendaciones"
            )


            recomendaciones = (
                recomendaciones_por_nivel(
                    nivel
                )
            )


            for titulo, descripcion in (
                recomendaciones
            ):

                st.markdown(

                    f"""
                    <div class="tip">

                        <h4>
                        {titulo}
                        </h4>

                        <p>
                        {descripcion}
                        </p>

                    </div>
                    """,

                    unsafe_allow_html=True

                )


# ============================================================
# BASE DE DATOS
# ============================================================

elif opcion == "📊 Base de datos":

    st.header(
        "📊 Base de datos de usuarios"
    )


    df = normalizar_df(
        st.session_state.df
    )


    if df.empty:

        st.info(
            "💧 Todavía no existen registros."
        )


    else:

        c1, c2 = st.columns(2)


        with c1:

            filtro_nivel = st.selectbox(

                "📊 Filtrar por nivel",

                [

                    "TODOS",

                    "BAJO",

                    "MODERADO",

                    "ALTO"

                ]

            )


        with c2:

            busqueda = st.text_input(

                "🔎 Buscar código",

                placeholder="Ejemplo: U001"

            )


        filtrado = df.copy()


        if filtro_nivel != "TODOS":

            filtrado = filtrado[

                filtrado[
                    "Nivel"
                ]

                == filtro_nivel

            ]


        if busqueda.strip():

            filtrado = filtrado[

                filtrado[
                    "Hogar"
                ]

                .astype(str)

                .str.contains(

                    busqueda.strip(),

                    case=False,

                    na=False

                )

            ]


        st.dataframe(

            filtrado,

            use_container_width=True,

            hide_index=True

        )


        # DESCARGA

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

            "📥 Descargar datos en CSV",

            data=csv,

            file_name=
            "AquaLog_usuarios.csv",

            mime="text/csv",

            use_container_width=True

        )


        # IMPORTAR

        st.divider()


        st.subheader(
            "📤 Importar datos"
        )


        archivo = st.file_uploader(

            "Sube un archivo CSV de AquaLog BI",

            type=[
                "csv"
            ]

        )


        if archivo is not None:

            try:

                importado = (
                    pd.read_csv(
                        archivo
                    )
                )

                importado = (
                    normalizar_df(
                        importado
                    )
                )


                if st.button(

                    "✅ REEMPLAZAR BASE "
                    "CON ESTE CSV",

                    use_container_width=True

                ):

                    st.session_state.df = (
                        importado
                    )

                    guardar_datos(
                        importado
                    )

                    st.success(
                        "✅ Base de datos "
                        "importada correctamente."
                    )

                    st.rerun()


            except Exception as error:

                st.error(
                    f"No se pudo leer "
                    f"el archivo: {error}"
                )


        # ELIMINAR

        st.divider()


        st.subheader(
            "🗑️ Eliminar un registro"
        )


        eliminar = st.text_input(

            "Código del usuario "
            "que deseas eliminar",

            placeholder="Ejemplo: U001"

        )


        if st.button(

            "🗑️ ELIMINAR REGISTRO",

            use_container_width=True

        ):


            codigo_eliminar = (

                eliminar
                .strip()
                .upper()

            )


            codigos_actuales = (

                df["Hogar"]

                .astype(str)

                .str.upper()

                .tolist()

            )


            if (
                codigo_eliminar
                in codigos_actuales
            ):

                st.session_state.df = (

                    df[

                        df["Hogar"]

                        .astype(str)

                        .str.upper()

                        != codigo_eliminar

                    ]

                    .reset_index(
                        drop=True
                    )

                )


                guardar_datos(
                    st.session_state.df
                )


                st.success(
                    "✅ Registro eliminado."
                )


                st.rerun()


            else:

                st.error(
                    "⚠️ No se encontró "
                    "ese código."
                )


# ============================================================
# ANÁLISIS Y GRÁFICOS
# ============================================================

elif opcion == "📈 Análisis y gráficos":

    st.header(
        "📈 Análisis del consumo de agua"
    )


    df = normalizar_df(
        st.session_state.df
    )


    if df.empty:

        st.info(
            "💧 Registra usuarios "
            "para generar gráficos."
        )


    else:


        # GRÁFICO 1

        st.subheader(
            "💧 Consumo mensual por usuario"
        )


        fig, ax = plt.subplots(
            figsize=(10, 5)
        )


        ax.bar(

            df["Hogar"]
            .astype(str),

            pd.to_numeric(

                df[
                    "Consumo mensual (m³)"
                ],

                errors="coerce"

            )

        )


        ax.set_xlabel(
            "Usuario"
        )


        ax.set_ylabel(
            "Consumo mensual (m³)"
        )


        ax.set_title(
            "Consumo mensual registrado"
        )


        ax.grid(
            axis="y",
            alpha=0.2
        )


        plt.xticks(
            rotation=45
        )


        st.pyplot(
            fig
        )


        plt.close(
            fig
        )


        # GRÁFICO 2

        st.subheader(
            "👤 Consumo diario por persona"
        )


        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )


        valores = pd.to_numeric(

            df[
                "Consumo por persona (L/día)"
            ],

            errors="coerce"

        )


        ax2.bar(

            df["Hogar"]
            .astype(str),

            valores

        )


        ax2.axhline(

            100,

            linestyle="--",

            label=
            "Referencia 100 L/persona/día"

        )


        ax2.axhline(

            170,

            linestyle="--",

            label=
            "Referencia 170 L/persona/día"

        )


        ax2.set_xlabel(
            "Usuario"
        )


        ax2.set_ylabel(
            "Litros/persona/día"
        )


        ax2.set_title(
            "Consumo diario por persona"
        )


        ax2.legend()


        ax2.grid(
            axis="y",
            alpha=0.2
        )


        plt.xticks(
            rotation=45
        )


        st.pyplot(
            fig2
        )


        plt.close(
            fig2
        )


        c1, c2 = st.columns(2)


        # GRÁFICO 3

        with c1:

            st.subheader(
                "📊 Distribución por nivel"
            )


            niveles = (
                df[
                    "Nivel"
                ]
                .value_counts()
            )


            fig3, ax3 = (
                plt.subplots(
                    figsize=(7, 5)
                )
            )


            ax3.pie(

                niveles.values,

                labels=
                niveles.index,

                autopct=
                "%1.1f%%"

            )


            ax3.set_title(
                "Nivel de consumo"
            )


            st.pyplot(
                fig3
            )


            plt.close(
                fig3
            )


        # GRÁFICO 4

        with c2:

            st.subheader(
                "🔢 Índice logarítmico"
            )


            fig4, ax4 = (
                plt.subplots(
                    figsize=(7, 5)
                )
            )


            ax4.bar(

                df["Hogar"]
                .astype(str),

                pd.to_numeric(

                    df[
                        "Índice logarítmico"
                    ],

                    errors="coerce"

                )

            )


            ax4.set_xlabel(
                "Usuario"
            )


            ax4.set_ylabel(
                "Índice logarítmico"
            )


            ax4.set_title(
                "Índice logarítmico "
                "por usuario"
            )


            ax4.grid(
                axis="y",
                alpha=0.2
            )


            plt.xticks(
                rotation=45
            )


            st.pyplot(
                fig4
            )


            plt.close(
                fig4
            )


        # RANKING

        st.subheader(
            "🏆 Usuarios con mayor consumo"
        )


        ranking = (

            df

            .sort_values(

                "Consumo mensual (m³)",

                ascending=False

            )

            [

                [

                    "Hogar",

                    "Habitantes",

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
# RECOMENDACIONES GENERALES
# ============================================================

elif opcion == "💡 Recomendaciones":

    st.header(
        "💡 Recomendaciones "
        "para el ahorro de agua"
    )


    st.write(
        "Pequeñas acciones cotidianas "
        "pueden contribuir a reducir "
        "el desperdicio de agua."
    )


    recomendaciones_generales = [

        (
            "🚰 Cierra los caños",

            "No dejes abierto el caño "
            "mientras te cepillas los dientes, "
            "te enjabonas o realizas actividades "
            "que no requieren flujo continuo."
        ),

        (
            "🚿 Reduce las duchas",

            "Disminuye el tiempo de ducha "
            "y cierra el agua mientras "
            "utilizas jabón o champú."
        ),

        (
            "🔧 Repara las fugas",

            "Revisa caños, conexiones, "
            "tanques, tuberías e inodoros. "
            "Una fuga constante puede "
            "incrementar considerablemente "
            "el consumo."
        ),

        (
            "🪣 Usa recipientes",

            "En determinadas tareas "
            "de limpieza utiliza un balde "
            "en lugar de mantener "
            "el agua corriendo."
        ),

        (
            "🧺 Optimiza la lavadora",

            "Utiliza cargas completas "
            "y evita realizar ciclos "
            "innecesarios."
        ),

        (
            "🌱 Riega responsablemente",

            "Riega temprano por la mañana "
            "o al finalizar la tarde para "
            "disminuir la pérdida de agua "
            "por evaporación."
        ),

        (
            "🚽 Revisa el inodoro",

            "Comprueba que el tanque "
            "no continúe descargando agua "
            "después de ser utilizado."
        ),

        (
            "♻️ Reutiliza agua",

            "Cuando sea apropiado y seguro, "
            "reutiliza agua para actividades "
            "como limpieza o riego."
        ),

        (
            "📊 Controla tu consumo",

            "Registra periódicamente "
            "el consumo para identificar "
            "aumentos y evaluar tus "
            "hábitos de ahorro."
        )

    ]


    for titulo, descripcion in (
        recomendaciones_generales
    ):

        st.markdown(

            f"""
            <div class="tip">

                <h4>
                {titulo}
                </h4>

                <p>
                {descripcion}
                </p>

            </div>
            """,

            unsafe_allow_html=True

        )


# ============================================================
# MODELO MATEMÁTICO
# ============================================================

elif opcion == "🧮 Modelo matemático":

    st.header(
        "🧮 Modelo matemático "
        "de AquaLog BI"
    )


    st.markdown(
        """
        <div class="glass">

            <h3>
            1. Consumo diario por persona
            </h3>

            <p>
            El consumo mensual se distribuye
            entre el número de habitantes
            y los días correspondientes
            al periodo analizado.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.latex(
        r"C_p=\frac{V}{P\times D}"
    )


    st.write(
        "**V** = volumen mensual "
        "consumido en metros cúbicos."
    )


    st.write(
        "**P** = número de habitantes "
        "del hogar."
    )


    st.write(
        "**D** = cantidad de días "
        "del periodo."
    )


    st.write(
        "**Cₚ** = consumo por persona "
        "en m³/persona/día."
    )


    st.divider()


    st.markdown(
        """
        <div class="glass">

            <h3>
            2. Índice logarítmico
            </h3>

            <p>
            AquaLog BI aplica una
            transformación logarítmica
            al consumo por persona para
            representar los valores en
            una escala comprimida y
            facilitar su comparación.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )


    st.write(
        "**Iₗ** representa el "
        "índice logarítmico obtenido."
    )


    st.write(
        "El valor 1 se incorpora "
        "para mantener definida "
        "la expresión matemática "
        "cuando el consumo sea cero."
    )


    st.warning(
        "⚠️ Los rangos de consumo "
        "utilizados para clasificar "
        "BAJO, MODERADO y ALTO "
        "son criterios referenciales "
        "del prototipo y deben quedar "
        "sustentados metodológicamente "
        "en la investigación."
    )


# ============================================================
# ACERCA DEL PROYECTO
# ============================================================

elif opcion == "ℹ️ Acerca del proyecto":

    st.header(
        "ℹ️ Acerca de AquaLog BI"
    )


    st.markdown(
        """
        <div class="glass">

            <h3>
            📘 Proyecto de investigación
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
            📍 Ámbito de aplicación:
            <b>
            Sector La Esperanza –
            CAS Los Berros
            </b>
            </p>

            <p>
            👥 Muestra:
            <b>
            75 usuarios
            </b>
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # DOCENTE

    st.subheader(
        "👩‍🏫 Docente"
    )


    st.markdown(
        """
        <div class="credit">

            <h3>
            👩‍🏫 Paola Ponce
            </h3>

        </div>
        """,
        unsafe_allow_html=True
    )


    # INTEGRANTES

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

        st.markdown(

            f"""
            <div class="credit">

                👤
                <b>
                {integrante}
                </b>

            </div>
            """,

            unsafe_allow_html=True

        )


    # FINALIDAD

    st.subheader(
        "🎯 Finalidad del proyecto"
    )


    st.markdown(
        """
        <div class="glass">

            <p>
            AquaLog BI busca apoyar el
            registro, procesamiento y análisis
            del consumo doméstico de agua
            mediante herramientas matemáticas
            y tecnológicas que faciliten
            la interpretación de los datos
            y contribuyan a promover
            un uso responsable del agua.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # FUNCIONES

    st.subheader(
        "⚙️ ¿Qué realiza AquaLog BI?"
    )


    st.markdown(
        """
        <div class="glass">

        <p>
        📝 Registra información de los usuarios.
        </p>

        <p>
        💧 Procesa el consumo mensual de agua.
        </p>

        <p>
        👤 Calcula el consumo diario por persona.
        </p>

        <p>
        🧮 Aplica un modelo basado en logaritmos.
        </p>

        <p>
        📊 Clasifica los resultados obtenidos.
        </p>

        <p>
        📈 Genera gráficos para interpretar
        la información.
        </p>

        <p>
        💡 Proporciona recomendaciones
        relacionadas con el ahorro de agua.
        </p>

        <p>
        📥 Permite descargar los datos
        registrados.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()


st.markdown(
    """
    <div class="footer">

        💧
        <b>
        AquaLog BI
        </b>

        <br><br>

        Inteligencia matemática para
        el cuidado y gestión eficiente
        del agua

        <br>

        📍 Sector La Esperanza
        · CAS Los Berros
        · Baños del Inca
        · Cajamarca

        <br>

        📅 2026

    </div>
    """,
    unsafe_allow_html=True
)
