from urllib.error import URLError
import numpy as np

import pandas as pd
import pydeck as pdk
import json

import streamlit as st
from streamlit.hello.utils import show_code

import requests
import time

def fetch_json_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch JSON file from GitHub.")
        return None

def mapping_demo():
    @st.cache_data
    def from_data_file(filename):
        url = "https://raw.githubusercontent.com/Arshadshemilk/ldr-data/main/%s" % filename
        data = pd.read_json(url)
        filtered_data = data[data['temp'] < 30]
        return filtered_data

    try:
        while True:
            json_content = fetch_json_from_github("https://raw.githubusercontent.com/Arshadshemilk/ldr-data/main/gps_temp.json")
            if json_content:
                st.sidebar.info("Detected changes in JSON file. Updating...")
                filtered_data = pd.DataFrame(json_content)
                filtered_data = filtered_data[filtered_data['temp'] < 30]

                ALL_LAYERS = {
                    "Points": pdk.Layer(
                        "ScatterplotLayer",
                        data=filtered_data,
                        get_position=["lon", "lat"],
                        get_color=[255, 0, 0],  # Set color to red
                        get_radius=50,
                    ),
                }

                mapstyle=st.sidebar.selectbox(
                    "Choose Map Style:",
                    options=["dark","light","road"],
                    format_func=str.capitalize,
                )
                st.sidebar.markdown("### Map Layers")
                selected_layers = [
                    layer
                    for layer_name, layer in ALL_LAYERS.items()
                    if st.sidebar.checkbox(layer_name, True)
                ]
                if selected_layers:
                    st.pydeck_chart(
                        pdk.Deck(
                            map_style=f"{mapstyle}",
                            initial_view_state={
                                "latitude": 10.068393,
                                "longitude": 76.593363,
                                "zoom": 15,
                                "pitch": 50,
                            },
                            layers=selected_layers,
                        )
                    )
                else:
                    st.error("Please choose at least one layer above.")
                time.sleep(60)  # Check for changes every 60 seconds
    except URLError as e:
        st.error(
            """
            **This requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Mapping", page_icon="🌍")
st.markdown("# Mapping")
st.sidebar.header("Mapping")

mapping_demo()
