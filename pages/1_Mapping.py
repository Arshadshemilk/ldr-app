# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.error import URLError
import numpy as np

import pandas as pd
import pydeck as pdk
import json

import streamlit as st
from streamlit.hello.utils import show_code


def mapping_demo():
    @st.cache_data
    def from_data_file(filename):
        url = (
            "https://raw.githubusercontent.com/Arshadshemilk/ldr-data/main/%s" % filename
        )
        data=pd.read_json(url)
        filtered_data = data[data['temp'] < 30]
        return filtered_data

    try:
        ALL_LAYERS = {
            "Points": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("gps_temp.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=13,
            ),
         }
        mapstyle=st.sidebar.selectbox(
            "Choose Map Style:",
            options=["light","dark","satellite","road"],
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
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Mapping", page_icon="🌍")
st.markdown("# Mapping")
st.sidebar.header("Mapping")

mapping_demo()
