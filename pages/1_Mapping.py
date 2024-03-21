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
    st.sidebar.info("Checking for changes in JSON file...")
    
    map_container = st.empty()
    ALL_LAYERS = {
        "Points": None,
    }

    mapstyle = st.sidebar.selectbox(
        "Choose Map Style:",
        options=["dark", "light", "road"],
        format_func=str.capitalize,
        key="mapstyle_selectbox"  # Add a unique key
    )

    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer_name
        for layer_name in ALL_LAYERS.keys()
        if st.sidebar.checkbox(layer_name, True, key=f"{layer_name}_checkbox")  # Add a unique key
    ]

    try:
        while True:
            json_content = fetch_json_from_github("https://raw.githubusercontent.com/Arshadshemilk/ldr-data/main/gps_temp.json")
            st.write(json_content)
            if json_content:
                filtered_data = pd.DataFrame(json_content)
                filtered_data = filtered_data[filtered_data['temp'] < 30]

                ALL_LAYERS["Points"] = pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_data,
                    get_position=["lon", "lat"],
                    get_color=[255, 0, 0, 160],  # Red color for temperature less than 30
                    get_radius=50,
                )

                if selected_layers:
                    map_component = pdk.Deck(
                        map_style=f"{mapstyle}",
                        initial_view_state={
                            "latitude": 10.068393,
                            "longitude": 76.593363,
                            "zoom": 15,
                            "pitch": 50,
                        },
                        layers=[ALL_LAYERS[layer_name] for layer_name in selected_layers]
                    )
                    map_container.pydeck_chart(map_component)
                else:
                    map_container.error("Please choose at least one layer above.")
                
            time.sleep(10)  # Check for changes every 60 seconds

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

st.set_page_config(page_title="Mapping", page_icon="🌍")
st.markdown("# Mapping")
st.sidebar.header("Mapping")

mapping_demo()
