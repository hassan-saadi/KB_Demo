import pandas as pd
import streamlit as st
import numpy as np

st.set_page_config(layout='wide')

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.title('Compare two companies graphs')

comp_pair = st.sidebar.selectbox("Please select a company pair:", ["(Goldman Sachs, J.P. Morgan)", 
																   "(Microsoft, Alphabet)", 
																   "(Pepsi, Coca-cola)"])
category = st.sidebar.selectbox("Please select a category:", ["All_events", 
															  "Criminal", 
															  "Cyber", 
															  "Disruption", 
															  "Investigation"])

if comp_pair == "(Goldman Sachs, J.P. Morgan)":
	filename = f"https://raw.githubusercontent.com/andychak/KB_Demo/master/data/graphs/df_goldman_jpmorgan_{category}.csv"	
elif comp_pair == "(Microsoft, Alphabet)":
	filename = f"https://raw.githubusercontent.com/andychak/KB_Demo/master/data/graphs/df_alphabet_microsoft_{category}.csv"
elif comp_pair == "(Pepsi, Coca-cola)":
	filename = f"https://raw.githubusercontent.com/andychak/KB_Demo/master/data/graphs/df_pepsi_coca_{category}.csv"

df = pd.read_csv(filename, index_col=0)
st.dataframe(df, width=2600, height=500)

st.download_button(
    label="Download data as CSV",
    data=convert_df(df),
    file_name=f"{filename}",
    mime='text/csv',
)

st.markdown(r"""Total number of features is 47.

1. number of nodes: The number of nodes in graph.

2. number of edge: The number of edges in graph.

3. weighted edges sum: The sum of edges weights in graph. If the graph is unweighted, then the weight is equal to 1.

4. average/maximum/minimum node connections: The mean, maximum, and minimum of number of edges coming inside and out of all nodes.

5. average/maximum/minimum node incoming connections: The mean, maximum, and minimum of number of edges coming inside of all nodes.

6. average/maximum/minimum node outcoming connections: The mean, maximum, and minimum of number of edges coming out of all nodes.

7. average/maximum/minimum closeness to other nodes: The mean, maximum, and minimum of closeness centrality for all nodes. Closeness centrality measures how close and central a node is to other nodes. For a given node $u$, it represents the reciprocal of the sum of the shortest path distances from $u$ to all $n-1$ other nodes, as described in the formula: 
$$
        C(u) = \frac{n-1}{\sum_{v=1}^{n-1} d(u,v)}
$$
where $d(u,v)$ is the shortest-path distance between $v$ and $u$ and $n$ is the number of nodes in the graph.

8. average/maximum/minimum node importance based on neighbors: The mean, maximum, and minimum of eigenvector centrality for all nodes. The eigenvector centrality is a measure of the influence of a node in a network. In more details, it captures the centrality for a node based on the centrality of its neighbors. This means that a node with a high score is a node that is connected to other influential nodes with high scores as well. Let A be the adjacency matrix of the graph, then $Ax = \lambda x$ where $\lambda$ is an eigenvalue, and the vth component of $x$ gives the relative centrality score of the vertex $v$ in the network.

9. average/maximum/minimum node importance based on incoming links: The mean, maximum, and minimum of pagerank centrality for all nodes. PageRank can help uncover influential or important nodes whose reach extends beyond just their direct connections. PageRank’s main difference from Eigenvector Centrality is that it accounts for link direction, i.e., Eigenvector centrality is based on the importance of a node's neighbors, while PageRank centrality is how important a node is in a network based on the number of links that point to it. Each node in a network is assigned a score based on its number of incoming links (its ‘indegree’). These links are also weighted depending on the relative score of its originating node.

10. probability of connected communities: Transitivity is the overall probability for the network to have adjacent nodes interconnected, thus revealing the existence of tightly connected communities (or clusters, subgroups, cliques). It is calculated by the ratio between the observed number of closed triplets and the maximum possible number of closed triplets in the graph.

11. density: Graph density represents the ratio between the edges present in a graph and the maximum number of edges that the graph can contain. Conceptually, it provides an idea of how dense a graph is in terms of edge connectivity. The density of a directed graph is
$$
D = \frac{|E|}{|V|(|V|-1)}
$$
where $|E|$ is the number of edges and $|V|$ is the number of vertices in the direceted graph.

12. overall_reciprocity: The reciprocity of a directed graph is defined as the ratio of the number of edges pointing in both directions to the total number of edges in the graph.

13. wiener_index: The Wiener index of a graph is the sum of the shortest-path distances between each pair of reachable nodes. If a pair of nodes is not reachable, the distance is assumed to be infinity. This means that for graphs that are not strongly-connected, this function returns inf. The Wiener index is not usually defined for directed graphs, however this function uses the natural generalization of the Wiener index to directed graphs.

14. global_efficiency_F, global_efficiency_T, local_efficiency_F, local_efficiency_T: The efficiency of a pair of nodes in a graph is the multiplicative inverse of the shortest path distance between the nodes. Edge weights are ignored when computing the shortest path distances. The average global efficiency of a graph is the average efficiency of all pairs of nodes. The local efficiency of a node in the graph is the average global efficiency of the subgraph induced by the neighbors of the node. The average local efficiency is the average of the local efficiencies of each node. The direct graph was converted to a directed graph by using two different methods; reciprocal: If True only keep edges that appear in both directions in the original digraph. Hence, we have 4 combinations made from efficiency and reciprocal value: (global, False), (global, True), (local, False), (local, True).

15. triads: https://eehh-stanford.github.io/SNA-workshop/graphs.html#dyads-triads-and-other-local-structures for an explanation of all the triad codes.

16. cycle_basis_F, cycle_basis_T: A basis for cycles of a network is a minimal collection of cycles such that any cycle in the network can be written as a sum of cycles in the basis. Here summation of cycles is defined as “exclusive or” of the edges. """)

# Footer
st.sidebar.markdown(
    """
    <h6><a href="https://fiscalnote.com/terms" target="_blank">Terms of Service</a></h6><h6><a href="https://fiscalnote.com/privacy" target="_blank">Privacy policy</a></h6>
    <h6><a href="mailto:Clinton.Stephens@fiscalnote.com">Learn More</a></h6><h6>All rights reserved. Copyright 2023 FiscalNote.</h6>
    """, unsafe_allow_html=True
    )
