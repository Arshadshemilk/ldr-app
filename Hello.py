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

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="UWLDR",
        page_icon="🤖",
    )

    st.write("# ROBOTICS IN UNDERGROUND WATER LEAK DETECTION ")

    st.markdown(
        """
        Leaks in water distribution networks (WDNs) produce significant economic losses. These leaks from underground pipelines affect the surrounding environment in different ways that can be detected
using various technologies. This article introduces an unmanned ground vehicle (UGV) equipped with an infrared temperature sensor to remotely detect thermal anomalies on the surface caused by underground
leaking pipelines. An MLX90614 low-cost thermopile infrared sensor was proposed to trace the surface temperature above leaking pipelines and record the corresponding position of each reading.
    """
    )


if __name__ == "__main__":
    run()
