import streamlit as st
import leafmap.foliumap as leafmap
import json
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Visualizador de GeoJSON",
    layout="wide",
)

# Título de la aplicación
st.title("Visualizador de GeoJSON")

# Cargar archivo GeoJSON
uploaded_geojson = st.file_uploader("Cargar archivo GeoJSON", type=["geojson"])

if uploaded_geojson is not None:
    try:
        # Leer el archivo GeoJSON
        geojson_data = json.load(uploaded_geojson)

        # Crear un mapa usando leafmap
        m = leafmap.Map(center=[-33.45, -70.65], zoom=10)  # Coordenadas centradas en Santiago, Chile

        # Añadir el archivo GeoJSON al mapa
        m.add_geojson(geojson_data)

        # Mostrar el mapa en Streamlit
        m.to_streamlit(height=700)

        # Extraer las propiedades de las características del GeoJSON
        features = geojson_data['features']
        properties = [feature['properties'] for feature in features]

        # Convertir las propiedades en un DataFrame de pandas
        df = pd.DataFrame(properties)

        # Mostrar el DataFrame en Streamlit
        st.subheader("Datos del GeoJSON")
        st.write(df)

        # Análisis descriptivo
        st.header("Análisis Descriptivo")

        if not df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Estadísticas Descriptivas")
                st.write(df.describe())

            with col2:
                st.subheader("Distribución de Categorías")
                for column in df.select_dtypes(include=['object']).columns:
                    st.write(f"Distribución de {column}")
                    st.bar_chart(df[column].value_counts())

            st.subheader("Primeras 10 Filas del DataFrame")
            st.write(df.head(10))
        else:
            st.write("No hay datos disponibles para análisis.")

    except Exception as e:
        st.error(f"Error al leer el archivo GeoJSON: {e}")
else:
    st.info("Por favor, sube un archivo GeoJSON para visualizarlo.")