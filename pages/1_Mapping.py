from urllib.error import URLError
import requests
import pandas as pd
import pydeck as pdk
import streamlit as st
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

    # Create map and checkboxes outside the loop
    st.sidebar.info("Checking for changes in JSON file...")

    ALL_LAYERS = {
        "Points": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("gps_temp.json"),  # Initially load the data
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 160],  # Red color for temperature less than 30
            get_radius=50,
        ),
    }

    mapstyle = st.sidebar.selectbox(
        "Choose Map Style:",
        options=["dark", "light", "road"],
        format_func=str.capitalize,
        key="mapstyle_selectbox"  # Add a unique key
    )

    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True, key=f"{layer_name}_checkbox")  # Add a unique key
    ]
    if selected_layers:
        map_component = st.pydeck_chart(
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
        map_component = st.error("Please choose at least one layer above.")

    try:
        while True:
            json_content = fetch_json_from_github("https://raw.githubusercontent.com/Arshadshemilk/ldr-data/main/gps_temp.json")
            if json_content:
                filtered_data = pd.DataFrame(json_content)
                filtered_data = filtered_data[filtered_data['temp'] < 30]
                
                # Update map data
                ALL_LAYERS["Points"].data = filtered_data
                
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
