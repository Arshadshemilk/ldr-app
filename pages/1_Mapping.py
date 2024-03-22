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
    st.sidebar.info("Checking for changes in JSON file...")

    # Add your personal access token here
    token = "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"

    ALL_LAYERS = {
        "Points": pdk.Layer(
            "ScatterplotLayer",
            data=None,
            get_position=["lon", "lat"],
            get_color=[255, 0, 0, 160],
            get_radius=50,
        ),
    }

    mapstyle = st.sidebar.selectbox(
        "Choose Map Style:",
        options=["dark", "light", "road"],
        format_func=str.capitalize,
        key="mapstyle_selectbox"
    )

    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True, key=f"{layer_name}_checkbox")
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
                layers=[layer for layer in ALL_LAYERS.values()],
            )
        )
    else:
        map_component = st.error("Please choose at least one layer above.")

    try:
        while True:
            repo_url = "Arshadshemilk/ldr-data"
            file_path = "gps_temp.json"
            json_content = fetch_github_json(repo_url, file_path, token)
            if json_content:
                parsed_json = json.loads(json_content)
                filtered_data = pd.DataFrame(parsed_json)
                filtered_data = filtered_data[filtered_data['temp'] < 30]
                ALL_LAYERS["Points"].data = filtered_data.to_dict(orient='records') if not filtered_data.empty else None
                # Update the map component to reflect changes
                map_component.deck_layers = [
                    pdk.Layer(
                        map_component.deck_layers[0].type,
                        data=ALL_LAYERS["Points"].data,
                        get_position=["lon", "lat"],
                        get_color=[255, 0, 0, 160],  # Red color for temperature less than 30
                        get_radius=50,
                    )
                ]
            time.sleep(10)  # Increase interval
    except KeyboardInterrupt:
        st.error("Fetching interrupted by user.")
    except URLError as e:
        st.error(f"This requires internet access. Connection error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.set_page_config(page_title="Mapping", page_icon="🌍")
st.markdown("# Mapping")
st.sidebar.header("Mapping")

mapping_demo()
