import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Datos Geoespaciales de Chile")

# Subir archivo CSV
uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Leer el archivo CSV con el delimitador ';'
    data = pd.read_csv(uploaded_file, delimiter=';')

    # Filtrar las columnas importantes
    columns_of_interest = [
        'region', 'cod_nodo', 'nombre_nodo', 'altura sig espectral (m)',
        'Período de cruces por cero. Equivalente a T0,2 (seg.)', 'Período energético del oleaje (seg)',
        'Período medio del oleaje. Equivalente a T0,1 (seg)', 'Período pico del oleaje (seg)',
        'Dirección media del oleaje (°)', 'Dirección pico del oleaje(°)', 'Ancho espectral',
        'Ancho de banda espectral', 'Agudeza de pico del espectro', 'Parámetro de acentuación del máximo espectral',
        'Parámetro de dispersión direccional del oleaje', 'año', 'fecha'
    ]
    data = data[columns_of_interest]

    # Mostrar análisis descriptivo
    st.header("Análisis Descriptivo")
    st.write(data.describe())

    # Selección de columnas para visualizar
    x_column = st.selectbox("Selecciona la columna para el eje X", data.columns)
    y_column = st.selectbox("Selecciona la columna para el eje Y", data.columns)

    # Mostrar gráfico de dispersión usando Streamlit
    st.header(f"Gráfico de {x_column} vs {y_column}")
    st.line_chart(data[[x_column, y_column]].set_index(x_column))
else:
    st.info("Por favor, sube un archivo CSV.")