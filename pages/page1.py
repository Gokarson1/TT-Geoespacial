import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk

# Contenido de la página 1
st.title("Página de Visualización de Datos")
st.write("Sube un archivo de datos geoespaciales para visualizar.")

# Cargar archivo
# Cargar y mostrar datos geoespaciales
uploaded_file = st.file_uploader("Cargar archivo de datos geoespaciales", type=["geojson", "shp"])

if uploaded_file:
    # Leer el archivo subido con geopandas (por ejemplo, un GeoJSON o un SHP)
    gdf = gpd.read_file(uploaded_file)
    
    # Configuración del mapa con pydeck
    layer = pdk.Layer(
        "GeoJsonLayer",
        data=gdf.__geo_interface__,  # Convertir a un formato que pydeck entienda
        get_fill_color=[0, 0, 255, 100],
        pickable=True,
    )

    # Renderizar el mapa
    view_state = pdk.ViewState(latitude=gdf.geometry.centroid.y.mean(),
                               longitude=gdf.geometry.centroid.x.mean(),
                               zoom=10)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    # Mostrar datos en tabla
    st.write("Datos:", gdf.head())