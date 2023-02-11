import pandas as pd
import snowflake.connector as snowflake
import os
from PIL import Image
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import numpy as np
import requests
import folium
from streamlit_folium import st_folium
st.set_page_config(page_title = 'CQ RiskConnector', layout="wide")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/0/05/CQ_Logo.jpeg', width = 40)
st.sidebar.markdown("<font size="8">Improve Your :blue[C]hange :blue[Q]uotient</font>")
#st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.sidebar.title ('Welcome to the RiskConnector Sample')
st.sidebar.caption ('Limited connections shown')
st.text('Connection Related Events in Categories: Natural Disaster, \nLegal, Political, Government, Supply Chain, Contracts, Banking Operations, Financing')

data = pd.read_csv('https://raw.githubusercontent.com/andychak/KB_Demo/master/result.csv')
graphname = st.sidebar.selectbox("Please select a company as a starting node:", data['GRAPH'].unique())

import streamlit as st

def snow():
    """
       This function takes a user id, password, and account and creates a snowflake connection using the snowflake python connector

    :param id: id, saved in os environment variables
    :param passwd: password, saved in os environment variables
    :param account: account, saved in os environment variables
    :param database: per global constant or defined in function call
    :param schema: per global constant or defined in function call
    :return: cursor that connects to snowflake  and the connection itself
    """
    ctx = snowflake.connect(
        user=os.environ["snowflake_user"],
        password=os.environ['snowflake_password'],
        account=os.environ['snowflake_account'],
        database="FORGEAI_ARTICLES_V0660",
        schema="ARTICLES_V0660"
    )
    print('Snowflake connected to database:{}'.format(database))
    return ctx.cursor(), ctx


@st.cache_data
def mapdata():
    cs, ctx = snow()

    try:
        cs.execute("""
            select distinct any_value(graph), any_value(to_date(nvl(docdatetime, processdatetime))) as date, ENDING_NODE, any_value(url), 
            any_value(latitude) as latitude, any_value(longitude) as longitude
            from "SCRATCH_FORGEAI"."ANDYC"."KBWEB" kb
            join "PROD_V06XX"."FORGEAI_SURGES"."DOCUMENTS" docs on docs.uripath = kb.ENDING_NODE and docs.saliency_V1 >= .25
            join "PROD_V06XX"."ARTICLES_V0670"."INTRINSICEVENTS" ievents on ievents.docid = docs.docid and ievents.confidence >= 0.35
            join "PROD_V06XX"."ARTICLES_V0670"."ENTITYASSERTIONS" serts on serts.docid = docs.docid and serts.confidence >= 0.7
            join "PROD_V06XX"."KG_V0660"."LOCATIONS" locs on locs.type = serts.assertedclass where starting_node != ending_node
            and ending_node not in ('pepsico_inc', 'coca-cola_company', 'goldman_sachs_group_inc', 'jp_morgan_chase_and_co'
                        , 'alphabet_inc', 'microsoft_corp', 'google')
            and category in ('NaturalDisaster', 'Legal', 'Political', 'Government', 'SupplyChain', 'Contract', 'Basel', 'Financing', 'Corporate')
            and url not like('https://forgeai.net/naviga%')
            and label not in ('earnings call', 'Earnings Call')
            and latitude is not NULL
            and docdatetime >= DATEADD(day, -30, CURRENT_DATE())
            group by 3 limit 600;""")
        rows = cs.fetchall()
    except:
        print("database connection error")
    finally:
        cs.close()
    ctx.close()
    return pd.DataFrame(rows, columns = ['GRAPH', 'DATE', 'ENDING_NODE', 'URL', 'LATITUDE', 'LONGITUDE'])

mapdf = mapdata()
mapdf
# center on Liberty Bell, add marker
m = folium.Map(location=[39.949610, -75.150282], zoom_start=10)
folium.Marker(
    [39.949610, -5.150282], popup="https://fiscalnote.com/", tooltip="Liberty Bell"
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)

# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6><h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6><a href="mailto:Clinton.Stephens@fiscalnote.com">Learn More</a></h6><h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
    )
