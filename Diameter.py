import openpickle as op
import networkx as nx
from tqdm import tqdm
from collections import deque

# transform a directed graph into an undirected graph
def undirected(G): 
    U = nx.Graph()
    for u, v in tqdm(G.edges(), desc="Making Graph Undirected"):
        U.add_edge(u, v)
    return U

# find the largest connected component in a graph
def largest_connected_component(G):
    largest_cc = max(nx.connected_components(G), key=len)
    return G.subgraph(largest_cc).copy()

# find the starting node for the diameter calculation
def starting_node(G):
    max_deg = 0
    max_deg_node = None
    for node in G.nodes():
        if max_deg < G.degree(node):
            max_deg = G.degree(node)
            max_deg_node = node
    return max_deg_node

def get_fringe(G, start_node, i):

    visited = set()
    current_level_nodes = set()

    queue = deque([(start_node, 0)])

    while queue:
        node, level = queue.popleft()

        if level == i:
            current_level_nodes.add(node)

        if node not in visited:
            visited.add(node)
            neighbors = G.neighbors(node)

            for neighbor in neighbors:
                if neighbor not in visited and level < i:
                    queue.append((neighbor, level + 1))

    return current_level_nodes

def eccentricity(G, start_node):
    eccentricity = 0
    visited = set()
    queue = deque([(start_node, 0)])
    total_nodes = len(G)  # Total number of nodes in the graph
    progress = tqdm(total=total_nodes, desc="Processing Nodes", unit="node")
    
    while queue:
        node, level = queue.popleft()
        if node not in visited:
            visited.add(node)
            eccentricity = max(eccentricity, level)
            progress.update(1)  # Update progress bar
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))
    
    progress.close()  # Close the progress bar
    return eccentricity

def Bi(G, start_node, i):# da sistemare con la roba della fringe
    max_ecc = -1
    fringe = get_fringe(G, start_node, i)

    progress_bar = tqdm(total=len(fringe), desc="Processing nodes")

    for node in fringe:
        e = eccentricity(G, node)  # eccentricity viene calcolata facendo una bfs
        if e > max_ecc:
            max_ecc = e

        progress_bar.update(1)

    progress_bar.close()

    return max_ecc

# calculate the diameter of a graph
def diameter(G, start_node):
    i = eccentricity(G, start_node)
    lb = i
    ub = 2 * i
    iterations = i  # Total number of iterations
    progress = tqdm(total=iterations, desc="Computing Diameter", unit="step")
    
    while ub > lb:
        bi = Bi(G, start_node, i)
        if max(lb, bi) > 2 * (i - 1):
            progress.close()
            return max(lb, bi)
        else:
            lb = max(lb, bi)
            ub = 2 * (i - 1)
        i = i - 1
        progress.update(1)  # Update progress bar
    
    progress.close()
    return lb


def pipeline(G):
    print("Making graph undirected")
    U = undirected(G)
    print("Finding largest connected component")
    LCC = largest_connected_component(U)
    print("Finding starting node")
    start_node = starting_node(LCC)
    print("Calculating diameter")
    diam = diameter(LCC, start_node)
    print(f"Diameter: {diam}")



if __name__ == "__main__":
    loaded_graph = op.open_pickle()
    pipeline(loaded_graph)
