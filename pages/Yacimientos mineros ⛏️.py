import streamlit as st
import pydeck as pdk
import json
import pandas as pd
from PIL import Image
import unicodedata

# Abrir la imagen del logo
img = Image.open("img/GeoHub1.jpeg")

# Configuración de la página
st.set_page_config(
    page_title="Mapa de Yacimientos Mineros en Chile",
    layout="wide",
    page_icon=img
)

st.title("Visualización de Yacimientos Mineros en Chile")
st.write("""Esta página permite explorar los **yacimientos mineros de Chile** a través de un mapa interactivo. Este visualizador interactivo tiene como objetivo proporcionar una forma sencilla de visualizar la distribución de los yacimientos mineros en Chile. Puede ser útil para análisis geoespaciales, investigaciones sobre la minería en Chile y toma de decisiones basadas en datos geográficos.""")

# Instrucciones
with st.expander("Manual de Uso: Filtro de Yacimientos Mineros"):
    st.write("""
    Esta sección describe cómo interactuar con el sistema para consultar y visualizar yacimientos mineros en Chile.

    Ejemplos de consulta:
    - `filter campo='valor'`: Filtra por el campo y valor especificado. Por ejemplo, `filter grupo_recu='Cu'`.         
    - `filter all`: Muestra todos los yacimientos.
    - `filter region='Región de Atacama'`: Muestra todos los yacimientos de esa región.
    - `filter comuna='San José de Maipo'`: Muestra todos los yacimientos de esa región.

    Este sistema es insensible a mayúsculas, minúsculas y tildes.
    """)

# Función para normalizar texto (quitar tildes y convertir a minúsculas)
def normalize_text(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()
    return text

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
                # Extraer el campo y valor del filtro
                field, value = query.replace("filter", "").strip().split("=")
                field, value = normalize_text(field.strip()), normalize_text(value.strip().strip("'\""))

                # Verificar si el campo existe
                if field in df.columns:
                    # Filtrar el DataFrame
                    filtered_df = df[df[field] == value]

                    # Reconstruir el GeoJSON filtrado
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

# Cargar el archivo GeoJSON
try:
    with open('data/Yacimientos Mineros.geojson', 'r', encoding='utf-8-sig') as file:
        geojson_data = json.load(file)

    # Cargar datos como DataFrame
    df = pd.json_normalize(geojson_data['features'])
    df = df.rename(columns=lambda x: x.replace('properties.', ''))  # Simplificar nombres de columnas

    # Entrada del usuario para el filtro
    st.subheader("Escribe una consulta para filtrar los yacimientos")
    query = st.text_area("Consulta", value="filter all")

    # Aplicar el filtro
    filtered_geojson = process_geojson(geojson_data, query)

    # Crear la capa de mapa con los datos filtrados o completos
    if filtered_geojson:
        # Verificar si ya existe información seleccionada en el estado
        if "last_hovered" not in st.session_state:
            st.session_state["last_hovered"] = None

        geojson_layer = pdk.Layer(
            "GeoJsonLayer",
            filtered_geojson,
            pickable=True,  # Habilitar interacción con los puntos
            stroked=True,
            filled=True,
            get_radius=500,
            point_radius_min_pixels=3,  # Tamaño mínimo visible en pantalla
            get_fill_color="[255, 140, 0, 180]",
            get_line_color="[255, 0, 0, 200]",
        )

        # Configuración del mapa centrado en Chile
        view_state = pdk.ViewState(
            latitude=-35.6751,
            longitude=-71.543,
            zoom=5,
            pitch=0,
        )

        # Crear el mapa con pydeck
        r = pdk.Deck(
            layers=[geojson_layer],
            initial_view_state=view_state,
            tooltip={
                "html": "<b>Nombre:</b> {nombre}<br><b>Región:</b> {region}<br><b>Comuna:</b> {comuna}",
                "style": {"color": "white", "backgroundColor": "black", "fontSize": "12px"}
            },
        )

        # Mostrar el mapa
        st.pydeck_chart(r, use_container_width=True)

except Exception as e:
    st.error(f"Hubo un problema al cargar el archivo GeoJSON: {e}")
