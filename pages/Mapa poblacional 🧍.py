import streamlit as st
import pandas as pd
import folium
from PIL import Image
from streamlit_folium import st_folium
from folium.plugins import HeatMap, Fullscreen

# Configuración de la página
img = Image.open("img/logo.png")
st.set_page_config(layout="wide", page_icon=img)

# Título de la aplicación
st.title("Población en el Mundo")

# Path del archivo CSV de demostración
test_csv_path = "data/us_cities.csv"

# Cargar archivo CSV
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

# Verificar si se subió un archivo o usar el archivo de demostración
if uploaded_file is not None:
    file_to_read = uploaded_file
    st.success("Archivo cargado desde la subida.")
else:
    file_to_read = test_csv_path
    st.info("Usando archivo de demostración.")

try:
    # Leer los datos del archivo CSV
    data = pd.read_csv(file_to_read)

    if 'latitude' in data.columns and 'longitude' in data.columns and 'pop_max' in data.columns:
        # Crear el mapa de calor
        m = folium.Map(location=[40, -100], zoom_start=4, tiles="OpenStreetMap")

        # Añadir el mapa de calor
        heat_data = [[row['latitude'], row['longitude'], row['pop_max']] for index, row in data.iterrows()]
        HeatMap(heat_data, radius=15).add_to(m)

        # **Añadir el botón de pantalla completa debajo de los controles de zoom**
        Fullscreen().add_to(m)

        # Añadir control de capas
        folium.LayerControl().add_to(m)

        # Añadir un marcador con un popup
        folium.Marker([40, -100], popup="Marcador inicial").add_to(m)

        # Mostrar el mapa en Streamlit
        st_folium(m, width=1000, height=500)

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

# Manual de uso CSV
st.markdown("""
### Manual de uso
- **Sube un archivo CSV con la información poblacional.**
- Los campos esperados son: `name,sov_a3,latitude,longitude,pop_max,region`
- Opcionalmente, puedes encontrar varios archivos en la web para adaptarlos a este formato.
- Una vez cargado, se desplegará el mapa de calor, y en la parte inferior datos estadísticos del despliegue.
            
:red[*Cabe recalcar que el mapa carga un archivo como demostración, la subida de archivos es opcional.*]
""")
