import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Težine
W1 = np.array([[0.2, 0.4, -0.5], [-0.3, 0.1, 0.2], [0.7, -0.1, -0.4]])
W2 = np.array([[0.1, -0.2, 0.3], [0.4, 0.6, -0.1]])  # Adjusted dimensions
W3 = np.array([0.3, -0.7])

# Creating a directed graph
G = nx.DiGraph()

# Add nodes for each layer
G.add_nodes_from(['Input', 'Hidden Layer 1', 'Hidden Layer 2', 'Output'])

# Add edges between nodes
for i in range(W1.shape[0]):
    for j in range(W1.shape[1]):
        G.add_edge('Input', f'H1_{j+1}', weight=W1[i][j])

for i in range(W2.shape[0]):
    for j in range(W2.shape[1]):
        G.add_edge(f'H1_{i+1}', f'H2_{j+1}', weight=W2[i][j])

for i in range(W3.shape[0]):
    G.add_edge(f'H2_{i+1}', 'Output', weight=W3[i])

# Draw the graph
pos = nx.spring_layout(G)  # Positions of nodes
labels = nx.get_edge_attributes(G, 'weight')  # Get weights for edges

plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Neural Network Architecture")
plt.show()
