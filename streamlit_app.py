import pandas as pd
import snowflake.connector as snowflake
import os
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.title ('Welcome to the FiscalNote _DeepRisk360_ Demo')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/data/result.csv?token=GHSAT0AAAAAAB4J2SZYQQUUCBVEGWDZWT5IY7FRPNA')

data

