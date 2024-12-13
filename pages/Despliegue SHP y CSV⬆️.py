import streamlit as st
import geopandas as gpd
import pandas as pd
import json
import streamlit.components.v1 as components
from PIL import Image

img = Image.open("img/GeoHub1.jpeg")
# Configuración de la página
st.set_page_config(page_title=
     "Visualización de Datos Geoespaciales" ,
     layout="wide",
     page_icon=img
    )

# Sidebar para navegación
st.sidebar.header("Navegación")
page = st.sidebar.radio("Selecciona la página", ["Shapefile", "CSV"])

# Selección de mapa base
st.sidebar.header("Seleccione el mapa base")
map_base = st.sidebar.selectbox(
    "Seleccione el mapa base",
    ["OpenStreetMap", "OpenTopoMap", "Esri World Imagery"]
)
# Generador de código HTML + JavaScript para Leaflet
def render_map_js(map_base, geojson_data=None, markers=None):
    tiles_dict = {
        "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",  # Nueva capa
        "Esri World Imagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"  # Nueva capa
    }
    tile_url = tiles_dict[map_base]

    geojson_script = f"""
    var geojsonData = {json.dumps(geojson_data)};
    try {{
        var geojson = L.geoJSON(geojsonData).addTo(map);
        map.fitBounds(geojson.getBounds());  // Ajustar el mapa a los datos
    }} catch (error) {{
        console.error("Error al renderizar el GeoJSON:", error);
    }}
    """ if geojson_data else ""

    marker_script = ""
    if markers:
        for marker in markers:
            lat, lon, popup = marker
            marker_script += f"""
                L.marker([{lat}, {lon}]).addTo(map).bindPopup("{popup}");
            """

    # JavaScript para incluir plugins y funcionalidad de maximización
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
                fullscreenControl: true
            }}).setView([0, 0], 2);

            L.tileLayer('{tile_url}', {{
                maxZoom: 18,
            }}).addTo(map);

            {geojson_script}
            {marker_script}
        </script>
    </body>
    </html>
    """
    return map_code

def load_test_data(filepath):
    try:
        if filepath.endswith(".zip"):
            gdf = gpd.read_file(filepath)
            if not gdf.is_valid.all():
                gdf = gdf.buffer(0)  # Attempt to repair geometries
            geojson_data = json.loads(gdf.to_json())
            return geojson_data
        elif filepath.endswith(".csv"):
            df = pd.read_csv(filepath, delimiter=";")
            if "lat" in df.columns and "lon" in df.columns:
                markers = [
                    (row["lat"], row["lon"], row["Nombre"] if "Nombre" in df.columns else "Sin nombre")
                    for _, row in df.iterrows()
                ]
                return markers
            else:
                st.error("CSV de demostracion debe contener 'lat' y 'lon'.")
                return None
        else:
            st.error(f"Tipo de archivo incorrecto: {filepath}")
            return None
    except Exception as e:
        st.error(f"Error cargando la informacion de prueba: {e}")
        return None

# Path de las cargas iniciales
test_shapefile_path = 'data/prms-region-metropolitana-area_shapefile.zip'
test_csv_path = "data/Mineras en sudamerica.csv"

# Informacion inicial segun pagina
if page == "Shapefile":
    st.header("Sube un archivo ShapeFile para visualizar.")
    with st.expander("Manual de Uso: subida ShapeFile"):
        st.write("""
        ### Manual de uso
        - **Sube un archivo Shapefile comprimido en formato ZIP.**
        - El archivo debe incluir todos los componentes necesarios: `.shp`, `.shx`, `.dbf`, etc.
        - Una vez cargado, el mapa se actualizará automáticamente para mostrar la geometría.
        - Puedes usar las herramientas de maximización del mapa para ver detalles más específicos.
                    
        :red[*Cabe recalcar que el mapa carga un archivo como demostración, la subida de archivos es opcional.*]
        """)  

    # Load test data (optional)
    test_geojson_data = load_test_data(test_shapefile_path)
    shapefile_upload = st.file_uploader("Subir archivo Shapefile (opcional)", type=["zip"])

    geojson_data = test_geojson_data  # Default test data

    if shapefile_upload:
        with open("temp.zip", "wb") as f:
            f.write(shapefile_upload.getbuffer())

        try:
            gdf = gpd.read_file("temp.zip")
            if not gdf.is_valid.all():
                gdf = gdf.buffer(0)  # arreglo de 'geometries'
            geojson_data = json.loads(gdf.to_json())
            st.success("Shapefile cargado correctamente.")
        except Exception as e:
            st.error(f"Error al procesar el archivo Shapefile: {e}")

    components.html(render_map_js(map_base, geojson_data=geojson_data), height=550)

elif page == "CSV":
    st.header("Sube un archivo CSV con coordenadas para visualizar.")
    with st.expander("Manual de Uso: subida de CSV"):
        st.write("""
        ### Manual de uso
        - **Sube un archivo CSV con coordenadas.**
        - Asegúrate de que el archivo tenga las columnas `lat` (latitud) y `lon` (longitud).
        - Opcionalmente, puedes agregar una columna `Nombre` para personalizar las etiquetas de los marcadores.
        - Una vez cargado, el mapa mostrará los puntos correspondientes.
                    
        :red[*Cabe recalcar que el mapa carga un archivo como demostración, la subida de archivos es opcional.*]
        """)  

    test_markers = load_test_data(test_csv_path)
    csv_upload = st.file_uploader("Subir archivo CSV (opcional)", type=["csv"])

    markers = test_markers

    if csv_upload:
        try:
            df = pd.read_csv(csv_upload, delimiter=";")
            if "lat" in df.columns and "lon" in df.columns:
                markers = [
                    (row["lat"], row["lon"], row["Nombre"] if "Nombre" in df.columns else "Sin nombre")
                    for _, row in df.iterrows()
                ]
                st.success("CSV cargado correctamente.")
            else:
                st.error("El archivo CSV debe contener columnas 'lat' y 'lon'.")
        except Exception as e:
            st.error(f"No se pudo procesar el archivo CSV: {e}")

    components.html(render_map_js(map_base, markers=markers), height=550)