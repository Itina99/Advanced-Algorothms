import graph_tool.all as gt
from tqdm import tqdm
from collections import deque
import gzip
import pickle

# Transform a directed graph into an undirected graph
def undirected(G):
    U = gt.Graph(directed=False)
    U.add_edge_list(G.edges())
    return U

# Find the largest connected component in a graph
def largest_connected_component(G):
    comp, hist = gt.label_components(G)
    largest_comp = comp.a.argmax()
    return gt.GraphView(G, vfilt=comp.a == largest_comp).copy()

# Find the starting node for the diameter calculation
def starting_node(G):
    degrees = G.get_out_degrees(G.get_vertices())
    max_deg_node = G.vertex(degrees.argmax())
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
            neighbors = node.out_neighbours()
            for neighbor in neighbors:
                if neighbor not in visited and level < i:
                    queue.append((neighbor, level + 1))
    return current_level_nodes

def eccentricity(G, start_node):
    eccentricity = 0
    visited = set()
    queue = deque([(start_node, 0)])
    total_nodes = G.num_vertices()
    progress = tqdm(total=total_nodes, desc="Processing Nodes", unit="node")

    while queue:
        node, level = queue.popleft()
        if node not in visited:
            visited.add(node)
            eccentricity = max(eccentricity, level)
            progress.update(1)
            neighbors = node.out_neighbours()
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))

    progress.close()
    return eccentricity

def Bi(G, start_node, i):
    max_ecc = -1
    fringe = get_fringe(G, start_node, i)
    progress_bar = tqdm(total=len(fringe), desc="Processing nodes")

    for node in fringe:
        e = eccentricity(G, node)
        if e > max_ecc:
            max_ecc = e
        progress_bar.update(1)

    progress_bar.close()
    return max_ecc

# Calculate the diameter of a graph
def diameter(G, start_node):
    i = eccentricity(G, start_node)
    lb = i
    ub = 2 * i
    iterations = i
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
        progress.update(1)

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
    filename = 'enwiki-2023/enwiki-2023.graph.pkl.gz'
    with gzip.open(filename, 'rb') as f:
        loaded_graph, node_id, node_name = pickle.load(f)
    pipeline(loaded_graph)
