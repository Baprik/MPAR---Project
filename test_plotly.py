import matplotlib.pyplot as plt
import networkx as nx

# Création du graphe
G = nx.Graph()

# Ajout des nœuds
G.add_nodes_from(['A', 'B', 'C'])

# Ajout des arêtes
G.add_edge('A', 'B')
G.add_edge('B', 'C')

# Positionnement des nœuds
pos = {'A': (0, 1), 'B': (1, 0), 'C': (2, 1)}

# Tracé du graphe
nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=20, font_color='black', font_weight='bold')
plt.title("Graphe avec 3 nœuds et des liens")
plt.show()
