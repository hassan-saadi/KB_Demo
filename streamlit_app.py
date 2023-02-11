import pandas as pd
import snowflake.connector as snowflake
import os
from PIL import Image
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import numpy as np
import requests
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/0/05/CQ_Logo.jpeg', width = 50, caption="Improve your Change Quotient")
#st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.title ('Welcome to the RiskConnector Sample Preview')
st.sidebar.text ('Limited connections shown')
data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())

df_graph = data[data['GRAPH']==graphname]
#location = 'https://drive.google.com/file/d/1DpJtnYV9M9KfsxVMKmjNhvoPmiAuAeox/view?usp=share_link'
#location = ("https://github.com/andychak/KB_Demo/blob/master/" + graphname + ".html")
#location = ("https://raw.githubusercontent.com/andychak/KB_Demo/master/"  + graphname + ".html")
#response = requests.get(location)
#components.html(response.text,width=1000, height=800)


nodes = []
nodelist = list(set(df_graph['ENDING_NODE'].to_list()))
nodelist = [x for x in nodelist if x != graphname]
edges =[]
nodes.append(Node(id = graphname, label = graphname, size =25, color = 'black'))
for element in nodelist:
    nodes.append(Node(id = element, label = element, size =25))
for i, row in df_graph.iterrows():
    edges.append( Edge(source=row['STARTING_NODE'], 
                   
                   target=row['ENDING_NODE'], 
                   # **kwargs
                   ) 
            ) 


config = Config(width=1200,
                height=1200,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)



# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6>
    <h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6><a href="mailto:Clinton.Stephens@fiscalnote.com">Learn More</a></h6>
    <h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
    )
