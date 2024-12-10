import streamlit as st
import leafmap.foliumap as leafmap
from streamlit.components.v1 import html
import json
from PIL import Image

# Cargar el logo
img = Image.open("img/logo.png")
st.set_page_config(layout="wide", page_icon=img)

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
def create_map(selected_layer_url, layer_name, layer_attribution):
    # Crear el mapa con herramientas de dibujo y exportación habilitadas
    m = leafmap.Map(center=[20.0, 0.0], zoom=2, draw_export=True)

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
    
    return m

# Título y descripción en la página
st.title("Mapa Interactivo con Herramientas de Dibujo y Selección de Capas")
st.markdown("""
Esta herramienta te permite interactuar con un mapa en blanco, 
dibujar formas (líneas, polígonos, marcadores, círculos, etc.), 
y visualizar los datos en formato GeoJSON. 
Puedes seleccionar capas base mediante un buscador.
""")

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

    # Crear el mapa con la capa seleccionada
    m = create_map(selected_layer_url, selected_layer_name, selected_layer_attribution)

    # Verificar que el mapa se haya creado correctamente antes de renderizarlo
    if m:
        map_html = m.to_html()
        html(map_html, height=600)
else:
    st.warning("No se pudieron cargar las capas desde el archivo JSON.")

# Instrucciones para exportar
st.info("Use las herramientas de dibujo para crear formas en el mapa. Luego, haga clic en el botón de descarga en la esquina superior derecha del mapa para exportar los datos en formato GeoJSON.")
