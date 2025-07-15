import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Seguimiento de precios Alkosto", layout="wide")
st.title("📊 Evolución de precios - Alkosto")

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("productos.csv", parse_dates=["fecha"])
    return df

df = cargar_datos()

# --- Filtro por producto(s) ---
productos_disponibles = df["nombre"].dropna().unique()
productos_seleccionados = st.multiselect(
    "🛍 Selecciona uno o varios productos:",
    options=productos_disponibles,
    default=productos_disponibles[72:74],
)

# --- Filtro por rango de fechas ---
min_fecha = df["fecha"].min().date()
max_fecha = df["fecha"].max().date()
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("📅 Fecha de inicio:", min_value=min_fecha, max_value=max_fecha, value=min_fecha)
with col2:
    fecha_fin = st.date_input("📅 Fecha de fin:", min_value=min_fecha, max_value=max_fecha, value=max_fecha)

# --- Filtrar dataframe ---
df_filtrado = df[
    (df["nombre"].isin(productos_seleccionados)) &
    (df["fecha"].dt.date >= fecha_inicio) &
    (df["fecha"].dt.date <= fecha_fin)
]

# --- Mostrar alerta visual si hay baja de precio ---
st.subheader("🔔 Alertas de baja de precio")
for producto in productos_seleccionados:
    precios = df_filtrado[df_filtrado["nombre"] == producto].sort_values("fecha")["precio"]
    if len(precios) >= 2 and precios.iloc[-1] < precios.max():
        st.warning(f"⬇️ {producto}: bajó a ${precios.iloc[-1]:,}")

# --- Gráfico de evolución de precios ---
if not df_filtrado.empty:
    fig = px.line(
        df_filtrado,
        x="fecha",
        y="precio",
        color="nombre",
        markers=True,
        title="Evolución del precio en el tiempo"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay datos para el rango de fechas o productos seleccionados.")


