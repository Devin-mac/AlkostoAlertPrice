import pandas as pd
import streamlit as st
import plotly.express as px

# Archivos
CSV_HISTORICO = "productos.csv"
GTINS_FILE = "gtins.csv"

st.set_page_config(page_title="Alkosto Alert Price", layout="wide")
st.title("🛒 Evolución de precios - Alkosto")

# Leer datos históricos
try:
    df = pd.read_csv(CSV_HISTORICO, dtype=str)
    df["precio"] = df["precio"].astype(float)
    df["fecha"] = pd.to_datetime(df["fecha"])
except Exception as e:
    st.error(f"Error al cargar {CSV_HISTORICO}: {e}")
    st.stop()

# Leer nombres desde gtins.csv
try:
    df_gtins = pd.read_csv(GTINS_FILE, dtype=str)
    df_gtins = df_gtins[df_gtins["nombre"].notna() & (df_gtins["nombre"] != "")]
except Exception as e:
    st.error(f"Error al cargar {GTINS_FILE}: {e}")
    st.stop()

# Diccionarios para acceso
nombre_a_gtin = dict(zip(df_gtins["nombre"], df_gtins["gtin"]))
gtin_a_nombre = dict(zip(df_gtins["gtin"], df_gtins["nombre"]))

# Sidebar: buscador de productos
texto_busqueda = st.sidebar.text_input("🔍 Buscar productos por nombre (ej. 'Galaxy')", "")

# Filtrar productos según el texto ingresado
if texto_busqueda:
    nombres_filtrados = [n for n in nombre_a_gtin.keys() if texto_busqueda.lower() in n.lower()]
else:
    nombres_filtrados = list(nombre_a_gtin.keys())

seleccionados = st.sidebar.multiselect(
    "Selecciona uno o más productos",
    nombres_filtrados,
    default=nombres_filtrados[:1]
)


# Sidebar: filtro de fechas
fechas_disponibles = df["fecha"].sort_values().unique()
fecha_min, fecha_max = pd.to_datetime(fechas_disponibles[0]), pd.to_datetime(fechas_disponibles[-1])
rango_fechas = st.sidebar.date_input("📅 Filtrar por fechas", [fecha_min, fecha_max], min_value=fecha_min, max_value=fecha_max)

# --- Alertas visuales de baja de precio ---
st.subheader("🔔 Alertas de baja de precio")
for nombre in seleccionados:
    gtin = nombre_a_gtin[nombre]
    df_p = df[df["gtin"] == gtin]
    precios = df_p["precio"].astype(float)
    if len(precios) >= 2 and precios.iloc[-1] < precios.max():
        st.warning(f"⬇️ {nombre}: bajó a ${precios.iloc[-1]:,.0f}")

# --- Gráfico de evolución de precios ---
if seleccionados:
    fig = px.area()
    for nombre in seleccionados:
        gtin = nombre_a_gtin[nombre]
        df_p = df[df["gtin"] == gtin].copy()
        df_p = df_p[(df_p["fecha"] >= pd.to_datetime(rango_fechas[0])) & (df_p["fecha"] <= pd.to_datetime(rango_fechas[1]))]
        if not df_p.empty:
            fig.add_scatter(
                x=df_p["fecha"], y=df_p["precio"],
                mode="lines+markers", name=nombre,
                fill="tozeroy"
            )
        else:
            st.warning(f"⚠️ No hay datos para {nombre} en el rango seleccionado.")

    fig.update_layout(
        title="📈 Evolución de precios (gráfico de áreas)",
        xaxis_title="Fecha",
        yaxis_title="Precio (COP)",
        hovermode="x unified",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Selecciona al menos un producto para ver la gráfica.")



