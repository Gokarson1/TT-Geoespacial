import zipfile
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap
import os

# Subir el archivo .zip
uploaded_file = st.file_uploader("Sube un archivo .zip", type="zip")

if uploaded_file is not None:
    # Descomprimir el archivo .zip
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("temp_dir")

    # Buscar el archivo .shp dentro del directorio descomprimido
    shapefile_path = None
    for root, dirs, files in os.walk("temp_dir"):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                break

    if shapefile_path is not None:
        # Leer el archivo .shp usando geopandas
        gdf = gpd.read_file(shapefile_path)

        # Extraer las coordenadas en formato adecuado
        gdf['lon'] = gdf.geometry.x
        gdf['lat'] = gdf.geometry.y

        # Mostrar el DataFrame completo en Streamlit
        st.write(gdf)

        # Crear un mapa usando leafmap
        m = leafmap.Map(center=[gdf['lat'].mean(), gdf['lon'].mean()], zoom=10)

        # Añadir los datos al mapa
        m.add_gdf(gdf, layer_name="Datos")

        # Mostrar el mapa en Streamlit
        m.to_streamlit(height=700)
    else:
        st.error("No se encontró ningún archivo .shp en el archivo .zip.")