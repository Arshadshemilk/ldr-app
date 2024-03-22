from urllib.error import URLError
import requests
import pandas as pd
import pydeck as pdk
import streamlit as st
import time
import base64
import json

def fetch_github_json(repo_url, file_path, token):
    try:
        headers = {
            'Authorization': f'token {token}',
        }
        api_url = f"https://api.github.com/repos/{repo_url}/contents/{file_path}"
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 403:
            st.error("GitHub API rate limit exceeded. Please try again later.")
            return None
        
        response.raise_for_status()  # Raise an exception for HTTP errors
        content = response.json()
        decoded_content = base64.b64decode(content['content']).decode('utf-8')
        return decoded_content
    except (requests.RequestException, KeyError) as e:
        st.error(f"Failed to fetch JSON content from GitHub: {e}")
        return None

def mapping_demo():
    token = "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"
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
            repo_url = "Arshadshemilk/ldr-data"
            file_path = "gps_temp.json"
            json_content = fetch_github_json(repo_url, file_path,token)
            if json_content:
                parsed_json = json.loads(json_content)
                filtered_data = pd.DataFrame(parsed_json)
                st.write(filtered_data)
                filtered_data = filtered_data[filtered_data['temp'] < 30]

                # Update map data
                ALL_LAYERS["Points"].data = filtered_data

            time.sleep(5)  # Check for changes every 60 seconds
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
