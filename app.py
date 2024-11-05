import streamlit as st

# Configuración de la aplicación
st.set_page_config(page_title="App de Visualización Geoespacial", page_icon="🌍")
st.image("img/logo2.png", width=500)
st.title("Bienvenido a la App de Visualización Geoespacial")

# Menú de navegación
st.write("Selecciona una opción en el menú para navegar:")
pages = ["Home", "Page 1", "Page 2"]  # Nombres de las páginas
selection = st.selectbox("Navegar a:", pages)

# Mostrar la página seleccionada
if selection == "Home":
    st.write("Esta es la página principal. Aquí puedes incluir información de introducción.")
elif selection == "Page 1":
    import pages.page1  # Importa la primera página
elif selection == "Page 2":
    import pages.page2  # Importa la segunda página
