import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")


st.title("Heatmap")

filepath = "data/us_cities.csv"
data = pd.read_csv(filepath)

if 'latitude' in data.columns and 'longitude' in data.columns and 'pop_max' in data.columns:
    m = leafmap.Map(center=[40, -100], zoom=4)
    m.add_heatmap(
        filepath,
        latitude="latitude",
        longitude="longitude",
        value="pop_max",
        name="Heat map",
            radius=40,
        )
    m.to_streamlit(height=700)
else:
    st.write("El archivo CSV debe contener las columnas 'latitude', 'longitude', y 'pop_max'.")