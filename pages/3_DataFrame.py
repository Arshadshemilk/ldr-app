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
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# Check if Firebase app has already been initialized
if not firebase_admin._apps:
    # Initialize Firebase
    cred = credentials.Certificate("pages/ldr-ro-firebase-adminsdk-var6u-d008f4eb5b.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ldr-ro-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Function to read Firebase data and convert it to dataframe
def read_firebase_data():
    path = "/" + text_input
    ref = db.reference(path)  # Reference to the root of your Firebase database
    data = ref.get()  # Fetch data
    df = pd.DataFrame.from_dict(data, orient='index')
    return df

def data_frame_demo():

    # Read and display data
    data = read_firebase_data()
    st.write('Raw Data:')
    st.write(data)


st.set_page_config(page_title="DataFrame", page_icon="📊")
st.markdown("# DataFrame")
st.sidebar.header("DataFrame")
text_input = st.text_input("Enter Field Name / User Name")
if st.button("Get"):
    # Print the value entered in the textbox when the button is clicked
    if text_input:
        st.write("You entered:", text_input)
    else:
        st.write("Please enter a name")

data_frame_demo()

