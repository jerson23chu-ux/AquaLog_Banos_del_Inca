import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="AquaLog BI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ARCHIVO PERMANENTE
# ============================================================

ARCHIVO_DATOS = "hogares.csv"


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

/* FONDO GENERAL */

.stApp {
    background: linear-gradient(
        135deg,
        #e8f8ff 0%,
        #d5f3ff 50%,
        #f8fdff 100%
    );

    color: #123047;
}


/* TEXTO GENERAL */

.stApp p,
.stApp label,
.stApp span {
    color: #123047;
}


/* TÍTULOS */

h1, h2, h3, h4 {
    color: #064b75 !important;
}


/* ENCABEZADO */

.main-title {
    background: linear-gradient(
        135deg,
        #005bea,
        #00a8e8
    );

    padding: 30px;

    border-radius: 22px;

    color: white;

    text-align: center;

    box-shadow:
        0 8px 25px rgba(0, 80, 150, 0.25);

    margin-bottom: 25px;
}

.main-title h1 {
    color: white !important;
    font-size: 44px;
    margin: 0;
    font-weight: 800;
}

.main-title p {
    color: white !important;
    font-size: 18px;
    margin-top: 8px;
}


/* TARJETAS DEL DASHBOARD */

.dashboard-card {
    background: white;

    padding: 20px;

    border-radius: 18px;

    text-align: center;

    box-shadow:
        0 5px 18px rgba(0,0,0,0.10);

    min-height: 145px;
}

.dashboard-card .icon {
    font-size: 32px;
}

.dashboard-card .number {
    font-size: 30px;
    font-weight: bold;
    color: #005bea !important;
}

.dashboard-card .title {
    font-size: 15px;
    font-weight: bold;
    color: #31566b !important;
}


/* TARJETAS DE NIVELES */

.level-low {
    background: #e8f8ee;
    border-left: 7px solid #20a05a;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
}

.level-medium {
    background: #fff8df;
    border-left: 7px solid #e3a900;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
}

.level-high {
    background: #ffe9e9;
    border-left: 7px solid #d93636;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
}


/* TARJETAS BLANCAS */

.card {
    background: white;

    padding: 25px;

    border-radius: 20px;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.08);

    margin-bottom: 20px;
}

.card h3 {
    color: #064b75 !important;
}

.card p {
    color: #123047 !important;
    font-size: 16px;
}


/* TARJETAS AZULES */

.card-blue {
    background: linear-gradient(
        135deg,
        #0066cc,
        #00a6d6
    );

    color: white;

    padding: 28px;

    border-radius: 20px;

    text-align: center;

    min-height: 170px;

    box-shadow:
        0 7px 20px rgba(0,90,160,0.20);
}

.card-blue h2,
.card-blue h3,
.card-blue p {
    color: white !important;
}


/* RECOMENDACIONES */

.recommendation {
    background: white;

    border-left: 7px solid #008ed6;

    padding: 20px;

    border-radius: 14px;

    margin: 12px 0;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.08);
}

.recommendation h3 {
    color: #064b75 !important;
}

.recommendation p {
    color: #123047 !important;
    font-size: 16px;
}


/* BARRA LATERAL */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #005bea,
        #008ed6,
        #00a6d6
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* BOTONES */

.stButton button {
    background: linear-gradient(
        90deg,
        #0066cc,
        #00a6d6
    );

    color: white !important;

    border: none;

    border-radius: 14px;

    padding: 12px 20px;

    font-size: 16px;

    font-weight: bold;
}


/* INPUTS */

input,
textarea {
    color: #123047 !important;
    background-color: white !important;
}


/* MÉTRICAS */

[data-testid="stMetricValue"] {
    color: #064b75 !important;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #123047 !important;
}


/* PIE */

.footer {
    text-align: center;
    color: #31566b;
    padding: 25px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARGAR DATOS
# ============================================================

if "hogares" not in st.session_state:

    if os.path.exists(ARCHIVO_DATOS):

        try:

            df_guardado = pd.read_csv(
                ARCHIVO_DATOS
            )

            st.session_state.hogares = (
                df_guardado.to_dict(
                    orient="records"
                )
            )

        except Exception:

            st.session_state.hogares = []

    else:

        st.session_state.hogares = []


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown("""
<div class="main-title">

<h1>💧 AquaLog BI</h1>

<p>
Sistema inteligente para la gestión eficiente del agua
</p>

<p>
📍 Baños del Inca - Cajamarca | 📅 2026
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIÓN DE ANÁLISIS
# ============================================================

def analizar_consumo(
    habitantes,
    consumo,
    dias
):

    consumo_diario = consumo / dias

    consumo_persona = (
        consumo /
        (habitantes * dias)
    )

    litros_persona = (
        consumo_persona * 1000
    )

    indice_log = math.log10(
        1 + consumo_persona
    )

    if litros_persona < 100:

        nivel = "BAJO"

    elif litros_persona <= 170:

        nivel = "MODERADO"

    else:

        nivel = "ALTO"

    return (
        consumo_diario,
        consumo_persona,
        litros_persona,
        indice_log,
        nivel
    )


# ============================================================
# RECOMENDACIONES
# ============================================================

def obtener_recomendaciones(nivel):

    if nivel == "BAJO":

        return [
            "🚰 Cierra los caños cuando no estén en uso.",
            "🦷 Cierra el caño mientras te cepillas los dientes.",
            "🚿 Mantén un tiempo adecuado durante la ducha.",
            "🌱 Riega las plantas en horarios de menor evaporación.",
            "🔧 Revisa periódicamente las instalaciones.",
            "💧 Continúa monitoreando el consumo."
        ]

    elif nivel == "MODERADO":

        return [
            "🚰 Cierra los caños mientras no estés utilizando el agua.",
            "🦷 No dejes correr el agua mientras te cepillas los dientes.",
            "🚿 Reduce el tiempo de las duchas.",
            "🔧 Revisa caños, grifos e inodoros para detectar fugas.",
            "🧺 Utiliza la lavadora con cargas completas.",
            "🪣 Utiliza recipientes para determinadas actividades.",
            "🌱 Evita utilizar más agua de la necesaria para regar.",
            "📊 Registra periódicamente el consumo."
        ]

    else:

        return [
            "🔧 Revisa inmediatamente caños, grifos, inodoros y tuberías.",
            "🚰 Cierra los caños cuando no estén siendo utilizados.",
            "🚿 Reduce el tiempo de las duchas.",
            "🦷 Cierra el caño mientras te cepillas los dientes.",
            "🪣 Utiliza recipientes en lugar de dejar correr el agua.",
            "🧺 Evita utilizar la lavadora con cargas pequeñas.",
            "🌱 Controla el agua utilizada para el riego.",
            "♻️ Reutiliza agua cuando sea apropiado.",
            "🚽 Comprueba que el inodoro no tenga fugas.",
            "📊 Registra nuevamente el consumo."
        ]


# ============================================================
# MENÚ
# ============================================================

st.sidebar.markdown(
    """
    <h1 style="text-align:center;color:white!important;">
    💧
    </h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <h2 style="text-align:center;color:white!important;">
    AquaLog BI
    </h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <p style="text-align:center;color:white!important;">
    Gestión inteligente del agua
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

opcion = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "🏠 Inicio",
        "📝 Registrar hogar",
        "📊 Resultados",
        "📈 Gráficos",
        "💡 Recomendaciones"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if opcion == "🏠 Inicio":

    st.header(
        "🌊 Dashboard de AquaLog BI"
    )

    df = pd.DataFrame(
        st.session_state.hogares
    )

    # --------------------------------------------------------
    # SI NO HAY DATOS
    # --------------------------------------------------------

    if df.empty:

        st.markdown("""
        <div class="card">

        <h3>💧 Bienvenido a AquaLog BI</h3>

        <p>
        Aún no existen hogares registrados.
        Comienza registrando el primer hogar para
        visualizar los indicadores del sistema.
        </p>

        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("""
            <div class="card-blue">

            <h2>📝</h2>

            <h3>Registrar</h3>

            <p>
            Ingresa los datos de los hogares.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class="card-blue">

            <h2>🧮</h2>

            <h3>Analizar</h3>

            <p>
            Calcula el consumo y el índice logarítmico.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown("""
            <div class="card-blue">

            <h2>📊</h2>

            <h3>Visualizar</h3>

            <p>
            Consulta gráficos y resultados.
            </p>

            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # SI YA HAY DATOS
    # --------------------------------------------------------

    else:

        # INDICADORES

        total_hogares = len(df)

        consumo_promedio = df[
            "Consumo mensual (m³)"
        ].mean()

        promedio_persona = df[
            "Consumo por persona (L/día)"
        ].mean()

        indice_promedio = df[
            "Índice logarítmico"
        ].mean()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="dashboard-card">

                <div class="icon">🏠</div>

                <div class="number">
                {total_hogares}
                </div>

                <div class="title">
                HOGARES REGISTRADOS
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="dashboard-card">

                <div class="icon">💧</div>

                <div class="number">
                {consumo_promedio:.2f}
                </div>

                <div class="title">
                CONSUMO PROMEDIO (m³)
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="dashboard-card">

                <div class="icon">👤</div>

                <div class="number">
                {promedio_persona:.1f}
                </div>

                <div class="title">
                LITROS/PERSONA/DÍA
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                f"""
                <div class="dashboard-card">

                <div class="icon">🔢</div>

                <div class="number">
                {indice_promedio:.4f}
                </div>

                <div class="title">
                ÍNDICE LOGARÍTMICO
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # ----------------------------------------------------
        # NIVELES
        # ----------------------------------------------------

        bajos = len(
            df[df["Nivel"] == "BAJO"]
        )

        moderados = len(
            df[df["Nivel"] == "MODERADO"]
        )

        altos = len(
            df[df["Nivel"] == "ALTO"]
        )

        st.subheader(
            "📊 Clasificación de los hogares"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="level-low">

                <h2>🟢</h2>

                <h3>Consumo bajo</h3>

                <h1>{bajos}</h1>

                <p>hogares</p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="level-medium">

                <h2>🟡</h2>

                <h3>Consumo moderado</h3>

                <h1>{moderados}</h1>

                <p>hogares</p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="level-high">

                <h2>🔴</h2>

                <h3>Consumo alto</h3>

                <h1>{altos}</h1>

                <p>hogares</p>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # ----------------------------------------------------
        # MAYOR Y MENOR CONSUMO
        # ----------------------------------------------------

        hogar_mayor = df.loc[
            df["Consumo mensual (m³)"].idxmax()
        ]

        hogar_menor = df.loc[
            df["Consumo mensual (m³)"].idxmin()
        ]

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                f"""
                <div class="card">

                <h3>🔴 Mayor consumo</h3>

                <p>
                <b>Hogar:</b> {hogar_mayor["Hogar"]}
                </p>

                <p>
                <b>Consumo:</b>
                {hogar_mayor["Consumo mensual (m³)"]:.2f} m³
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="card">

                <h3>🟢 Menor consumo</h3>

                <p>
                <b>Hogar:</b> {hogar_menor["Hogar"]}
                </p>

                <p>
                <b>Consumo:</b>
                {hogar_menor["Consumo mensual (m³)"]:.2f} m³
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # GRÁFICO DEL DASHBOARD
        # ----------------------------------------------------

        st.subheader(
            "📈 Distribución de hogares"
        )

        niveles = df[
            "Nivel"
        ].value_counts()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.pie(
            niveles.values,
            labels=niveles.index,
            autopct="%1.1f%%"
        )

        ax.set_title(
            "Distribución según nivel de consumo"
        )

        st.pyplot(fig)

        plt.close(fig)

        st.info(
            "💡 Los indicadores se actualizan automáticamente "
            "cuando registras nuevos hogares."
        )


# ============================================================
# REGISTRAR HOGAR
# ============================================================

elif opcion == "📝 Registrar hogar":

    st.header(
        "📝 Registro de consumo de agua"
    )

    st.write(
        "Ingresa los datos correspondientes al hogar."
    )

    col1, col2 = st.columns(2)

    with col1:

        codigo = st.text_input(
            "🏠 Código del hogar",
            placeholder="Ejemplo: H001"
        )

        habitantes = st.number_input(
            "👥 Número de habitantes",
            min_value=1,
            max_value=20,
            value=4
        )

    with col2:

        consumo = st.number_input(
            "💧 Consumo mensual (m³)",
            min_value=0.0,
            value=18.0,
            step=0.1
        )

        dias = st.number_input(
            "📅 Número de días",
            min_value=1,
            max_value=31,
            value=30
        )

    st.write("")

    if st.button(
        "💧 ANALIZAR Y REGISTRAR",
        use_container_width=True
    ):

        if codigo.strip() == "":

            st.error(
                "⚠️ Ingresa el código del hogar."
            )

        elif consumo <= 0:

            st.error(
                "⚠️ El consumo debe ser mayor que cero."
            )

        else:

            (
                consumo_diario,
                consumo_persona,
                litros_persona,
                indice_log,
                nivel
            ) = analizar_consumo(
                habitantes,
                consumo,
                dias
            )

            hogar = {

                "Hogar": codigo.upper(),

                "Habitantes": habitantes,

                "Consumo mensual (m³)": consumo,

                "Consumo diario (m³)": round(
                    consumo_diario,
                    3
                ),

                "Consumo por persona (L/día)": round(
                    litros_persona,
                    2
                ),

                "Índice logarítmico": round(
                    indice_log,
                    4
                ),

                "Nivel": nivel
            }

            st.session_state.hogares.append(
                hogar
            )

            df_guardado = pd.DataFrame(
                st.session_state.hogares
            )

            df_guardado.to_csv(
                ARCHIVO_DATOS,
                index=False,
                encoding="utf-8-sig"
            )

            st.success(
                "✅ ¡Hogar registrado y guardado correctamente!"
            )

            st.divider()

            st.subheader(
                "📊 Resultado del análisis"
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "💧 Consumo diario",
                    f"{consumo_diario:.2f} m³"
                )

            with c2:

                st.metric(
                    "👤 Por persona",
                    f"{litros_persona:.1f} L/día"
                )

            with c3:

                st.metric(
                    "🔢 Índice logarítmico",
                    f"{indice_log:.4f}"
                )

            with c4:

                st.metric(
                    "📊 Nivel",
                    nivel
                )

            st.divider()

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

            st.divider()

            st.subheader(
                "🧮 Modelo matemático"
            )

            st.latex(
                r"I_L = \log_{10}(1+C_p)"
            )

            st.write(
                f"Consumo por persona: "
                f"{consumo_persona:.4f} m³/persona/día"
            )

            st.write(
                f"Índice logarítmico obtenido: "
                f"{indice_log:.4f}"
            )

            st.divider()

            st.subheader(
                "💡 Recomendaciones para este hogar"
            )

            recomendaciones = obtener_recomendaciones(
                nivel
            )

            for recomendacion in recomendaciones:

                st.markdown(
                    f"""
                    <div class="recommendation">

                    <p>{recomendacion}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# RESULTADOS
# ============================================================

elif opcion == "📊 Resultados":

    st.header(
        "📊 Resultados de los hogares"
    )

    if len(st.session_state.hogares) == 0:

        st.info(
            "💧 Todavía no hay hogares registrados."
        )

    else:

        df = pd.DataFrame(
            st.session_state.hogares
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.write("")

        csv = df.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="📥 Descargar datos en CSV",
            data=csv,
            file_name="AquaLog_Hogares.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "📌 Resumen general"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "🏠 Hogares",
                len(df)
            )

        with c2:

            promedio = df[
                "Consumo mensual (m³)"
            ].mean()

            st.metric(
                "💧 Consumo promedio",
                f"{promedio:.2f} m³"
            )

        with c3:

            promedio_persona = df[
                "Consumo por persona (L/día)"
            ].mean()

            st.metric(
                "👤 Promedio/persona",
                f"{promedio_persona:.1f} L/día"
            )

        with c4:

            promedio_log = df[
                "Índice logarítmico"
            ].mean()

            st.metric(
                "🔢 Índice promedio",
                f"{promedio_log:.4f}"
            )


# ============================================================
# GRÁFICOS
# ============================================================

elif opcion == "📈 Gráficos":

    st.header(
        "📈 Visualización del consumo"
    )

    if len(st.session_state.hogares) == 0:

        st.info(
            "💧 Registra hogares para visualizar los gráficos."
        )

    else:

        df = pd.DataFrame(
            st.session_state.hogares
        )

        st.subheader(
            "💧 Consumo mensual por hogar"
        )

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        ax.bar(
            df["Hogar"],
            df["Consumo mensual (m³)"]
        )

        ax.set_xlabel(
            "Hogar"
        )

        ax.set_ylabel(
            "Consumo mensual (m³)"
        )

        ax.set_title(
            "Consumo mensual de agua"
        )

        ax.grid(
            axis="y",
            alpha=0.2
        )

        st.pyplot(fig)

        plt.close(fig)

        st.subheader(
            "👤 Consumo diario por persona"
        )

        fig2, ax2 = plt.subplots(
            figsize=(10, 5)
        )

        ax2.bar(
            df["Hogar"],
            df[
                "Consumo por persona (L/día)"
            ]
        )

        ax2.set_xlabel(
            "Hogar"
        )

        ax2.set_ylabel(
            "Litros/persona/día"
        )

        ax2.set_title(
            "Consumo diario por persona"
        )

        ax2.grid(
            axis="y",
            alpha=0.2
        )

        st.pyplot(fig2)

        plt.close(fig2)


# ============================================================
# RECOMENDACIONES
# ============================================================

elif opcion == "💡 Recomendaciones":

    st.header(
        "💡 Consejos para ahorrar agua"
    )

    st.write(
        "Pequeñas acciones diarias pueden ayudar "
        "a reducir el consumo de agua."
    )

    recomendaciones_generales = [

        (
            "🚰 Cerrar los caños",
            "Cierra el caño mientras te cepillas "
            "los dientes, te enjabonas las manos "
            "o realizas una actividad que no "
            "requiera que el agua esté corriendo."
        ),

        (
            "🚿 Reducir el tiempo de ducha",
            "Procura reducir el tiempo de la ducha "
            "y evita dejar correr el agua mientras "
            "te aplicas jabón o champú."
        ),

        (
            "🔧 Revisar fugas",
            "Revisa periódicamente caños, grifos, "
            "inodoros y tuberías. Una fuga puede "
            "generar desperdicio constante."
        ),

        (
            "🦷 Cepillarse los dientes",
            "Cierra el caño mientras te cepillas "
            "los dientes y ábrelo solamente para "
            "enjuagarte."
        ),

        (
            "🧺 Usar correctamente la lavadora",
            "Procura utilizar la lavadora cuando "
            "tenga una carga suficiente para evitar "
            "utilizar agua innecesariamente."
        ),

        (
            "🪣 Utilizar recipientes",
            "Para algunas tareas de limpieza, utiliza "
            "un recipiente con agua en lugar de dejar "
            "el caño abierto continuamente."
        ),

        (
            "🌱 Cuidar el agua de riego",
            "Riega las plantas preferentemente durante "
            "las primeras horas de la mañana o al final "
            "de la tarde."
        ),

        (
            "♻️ Reutilizar agua",
            "Cuando sea apropiado y seguro, reutiliza "
            "agua para actividades como limpieza "
            "o riego."
        ),

        (
            "🚽 Revisar el inodoro",
            "Comprueba que el inodoro no tenga fugas "
            "y evita utilizar más agua de la necesaria."
        ),

        (
            "📊 Registrar el consumo",
            "Anota periódicamente el consumo del hogar "
            "para identificar aumentos o disminuciones."
        )
    ]

    for titulo, descripcion in recomendaciones_generales:

        st.markdown(
            f"""
            <div class="recommendation">

            <h3>{titulo}</h3>

            <p>{descripcion}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.divider()

st.markdown("""
<div class="footer">

💧 <b>AquaLog BI</b><br><br>

Gestión eficiente del agua mediante herramientas matemáticas<br>

📍 Baños del Inca - Cajamarca | 📅 2026

</div>
""", unsafe_allow_html=True)