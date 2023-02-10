import pandas as pd
import snowflake.connector as snowflake
import os
from PIL import Image
import streamlit.components.v1 as components
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.title ('Welcome to RiskHorizon')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())
graphname

df_graph = data[data['GRAPH']==graphname]
net = Network(notebook=False, height="1000px", width="100%", select_menu=True, filter_menu=True, neighborhood_highlight=True)
net.add_node(graphname, label = graphname, color = 'black', value = 100)
for index, row in df_graph.iterrows():
  net.add_node(row['ENDING_NODE'], physics = False, label =row['ENDING_NODE'], title = row['ENDING_NODE'], group = row['NODE_DISTANCE'], value = 10) 
for index, row in df_graph.iterrows():
  try:
    net.add_edge(row['STARTING_NODE'], row['ENDING_NODE'], value=row['INTENSITY'], color = (row['ENDNODE_SENTIMENT'] + row['STARTNODE_SENTIMENT'])/2,
    physics = False)
  except: 
    pass
path = 'tmp'
net.save_graph(f'pyvis_graph.html')
HtmlFile = open(f'pyvis_graph.html','r',encoding='utf-8')
# Load HTML into HTML component for display on Streamlit
components.html(HtmlFile.read())
