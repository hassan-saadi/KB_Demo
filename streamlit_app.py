import pandas as pd
import snowflake.connector as snowflake
import os
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.title ('Welcome to the FiscalNote _DeepRisk360_ Demo')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())
graphname


