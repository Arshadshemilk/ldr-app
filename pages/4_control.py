import streamlit as st

def main():
    st.title("Local Webserver Inside Streamlit")
    st.write("Below is the local webserver embedded within Streamlit:")
    st.write("<iframe src='http://192.168.69.133' width='100%' height='500px'></iframe>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
