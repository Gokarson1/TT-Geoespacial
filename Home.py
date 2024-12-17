import folium
import streamlit as st
from PIL import Image
from streamlit_folium import st_folium

# Open the logo image
img = Image.open("img/GeoHub1.jpeg")

# Set page configuration with icon
#img= Image.open("img/GeoHub1.jpeg")
st.set_page_config(
    page_title="GeoHub",
    layout="wide",
    page_icon=img
)

# Create sidebar

st.sidebar.title("About")
st.sidebar.info(
    """
    - Este es nuetro trabajo de titulo
    - V1.0.0
    """
)
st.sidebar.image(img, width=150)  # Display image in the sidebar
st.image("img/logo2.png", use_column_width=True)
st.title(":gray[_Bienvenido a GeoHub_]")
st.markdown("""
    La ***App de Visualización Geoespacial*** permite explorar y analizar datos geoespaciales de manera interactiva. 
    Ya sea para análisis de yacimientos mineros, monitoreo ambiental o cualquier otro uso, nuestra plataforma ofrece una herramienta potente para visualizar y trabajar con datos geográficos en tiempo real.
""")
st.info("Puedes navegar entre las herramientas en la barra lateral a tu izquierda.",icon="ℹ️")

st.header(":gray[Ejemplos de uso de GeoHub]", divider="blue")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Area limitrofe de la región Metropolitana**")
    st.image("img/home1.png",use_column_width=True)

with col2:
    st.markdown("**Población segun ciudades en Estados Unidos**")
    st.image("img/home2.png",use_column_width=True)

with col3:
    st.markdown("**Infraestructura institucional en Magallanes**")
    st.image("img/home3.png",use_column_width=True)

# Segunda fila con 3 columnas adicionales
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("**Análisis de yacimientos mineros en el norte**")
    st.image("img/home4.png",use_column_width=True)

with col5:
    st.markdown("**Aeropuertos en territorio nacional**")
    st.image("img/home5.png",use_column_width=True)

with col6:
    st.markdown("**Limites urbanos de la provincia Chacabuco**")
    st.image("img/home6.png", use_column_width=True)

#crea el mapa
#m = folium.Map(location=[-33.466, -70.597], zoom_start=10)

# Mostrar el mapa
#st_folium(m, width=1000, height=500)