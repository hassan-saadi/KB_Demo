import pandas as pd
import snowflake.connector as snowflake
import os
from PIL import Image
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import numpy as np
import requests

st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.title ('Welcome to the RiskConnector Sample Preview')
st.sidebar.text ('Limited connections per node are shown')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())

df_graph = data[data['GRAPH']==graphname]
#location = 'https://drive.google.com/file/d/1DpJtnYV9M9KfsxVMKmjNhvoPmiAuAeox/view?usp=share_link'
#location = ("https://github.com/andychak/KB_Demo/blob/master/" + graphname + ".html")
location = ("https://raw.githubusercontent.com/andychak/KB_Demo/master/"  + graphname + ".html")
response = requests.get(location)
st.markdown(response.text, unsafe_allow_html = True)


# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6>
    <h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
    )
