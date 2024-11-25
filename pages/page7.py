import streamlit as st
import geopandas as gpd
import tempfile
import os
import zipfile
from PIL import Image
import folium
from streamlit_folium import st_folium


def procesar_archivo(archivo):
    """
    Procesa el archivo GeoJSON o Shapefile cargado.
    """
    try:
        geojson_path = None
        shapefile_dir = None

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Procesar archivo .zip o .geojson
            if archivo.name.endswith(".zip"):
                zip_path = os.path.join(tmp_dir, archivo.name)
                with open(zip_path, "wb") as f:
                    f.write(archivo.getbuffer())

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(tmp_dir)

                for root, _, files in os.walk(tmp_dir):
                    for file in files:
                        if file.endswith(".geojson"):
                            geojson_path = os.path.join(root, file)
                            break
                        elif file.endswith(".shp"):
                            shapefile_dir = root
                            break

            elif archivo.name.endswith(".geojson"):
                geojson_path = os.path.join(tmp_dir, archivo.name)
                with open(geojson_path, "wb") as f:
                    f.write(archivo.getbuffer())

            elif archivo.name.endswith(".shp"):
                shapefile_dir = tmp_dir
                with open(os.path.join(shapefile_dir, archivo.name), "wb") as f:
                    f.write(archivo.getbuffer())

            # Leer datos del archivo
            if geojson_path:
                data = gpd.read_file(geojson_path)
            elif shapefile_dir:
                data = gpd.read_file(shapefile_dir)
            else:
                st.error("No se pudo identificar un archivo compatible.")
                return None

        return data

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return None


def validar_y_corregir_geometria(data):
    """
    Valida y corrige el CRS y las geometrías del archivo cargado.
    """
    # Validar CRS
    if data.crs is not None:
        if data.crs.to_string() != "EPSG:4326":
            data = data.to_crs(epsg=4326)
    else:
        st.warning("El CRS del archivo no está definido. Esto puede causar problemas en el mapa.")

    # Corregir geometrías inválidas
    if not data.is_valid.all():
        st.warning("Algunas geometrías son inválidas. Intentando corregir...")
        data = data.buffer(0)

    # Filtrar geometrías con valores fuera de rango
    data = data[data.geometry.bounds.minx >= -180]
    data = data[data.geometry.bounds.maxx <= 180]
    data = data[data.geometry.bounds.miny >= -90]
    data = data[data.geometry.bounds.maxy <= 90]

    return data


def crear_mapa(data):
    """
    Crea y muestra un mapa interactivo con los datos procesados.
    """
    st.subheader("Visualización en el Mapa")
    centro = [data.geometry.centroid.y.mean(), data.geometry.centroid.x.mean()]
    mapa = folium.Map(location=centro, zoom_start=10, tiles="OpenStreetMap")
    folium.GeoJson(data).add_to(mapa)
    st_folium(mapa, width=700, height=500)


# Configuración de la página
img = Image.open("img/logo.png")
st.set_page_config(page_title="Análisis geoespacial de archivos", page_icon=img)
st.title("Análisis Geoespacial")

# Subir archivo
st.sidebar.header("Cargar Archivo")
archivo = st.sidebar.file_uploader("Sube un archivo GeoJSON, ZIP o SHP", type=["geojson", "zip", "shp"])

if archivo:
    data = procesar_archivo(archivo)
    if data is not None:
        data = validar_y_corregir_geometria(data)
        crear_mapa(data)
else:
    st.warning("Por favor, sube un archivo para comenzar.")
