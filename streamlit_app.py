import pandas as pd
import snowflake.connector as snowflake
import os
from PIL import Image
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import numpy as np

st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.title ('Welcome to RiskHorizon')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())

df_graph = data[data['GRAPH']==graphname]



nodes = []
edges = []
nodeslist = []

nodes.append(Node (id=graphname, label = graphname, color = 'black', size = 15))
nodeslist = list(set(df_graph['ENDING_NODE'].to_list()))
nodeslist = [x for x in nodeslist if x != graphname]
for index, row in df_graph.iterrows():
  try:
    edges.append(Edge(source = row['STARTING_NODE'], target = row['ENDING_NODE'], size =10))
  except: 
    pass
config = Config(height=800,
		#width=700, 
                nodeHighlightBehavior=True,
                highlightColor="#F7A7A6", 
                directed=True, 
                collapsible=True)
                 
                 
return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6>
    <h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
    )
