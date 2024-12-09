import streamlit as st
import pandas as pd
import folium
from PIL import Image
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Configuración de la página
img = Image.open("img/logo.png")
st.set_page_config(layout="wide", page_icon=img)

# Título de la aplicación
st.title("Población en el Mundo")

# Cargar archivo CSV
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        if 'latitude' in data.columns and 'longitude' in data.columns and 'pop_max' in data.columns:
            # Crear el mapa de calor
            m = folium.Map(location=[40, -100], zoom_start=4, tiles="OpenStreetMap")

            # Añadir el mapa de calor
            heat_data = [[row['latitude'], row['longitude'], row['pop_max']] for index, row in data.iterrows()]
            HeatMap(heat_data, radius=15).add_to(m)

            # Añadir control de capas
            folium.LayerControl().add_to(m)

            # Añadir un marcador con un popup
            folium.Marker([40, -100], popup="Marcador inicial").add_to(m)

            # Mostrar el mapa en Streamlit
            st_folium(m, width=600, height=500)

            # Análisis descriptivo
            st.header("Análisis Descriptivo")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Estadísticas Descriptivas")
                st.write(data['pop_max'].describe())

            with col2:
                st.subheader("Distribución por Región")
                if 'region' in data.columns:
                    st.bar_chart(data['region'].value_counts())
                else:
                    st.write("La columna 'region' no está presente en el archivo CSV.")

            st.subheader("Top 10 Ciudades Más Pobladas")
            st.table(data.nlargest(10, 'pop_max')[['name', 'pop_max']])

            # Visualización adicional
            st.header("Visualización Adicional")
            st.map(data[['latitude', 'longitude']])
        else:
            st.error("El archivo CSV debe contener las columnas 'latitude', 'longitude', y 'pop_max'.")
    except Exception as e:
        st.error(f"Error al leer el archivo CSV: {e}")
else:
    st.info("Por favor, carga un archivo CSV para comenzar.")