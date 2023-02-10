import pandas as pd
import snowflake.connector as snowflake
import os
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
image = Image.open('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.image(image)
st.sidebar.title ('Welcome to RiskHorizon')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())
graphname


