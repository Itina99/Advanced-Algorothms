import networkx as nx
import matplotlib.pyplot as plt
import random

def out_degree_distribution(G): #al posto di questo ci andrà il caricamento del file 
    # Calcola i gradi uscenti di tutti i nodi
    out_degrees = [d for n, d in G.out_degree()]

    # Calcola la distribuzione del grado uscente
    out_degree_count = {}
    for degree in out_degrees:
        if degree in out_degree_count:
            out_degree_count[degree] += 1
        else:
            out_degree_count[degree] = 1

    # Normalizza per ottenere la distribuzione di probabilità
    num_nodes = G.number_of_nodes()
    out_degree_distribution = {k: v / num_nodes for k, v in out_degree_count.items()}

    return out_degree_distribution

# Creazione di un grafo diretto di esempio con almeno 15 nodi e vari archi
G = nx.DiGraph()
edges = [
    (0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (1, 5), (2, 3), (2, 6),
    (3, 4), (3, 7), (4, 5), (4, 8), (5, 6), (5, 9), (6, 7), (6, 10),
    (7, 8), (7, 11), (8, 9), (8, 12), (9, 10), (9, 13), (10, 11),
    (10, 14), (11, 12), (12, 13), (13, 14), (14, 0), (14, 1), (13, 0),
    (12, 1), (11, 2), (10, 3), (9, 4), (8, 5), (7, 6), (6, 7), (5, 8),
    (4, 9), (3, 10), (2, 11), (1, 12), (0, 13), (0, 14), (1, 13)
]

# Aggiunta di archi per maggiore varietà nei gradi uscenti
# fa un ciclo su tutti i nodi e aggiunge un numero casuale di archi
additional_edges = [(i, random.choice(range(15))) for i in range(15) for _ in range(random.randint(0, 5))]
edges.extend(additional_edges)

G.add_edges_from(edges)

# Plot del grafo
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10, font_color='black')
plt.show()

# Calcolo della distribuzione del grado uscente
distribution = out_degree_distribution(G)
print("Distribuzione del grado uscente:", distribution)

# Visualizzazione della distribuzione del grado uscente
plt.figure(figsize=(10, 6))
plt.bar(distribution.keys(), distribution.values(), width=0.5, color='b', align='center')
plt.xlabel('Grado Uscente')
plt.ylabel('Frazione di Nodi')
plt.title('Distribuzione del Grado Uscente')
plt.show()

# Identifica i top 10 nodi con il grado uscente più alto
top_out_degree_nodes = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodi con il grado uscente più alto:", top_out_degree_nodes)

# Evidenzia i top 10 nodi nel grafico del grafo
node_colors = ['red' if node in [n for n, d in top_out_degree_nodes] else 'blue' for node in G.nodes()]
plt.figure(figsize=(10, 7))
nx.draw(G, with_labels=True, node_color=node_colors, edge_color='gray', node_size=500, font_size=10, font_color='black')
plt.show()
