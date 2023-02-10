import pandas as pd
import snowflake.connector as snowflake
import os
from PIL import Image
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.title ('Welcome to RiskHorizon')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())
graphname


