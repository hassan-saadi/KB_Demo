import pandas as pd
import snowflake.connector as snowflake
import os
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
ctx = snowflake.connect(user=os.environ['snowflake_user'],password=os.environ['snowflake_password'],
        account=os.environ['snowflake_account'],database="FORGEAI_ARTICLES_V0660",schema="ARTICLES_V0660")
cs = ctx.cursor()
try:
    cs.execute("""        
            select node_distance, starting_node, ending_node,array_agg(distinct concat(nvl(ievent,''),' : ', nvl(ievents2.label,''), ' : ',nvl(topics.name,''))) as category_event_and_topic, sum(intensity) as intensity
            , round(nvl(avg(codocs.sentiment),0),3) as endnode_sentiment, round(nvl(avg(codocs.financialsentiment),0),3) as endnode_financialsentiment
            , round(nvl(avg(codocs2.sentiment),0),3) as startnode_sentiment, round(nvl(avg(codocs2.financialsentiment),0),3) as startnode_financialsentiment
            from "SCRATCH_FORGEAI"."ANDYC"."KEVINBACON" KB
            left join "PROD_V06XX"."COMPANY_DATASET_V0650"."COMPANYSENTIMENTS" codocs on codocs.uripath = ending_node and codocs.confidence >=0.6 
            left join "PROD_V06XX"."COMPANY_DATASET_V0650"."COMPANYSENTIMENTS" codocs2 on codocs2.uripath = starting_node and codocs.docid = codocs2.docid and codocs2.confidence >=0.6
            left join "PROD_V06XX"."ARTICLES_V0670"."DOCUMENTTOPICS" topics on topics.docid = codocs.docid and topics.score >= .7
            left join "DEV_V06XX"."ARTICLES_V0670"."INTRINSICEVENTS" ievents2 on ievents2.docid = codocs.docid and ievents2.confidence >=.7
            where graph = 'goldman_sachs_group_inc'
            and KB.ievent is not null
            and KB.ievent not in ('Communication', '')
            group by 1 , 2,3
           ;""")
    rows_big = cs.fetchall()
except:
    pass
finally:
    cs.close()
ctx.close()
    
data = pd.DataFrame(rows_big, columns=['NODE_DISTANCE', 'STARTING_NODE', 'ENDING_NODE', 'CATEGORY_EVENT_AND_TOPIC', 'INTENSITY', "ENODE_SENTIMENT", "ENODE_FINSENTIMENT",
                                           'STNODE_SENTIMENT','STNODE_FINSENTIMENT'])
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='material', #Add theme color to the table
    enable_enterprise_modules=False,
    height=350, 
    width='100%',
    reload_data=True
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
