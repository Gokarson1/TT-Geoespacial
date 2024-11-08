import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import LayerControl
from PIL import Image

img= Image.open("img/logo.png")

# Contenido de la página 1
st.set_page_config(page_title="Página de Visualización de Datos", page_icon=img)
st.write("Sube un archivo de datos geoespaciales para visualizar.")

# Selección de mapas base
st.sidebar.header("Seleccione el mapa base")
map_base = st.sidebar.selectbox(
    "Mapa base", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"]
)


# Crear el mapa con el mapa base seleccionado
if map_base == "OpenStreetMap":
    base_map = folium.Map(location=[0, 0], zoom_start=2, tiles="OpenStreetMap")
elif map_base == "Stamen Terrain":
    base_map = folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Terrain")
elif map_base == "Stamen Toner":
    base_map = folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Toner")
elif map_base == "Stamen Watercolor":
    base_map = folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Watercolor")

# Función para cargar y visualizar archivos ShapeFile
def load_shapefile(shapefile_path):
    gdf = gpd.read_file(shapefile_path)
    folium.GeoJson(gdf).add_to(base_map)

# Función para cargar y visualizar archivos CSV con coordenadas
def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    if "latitude" in df.columns and "longitude" in df.columns:
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=row["name"] if "name" in df.columns else None
            ).add_to(base_map)
    else:
        st.error("El archivo CSV no contiene las columnas 'latitude' y 'longitude'.")
        
# Cargar archivo ShapeFile
shapefile_upload = st.sidebar.file_uploader("Subir archivo ShapeFile (.shp, .shx, .dbf)", type=["zip"])
if shapefile_upload:
    with open("temp.zip", "wb") as f:
        f.write(shapefile_upload.getbuffer())
    load_shapefile("temp.zip")

# Cargar archivo CSV
csv_upload = st.sidebar.file_uploader("Subir archivo CSV", type=["csv"])
if csv_upload:
    load_csv(csv_upload)

# Agregar control de capas
LayerControl().add_to(base_map)

# Mostrar el mapa en la aplicación de Streamlit
st_folium(base_map, width=700, height=500)