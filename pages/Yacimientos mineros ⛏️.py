import streamlit as st
import pydeck as pdk
import json
from PIL import Image

# Open the logo image
img = Image.open("img/logo.png")

# Configuración de la página
st.set_page_config(
    page_title="Mapa de Yacimientos Mineros en Chile",
    layout="wide",
    page_icon=img
)

st.title("Visualización de Yacimientos Mineros en Chile")
st.write("""Esta página permite explorar los **yacimientos mineros de Chile** a través de un mapa interactivo.
         Este visualizador interactivo tiene como objetivo proporcionar una forma sencilla de visualizar la distribución de los yacimientos mineros en Chile. 
         Puede ser útil para análisis geoespaciales, investigaciones sobre la minería en Chile y toma de decisiones basadas en datos geográficos.
         """)


try:
        with open('data/Yacimientos Mineros.geojson', 'r', encoding='utf-8-sig') as file:
            geojson_data = json.load(file)

        # Definir la capa GeoJsonLayer con tamaño predeterminado
        geojson_layer = pdk.Layer(
            "GeoJsonLayer",
            geojson_data,
            pickable=True,
            stroked=True,
            filled=True,
            get_radius=500,  # Tamaño fijo de los puntos
            point_radius_min_pixels=5,  # Tamaño mínimo visible en pantalla
            get_fill_color="[255, 140, 0, 180]",  # Naranja con transparencia
            get_line_color="[255, 0, 0, 200]",  # Rojo
        )

        # Configurar el mapa centrado en Chile
        view_state = pdk.ViewState(
            latitude=-35.6751,  # Latitud de Chile
            longitude=-71.543,  # Longitud de Chile
            zoom=5,             # Zoom inicial
            pitch=0,            # Ángulo de vista
        )

        # Crear la visualización con pydeck
        r = pdk.Deck(
            layers=[geojson_layer],
            initial_view_state=view_state,
            tooltip={"text": "{nombre}"},  # Mostrar información en el tooltip
        )

        # Mostrar el mapa
        st.pydeck_chart(r)

except Exception as e:
    st.error(f"Hubo un problema al procesar el archivo GeoJSON: {e}")

