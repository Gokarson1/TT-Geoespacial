import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import json  # Para manejar los datos GeoJSON

# Cargar el logo
img = Image.open("img/logo.png")

# Configuración de la página
st.set_page_config(page_title="Mapa de Yacimientos Mineros en Chile", page_icon=img)
st.title("Visualización de Yacimientos Mineros en Chile")
st.write("Sube un archivo GeoJSON para visualizar los yacimientos en el mapa interactivo:")

# Campo para subir archivo GeoJSON
uploaded_file = st.file_uploader("Selecciona tu archivo GeoJSON", type="geojson")

# Procesar el archivo GeoJSON y mostrar el mapa
if uploaded_file:
    try:
        # Leer y cargar el contenido del archivo GeoJSON
        geojson_data = json.load(uploaded_file)

        # Crear el mapa base centrado en Chile
        chile_map = folium.Map(location=[-35.6751, -71.543], zoom_start=5)

        # Añadir los datos GeoJSON al mapa
        folium.GeoJson(
            geojson_data,
            name="Yacimientos Mineros",
            style_function=lambda x: {
                "fillColor": "orange",
                "color": "red",
                "weight": 2,
                "fillOpacity": 0.5,
            },
        ).add_to(chile_map)

        # Mostrar el mapa interactivo
        st.write("Mapa interactivo de los yacimientos mineros:")
        st_folium(chile_map, width=700, height=500)

    except Exception as e:
        st.error(f"Hubo un problema al procesar el archivo GeoJSON: {e}")
else:
    st.info("Por favor, sube un archivo GeoJSON para comenzar.")
