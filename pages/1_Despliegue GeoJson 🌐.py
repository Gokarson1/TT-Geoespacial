import streamlit as st
import json
import streamlit.components.v1 as components
from PIL import Image

# Configuración de la página dasdasddas
img = Image.open("img/GeoHub1.jpeg")
st.set_page_config(
    page_title="Visualización de Archivos GeoJSON",
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

# Generador de código HTML + JavaScript para Leaflet
# Actualización para permitir capas seleccionables
def render_map_js(geojson_data, selected_layer_url=None):
    tile_url = selected_layer_url if selected_layer_url else "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

    geojson_script = f"""
    var geojsonData = {json.dumps(geojson_data)};
    try {{
        var geojson = L.geoJSON(geojsonData).addTo(map);
        map.fitBounds(geojson.getBounds());
    }} catch (error) {{
        console.error("Error al renderizar el GeoJSON:", error);
    }}
    """ if geojson_data else ""

    map_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet-fullscreen/dist/leaflet.fullscreen.css" />
        <style>
            #map {{
                height: 800px;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet-fullscreen/dist/Leaflet.fullscreen.min.js"></script>
        <script>
            var map = L.map('map', {{
                fullscreenControl: true  // Habilita el control de pantalla completa
            }}).setView([0, 0], 2);

            L.tileLayer('{tile_url}', {{
                maxZoom: 18,
            }}).addTo(map);

            {geojson_script}
        </script>
    </body>
    </html>
    """
    return map_code

# Página principal
st.title("Visualización de Archivos GeoJSON")
with st.expander("Manual de Uso: Uso de geojson"):
    st.write("""
        ### Manual de uso
        - **Sube un archivo geojson con información de carga válida.**
        - Asegúrate de usar un archivo válido para el despliegue del json
        - Opcionalmente, si no posee un archivo geojson, puedes ir al apartado de mapa interactivo
                    
        :red[*Cabe recalcar que el mapa carga un archivo como demostración, la subida de archivos es opcional.*]
        """)
st.write("Sube un archivo GeoJSON para visualizar sus datos geoespaciales en el mapa.")

# Intentar cargar el archivo GeoJSON inicial (archivo de prueba)
test_gjson_path = "data/Test_Geojson.geojson"

try:
    with open(test_gjson_path, "r") as file:
        initial_geojson_data = json.load(file)
except Exception as e:
    initial_geojson_data = None
    st.warning(f"No se pudo cargar el archivo de prueba GeoJSON: {e}")

# Carga del archivo GeoJSON
geojson_upload = st.file_uploader("Sube tu archivo GeoJSON", type=["geojson", "json"])
geojson_data = initial_geojson_data  # Usar datos iniciales por defecto

if geojson_upload:
    try:
        geojson_data = json.load(geojson_upload)
        st.success("Archivo GeoJSON cargado correctamente.")
        if st.checkbox("Mostrar datos crudos del GeoJSON"):
            st.json(geojson_data)
    except Exception as e:
        st.error(f"Error al procesar el archivo GeoJSON: {e}")

# Cargar las capas desde el archivo JSON
layers = load_layers_from_json("data/layers.json")
selected_layer_url = None

if layers:
    layer_names = [layer["name"] for layer in layers]
    selected_layer_name = st.selectbox("Selecciona una capa base", layer_names)
    selected_layer = next(layer for layer in layers if layer["name"] == selected_layer_name)
    selected_layer_url = selected_layer.get("url", "")
    st.write(f"Capa seleccionada: {selected_layer_name}")

# Renderizar el mapa
if geojson_data:
    components.html(render_map_js(geojson_data, selected_layer_url), height=550)
else:
    st.info("Carga un archivo GeoJSON válido para visualizar el mapa.")
