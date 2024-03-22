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

import altair as alt
import pandas as pd
import json
import base64

import streamlit as st

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


def data_frame_demo():
    @st.cache_data


    try:
        token = "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"
        repo_url = "Arshadshemilk/ldr-data"
        file_path = "gps_temp.json"
        data = fetch_github_json(repo_url, file_path,token)
        parsed_data = json.loads(json_data)
        filtered_data = pd.DataFrame(parsed_data)
        filtered_data = filtered_data.T.reset_index()
        filtered_data = pd.melt(filtered_data, id_vars=["index"]).rename(
            columns={"index": "logitude", "latitude": "temperature"}
            )
        st.write(filtered_data)
            chart = (
                alt.Chart(filtered_data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="DataFrame", page_icon="📊")
st.markdown("# DataFrame")
st.sidebar.header("DataFrame")

data_frame_demo()

