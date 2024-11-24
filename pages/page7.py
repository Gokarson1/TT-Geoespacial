import streamlit as st
import folium
from streamlit_folium import st_folium
import geojson
from shapely.geometry import shape
import json
from io import BytesIO
from PIL import Image

img= Image.open("img/logo.png")

st.set_page_config(page_title="Analisis geoespacial a aarchivos geojson", layout="wide")
# Configuración básica de Streamlit
st.title("Analisis Geoespacial")
st.write(":V")


# Subida del archivo
uploaded_file = st.file_uploader("Cargar archivo GeoJSON", type=["geojson"])

if uploaded_file:
    try:
        # Leer y cargar el archivo GeoJSON
        geojson_data = geojson.load(uploaded_file)
        st.success("Archivo GeoJSON cargado correctamente.")
        
        # Mostrar breve resumen del archivo
        features = geojson_data.get("features", [])
        st.write(f"Total de características en el archivo: {len(features)}")
        st.json(features[0], expanded=False)  # Mostrar el primer feature como ejemplo

        # --- SECCIÓN 2: Visualización del archivo ---
        st.header("2. Visualización en Mapa")
        mapa = folium.Map(location=[0, 0], zoom_start=2)  # Mapa base
        folium.GeoJson(geojson_data, name="GeoJSON Data").add_to(mapa)
        st_folium(mapa, width=800, height=600)

        # --- SECCIÓN 3: Análisis Geoespacial ---
        st.header("3. Análisis Geoespacial")
        puntos = []
        areas = []

        # Analizar las geometrías del archivo
        for feature in features:
            geom = feature["geometry"]
            if geom["type"] == "Point":
                puntos.append(geom["coordinates"])
            elif geom["type"] == "Polygon":
                poly = shape(geom)
                areas.append(poly.area)

        # Mostrar resultados del análisis
        st.subheader("Puntos Encontrados")
        st.write(f"Cantidad de puntos: {len(puntos)}")
        if puntos:
            st.write("Primeros puntos:", puntos[:5])

        st.subheader("Áreas de Polígonos")
        st.write(f"Cantidad de polígonos: {len(areas)}")
        if areas:
            st.write("Primeras áreas calculadas:", areas[:5])

        # --- SECCIÓN 4: Exportar resultados ---
        st.header("4. Exportar Resultados")
        if puntos:
            new_geojson = {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": coord},
                        "properties": {}
                    }
                    for coord in puntos
                ]
            }

            # Convertir a BytesIO para descarga
            new_file = BytesIO(json.dumps(new_geojson).encode("utf-8"))
            st.download_button("Descargar GeoJSON procesado", new_file, "nuevo_geojson.geojson", "application/json")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("Por favor, carga un archivo GeoJSON para empezar.")