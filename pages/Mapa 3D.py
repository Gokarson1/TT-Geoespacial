import streamlit as st
import pandas as pd
import pydeck as pdk

# Configuración de la página
st.set_page_config(page_title="Mapa 3D de Santiago", layout="wide")

# Título
st.title("Visualización de edificios 3D en Santiago")

# Subir archivo
uploaded_file = st.file_uploader("Carga el archivo de edificios (CSV)", type=["csv"])

if uploaded_file:
    # Cargar datos del archivo
    data = pd.read_csv(uploaded_file)

    # Verificar que las columnas necesarias estén presentes
    required_columns = {"latitude", "longitude", "height", "building_name"}
    if required_columns.issubset(data.columns):
        st.success("Archivo cargado correctamente. Generando visualización...")

        # Capa para edificios en 3D
        layer = pdk.Layer(
            "ColumnLayer",
            data=data,
            get_position="[longitude, latitude]",
            get_elevation="height",
            elevation_scale=1,
            radius=20,
            get_fill_color="[height, 140, 200]",
            pickable=True,  # Habilita clics en los elementos
        )

        # Estado inicial del mapa
        view_state = pdk.ViewState(
            latitude=data["latitude"].mean(),
            longitude=data["longitude"].mean(),
            zoom=14,
            pitch=50,
        )

        # Renderizar el mapa
        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"html": "<b>Edificio:</b> {building_name}<br><b>Altura:</b> {height} m"},
            )
        )

        # Interactividad adicional (uso de eventos JS)
        st.write(
            """
            <script>
                // Puedes agregar más interactividad con JavaScript aquí.
                // Por ejemplo, registrar clics o animaciones al mover el mapa.
                console.log('Mapa cargado en 3D con edificios interactivos.');
            </script>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("El archivo no contiene las columnas requeridas: latitude, longitude, height, building_name.")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
# Manual de uso CSV
    st.markdown("""
    ### Manual de uso
    - **Sube un archivo geojson para la carga de datos.**
    - Asegúrate de que el geojson sea válido.
    - Una vez cargado, el mapa desplegará visualización 3D, del geojson ingresado.
                
    :red[*Cabe recalcar que el mapa carga un archivo como demostración, la subida de archivos es opcional.*]
    """)
