import streamlit as st
import pandas as pd
import pydeck as pdk
import json

# Configuración de la página
st.set_page_config(page_title="Mapa 3D de Santiago", layout="wide")

# Título
st.title("Visualización de edificios 3D en Santiago")

# Subir archivo
uploaded_file = st.file_uploader("Carga el archivo de edificios (GeoJSON)", type=["geojson"])

if uploaded_file:
    # Cargar datos del archivo GeoJSON
    data = json.load(uploaded_file)

    # Convertir GeoJSON a DataFrame
    features = data["features"]
    df = pd.json_normalize(features)

    # Verificar que las columnas necesarias estén presentes
    required_columns = {"geometry.coordinates", "properties.height_m", "properties.name"}
    if required_columns.issubset(df.columns):
        st.success("Archivo cargado correctamente. Generando visualización...")

        # Renombrar columnas para consistencia
        df.rename(columns={
            "geometry.coordinates": "coordinates",
            "properties.height_m": "height",
            "properties.name": "building_name"
        }, inplace=True)

        # Separar coordenadas en latitud y longitud
        df["longitude"] = df["coordinates"].apply(lambda x: x[0])
        df["latitude"] = df["coordinates"].apply(lambda x: x[1])

        # Capa para edificios en 3D
        layer = pdk.Layer(
            "ColumnLayer",
            data=df,
            get_position="[longitude, latitude]",
            get_elevation="height",
            elevation_scale=100,  # Aumentar la escala de elevación
            radius=100,  # Aumentar el radio de los puntos
            get_fill_color="[height, 140, 200]",
            pickable=True,  # Habilita clics en los elementos
        )

        # Estado inicial del mapa
        view_state = pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
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
                // Función para mostrar información detallada del edificio al hacer clic
                function showBuildingInfo(info) {
                    alert('Edificio: ' + info.object.building_name + '\\nAltura: ' + info.object.height + ' m');
                }

                // Añadir evento de clic a los edificios
                document.querySelectorAll('.deckgl-overlay').forEach(function(element) {
                    element.addEventListener('click', function(event) {
                        const info = deck.pickObject({x: event.clientX, y: event.clientY});
                        if (info) {
                            showBuildingInfo(info);
                        }
                    });
                });

                // Añadir animación al mover el mapa
                deck.setProps({
                    onViewStateChange: ({viewState}) => {
                        deck.setProps({viewState: {...viewState, transitionDuration: 500}});
                    }
                });

                console.log('Mapa cargado en 3D con edificios interactivos.');
            </script>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("El archivo no contiene las columnas requeridas: geometry.coordinates, properties.height_m, properties.name.")
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
