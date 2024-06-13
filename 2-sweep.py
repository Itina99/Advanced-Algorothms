import random
import networkx as nx
from tqdm import tqdm
from collections import deque
import pickle
import openpickle as op

def bfs_farthest_node(graph, start):
    """ Perform BFS and return the farthest node and its distance from the start node. """
    visited = set([start])
    queue = deque([(start, 0)])  # (node, distance)
    farthest_node = start
    max_distance = 0
    
    while queue:
        node, distance = queue.popleft()
        
        if distance > max_distance:
            max_distance = distance
            farthest_node = node
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return farthest_node, max_distance


def two_sweep_approximation(graph):
    # Step 1: Convert the graph to an undirected graph if it is directed
    if graph.is_directed():
        graph = graph.to_undirected()
    
    # Step 2: Choose an arbitrary starting vertex v1 in the graph

    # Randomly choose a vertex as v1
    v1 = random.choice(list(graph.nodes()))

    # Step 3: Perform BFS from v1 to find v2
    v2, _ = bfs_farthest_node(graph, v1)
    
    # Step 4: Perform BFS from v2 to find the farthest vertex v3
    v3, diameter_approx = bfs_farthest_node(graph, v2)
    
    return diameter_approx

def undirected(G): 
    U = nx.Graph()
    for u, v in tqdm(G.edges(), desc="Making Graph Undirected"):
        U.add_edge(u, v)
    return U

def largest_connected_component(G):
    largest_cc = max(nx.connected_components(G), key=len)
    return G.subgraph(largest_cc).copy()

if __name__ == '__main__':
    # open graph from pickle file
    filename = 'itwiki-2013/itwiki13.pickle'
    print("Loading graph from pickle file...")
    G = op.open_pickle(filename)
    print("Graph loaded from pickle file.")
    print("making graph undirected...")
    U = undirected(G)
    print("Finding the largest connected component...")
    largest_cc = largest_connected_component(U)
    print("Largest connected component found.")
    print("Calculating the approximated diameter of the largest connected component...")
    diameter_approx_cc = two_sweep_approximation(largest_cc)
    print("Approximated Diameter of Largest Connected Component:", diameter_approx_cc)