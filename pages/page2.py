import streamlit as st
import geopandas as gpd     # estoe s para manejar los datos espaciales, vectoriales jiji
import folium                       #para visualizar mapas de forma interactiva
from streamlit_folium import st_folium #esto igual xd
from PIL import Image

img= Image.open("img/logo.png")

# Cargar los datos geoespaciales

st.set_page_config(page_title="Mapa de Yacimientos Mineros en Chile", layout="wide")
# Configuración básica de Streamlit
st.title("Visualización de Yacimientos Mineros en Chile")
st.write("Este mapa muestra yacimientos mineros en Chile.")

# Cargar archivo GeoJSON
uploaded_file = st.file_uploader("Sube tu archivo GeoJSON de los yacimientos mineros", type="geojson")

if uploaded_file is not None:
    # Leer archivo GeoJSON como GeoDataFrame
    gdf = gpd.read_file(uploaded_file)
    
    # Limitar el número de yacimientos para mejorar el rendimiento
    if len(gdf) > 500:
        gdf = gdf.sample(500, random_state=1)
    
    # Simplificar geometría para mayor rendimiento
    gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.05, preserve_topology=True)
    
    # Crear un mapa centrado en Chile
    mapa = folium.Map(location=[-30.0, -71.0], zoom_start=5)

    # Añadir marcadores circulares para cada yacimiento
    for _, row in gdf.iterrows():
        coords = row.geometry.centroid.coords[0] if not row.geometry.is_empty else None
        if coords:
            folium.CircleMarker(
                location=[coords[1], coords[0]],
                radius=5,
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.6,
                popup=f"Yacimiento: {row['nombre']}",
                tooltip=row['nombre']
            ).add_to(mapa)
    
    # Mostrar el mapa en Streamlit
    st_folium(mapa, width=800, height=600)
else:
    st.write("Por favor, sube un archivo GeoJSON para visualizar los yacimientos en el mapa.")