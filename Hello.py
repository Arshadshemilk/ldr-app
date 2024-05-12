import time
import streamlit as st
from streamlit.logger import get_logger
import streamlit_extras
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row

LOGGER = get_logger(__name__)
_text1 = """
    Leaks in water distribution networks (WDNs) produce significant economic losses. These leaks
from underground pipelines affect the surrounding environment in different ways that can be detected
using various technologies. This project introduces an unmanned ground vehicle (UGV) equipped with
an infrared temperature sensor to remotely detect thermal anomalies on the surface caused by
underground leaking pipelines. An MLX90614 low-cost thermopile infrared sensor was proposed to
trace the surface temperature above leaking pipelines and record the corresponding position of each
reading. A satellite navigation system used to acquire precise location.
"""


def stream_data():
    for word in _text1.split(" "):
        yield word + " "
        time.sleep(0.02)

def run():
    st.set_page_config(
        page_title="UWLDR",
        page_icon="🤖",
    )

    st.write("# ROBOTICS IN UNDERGROUND WATER LEAK DETECTION ")

    st.write_stream(stream_data)
    add_vertical_space(1)
    st.markdown("### Developed by : ")
    st.write("###### ARSHAD SHEMIL K ")
    st.write("###### ASHISH K JOSE ")
    st.write("###### SHIN SIBI ")
    st.write("###### ANANDHU S ANIL ")
    st.markdown("#### Learn more")
    links_row = row(2, vertical_align="center")
    links_row.link_button(
        "📖  Visit our documentation",
        "https://drive.google.com/file/d/1zlkA7DFn8Lxb4IP3sDncnKlo2koufGak/view?usp=drivesdk ",
        use_container_width=True,
    )
    links_row.link_button(
        "🐙  Visit our repository",
        "https://github.com/Arshadshemilk/ldr-app",
        use_container_width=True,
    )
    add_vertical_space(1)
    image_path = "logo.png"

    # Add image and caption on the right side
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image(image_path, width=100)  # Adjust width as needed
    with col2:
        add_vertical_space(1)
        st.markdown("### INDIRA GANDHI INSTITUTE OF ENGINEERING AND TECHNOLOGY, KOTHAMANGALAM")
    
    
    


if __name__ == "__main__":
    run()
