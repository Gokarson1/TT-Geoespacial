import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# Título de la página
st.title("Mapa Interactivo de Datos Geoespaciales")

# Entrada de dirección por parte del usuario
address = st.text_input("Ingresa una dirección o ubicación:")

if address:
    # Usar la API de OpenStreetMap para obtener las coordenadas de la dirección
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        data = response.json()

        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])

            # Crear un mapa centrado en la ubicación ingresada
            m = folium.Map(location=[lat, lon], zoom_start=15)

            # Añadir un marcador en la ubicación ingresada
            folium.Marker(
                location=[lat, lon],
                popup=f"Ubicación: {address}",
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)

            # Mostrar el mapa en la aplicación
            st_folium(m, width=1000, height=500)

            # Mostrar algunos datos interesantes (ejemplo: coordenadas)
            st.write(f"Coordenadas de {address}:")
            st.write(f"Latitud: {lat}")
            st.write(f"Longitud: {lon}")

            # Usar la API de Open-Elevation para obtener la altitud
            elevation_url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
            elevation_response = requests.get(elevation_url)
            elevation_data = elevation_response.json()

            if elevation_data and 'results' in elevation_data:
                elevation = elevation_data['results'][0]['elevation']
                st.write(f"Altitud: {elevation} metros")
            else:
                st.write("No se pudo obtener la altitud.")

            # Usar la API de GeoNames para obtener la población
            geonames_url = f"http://api.geonames.org/findNearbyPlaceNameJSON?lat={lat}&lng={lon}&username=demo"
            geonames_response = requests.get(geonames_url)
            geonames_data = geonames_response.json()

            if geonames_data and 'geonames' in geonames_data and len(geonames_data['geonames']) > 0:
                population = geonames_data['geonames'][0].get('population', 'No disponible')
                st.write(f"Población: {population}")
            else:
                st.write("No se pudo obtener la población.")
        else:
            st.write("No se encontraron resultados para la dirección ingresada.")
    except requests.exceptions.RequestException as e:
        st.write(f"Error al realizar la solicitud: {e}")
    except ValueError as e:
        st.write(f"Error al procesar los datos: {e}")
else:
    # Crear un mapa centrado en una ubicación predeterminada
    m = folium.Map(location=[-33.466, -70.597], zoom_start=10)

    # Mostrar el mapa en la aplicación
    st_folium(m, width=1000, height=500)