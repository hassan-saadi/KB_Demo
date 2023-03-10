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
import branca
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='CQ RiskConnector', layout="wide")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/0/05/CQ_Logo.jpeg', width=40)
st.sidebar.caption("Improving Your :blue[C]hange :blue[Q]uotient")
# st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.title('CQ RiskConnector Sample')
st.caption('Limited connections shown')
st.caption(
    "Key: :green[Favorable Business Impacting Events/News Sample.] :red[Favorable Business Impacting Events/News Sample.] :gray[Neutral News/Events]")
mapdict = {}
markerdict = {}


@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


conn = init_connection()


@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


query = """
with documentlist as (
  select distinct any_value(docs.docid) as docid, any_value(graph) as graph, any_value(node_distance) as node_distance
    ,any_value(to_date(nvl(docs.docdatetime, docs.processdatetime))) as date, ENDING_NODE 
    ,any_value(url) as url, any_value(title) as title, any_value(description) as description 
    ,any_value(case when sentiment is NULL then 'gray' when sentiment <= -.02 then 'red' when sentiment >= .3 then 'green' ELSE 'gray' END) as sentimentcolor
    ,any_value(latitude) as latitude, any_value(longitude) as longitude, any_value(ABS(MOD(HASH(ENDING_NODE), 1000000))/10000000) as hash_value
  from "SCRATCH_FORGEAI"."ANDYC"."KBWEB2" kb
  //join "PROD_V06XX"."FORGEAI_SURGES"."DOCUMENTS" docs on docs.uripath = kb.ENDING_NODE and docs.saliency_V1 >=.25
  join "PROD_V06XX"."FORGEAI_ARTICLES"."COMPANYDOCUMENTS" docs on docs.uripath = kb.ENDING_NODE and docs.saliency_V1 >=.25 and docs.confidence >= .5
  join "PROD_V06XX"."ARTICLES_V0670"."INTRINSICEVENTS" ievents on ievents.docid = docs.docid //and ievents.confidence >= 0.35
  join "PROD_V06XX"."ARTICLES_V0670"."ENTITYASSERTIONS" serts on serts.docid = docs.docid and serts.confidence >= 0.55
  join "PROD_V06XX"."ARTICLES_V0670"."ENTITYLOCATIONS" elocs on elocs.docid = docs.docid and elocs.entityid = serts.entityid and elocs.sentenceid <=5
  join  "PROD_V06XX"."KG_V0660"."LOCATIONS" locs on locs.type = serts.assertedclass
  where starting_node != ending_node
  and ending_node not in ('pepsico_inc','coca-cola_company','goldman_sachs_group_inc','jp_morgan_chase_and_co'
        ,'alphabet_inc' ,'microsoft_corp', 'google', 'morgan_stanley_international_holdings_inc')
  //and category in ('NaturalDisaster', 'Legal', 'Political', 'Government', 'SupplyChain', 'Contract', 'Basel', 'Financing', 'Corporate')
  and category is not NULL
  and url not like ('https://forgeai.net/naviga%')
  and label not in ('earnings call', 'Earnings Call')
  and latitude is not NULL
  and longitude is not NULL
  and docs.docdatetime >= DATEADD(day, -14, CURRENT_DATE())
  group by 5) 
  select  any_value(graph), any_value(node_distance), any_value(date) as date, ENDING_NODE, any_value(url), any_value(title),any_value(description),
            any_value(sentimentcolor) as sentimentcolor,any_value(latitude-hash_value) as latitude, any_value(longitude+hash_value) as longitude
            ,array_agg(distinct topics.name) as topics, array_agg(distinct ievents.label) as ievents
  from documentlist
  left join "PROD_V06XX"."ARTICLES_V0670"."DOCUMENTTOPICS" topics on topics.docid = documentlist.docid and topics.score >=.8
  left join"PROD_V06XX"."ARTICLES_V0670"."INTRINSICEVENTS" ievents on ievents.docid = documentlist.docid and ievents.confidence >=.75

  group by 4
  order by 3 DESC
            ;"""
rows = run_query(query)
mapdf = pd.DataFrame(rows, columns=['GRAPH', 'NODE_DISTANCE', 'DATE', 'ENDING_NODE', 'URL', 'TITLE', 'DESCRIPTION',
                                    'SENTIMENT_COLOR', 'LATITUDE', 'LONGITUDE', 'TOPICS', 'IEVENTS'])
graphs = mapdf['GRAPH'].unique()
graphname = st.sidebar.selectbox("Please select a company as a starting node:", graphs)

graph_df = mapdf[mapdf['GRAPH'] == graphname]
newsmap = folium.Map(control_scale=True, width="100%", zoom_start=4, tiles='Stamen Terrain')

fg = folium.FeatureGroup(name="Markers")
for index, row in graph_df.iterrows():
    events = row['IEVENTS'][1:-1].replace('"', '')
    topics = row['TOPICS'][1:-1].replace('"', '')
  
    
    htmlpop = f"""<b> {row['ENDING_NODE']} <br/> {str(row['DATE'])} </b><br/><a href={row['URL']} 
                  " target="_blank"> {row['TITLE']} </a><br/> {row['DESCRIPTION']} <br/><table 
                  style="border:1"><tr><td style="background-color: lightgray;">
                  Node Distance</td><td> {row['NODE_DISTANCE']} </td></tr><tr>
                  <td style="background-color: lightgray;">Topics</td><td> {topics}
                  </td></tr><tr><td style="background-color: lightgray;">Events</td><td> 
                  {events} </td></tr></table>"""
    popup = folium.Popup(htmlpop, min_width=700)
    tooltip = str(row['ENDING_NODE'])
    color = str(row['SENTIMENT_COLOR'])
    latitude = float(row['LATITUDE'])
    longitude = float(row['LONGITUDE'])
    if color == 'green':
        folium.Marker(location=[latitude, longitude], popup=popup, tooltip=tooltip,
                      icon=folium.Icon(color=color, icon='thumbs-up', prefix='fa')).add_to(fg)
    elif color == 'red':
        folium.Marker(location=[latitude, longitude], popup=popup, tooltip=tooltip,
                      icon=folium.Icon(color=color, icon='thumbs-down', prefix='fa')).add_to(fg)

    else:
        folium.Marker(location=[latitude, longitude], popup=popup, tooltip=tooltip,
                      icon=folium.Icon(color=color, icon='circle', prefix='fa')).add_to(fg)
fg.add_to(newsmap)

# call to render Folium map in Streamlit
st_folium(
    newsmap,
    key="new",
    feature_group_to_add=fg,
    # height=400,
    width=1000,
)
# st_data = st_folium(newsmap,  width=1000)

# st_data = st_folium(newsmap, key="new", feature_group_to_add=fg, width=1000)
# graph_df


# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6><h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6><a href="mailto:Clinton.Stephens@fiscalnote.com">Learn More</a></h6><h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
)
