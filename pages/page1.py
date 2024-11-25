import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium import LayerControl
from PIL import Image

# Open the logo image
img = Image.open("img/logo.png")

# Set page configuration with icon
st.set_page_config(page_title="Visualización de Datos Geoespaciales", page_icon=img)



# Sidebar navigation
st.sidebar.header("Navegación")
page = st.sidebar.radio("Selecciona la página", ["Shapefile", "CSV"])

# Map base selection in sidebar
st.sidebar.header("Seleccione el mapa base")
map_base = st.sidebar.selectbox(
    "Mapa base", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"]
)

# Function for creating base map with chosen tiles
def create_base_map(map_base_type):
    if map_base_type == "OpenStreetMap":
        return folium.Map(location=[0, 0], zoom_start=2, tiles="OpenStreetMap")
    elif map_base_type == "Stamen Terrain":
        return folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Terrain")
    elif map_base_type == "Stamen Toner":
        return folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Toner")
    elif map_base_type == "Stamen Watercolor":
        return folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Watercolor")

# Function to load and visualize ShapeFiles
def load_shapefile(shapefile_path, base_map):
    gdf = gpd.read_file(shapefile_path)
    folium.GeoJson(gdf).add_to(base_map)

# Function to load and visualize CSV with coordinates
def load_csv(csv_path, base_map):
    try:
        # Load the CSV file with semicolon as delimiter
        df = pd.read_csv(csv_path, delimiter=';')
        if "latitude" in df.columns and "longitude" in df.columns:
            for _, row in df.iterrows():
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=row["name"] if "name" in df.columns else None
                ).add_to(base_map)
        else:
            st.error("El archivo CSV no contiene las columnas 'latitude' y 'longitude'.")
    except Exception as e:
        st.error(f"No se pudo cargar el archivo CSV: {e}")

# Página Shapefile
if page == "Shapefile":
    st.header("Sube un archivo ShapeFile para visualizar.")
    shapefile_upload = st.file_uploader("Subir archivo ShapeFile (.shp, .shx, .dbf)", type=["zip"])
    base_map = create_base_map(map_base)
    if shapefile_upload:
        with open("temp.zip", "wb") as f:
            f.write(shapefile_upload.getbuffer())
        load_shapefile("temp.zip", base_map)
    LayerControl().add_to(base_map)
    st_folium(base_map, width=700, height=500)

# Página CSV
elif page == "CSV":
    st.header("Sube un archivo CSV con coordenadas para visualizar.")
    csv_upload = st.file_uploader("Subir archivo CSV", type=["csv"])
    base_map = create_base_map(map_base)
    if csv_upload:
        load_csv(csv_upload, base_map)
    LayerControl().add_to(base_map)
    st_folium(base_map, width=700, height=500)
