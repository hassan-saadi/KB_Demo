import pandas as pd
import snowflake.connector as snowflake
import os
from pyvis.network import Network
import streamlit as st
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.title ('Welcome to the FiscalNote _DeepRisk360_ Demo')

ctx = snowflake.connect(user=os.environ['snowflake_user'],password=os.environ['snowflake_password'],
        account=os.environ['snowflake_account'],database="FORGEAI_ARTICLES_V0660",schema="ARTICLES_V0660")
cs = ctx.cursor()
try:
    cs.execute("""        
           select NODE_DISTANCE,STARTING_NODE,ENDING_NODE,CATEGORY_EVENT_AND_TOPIC,INTENSITY,ENDNODE_SENTIMENT
                ,ENDNODE_FINANCIALSENTIMENT,STARTNODE_SENTIMENT, STARTNODE_FINANCIALSENTIMENT
                from "SCRATCH_FORGEAI"."ANDYC"."KBDemo"
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
    fit_columns_on_grid_load=True,
    theme='material', #Add theme color to the table
    enable_enterprise_modules=False,
    height=450, 
    width='100%',
    reload_data=True
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
