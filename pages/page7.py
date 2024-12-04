import streamlit as st
from PIL import Image
import json
import base64

# Open the logo image
img = Image.open("img/logo.png")

# Set page configuration with icon
st.set_page_config(layout="wide", page_icon=img)

# Título y descripción en Python
st.title("Mapa Interactivo con Herramientas de Dibujo y Selección de Capas")
st.markdown("""
Esta herramienta te permite interactuar con un mapa en blanco, 
dibujar formas (líneas, polígonos, marcadores, círculos, etc.), 
y visualizar los datos en formato GeoJSON. 
Puedes seleccionar capas base mediante un buscador.
""")

# Código HTML y JavaScript para el mapa interactivo con herramientas de dibujo y selección de capas
map_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Mapa con Dibujo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
    <style>
        /* Estilos para el mapa */
        #map {
            height: 600px;
            width: 100%;
        }

        /* Estilos del botón de descarga */
        .download-btn {
            display: inline-block;
            padding: 10px 20px;
            margin: 10px 0;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .download-btn:hover {
            background-color: #45a049;
        }

        /* Añadir un espacio entre el mapa y el botón */
        .map-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>
    <div class="map-container">
        <div id="map"></div>
        <button class="download-btn" onclick="downloadGeoJSON()">Descargar GeoJSON</button>
    </div>

    <script>
        // Inicializar el mapa
        var map = L.map('map').setView([0, 0], 2);
        
        // Añadir capa base de OpenStreetMap
        var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
        }).addTo(map);

        // Capa de OpenTopoMap (mapa topográfico)
        var topoLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
            maxZoom: 17,
        });

        // Capa de Satélite (Satélite ESRI)
        var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 18,
        });

        // Capa de Clima (OpenWeatherMap)
        var weatherLayer = L.tileLayer('https://{s}.tile.openweathermap.org/map/{layer}/{z}/{x}/{y}.png?appid=4ddfe4a7886cf75ff86a1cfbc537f255', {
            attribution: '&copy; <a href="https://openweathermap.org">OpenWeatherMap</a>',
            maxZoom: 19,
            layer: 'temp_new'  // Puede cambiarse por otros tipos de clima como 'precipitation_new', 'clouds_new', etc.
        });

        // Añadir control de capas
        var baseLayers = {
            "OpenStreetMap": osmLayer,
            "Mapa Topográfico": topoLayer,
            "Satélite": satelliteLayer,
            "Clima": weatherLayer
        };

        // Añadir control de capas al mapa
        L.control.layers(baseLayers).addTo(map);

        // Inicializar herramientas de dibujo
        var drawnItems = new L.FeatureGroup();
        map.addLayer(drawnItems);

        var drawControl = new L.Control.Draw({
            edit: {
                featureGroup: drawnItems,
            },
            draw: {
                polygon: true,
                polyline: true,
                rectangle: true,
                circle: true,
                marker: true,
            },
        });
        map.addControl(drawControl);

        // Manejar eventos de creación de formas
        map.on(L.Draw.Event.CREATED, function (e) {
            var layer = e.layer;
            drawnItems.addLayer(layer);
            
            // Convertir la forma a GeoJSON y actualizar un archivo GeoJSON global
            var geojson = layer.toGeoJSON();
            // Actualiza la variable 'geojsonData' con el objeto GeoJSON
            window.geojsonData = geojson;
        });

        // Función para descargar el archivo GeoJSON
        function downloadGeoJSON() {
            var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(window.geojsonData));
            var downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href", dataStr);
            downloadAnchorNode.setAttribute("download", "mapa_dibujo.geojson");
            downloadAnchorNode.click();
        }
    </script>
</body>
</html>
"""

# Integrar el mapa interactivo en Streamlit
st.components.v1.html(map_code, height=700)
#comentario