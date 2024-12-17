import streamlit as st
import pandas as pd
import pydeck as pdk
import json
from PIL import Image

# Cargar imagen para el ícono
img = Image.open("img/GeoHub1.jpeg")

# Configuración de la página
st.set_page_config(
    page_title="Mapa 3D",
    layout="wide",
    page_icon=img
)

# Título y manual de uso
st.title("Visualización de edificios 3D en Santiago")
with st.expander("Manual de Uso: Mapa 3D"):
    st.write("""
        ### Manual de uso
        - **Sube un archivo geojson para la carga de datos.**
        - Asegúrate de que el geojson sea válido.
        - Una vez cargado, el mapa desplegará visualización 3D del geojson ingresado.

        :red[*Cabe recalcar que el mapa carga un archivo como demostración. La subida de archivos es opcional.*]
    """)

# Función para cargar el archivo GeoJSON
@st.cache_data
def load_geojson(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

# Ruta del archivo GeoJSON inicial
default_geojson_path = "data/edificios_santiago_50_mas_altos.geojson"

# Verificar si el archivo predeterminado existe
try:
    # Cargar archivo GeoJSON predeterminado
    default_data = load_geojson(default_geojson_path)

    # Convertir GeoJSON a DataFrame
    features = default_data["features"]
    default_df = pd.json_normalize(features)

    # Renombrar columnas para consistencia
    default_df.rename(columns={
        "geometry.coordinates": "coordinates",
        "properties.height_m": "height",
        "properties.name": "building_name"
    }, inplace=True)

    # Extraer coordenadas de latitud y longitud
    default_df["longitude"] = default_df["coordinates"].apply(lambda x: x[0])
    default_df["latitude"] = default_df["coordinates"].apply(lambda x: x[1])

except Exception as e:
    st.error(f"No se pudo cargar el archivo predeterminado: {e}")
    default_df = pd.DataFrame()  # Crear DataFrame vacío en caso de error

# Subir archivo opcional
uploaded_file = st.file_uploader("Carga el archivo de edificios (GeoJSON)", type=["geojson"])

# Usar datos del archivo subido o los datos predeterminados
if uploaded_file:
    # Cargar datos del archivo subido
    user_data = json.load(uploaded_file)
    features = user_data["features"]
    df = pd.json_normalize(features)

    # Renombrar columnas
    df.rename(columns={
        "geometry.coordinates": "coordinates",
        "properties.height_m": "height",
        "properties.name": "building_name"
    }, inplace=True)

    # Extraer coordenadas
    df["longitude"] = df["coordinates"].apply(lambda x: x[0])
    df["latitude"] = df["coordinates"].apply(lambda x: x[1])
else:
    # Usar datos predeterminados
    st.info("Cargando archivo predeterminado: **Edificios más altos de Santiago**")
    df = default_df

# Validar que existan datos
if not df.empty:
    # Capa para edificios en 3D
    layer = pdk.Layer(
        "ColumnLayer",
        data=df,
        get_position="[longitude, latitude]",
        get_elevation="height",
        elevation_scale=10,  # Escala de elevación
        radius=100,  # Radio de los puntos
        get_fill_color="[height, 140, 200]",
        pickable=True,
    )

    # Estado inicial del mapa centralizado en Santiago
    view_state = pdk.ViewState(
        latitude=-33.4489,  # Latitud de Santiago
        longitude=-70.6693,  # Longitud de Santiago
        zoom=12,
        pitch=50,
    )

    # Renderizar el mapa
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"html": "<b>Edificio:</b> {building_name}<br><b>Altura:</b> {height} m"},
        )
    )
else:
    st.error("No se encontraron datos para mostrar en el mapa.")
