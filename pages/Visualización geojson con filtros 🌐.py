import streamlit as st
import pydeck as pdk
import json
import pandas as pd
from PIL import Image

# Abrir la imagen del logo
img = Image.open("img/GeoHub1.jpeg")

# Configuración de la página
st.set_page_config(
    page_title="Geojson con busqueda por campos",
    layout="wide",
    page_icon=img
)

st.title("**Visualización de geojson con posibilidad de filtrar**")
st.write("""Esta página permite desplegar gejsjon a través de un mapa interactivo permitiendo busquedas en Python. También puedes cargar tu propio archivo GeoJSON para realizar búsquedas y visualizaciones personalizadas.""")

# Instrucciones
with st.expander("Manual de Uso"):
    st.write("""
    ### Visualización base:
    - Muestra los yacimientos mineros en Chile por defecto.
    - Puedes realizar búsquedas avanzadas con múltiples condiciones.

    ### Filtros avanzados:
    - **Formato básico**: `filter campo='valor'`
    - **Múltiples valores (OR)**: `filter comuna='Puente Alto' || 'La Florida'`
    - **Todos los registros**: `filter all`
    """)

import unicodedata #Facilitar la busqueda

# Función para normalizar texto (quitar tildes y convertir a minúsculas)
def normalize_text(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()
    return text  # Devuelve el texto tal cual si no es un string

# Función para procesar el GeoJSON
def process_geojson(geojson_data, query):
    try:
        # Cargar datos como DataFrame
        df = pd.json_normalize(geojson_data['features'])
        df = df.rename(columns=lambda x: x.replace('properties.', ''))  # Simplificar nombres de columnas

        # Normalizar todas las columnas para búsqueda insensible
        df = df.applymap(normalize_text)

        # Filtrado basado en la consulta
        if query.startswith("filter"):
            if query.strip() == "filter all":
                return geojson_data  # Mostrar todos los datos
            else:
                # Extraer el campo y valores del filtro
                field_values = query.replace("filter", "").strip()
                field, values = field_values.split("=")
                field = normalize_text(field.strip())  # Normalizar el nombre del campo
                values = [normalize_text(v.strip().strip("'\"")) for v in values.split("||")]

                # Verificar si el campo existe
                if field in df.columns:
                    filtered_df = df[df[field].isin(values)]
                    return {
                        "type": "FeatureCollection",
                        "features": [geojson_data['features'][i] for i in filtered_df.index],
                    }
                else:
                    st.error(f"El campo '{field}' no existe en los datos.")
                    return None
        else:
            st.write("Escribe una consulta válida que comience con `filter`.")
            return None
    except Exception as e:
        st.error(f"Error al procesar la consulta: {e}")
        return None

# Cargar archivo GeoJSON por defecto
try:
    with open('data/RM Limite urbano.geojson', 'r', encoding='utf-8-sig') as file:
        base_geojson = json.load(file)
except Exception as e:
    st.error(f"Hubo un problema al cargar la base de datos de Yacimientos Mineros: {e}")
    base_geojson = None

# Selector para elegir la fuente de datos
st.subheader("Seleccionar la fuente de datos")
data_source = st.radio(
    "Elige la fuente de datos:",
    ("Limite urbano de región Metropolitana", "Cargar archivo GeoJSON personalizado")
)

# Inicializar GeoJSON
geojson_data = None

if data_source == "Limite urbano de región Metropolitana" and base_geojson:
    geojson_data = base_geojson
elif data_source == "Cargar archivo GeoJSON personalizado":
    uploaded_file = st.file_uploader("Sube tu archivo GeoJSON", type=["geojson"])
    if uploaded_file:
        try:
            geojson_data = json.load(uploaded_file)
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

# Aplicar filtros y mostrar el mapa
if geojson_data:
    query = st.text_area("Escribe una consulta para filtrar los datos", value="filter all")
    filtered_geojson = process_geojson(geojson_data, query)

    if filtered_geojson:
        # Crear la capa de mapa con los datos filtrados
        geojson_layer = pdk.Layer(
            "GeoJsonLayer",
            filtered_geojson,
            pickable=True,
            stroked=True,
            filled=True,
            get_radius=500,
            point_radius_min_pixels=3,
            get_fill_color="[255, 140, 0, 180]",
            get_line_color="[255, 0, 0, 200]",
        )

        # Configuración del mapa centrado en Chile
        view_state = pdk.ViewState(
            latitude=-33.45694,
            longitude=-70.64827,
            zoom=8,
            pitch=0,
        )

        # Crear el mapa con pydeck
        r = pdk.Deck(
            layers=[geojson_layer],
            initial_view_state=view_state,
            tooltip={"text": "{nombre}"},
        )

        # Mostrar el mapa
        st.pydeck_chart(r)
else:
    st.write("Selecciona una fuente de datos válida para continuar.")