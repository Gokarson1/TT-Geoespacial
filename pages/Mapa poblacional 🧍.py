import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
from PIL import Image

img= Image.open("img/logo.png")

st.set_page_config(layout="wide", page_icon=img)

st.title("Poblacion en el Mundo")

uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])


if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    if 'latitude' in data.columns and 'longitude' in data.columns and 'pop_max' in data.columns:
        # Crear el mapa de calor
        m = leafmap.Map(center=[40, -100], zoom=4)
        m.add_heatmap(
            data,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=40,
        )
        m.to_streamlit(height=700)
        
        # Análisis descriptivo
        st.header("Análisis Descriptivo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Estadísticas Descriptivas")
            st.write(data['pop_max'].describe())
        
        with col2:
            st.subheader("Distribución por Región")
            st.bar_chart(data['region'].value_counts())
        
        st.subheader("Top 10 Ciudades Más Pobladas")
        st.table(data.nlargest(10, 'pop_max')[['name', 'pop_max']])
        
        # Visualización adicional
        st.header("Visualización Adicional")
        st.map(data[['latitude', 'longitude']])
    else:
        st.write("El archivo CSV debe contener las columnas 'latitude', 'longitude', y 'pop_max'.")