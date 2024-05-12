import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import time
from urllib.error import URLError
import firebase_admin
from firebase_admin import credentials, db


if "markers" not in st.session_state:
    st.session_state["markers"] = []

# Check if Firebase app has already been initialized
if not firebase_admin._apps:
    # Initialize Firebase
    cred = credentials.Certificate("pages/ldr-ro-firebase-adminsdk-var6u-d008f4eb5b.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ldr-robot-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Function to read Firebase data and convert it to dataframe

def read_firebase_data():
    if(text_input):
        path = "/" + text_input
        ref = db.reference(path)  # Reference to the root of your Firebase database
        data = ref.get()  # Fetch data
        df = pd.DataFrame.from_dict(data, orient='index')
        return df
    else:
        st.write("Please enter a input")

def main():
    df = read_firebase_data()
    tempe = df
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
        coordinates = df[['latitude', 'longitude']].values.tolist()
        folium.PolyLine(locations=coordinates, color="blue", weight=2.5, opacity=1).add_to(map)
        if row['temperature'] > 34:
            marker = folium.Marker([row['latitude'], row['longitude']], icon=folium.Icon(color='red'))
            st.session_state["markers"].append(marker)
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
            df = read_firebase_data()
            comparison = df.equals(tempe)
            if not comparison:
                coordinates = df[['latitude', 'longitude']].values.tolist()
                folium.PolyLine(locations=coordinates, color="blue", weight=2.5, opacity=1).add_to(map)
                for index, row in df.iterrows():
                    if row['temperature'] > 34:
                        marker = folium.Marker([row['latitude'], row['longitude']], icon=folium.Icon(color='red'))
                        st.session_state["markers"].append(marker)

                    # Add path between locations
                               
            tempe = df
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
    text_input = st.text_input("Enter Field Name / User Name")
    if st.button("Get"):
        # Print the value entered in the textbox when the button is clicked
        if text_input:
            st.write("You entered:", text_input)
        else:
            st.write("Please enter a name")
    main()
