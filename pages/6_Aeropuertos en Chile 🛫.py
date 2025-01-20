import zipfile
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
import os
import json
from PIL import Image

# Abrir la imagen del logo
img = Image.open("img/GeoHub1.jpeg")

# Configuración de la página
st.set_page_config(
    page_title="Mapa de Aeropuertos en Chile",
    layout="wide",
    page_icon=img
)

# Función para cargar las capas desde el archivo JSON
def load_layers_from_json(file_path):
    try:
        with open(file_path, "r") as f:
            layers = json.load(f)
        return layers
    except Exception as e:
        st.error(f"Error al cargar el archivo JSON: {e}")
        return []

# Función para crear el mapa de Leafmap
def create_map(selected_layer_url, layer_name, layer_attribution, gdf=None):
    # Crear el mapa sin herramientas de dibujo ni exportación
    m = leafmap.Map(center=[20.0, 0.0], zoom=2, draw_control=False, search_control=False)

    # Verificar que la URL no esté vacía o mal formateada
    if selected_layer_url:
        try:
            st.write(f"URL de la capa seleccionada: {selected_layer_url}")  # Mostrar la URL seleccionada
            m.add_tile_layer(url=selected_layer_url, name=layer_name, attribution=layer_attribution)
        except Exception as e:
            st.error(f"Error al agregar la capa: {e}")
            return None
    else:
        st.error("La URL de la capa seleccionada no es válida.")
        return None
    
    # Si hay un GeoDataFrame, añadirlo al mapa
    if gdf is not None:
        m.add_gdf(gdf, layer_name="Aeropuertos")

    return m

# Título y descripción en la página
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

        # Cargar las capas desde el archivo JSON
        layers = load_layers_from_json("data/layers.json")

        # Mostrar un selector para elegir la capa
        if layers:
            layer_names = [layer["name"] for layer in layers]
            selected_layer_name = st.selectbox("Selecciona una capa base", layer_names)

            # Encontrar la URL de la capa seleccionada
            selected_layer = next(layer for layer in layers if layer["name"] == selected_layer_name)
            selected_layer_url = selected_layer.get("url", "")
            selected_layer_name = selected_layer.get("name", "")
            selected_layer_attribution = selected_layer.get("attribution", "")

            # Crear el mapa con la capa seleccionada y los aeropuertos
            m = create_map(selected_layer_url, selected_layer_name, selected_layer_attribution, gdf=gdf)

            # Verificar que el mapa se haya creado correctamente antes de renderizarlo
            if m:
                map_html = m.to_html()
                st.components.v1.html(map_html, height=800)

                # Mostrar la tabla completa debajo del mapa
                st.subheader("Datos de Aeropuertos")
                st.write(gdf)  # Mostrar la tabla con los datos

        else:
            st.warning("No se pudieron cargar las capas desde el archivo JSON.")
    else:
        st.error("No se encontró ningún archivo .shp en el archivo .zip.")
else:
    st.error("No se encontró el archivo 'data/Aeropuertos.zip'. Por favor, verifica la ruta.")
