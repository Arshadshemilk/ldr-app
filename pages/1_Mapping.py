import folium
import geopandas as gpd
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium
import time
import base64
import json
from urllib.error import URLError


if "markers" not in st.session_state:
    st.session_state["markers"] = []

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

def main():
    token = "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"
    repo_url = "Arshadshemilk/ldr-data"
    file_path = "gps_temp.json"
    json_content = fetch_github_json(repo_url, file_path,token)
    parsed_json = json.loads(json_content)
    df = pd.DataFrame(parsed_json)
    # Sample DataFrame with longitude, latitude, and temperature data

    START_LOCATION = [10.067921, 76.595418]
    START_ZOOM = 15
    
    map = folium.Map(
        location=START_LOCATION,
        zoom_start=START_ZOOM,
        tiles="OpenStreetMap",
        max_zoom=30,
    )
    for index, row in df.iterrows():
        if row['temp'] < 30:
            marker = folium.Marker([row['lat'], row['lon']], icon=folium.Icon(color='red'))
            st.session_state["markers"].append(marker)

            # Add path between locations
            coordinates = df[['lat', 'lon']].values.tolist()
            folium.PolyLine(locations=coordinates, color="blue", weight=2.5, opacity=1).add_to(map)
    fg = folium.FeatureGroup(name="Markers")
    for marker in st.session_state["markers"]:
        fg.add_child(marker)
    st_folium(
        map,
        key="new",
        feature_group_to_add=fg,
        height=700,
        width=700,
    )
    
    try:
        while True:
            token = "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"
            repo_url = "Arshadshemilk/ldr-data"
            file_path = "gps_temp.json"
            json_content = fetch_github_json(repo_url, file_path,token)
            parsed_json = json.loads(json_content)
            df = pd.DataFrame(parsed_json)
            tempe = df
            comparison = df.equals(tempe)
            if not comparison:
                for index, row in df.iterrows():
                    if row['temp'] < 30:
                        marker = folium.Marker([row['lat'], row['lon']], icon=folium.Icon(color='red'))
                        st.session_state["markers"].append(marker)

                    # Add path between locations
                    coordinates = df[['lat', 'lon']].values.tolist()
                    folium.PolyLine(locations=coordinates, color="blue", weight=2.5, opacity=1).add_to(map)           
            time.sleep(1)  # Check for changes every 60 seconds
    except URLError as e:
        st.error(
            """
            **This requires internet access.**
            Connection error: %s
        """
            % e.reason
        )

    # Add markers based on temperature condition
    

if __name__ == "__main__":
    st.set_page_config(page_title="Mapping", page_icon="🌍")
    st.markdown("# Mapping")
    st.sidebar.header("Mapping")
    main()
