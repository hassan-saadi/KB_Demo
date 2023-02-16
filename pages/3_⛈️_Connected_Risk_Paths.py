import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Load the data from the specified URL
url = 'https://raw.githubusercontent.com/andychak/KB_Demo/master/EVENTS.csv'
st.set_page_config(page_title='CQ RiskConnector', layout="wide")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/0/05/CQ_Logo.jpeg', width=40)
st.sidebar.caption("Improving Your :blue[C]hange :blue[Q]uotient")
# st.sidebar.image('https://fiscalnote-marketing.s3.amazonaws.com/logo-FN-white-red.png')
st.title('CQ RiskConnector Limited Data Sample')
st.markdown('Use this tool to understand the path of connected events. How much of the network do they touch? Forecast and display scenarios similar to tracking paths of a storm.')
data = pd.read_csv(url).fillna('')
data = data.query("STARTING_NODE != ENDING_NODE")
#data = data.query("CLASS != '9/11 ATTACK'")
#data = data[data['CLASS'].isin(['ACCOUNTING FRAUD', 'BANK FRAUD', 'CORPORATE MISCONDUCT', 'HACK', 'HACKING', 
#                                'CIVIL LAWSUIT', 'ANTI-TRUST VIOLATION', 'CLINICAL TRIAL', 'WIRE FRAUD', 'RANSOMWARE ATTACK',
#                                'LEGAL DISPUTE', 'MULTIDISTRICT LITIGATION', 'CYBER BREACH', 'CLASS-ACTION LAWSUIT',
#                                'PRIVACY BREACH', 'CRIMINAL INVESTIGATION', 'DDOS ATTACK', 'REGULATORY INVESTIGATION'])]
# Define the available graphs for the dropdown
graphs = sorted(data['GRAPH'].unique())
st.sidebar.caption('Track Connected Events Across Firms')
# Allow the user to select a graph using a dropdown
selected_graph = st.sidebar.selectbox('Select a company:', graphs, index=2)

# Filter the data based on the selected graph
filtered_data = data[data['GRAPH'] == selected_graph]

# Define the available events for the drop down filter
events = sorted(filtered_data['CLASS'].unique())

# Allow the user to select an event using a drop down filter
selected_event = st.sidebar.selectbox('Select an event class:', events, index=1)

# Filter the data based on the selected event
filtered_data = filtered_data[filtered_data['CLASS'] == selected_event]

links = {
    'source': [filtered_data['STARTING_NODE'].tolist().index(s) for s in filtered_data['STARTING_NODE']],
    'target': [filtered_data['ENDING_NODE'].tolist().index(e) for e in filtered_data['ENDING_NODE']],
    'value': filtered_data['DOCCOUNT'].tolist(),
}

# Use a list comprehension to remove the links where source is equal to target
links = [link for link in zip(links['source'], links['target'], links['value']) if link[0] != link[1]]

# Convert the filtered links back into a dictionary
links = {'source': [link[0] for link in links], 'target': [link[1] for link in links], 'value': [link[2] for link in links]}


sankey_data = go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = sorted(set(filtered_data['STARTING_NODE'].tolist() + filtered_data['ENDING_NODE'].tolist())),
        color = ["blue", "green", "purple", "orange", "red", "yellow"]
    ),
    link=links
)

# Define the layout for the Sankey diagram
sankey_layout = go.Layout(
    title = 'Flow for {} and for Events of Class {}'.format(selected_graph, selected_event),
    font = dict(size = 10)
)

# Create the figure
fig = go.Figure(data=[sankey_data], layout=sankey_layout)

# Display the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)
# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6><h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6><a href="mailto:Clinton.Stephens@fiscalnote.com">Learn More</a></h6><h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
)
