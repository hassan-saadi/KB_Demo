import pandas as pd
import snowflake.connector
import os
from PIL import Image
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import numpy as np
from bs4 import BeautifulSoup
import requests
import folium
from streamlit_folium import st_folium
st.set_page_config(page_title = 'CQ RiskConnector', layout="wide")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/0/05/CQ_Logo.jpeg', width = 40)
st.sidebar.caption("Improving Your :blue[C]hange :blue[Q]uotient")
#st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.title ('CQ RiskConnector Sample')
st.caption ('Limited connections shown')
st.text('Connection Related Business Impacting Events/News')
m = folium.Map(control_scale=True, attr="CQ RiskConnector", width = "100%", tiles='StamenToner')

#@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
conn = init_connection()

#@st.cache_data(ttl=600)
@st.cache
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
query = """
select distinct any_value(graph), any_value(node_distance), any_value(to_date(nvl(docs.docdatetime, docs.processdatetime))) as date, ENDING_NODE, any_value(url), 
            any_value(case when sentiment is NULL then 'gray' when sentiment <= -.02 then 'red' when sentiment >= .3 then 'green' ELSE 'gray' END) as sentimentcolor,
            any_value(latitude) as latitude, any_value(longitude) as longitude
  from "SCRATCH_FORGEAI"."ANDYC"."KBWEB" kb
  //join "PROD_V06XX"."FORGEAI_SURGES"."DOCUMENTS" docs on docs.uripath = kb.ENDING_NODE and docs.saliency_V1 >=.25
  join "PROD_V06XX"."FORGEAI_ARTICLES"."COMPANYDOCUMENTS" docs on docs.uripath = kb.ENDING_NODE and docs.saliency_V1 >=.25 and docs.confidence >= .5
  join "PROD_V06XX"."ARTICLES_V0670"."INTRINSICEVENTS" ievents on ievents.docid = docs.docid //and ievents.confidence >= 0.15
  join "PROD_V06XX"."ARTICLES_V0670"."ENTITYASSERTIONS" serts on serts.docid = docs.docid and serts.confidence >= 0.6
  join  "PROD_V06XX"."KG_V0660"."LOCATIONS" locs on locs.type = serts.assertedclass
  where starting_node != ending_node
  and ending_node not in ('pepsico_inc','coca-cola_company','goldman_sachs_group_inc','jp_morgan_chase_and_co'
        ,'alphabet_inc' ,'microsoft_corp', 'google')
  and category in ('NaturalDisaster', 'Legal', 'Political', 'Government', 'SupplyChain', 'Contract', 'Basel', 'Financing', 'Corporate')
  and url not like ('https://forgeai.net/naviga%')
  and label not in ('earnings call', 'Earnings Call')
  and latitude is not NULL
  and docs.docdatetime >= DATEADD(day, -60, CURRENT_DATE())
  group by 4
            ;"""
rows = run_query(query)
mapdf =  pd.DataFrame(rows, columns = ['GRAPH','NODE_DISTANCE', 'DATE', 'ENDING_NODE','SENTIMENT_COLOR', 'URL', 'LATITUDE', 'LONGITUDE'])
graphs = mapdf['GRAPH'].unique()
graphname = st.sidebar.selectbox("Please select a company as a starting node:", graphs)
graph_df = mapdf[mapdf['GRAPH']==graphname]
#graph_df



for index, row in graph_df.iterrows():
    pub_html = folium.Html(f"""<p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 21px;">{name}</span></p>
    <p style="text-align: center;"><iframe src={row['URL']}embed width="240" height="290" frameborder="0" scrolling="auto" allowtransparency="true"></iframe> 
    """, script=True)
    popup = folium.Popup(pub_html, max_width=700)
    folium.Marker(location = [row.loc['LATITUDE'], row.loc['LONGITUDE']], popup=popup, tooltip=row.loc['ENDING_NODE']).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 1000)


# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6><h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6><a href="mailto:Clinton.Stephens@fiscalnote.com">Learn More</a></h6><h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
    )
