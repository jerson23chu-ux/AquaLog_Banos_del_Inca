import streamlit as st
import pandas as pd
import math
import os
from datetime import date, datetime


# ============================================================
# AQUAlog BI
# Sistema interactivo para análisis y gestión eficiente del agua
# ============================================================


# ============================================================
# 1. CONFIGURACIÓN GENERAL
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
# 2. ESTILOS
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

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.25);
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
    }

    .alert-red {
        background: #fff4f4;
        border-left: 6px solid #dc3545;
        padding: 14px 17px;
        border-radius: 13px;
        margin-bottom: 9px;
    }

    .alert-green {
        background: #f0fff7;
        border-left: 6px solid #18a568;
        padding: 14px 17px;
        border-radius: 13px;
        margin-bottom: 9px;
    }

    .alert-yellow {
        background: #fffbea;
        border-left: 6px solid #e5ad17;
        padding: 14px 17px;
        border-radius: 13px;
        margin-bottom: 9px;
    }

    .tip {
        background: white;
        border-left: 6px solid #0b8fe3;
        border-radius: 14px;
        padding: 15px 18px;
        margin: 9px 0;
        box-shadow: 0 5px 16px rgba(0,0,0,0.05);
    }

    .footer {
        text-align: center;
        color: #557286;
        padding: 18px 0 5px 0;
        font-size: 13px;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 12px;
        font-weight: 750;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. COMPONENTES VISUALES
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
# 4. BASE DE DATOS
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
# 5. MOTOR MATEMÁTICO
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
# 6. COMPARACIÓN ENTRE PERIODOS
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
# 7. ALERTAS AUTOMÁTICAS
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
# 8. RECOMENDACIONES
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
# 9. REPORTES
# ============================================================

def crear_reporte_texto(
    fila,
    historial
):

    codigo = fila["Código"]

    variacion = variacion_ultimo_periodo(
        historial
    )

    tendencia = tendencia_consumo(
        historial
    )

    if variacion is None:
        texto_variacion = (
            "No disponible"
        )
    else:
        texto_variacion = (
            f"{variacion:+.2f}%"
        )

    contenido = f"""
AQUALOG BI
REPORTE DE ANÁLISIS DEL CONSUMO DE AGUA

Fecha de generación:
{datetime.now().strftime("%d/%m/%Y %H:%M")}

--------------------------------------------------
IDENTIFICACIÓN
--------------------------------------------------

Código:
{fila["Código"]}

Fecha del registro:
{fila["Fecha"]}

Sector / comunidad:
{fila["Sector / comunidad"]}

Zona / referencia:
{fila["Zona / referencia"]}

Tipo de uso:
{fila["Tipo de uso"]}

--------------------------------------------------
DATOS REGISTRADOS
--------------------------------------------------

Personas o unidades de referencia:
{fila["Personas"]}

Consumo del periodo:
{fila["Consumo del periodo (m³)"]:.2f} m³

Días del periodo:
{fila["Días"]}

Tarifa:
S/ {fila["Tarifa (S/ por m³)"]:.2f} por m³

--------------------------------------------------
RESULTADOS
--------------------------------------------------

Consumo diario:
{fila["Consumo diario (m³)"]:.4f} m³/día

Consumo individual de referencia:
{fila["Consumo por persona (L/día)"]:.2f} L/día

Índice logarítmico:
{fila["Índice logarítmico"]:.5f}

Nivel:
{fila["Nivel"]}

Costo estimado:
S/ {fila["Costo del periodo (S/)"]:.2f}

--------------------------------------------------
ANÁLISIS HISTÓRICO
--------------------------------------------------

Número de registros:
{len(historial)}

Variación frente al periodo anterior:
{texto_variacion}

Tendencia reciente:
{tendencia}

--------------------------------------------------
OBSERVACIONES
--------------------------------------------------

{fila["Observaciones"]}

--------------------------------------------------

AquaLog BI
Inteligencia matemática para la gestión eficiente del agua
Baños del Inca - Cajamarca - 2026
"""

    return contenido.strip()


# ============================================================
# 10. INICIO DE SESIÓN
# ============================================================

if "df" not in st.session_state:

    st.session_state.df = cargar_datos()

df = normalizar_df(
    st.session_state.df
)


# ============================================================
# 11. MENÚ
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
            "📄 Reportes",
            "ℹ️ Proyecto"
        ]
    )

    st.divider()

    st.caption(
        "AquaLog BI es un sistema general "
        "adaptable a distintos tipos de uso, "
        "sectores y contextos."
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
# 13. NUEVO REGISTRO
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

            if tipo_uso == "Doméstico":

                nivel = resultado["nivel"]

                if nivel == "BAJO":

                    st.success(
                        "🟢 Nivel referencial: BAJO"
                    )

                elif nivel == "MODERADO":

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
                    "AquaLog BI presenta indicadores "
                    "y análisis histórico sin aplicar "
                    "clasificación doméstica."
                )

            hist_actual = historial_codigo(
                st.session_state.df,
                codigo
            )

            if len(hist_actual) >= 2:

                variacion = (
                    variacion_ultimo_periodo(
                        hist_actual
                    )
                )

                if variacion is not None:

                    if variacion > 0:

                        st.warning(
                            f"📈 El consumo aumentó "
                            f"{variacion:.1f}% respecto "
                            f"al periodo anterior."
                        )

                    elif variacion < 0:

                        st.success(
                            f"📉 El consumo disminuyó "
                            f"{abs(variacion):.1f}% respecto "
                            f"al periodo anterior."
                        )

            with st.expander(
                "🧮 Ver cálculo matemático"
            ):

                st.latex(
                    r"C_p=\frac{V}{P\times D}"
                )

                st.write(
                    f"Cₚ = {consumo:.2f} / "
                    f"({personas} × {dias}) "
                    f"= {resultado['cp']:.6f} "
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

        st.subheader(
            f"Resumen de {codigo}"
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

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Máximo registrado",
            f'{hist["Consumo del periodo (m³)"].max():.2f} m³'
        )

        c2.metric(
            "Mínimo registrado",
            f'{hist["Consumo del periodo (m³)"].min():.2f} m³'
        )

        c3.metric(
            "Tendencia reciente",
            tendencia
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

        st.subheader(
            "🔍 Interpretación"
        )

        if variacion is None:

            st.info(
                "Se necesita al menos un registro "
                "anterior para realizar una comparación."
            )

        elif variacion >= 20:

            alerta_html(
                "rojo",
                "Aumento importante",
                f"El consumo aumentó "
                f"{variacion:.1f}%."
            )

        elif variacion <= -10:

            alerta_html(
                "verde",
                "Mejora detectada",
                f"El consumo disminuyó "
                f"{abs(variacion):.1f}%."
            )

        else:

            alerta_html(
                "amarillo",
                "Variación moderada",
                f"El cambio frente al periodo "
                f"anterior fue de "
                f"{variacion:+.1f}%."
            )

        if tendencia == "CRECIENTE":

            st.warning(
                "⚠️ Los últimos registros presentan "
                "una tendencia creciente."
            )

        elif tendencia == "DECRECIENTE":

            st.success(
                "✅ Los últimos registros presentan "
                "una tendencia decreciente."
            )

        st.subheader(
            "📋 Historial"
        )

        mostrar = hist.drop(
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

        c1, c2, c3 = st.columns(3)

        sectores = sorted(
            [
                x
                for x in
                df[
                    "Sector / comunidad"
                ]
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

        with c1:

            filtro_sector = st.selectbox(
                "Sector",
                ["Todos"] + sectores
            )

        with c2:

            filtro_tipo = st.selectbox(
                "Tipo",
                ["Todos"] + tipos
            )

        with c3:

            filtro_nivel = st.selectbox(
                "Nivel",
                ["Todos"] + niveles
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
                busqueda
                .strip()
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

            filtrado = filtrado[
                mascara
            ]

        st.caption(
            f"{len(filtrado)} registro(s)."
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
            "📥 Descargar datos filtrados",
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
            "Selecciona un CSV",
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
                    f"{len(importado)} registros "
                    f"detectados."
                )

                if st.button(
                    "USAR ESTA BASE",
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

        borrar_df = (
            df.reset_index()
        )

        opciones = borrar_df.apply(
            lambda fila:
                f'{fila["index"]} | '
                f'{fila["Código"]} | '
                f'{fila["Fecha"]} | '
                f'{fila["Consumo del periodo (m³)"]:.2f} m³',
            axis=1
        ).tolist()

        seleccionar = st.selectbox(
            "Selecciona el registro",
            ["Seleccionar..."] + opciones
        )

        if st.button(
            "🗑️ ELIMINAR",
            use_container_width=True
        ):

            if seleccionar == "Seleccionar...":

                st.warning(
                    "Selecciona un registro."
                )

            else:

                indice = int(
                    seleccionar.split(
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
            step=0.1,
            key="sim_ind_consumo"
        )

        tarifa_base = st.number_input(
            "💰 Tarifa (S/ por m³)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            key="sim_ind_tarifa"
        )

        reduccion = st.slider(
            "🎯 Meta de reducción",
            0,
            50,
            15,
            1,
            format="%d%%",
            key="sim_ind_red"
        )

        nuevo = consumo_base * (
            1 - reduccion / 100
        )

        ahorro = (
            consumo_base - nuevo
        )

        ahorro_anual = (
            ahorro * 12
        )

        dinero = (
            ahorro * tarifa_base
        )

        dinero_anual = (
            dinero * 12
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Actual",
            f"{consumo_base:.2f} m³"
        )

        c2.metric(
            "Proyectado",
            f"{nuevo:.2f} m³"
        )

        c3.metric(
            "Ahorro/periodo",
            f"{ahorro:.2f} m³"
        )

        c4.metric(
            "Ahorro anual",
            f"{ahorro_anual:.2f} m³"
        )

        if tarifa_base > 0:

            st.success(
                f"💰 Ahorro económico estimado: "
                f"S/ {dinero:.2f} por periodo "
                f"y S/ {dinero_anual:.2f} al año."
            )

        escenarios = pd.Series(
            {
                "Actual": consumo_base,
                "Ahorro 5%":
                    consumo_base * 0.95,
                "Ahorro 10%":
                    consumo_base * 0.90,
                "Ahorro 15%":
                    consumo_base * 0.85,
                "Ahorro 20%":
                    consumo_base * 0.80,
                "Ahorro 25%":
                    consumo_base * 0.75,
                f"Meta {reduccion}%":
                    nuevo
            }
        )

        st.subheader(
            "📊 Comparación"
        )

        st.bar_chart(
            escenarios
        )

    with tab2:

        st.subheader(
            "Proyección colectiva"
        )

        unidades = st.number_input(
            "👥 Número de unidades, usuarios o puntos",
            min_value=1,
            value=10,
            key="colectivo_unidades"
        )

        consumo_promedio = st.number_input(
            "💧 Consumo promedio por unidad (m³)",
            min_value=0.01,
            value=18.0,
            step=0.1,
            key="colectivo_consumo"
        )

        reduccion_colectiva = st.slider(
            "🎯 Meta colectiva",
            0,
            50,
            15,
            1,
            format="%d%%",
            key="colectivo_reduccion"
        )

        consumo_actual_total = (
            unidades *
            consumo_promedio
        )

        ahorro_total = (
            consumo_actual_total *
            reduccion_colectiva /
            100
        )

        consumo_nuevo_total = (
            consumo_actual_total -
            ahorro_total
        )

        ahorro_anual_total = (
            ahorro_total * 12
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Consumo colectivo",
            f"{consumo_actual_total:.2f} m³"
        )

        c2.metric(
            "Nuevo escenario",
            f"{consumo_nuevo_total:.2f} m³"
        )

        c3.metric(
            "Ahorro/periodo",
            f"{ahorro_total:.2f} m³"
        )

        c4.metric(
            "Ahorro anual",
            f"{ahorro_anual_total:.2f} m³"
        )

        st.info(
            f"Si {unidades} unidades reducen "
            f"su consumo en "
            f"{reduccion_colectiva}%, "
            f"el ahorro proyectado es de "
            f"{ahorro_anual_total:.2f} m³ "
            f"en doce periodos equivalentes."
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
            "No existen registros."
        )

    else:

        c1, c2 = st.columns(2)

        tipos = sorted(
            df["Tipo de uso"]
            .unique()
            .tolist()
        )

        sectores = sorted(
            [
                x
                for x in
                df[
                    "Sector / comunidad"
                ]
                .astype(str)
                .unique()
                .tolist()
                if x.strip()
            ]
        )

        with c1:

            tipos_sel = st.multiselect(
                "Tipos de uso",
                tipos,
                default=tipos
            )

        with c2:

            sectores_sel = st.multiselect(
                "Sectores",
                sectores,
                default=sectores
            )

        analisis = df[
            df["Tipo de uso"]
            .isin(
                tipos_sel
            )
        ].copy()

        if sectores and sectores_sel:

            analisis = analisis[
                analisis[
                    "Sector / comunidad"
                ]
                .isin(
                    sectores_sel
                )
            ]

        if analisis.empty:

            st.warning(
                "No existen resultados "
                "para los filtros seleccionados."
            )

        else:

            c1, c2, c3, c4 = st.columns(4)

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
                "📊 Distribución por tipo"
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
                "📍 Distribución territorial"
            )

            sector_temp = (
                analisis.copy()
            )

            sector_temp[
                "Sector / comunidad"
            ] = (
                sector_temp[
                    "Sector / comunidad"
                ]
                .replace(
                    "",
                    "Sin especificar"
                )
            )

            por_sector = (
                sector_temp.groupby(
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

            evolucion = (
                analisis.copy()
            )

            evolucion["Fecha"] = (
                pd.to_datetime(
                    evolucion["Fecha"],
                    errors="coerce"
                )
            )

            evolucion = (
                evolucion.dropna(
                    subset=["Fecha"]
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
                "🏆 Ranking"
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
                        "Consumo por persona (L/día)",
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

                alerta_html(
                    alerta["tipo"],
                    alerta["titulo"],
                    alerta["texto"]
                )

        st.caption(
            "Las alertas comparativas utilizan "
            "los registros históricos disponibles "
            "para cada código."
        )


# ============================================================
# 19. RECOMENDACIONES
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
# 20. MOTOR MATEMÁTICO
# ============================================================

elif opcion == "🧮 Motor matemático":

    st.title(
        "Motor matemático AquaLog"
    )

    card(
        "Etapa 1 — Medición",
        "El sistema recibe el volumen consumido, "
        "el número de unidades de referencia "
        "y los días correspondientes al periodo.",
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

    st.write(
        "**Cₚ:** consumo unitario diario."
    )

    card(
        "Etapa 2 — Transformación logarítmica",
        "AquaLog BI transforma el indicador "
        "mediante una función logarítmica.",
        "2️⃣"
    )

    st.latex(
        r"I_L=\log_{10}(1+C_p)"
    )

    st.info(
        "El término +1 permite aplicar "
        "la transformación cuando el consumo "
        "se aproxima a cero."
    )

    card(
        "Etapa 3 — Interpretación",
        "Los resultados obtenidos pueden compararse "
        "entre registros y periodos para identificar "
        "cambios y tendencias.",
        "3️⃣"
    )

    st.warning(
        "Las categorías domésticas BAJO, MODERADO "
        "y ALTO forman parte de los criterios "
        "referenciales del prototipo. "
        "Deben estar sustentadas metodológicamente "
        "en el informe de investigación."
    )

    st.subheader(
        "🧪 Laboratorio matemático"
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
        f"{cp:.6f} m³/unidad/día"
    )

    c2.metric(
        "Equivalencia",
        f"{cp * 1000:.2f} L/unidad/día"
    )

    c3.metric(
        "Iₗ",
        f"{il:.6f}"
    )

    st.subheader(
        "🔄 Flujo del sistema"
    )

    st.success(
        "DATOS → PROCESAMIENTO → "
        "MODELO MATEMÁTICO → INDICADORES → "
        "INTERPRETACIÓN → DECISIÓN"
    )


# ============================================================
# 21. REPORTES
# ============================================================

elif opcion == "📄 Reportes":

    st.title(
        "Reportes AquaLog"
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
            "Selecciona un código",
            codigos
        )

        hist = historial_codigo(
            df,
            codigo
        )

        fila = hist.iloc[-1]

        st.subheader(
            "Vista previa"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Código",
            codigo
        )

        c2.metric(
            "Último consumo",
            f'{fila["Consumo del periodo (m³)"]:.2f} m³'
        )

        c3.metric(
            "Índice",
            f'{fila["Índice logarítmico"]:.5f}'
        )

        c4.metric(
            "Nivel",
            fila["Nivel"]
        )

        reporte = crear_reporte_texto(
            fila,
            hist
        )

        st.text_area(
            "Contenido del reporte",
            reporte,
            height=420
        )

        st.download_button(
            "📥 DESCARGAR REPORTE",
            data=reporte.encode(
                "utf-8"
            ),
            file_name=
                f"AquaLog_Reporte_{codigo}.txt",
            mime="text/plain",
            use_container_width=True
        )

        csv_historial = (
            hist.drop(
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
            data=csv_historial,
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

    st.subheader(
        "🚀 Funciones principales"
    )

    funciones = [
        "Registro de consumos.",
        "Historial por código.",
        "Análisis matemático.",
        "Transformación logarítmica.",
        "Comparación entre periodos.",
        "Detección de aumentos y reducciones.",
        "Análisis de tendencias.",
        "Centro de alertas.",
        "Análisis por sector.",
        "Análisis por tipo de uso.",
        "Simulación individual.",
        "Simulación colectiva.",
        "Proyección de ahorro.",
        "Estimación económica.",
        "Recomendaciones.",
        "Descarga de datos.",
        "Generación de reportes."
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
