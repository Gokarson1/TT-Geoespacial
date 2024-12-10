import streamlit as st
from leafmap import Map

# Configurar la página de Streamlit
st.set_page_config(page_title="Herramienta de Análisis Geoespacial", layout="wide")
st.title("Herramienta de Análisis Geoespacial")

# Crear un mapa utilizando leafmap basado en ipyleaflet
m = Map(center=[0, 0], zoom=2)

# Agregar un control de dibujo
draw_control = {
    "position": "topright",
    "draw": {
        "circle": False,
        "rectangle": True,
        "polygon": True,
        "polyline": True,
        "marker": True,
    },
    "edit": {"featureGroup": "editable"},
}
m.add_draw_control(draw_control)

# Renderizar el mapa en Streamlit
m.to_streamlit(height=500)

# Exportar las geometrías como GeoJSON
if st.button("Exportar geometrías como GeoJSON"):
    # Obtener las características dibujadas
    drawn_features = m.get_draw_features()
    
    if drawn_features:
        st.subheader("Geometrías Dibujadas")
        st.json(drawn_features)
        
        # Preparar el archivo GeoJSON
        import json
        geojson_data = {"type": "FeatureCollection", "features": drawn_features}
        geojson_str = json.dumps(geojson_data, indent=2)
        
        # Botón para descargar el archivo GeoJSON
        st.download_button(
            label="Descargar GeoJSON",
            data=geojson_str,
            file_name="geometries.geojson",
            mime="application/json",
        )
    else:
        st.warning("No se han dibujado geometrías para exportar.")
