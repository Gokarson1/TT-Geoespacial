import zipfile
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
import os
from PIL import Image

# Abrir la imagen del logo
img = Image.open("img/GeoHub1.jpeg")

# Configuración de la página
st.set_page_config(
    page_title="Mapa de Aeropuertos en Chile",
    layout="wide",
    page_icon=img
)

# Título de la página
st.title("Visualización de Aeropuertos en Chile")
st.write("""
Esta página permite explorar los **aeropuertos de Chile** a través de un mapa interactivo. Este visualizador tiene como objetivo proporcionar una forma sencilla de visualizar la distribución de los aeropuertos en Chile, lo cual es útil para estudios de transporte aéreo, geografía y planificación de infraestructura.
""")

# Ruta del archivo zip
zip_file_path = "data/Aeropuertos.zip"

# Descomprimir el archivo .zip
if os.path.exists(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("temp_dir")

    # Buscar el archivo .shp dentro del directorio descomprimido
    shapefile_path = None
    for root, dirs, files in os.walk("temp_dir"):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                break

    if shapefile_path is not None:
        # Leer el archivo .shp usando geopandas
        gdf = gpd.read_file(shapefile_path)

        # Calcular el centro del mapa para centrarlo automáticamente
        gdf['lon'] = gdf.geometry.centroid.x
        gdf['lat'] = gdf.geometry.centroid.y

        # Crear un mapa usando leafmap sin herramientas de búsqueda o dibujo
        m = leafmap.Map(
            center=[gdf['lat'].mean(), gdf['lon'].mean()],
            zoom=6,
            draw_control=False,
            search_control=False
        )

        # Añadir los datos al mapa
        m.add_gdf(gdf, layer_name="Aeropuertos")

        # Mostrar el mapa en Streamlit
        st.subheader("Mapa de Aeropuertos")
        m.to_streamlit(height=800)

        # Mostrar la tabla completa debajo del mapa
        st.subheader("Datos de Aeropuertos")
        st.write(gdf)
    else:
        st.error("No se encontró ningún archivo .shp en el archivo .zip.")
else:
    st.error("No se encontró el archivo 'data/Aeropuertos.zip'. Por favor, verifica la ruta.")
