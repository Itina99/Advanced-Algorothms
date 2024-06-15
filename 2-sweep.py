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
    
    v1 = random.choice(list(graph.nodes()))
    v2, _ = bfs_farthest_node(graph, v1)
    v3, diameter_approx = bfs_farthest_node(graph, v2)
    
    return diameter_approx


def largest_connected_component(G):
    largest_cc = max(nx.connected_components(G), key=len)
    return G.subgraph(largest_cc).copy()

if __name__ == '__main__':
    # open graph from pickle file
    G = op.open_undirected()
    print("Graph loaded from pickle file.")
    G = largest_connected_component(G)
    print("Largest connected component found.")
    print("Calculating the approximated diameter of the largest connected component...")
    diameter_approx_cc = two_sweep_approximation(G)
    print("Approximated Diameter of Largest Connected Component:", diameter_approx_cc)