import streamlit as st
import zipfile
import os
import geopandas as gpd
import pydeck as pdk

# Contenido de la página 2
st.title("Página de Carga de Archivos ZIP")
st.write("Sube un archivo ZIP con datos geoespaciales (SHP).")

# Cargar archivo ZIP
uploaded_file_zip = st.file_uploader("Cargar archivo ZIP", type=["zip"])

if uploaded_file_zip is not None:
    # Crear un directorio temporal para extraer el contenido del ZIP
    with zipfile.ZipFile(uploaded_file_zip, "r") as zip_ref:
        zip_ref.extractall("temp_shapefile")

    # Buscar el archivo .shp en el directorio temporal
    shapefile_path = None
    for root, dirs, files in os.walk("temp_shapefile"):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                break

    # Leer y mostrar el shapefile en un mapa
    if shapefile_path:
        # Cargar el archivo SHP con geopandas
        gdf = gpd.read_file(shapefile_path)
        
        # Reproyectar a CRS proyectado adecuado
        gdf = gdf.to_crs(epsg=3857)

        # Configuración del mapa con pydeck
        layer = pdk.Layer(
            "GeoJsonLayer",
            data=gdf.__geo_interface__,
            get_fill_color=[0, 0, 255, 100],
            pickable=True,
        )

        # Calcular el centro del mapa
        view_state = pdk.ViewState(
            latitude=gdf.geometry.centroid.y.mean(),
            longitude=gdf.geometry.centroid.x.mean(),
            zoom=10
        )
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

        # Mostrar una tabla con los datos, excluyendo la columna geometry
