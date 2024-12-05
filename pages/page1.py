import streamlit as st
import geopandas as gpd
import pandas as pd
import json
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Visualización de Datos Geoespaciales")

# Sidebar para navegación
st.sidebar.header("Navegación")
page = st.sidebar.radio("Selecciona la página", ["Shapefile", "CSV"])

# Selección de mapa base
st.sidebar.header("Seleccione el mapa base")
map_base = st.sidebar.selectbox(
    "Mapa base", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"]
)

# Generador de código HTML + JavaScript para Leaflet
def render_map_js(map_base, geojson_data=None, markers=None):
    tiles_dict = {
        "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "Stamen Terrain": "https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg",
        "Stamen Toner": "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
        "Stamen Watercolor": "https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg"
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

    # Código JavaScript para renderizar el mapa
    map_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <style>
            #map {{
                height: 500px;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        <script>
            var map = L.map('map').setView([0, 0], 2);
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

# Mostrar las páginas
if page == "Shapefile":
    st.header("Sube un archivo ShapeFile para visualizar.")
    shapefile_upload = st.file_uploader("Subir archivo Shapefile (.zip)", type=["zip"])
    geojson_data = None

    if shapefile_upload:
        with open("temp.zip", "wb") as f:
            f.write(shapefile_upload.getbuffer())
        
        # Procesar Shapefile y convertir a GeoJSON
        try:
            gdf = gpd.read_file("temp.zip")
            if not gdf.is_valid.all():
                gdf = gdf.buffer(0)  # Intentar reparar geometrías
            geojson_data = json.loads(gdf.to_json())
            #st.json(geojson_data)

            st.success("Shapefile cargado correctamente.")
        except Exception as e:
            st.error(f"Error al procesar el archivo Shapefile: {e}")

    components.html(render_map_js(map_base, geojson_data=geojson_data), height=550)

elif page == "CSV":
    st.header("Sube un archivo CSV con coordenadas para visualizar.")
    csv_upload = st.file_uploader("Subir archivo CSV", type=["csv"])
    markers = []

    if csv_upload:
        try:
            # Leer CSV con delimitador ';'
            df = pd.read_csv(csv_upload, delimiter=';')
            if "lat" in df.columns and "lon" in df.columns:
                # Generar lista de marcadores
                for _, row in df.iterrows():
                    popup = row["nombre_nodo"] if "nombre_nodo" in df.columns else "Sin nombre"
                    markers.append((row["lat"], row["lon"], popup))
                st.success("CSV cargado correctamente.")
            else:
                st.error("El archivo CSV debe contener columnas 'lat' y 'lon'.")
        except Exception as e:
            st.error(f"No se pudo procesar el archivo CSV: {e}")

    components.html(render_map_js(map_base, markers=markers), height=550)
