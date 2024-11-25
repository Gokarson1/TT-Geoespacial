import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import folium
from shapely.geometry import Polygon
import json
from folium.plugins import Draw
from PIL import Image

# Open the logo image
img = Image.open("img/logo.png")

# Set page configuration with icon
st.set_page_config(page_title="Mapa interactivo", page_icon=img)

def app():
    st.title("Mapa interactivo con capas y dibujo")
    st.markdown(
        """
    Esta aplicación permite interactuar con mapas y cambiar entre diferentes capas como satélite, red fluvial o usos de suelos. Además, podrás trazar y exportar tus dibujos en formato GeoJSON.
    """
    )

    # Crear columnas para las opciones de la izquierda y mapa de la derecha
    row1_col1, row1_col2 = st.columns([3, 1])
    width = 800
    height = 600
    tiles = None

    # Panel de opciones en la columna de la izquierda
    with row1_col2:
        # Opción para cambiar entre capas
        checkbox_satellite = st.checkbox("Capa Satelital")
        checkbox_fluvial = st.checkbox("Red Fluvial")
        checkbox_landuse = st.checkbox("Usos de Suelo")

        # Exportar a GeoJSON
        export_geojson = st.button("Exportar a GeoJSON")

    # Crear el mapa en la columna de la derecha
    with row1_col1:
        m = leafmap.Map(center=[20, 0], zoom=2)

        # Añadir capas basadas en las opciones seleccionadas
        if checkbox_satellite:
            m.add_basemap("SATELLITE")
        if checkbox_fluvial:
            m.add_basemap("Stamen Toner")
        if checkbox_landuse:
            m.add_basemap("OpenStreetMap")

        # Usar folium para agregar control de dibujo
        draw = Draw(export=True)
        draw.add_to(m)

        # Mostrar el mapa
        m.to_streamlit(height=height)

        # Funcionalidad para exportar el dibujo como GeoJSON
        if export_geojson:
            geojson_data = m.get_drawings()
            if geojson_data:
                # Convertir GeoJSON a GeoDataFrame y exportar
                try:
                    geojson_obj = json.loads(geojson_data)
                    gdf = gpd.GeoDataFrame.from_features(geojson_obj["features"])
                    gdf.to_file("dibujo_exportado.geojson", driver="GeoJSON")
                    st.success("Dibujo exportado como GeoJSON.")
                except Exception as e:
                    st.error(f"Error al procesar el GeoJSON: {e}")
            else:
                st.error("No hay dibujos para exportar.")

# Ejecutar la aplicación
app()