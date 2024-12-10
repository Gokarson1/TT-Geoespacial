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
    <link rel="stylesheet" href="https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css" />
    <script src="https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.min.js"></script>

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
        <!-- Botón para descargar el archivo GeoJSON -->
        <button class="download-btn" onclick="downloadGeoJSON()">Descargar GeoJSON</button>
    </div>

<script>
    // Inicializar un FeatureCollection vacío para almacenar las formas dibujadas
    window.geojsonData = {
        type: "FeatureCollection",
        features: [] // Este array contendrá todas las formas en formato GeoJSON
    };

    // Crear el mapa y centrarlo en las coordenadas [0, 0] con un nivel de zoom de 2
    var map = L.map('map').setView([0, 0], 2);

    // Añadir capa base de OpenStreetMap
    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);

    // Capa de mapa topográfico
    var topoLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 17
    });

    // Capa de satélite
    var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 18
    });

    // Capa de clima (cambio según necesidad: precipitación, temperatura, etc.)
    var weatherLayer = L.tileLayer('https://{s}.tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=4ddfe4a7886cf75ff86a1cfbc537f255', {
        attribution: '&copy; <a href="https://openweathermap.org">OpenWeatherMap</a>',
        maxZoom: 19
    });

    // Control de capas para seleccionar entre diferentes vistas
    var baseLayers = {
        "OpenStreetMap": osmLayer,
        "Mapa Topográfico": topoLayer,
        "Satélite": satelliteLayer,
        "Clima (Temperatura)": weatherLayer
    };
    L.control.layers(baseLayers).addTo(map);

    // Crear un grupo para almacenar las formas dibujadas
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    // Configuración del control de dibujo
    var drawControl = new L.Control.Draw({
        edit: {
            featureGroup: drawnItems, // Permite editar las formas existentes
        },
        draw: {
            polygon: true,   // Permitir polígonos
            polyline: true,  // Permitir líneas
            rectangle: true, // Permitir rectángulos
            circle: true,    // Permitir círculos
            marker: true     // Permitir marcadores
            
        }
    });
    map.addControl(drawControl);

    // Evento al crear una nueva forma
    map.on(L.Draw.Event.CREATED, function (e) {
        var layer = e.layer; // Obtener la capa recién dibujada
        drawnItems.addLayer(layer); // Añadir la capa al mapa

        // Convertir la forma a GeoJSON y añadirla al FeatureCollection
        var newGeoJSON = layer.toGeoJSON();
        window.geojsonData.features.push(newGeoJSON);

        // Opcional: Mostrar información en la consola
        console.log("Nueva forma añadida:", newGeoJSON);
    });

    // Función para descargar todas las formas como un archivo GeoJSON
    function downloadGeoJSON() {
        if (window.geojsonData.features.length === 0) {
            alert("No hay datos para descargar.");
            return;
        }
        // Crear el archivo GeoJSON en formato de texto
        var geojsonText = JSON.stringify(window.geojsonData, null, 2); // Formateado para mayor legibilidad
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(geojsonText);

        // Crear un enlace temporal para descargar el archivo
        var downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "mapa_dibujo.geojson");
        document.body.appendChild(downloadAnchorNode); // Añadir al DOM (necesario para Firefox)
        downloadAnchorNode.click(); // Simular el clic para descargar
        downloadAnchorNode.remove(); // Limpiar el DOM
    }

    // Ejemplo: Vincular el botón de descarga al script
    document.querySelector('.download-btn').addEventListener('click', downloadGeoJSON);
</script>

</body>
</html>

"""

# Integrar el mapa interactivo en Streamlit
st.components.v1.html(map_code, height=700)
#comentario