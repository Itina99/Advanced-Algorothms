import random
import graph_tool.all as gt
from tqdm import tqdm
from collections import deque
import pickle
import openpickle as op

def bfs_farthest_node(graph, start):
    """ Perform BFS using graph-tool and return the farthest node and its distance from the start node. """
    visited = set([start])
    queue = deque([(start, 0)])  # (node, distance)
    farthest_node = start
    max_distance = 0
    
    while queue:
        node, distance = queue.popleft()
        
        if distance > max_distance:
            max_distance = distance
            farthest_node = node
        
        for neighbor in node.out_neighbours():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    
    return farthest_node, max_distance

def two_sweep_approximation(graph):
    # Randomly choose a vertex as v1
    v1 = random.choice(list(graph.vertices()))

    # Perform BFS from v1 to find v2
    v2, _ = bfs_farthest_node(graph, v1)
    
    # Perform BFS from v2 to find the farthest vertex v3
    v3, diameter_approx = bfs_farthest_node(graph, v2)
    
    return diameter_approx

def largest_connected_component(G):
    def bfs_component_size(start_vertex, progress):
        visited = set()
        queue = deque([start_vertex])
        size = 0
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                size += 1
                progress.update(1)
                for neighbor in vertex.out_neighbours():
                    if neighbor not in visited:
                        queue.append(neighbor)
        return visited, size
    
    visited_overall = set()
    largest_component = set()
    
    progress = tqdm(total=G.num_vertices(), desc="Finding Largest Connected Component", unit="vertex")
    
    for vertex in G.vertices():
        if vertex not in visited_overall:
            component, size = bfs_component_size(vertex, progress)
            visited_overall.update(component)
            if size > len(largest_component):
                largest_component = component
    
    progress.close()

    vfilt = G.new_vertex_property("bool")
    for v in largest_component:
        vfilt[v] = True

    largest_cc = gt.GraphView(G, vfilt=vfilt)
    
    # Save the largest connected component to a pickle file
    with open('enwiki-2023/largest_cc.pickle', 'wb') as f:
        pickle.dump(largest_cc, f)
    
    return largest_cc

if __name__ == '__main__':
    # Check if the largest connected component is already saved
    largest_cc = op.open_lcc()
    if largest_cc is None:
        # Open graph from pickle file
        G, node_id, node_name = op.load_undirected_graph_with_compression()
        print("Graph loaded from pickle file.")
        print("Calculating the largest connected component...")
        largest_cc = largest_connected_component(G)
        print("Largest connected component found and saved to pickle file.")
    else:
        print("Largest connected component loaded from pickle file.")
    
    print("Calculating the approximated diameter of the largest connected component...")
    diameter_approx_cc = two_sweep_approximation(largest_cc)
    print("Approximated Diameter of Largest Connected Component:", diameter_approx_cc)
