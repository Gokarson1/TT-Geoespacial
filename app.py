import folium
import streamlit as st
from PIL import Image
from streamlit_folium import st_folium

# Open the logo image
img = Image.open("img/logo.png")

# Set page configuration with icon
st.set_page_config(page_title="App de Visualización Geoespacial", page_icon=img)

# Create sidebar
st.sidebar.image(img, width=150)  # Display image in the sidebar

img= Image.open("img/logo.png")

st.image("img/logo2.png", width=500)
st.title("Bienvenido a la App de Visualización Geoespacial")


# Menú de navegación
st.write("Selecciona una opción en el menú para navegar:")
pages = ["Home", "wea 1", "wea 2"]  # Nombres de las páginas
selection = st.selectbox("Navegar a:", pages)

#crea el mapa
m = folium.Map(location=[-33.466, -70.597], zoom_start=10)

# Mostrar el mapa
st_folium(m, width=1000, height=500)

# Mostrar la página seleccionada
if selection == "Home":
    st.write("Esta es la página principal. Aquí puedes incluir información de introducción.")
elif selection == "Page 1":
    import pages.page1  # Importa la primera página
elif selection == "Page 2":
    import pages.page2  # Importa la segunda página
elif selection == "Page 3":
    import pages.page3
