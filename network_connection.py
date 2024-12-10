import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.patches import FancyArrowPatch
import matplotlib.colors as mcolors

# Streamlit app title
st.title("Improved Co-Funding Sponsors Network")

# Load dataset
uploaded_file = st.file_uploader("co_funding_sponsors_network_all.csv", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Initialize a graph
    G = nx.Graph()

    # Add edges from the dataset
    for _, row in df.iterrows():
        G.add_edge(row['Sponsor 1'], row['Sponsor 2'])

    # Use spring layout with more spacing
    pos = nx.spring_layout(G, seed=42, k=0.4, scale=2)  # Adjust k and scale for readability

    # Calculate node degrees and scale sizes
    degree_dict = dict(G.degree())
    node_sizes = [v * 50 for v in degree_dict.values()]  # Scale node sizes by degree

    # Color nodes by degree
    norm = mcolors.Normalize(vmin=min(degree_dict.values()), vmax=max(degree_dict.values()))
    cmap = plt.cm.plasma  # Choose a colormap
    node_colors = [cmap(norm(degree_dict[node])) for node in G.nodes]

    # Draw the network graph
    fig, ax = plt.subplots(figsize=(20, 15))  # Larger figure size for better readability

    # Draw nodes
    node_collection = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=cmap, ax=ax)

    # Draw curved edges
    for u, v in G.edges():
        path = FancyArrowPatch(
            posA=pos[u],
            posB=pos[v],
            connectionstyle="arc3,rad=0.2",  # Adjust curvature with 'rad'
            color='gray',
            alpha=0.5,
            linewidth=0.8
        )
        ax.add_patch(path)

    # Limit displayed labels to high-degree nodes
    min_degree = st.slider("Minimum degree for labels", min_value=1, max_value=max(degree_dict.values()), value=10)
    labels = {node: node for node, degree in degree_dict.items() if degree >= min_degree}

    # Draw labels
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='black', font_weight='bold', ax=ax)

    # Add a colorbar linked to the node colors
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    # cbar = plt.colorbar(sm, shrink=0.8)
    # cbar.set_label("Node Degree", fontsize=12)

    # Add title and show the graph
    ax.set_title("Co-Funding Sponsors Network", fontsize=18)
    ax.axis("off")

    # Display the graph in Streamlit
    st.pyplot(fig)
