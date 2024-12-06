import folium
import streamlit as st
from PIL import Image
from streamlit_folium import st_folium

# Open the logo image
img = Image.open("img/logo.png")

# Set page configuration with icon
img= Image.open("img/logo.png")
st.set_page_config(
    page_title="App de Visualización Geoespacial",
    layout="wide",
    page_icon=img
)

# Create sidebar

st.sidebar.title("About")
st.sidebar.info(
    """
    - Este es nuetro trabajo de titulo
    - V0.0.7
    """
)
st.sidebar.image(img, width=150)  # Display image in the sidebar
st.image("img/logo2.png", width=500)
st.title("Bienvenido a la App de Visualización Geoespacial")
st.markdown("""
    La **App de Visualización Geoespacial** permite explorar y analizar datos geoespaciales de manera interactiva. 
    Ya sea para análisis de yacimientos mineros, monitoreo ambiental o cualquier otro uso, nuestra plataforma ofrece una herramienta potente para visualizar y trabajar con datos geográficos en tiempo real.
""")
st.info("Puedes navegar entre las herramientas en la barra lateral a tu izquierda.")
#crea el mapa
m = folium.Map(location=[-33.466, -70.597], zoom_start=10)

# Mostrar el mapa
st_folium(m, width=1000, height=500)

