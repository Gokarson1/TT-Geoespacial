import streamlit as st
import json
import streamlit.components.v1 as components
from PIL import Image

# Configuración de la página
img = Image.open("img/logo.png")
st.set_page_config(
    page_title="Visualización de Archivos GeoJSON",
    layout="wide",
    page_icon=img
)

# Sidebar para seleccionar mapa base
st.sidebar.header("Configuración del mapa")
map_base = st.sidebar.selectbox(
    "Seleccione el mapa base",
    ["OpenStreetMap", "OpenTopoMap", "Esri World Imagery"]
)

# Generador de código HTML + JavaScript para Leaflet
def render_map_js(map_base, geojson_data):
    tiles_dict = {
        "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        "Esri World Imagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    }
    tile_url = tiles_dict[map_base]

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
st.write("Sube un archivo GeoJSON para visualizar sus datos geoespaciales en el mapa.")

test_gjson_path = "data/Test_Geojson.geojson"

# Intentar cargar el archivo GeoJSON inicial (archivo de prueba)
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
        # Cargar los datos del archivo subido
        geojson_data = json.load(geojson_upload)
        st.success("Archivo GeoJSON cargado correctamente.")
        
        # Mostrar los datos crudos (opcional)
        if st.checkbox("Mostrar datos crudos del GeoJSON"):
            st.json(geojson_data)
    except Exception as e:
        st.error(f"Error al procesar el archivo GeoJSON: {e}")

# Renderizar el mapa
if geojson_data:
    components.html(render_map_js(map_base, geojson_data), height=550)
    # Manual de cargar GeoJson
    st.markdown("""
    ### Manual de uso
    - **Sube un archivo geojson con información de carga válida.**
    - Asegurate de usar un archivo valido para el despliegue del json
    - Opcionalmente, si no posee un archivo geojson, puedes ir al apartado de mapa interactivo
                
    :red[*Cabe recalcar que el mapa carga un archivo como demostración, la subida de archivos es opcional.*]
    """)
else:
    st.info("Carga un archivo GeoJSON válido para visualizar el mapa.")
