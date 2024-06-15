import networkx as nx
import itertools
import random

def is_vertex_cover(G, cover):
    for u, v in G.edges():
        if u not in cover and v not in cover:
            return False
    return True

def minimal_vertex_cover(G):
    nodes = list(G.nodes())
    for r in range(1, len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            if is_vertex_cover(G, subset):
                return set(subset)
    return set()

# Create a smaller graph with 20 nodes and 50 edges
num_nodes = 20
num_edges = 50
G = nx.Graph()

# Add 20 nodes to the graph
G.add_nodes_from(range(1, num_nodes + 1))

# Add 50 edges randomly
while len(G.edges) < num_edges:
    u, v = random.sample(list(G.nodes), 2)  # Convert G.nodes to a list
    if not G.has_edge(u, v):
        G.add_edge(u, v)

# Apply the exact algorithm to find the minimal vertex cover
vertex_cover = minimal_vertex_cover(G)
print("Minimal Vertex Cover:", vertex_cover)
print("Number of vertices in the minimal cover:", len(vertex_cover))


