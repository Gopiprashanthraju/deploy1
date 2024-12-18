import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, RDF, OWL, URIRef
import pandas as pd

# Initialize Ontology and Namespace
g = Graph()
CYBERSEC = Namespace("http://example.org/cybersecurity#")
g.bind("cybersec", CYBERSEC)

# Define Classes and Property
g.add((CYBERSEC.Asset, RDF.type, OWL.Class))
g.add((CYBERSEC.Threat, RDF.type, OWL.Class))
g.add((CYBERSEC.Vulnerability, RDF.type, OWL.Class))
g.add((CYBERSEC.exploitedBy, RDF.type, OWL.ObjectProperty))

# Add Instances
asset = URIRef(CYBERSEC.Server)
vulnerability = URIRef(CYBERSEC.SQLInjection)
threat = URIRef(CYBERSEC.HackerAttack)

# Add Relationships
g.add((asset, RDF.type, CYBERSEC.Asset))
g.add((vulnerability, RDF.type, CYBERSEC.Vulnerability))
g.add((threat, RDF.type, CYBERSEC.Threat))
g.add((vulnerability, CYBERSEC.exploitedBy, threat))
g.add((asset, CYBERSEC.exploitedBy, vulnerability))

# Query Results
results = []
for s, p, o in g.triples((None, CYBERSEC.exploitedBy, None)):
    results.append((s.split("#")[-1], o.split("#")[-1]))

# Convert results to DataFrame
df = pd.DataFrame(results, columns=["Subject", "Exploited By"])

# Streamlit App
st.title("Cybersecurity Ontology Visualization")

# Display Ontology Data
st.header("Ontology Relationships")
st.write(df)

# Visualize Ontology as a Graph
st.header("Ontology Graph Visualization")

# Create NetworkX Graph
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row["Subject"], row["Exploited By"], label="exploitedBy")

# Draw the graph
fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, font_size=12, font_weight="bold", ax=ax)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)}, ax=ax)

st.pyplot(fig)
