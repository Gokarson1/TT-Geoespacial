import streamlit as st
import leafmap.foliumap as leafmap
from io import BytesIO
import geopandas as gpd
import zipfile
from PIL import Image

# Open the logo image
img = Image.open("img/logo.png")

# Set page configuration with icon
st.set_page_config(layout="wide", page_icon=img)

# Título de la aplicación
st.title("Mapa Interactivo")
st.sidebar.info(
    """
    - Dibuje puntos, líneas o polígonos directamente en el mapa.
    - Cambie las capas base.
    - Exporte los datos como GeoJSON o shapefiles.
    """
)
# Opciones de capas base
basemaps = {
    "Callejero": "OpenStreetMap",
    "Satélite": "Esri.WorldImagery",
    "Topográfico": "Esri.WorldTopoMap",
    "Oscuro": "CartoDB.DarkMatter",
}

# Selección de capa base
selected_basemap = st.sidebar.selectbox("Seleccionar capa base", list(basemaps.keys()))

# Botón para exportar datos
export_format = st.sidebar.radio("Formato de exportación", ["GeoJSON", "Shapefile"])

# Título de la aplicación
st.title("Herramienta de Mapa en Blanco")

# Crear un mapa interactivo
m = leafmap.Map(tiles=basemaps[selected_basemap])
m.add_draw_control()  # Agrega herramientas de dibujo al mapa
m.add_measure_control()  # Agrega herramientas de medición
st.markdown("### Mapa Interactivo")
m.to_streamlit(height=600)

# Exportar datos dibujados
if m.user_drawing:
    st.sidebar.subheader("Exportar Datos")
    st.sidebar.write("Visualice o exporte las geometrías dibujadas en el mapa.")
    
    # Convertir los datos a GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(m.user_drawing, crs="EPSG:4326")
    st.sidebar.write(gdf)

    # Generar archivo para descarga
    if export_format == "GeoJSON":
        output = BytesIO()
        gdf.to_file(output, driver="GeoJSON")
        st.sidebar.download_button(
            label="Descargar como GeoJSON",
            data=output.getvalue(),
            file_name="mapa_dibujado.geojson",
            mime="application/json",
        )
    elif export_format == "Shapefile":
        output = BytesIO()
        with zipfile.ZipFile(output, mode="w") as zf:
            for filename, content in gdf.to_file("/vsimem/temp_shapefile", driver="ESRI Shapefile"):
                zf.writestr(filename, content)
        st.sidebar.download_button(
            label="Descargar como Shapefile",
            data=output.getvalue(),
            file_name="mapa_dibujado.zip",
            mime="application/zip",
        )