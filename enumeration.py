import gzip
import pickle
import random
import graph_tool.all as gt
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD
import openpickle as op

from copy import deepcopy


def get_random_subgraph(graph, num_vertices=100):
    vertices = list(graph.vertices())
    subgraph_vertices = random.sample(vertices, num_vertices)
    subgraph = gt.Graph(directed=False)
    vertex_map = {}
    
    for v in subgraph_vertices:
        v_new = subgraph.add_vertex()
        vertex_map[v] = v_new
    
    for v in subgraph_vertices:
        for neighbor in v.out_neighbors():
            if neighbor in vertex_map:
                subgraph.add_edge(vertex_map[v], vertex_map[neighbor])
    
    return subgraph



def kernelize_graph(G):
    G = deepcopy(G)  # Work on a copy to preserve the original graph
    
    while True:
        change = False
        
        # Remove isolated vertices
        isolated = [v for v in G.vertices() if v.out_degree() == 0]
        if isolated:
            G.remove_vertex(isolated, fast=True)
            change = True
        
        # Remove vertices with degree 1 and include their neighbors in the cover
        degree_one = [v for v in G.vertices() if v.out_degree() == 1]
        for v in degree_one:
            u = list(v.all_neighbors())[0]
            G.remove_vertex(v, fast=True)
            change = True
        
        if not change:
            break
    
    return G

def is_vertex_cover(G, cover):
    for e in G.edges():
        if e.source() not in cover and e.target() not in cover:
            return False
    return True

def is_minimal_vertex_cover(G, cover):
    if not is_vertex_cover(G, cover):
        return False
    for v in cover:
        if is_vertex_cover(G, cover - {v}):
            return False
    return True

def enumerate_minimal_vertex_covers(G, k):
    # Compute the kernel
    kernel = kernelize_graph(G)
    
    # Initialize search tree
    covers = []
    def search(remaining_edges, current_cover):
        if len(current_cover) > k:
            return
        
        if not remaining_edges:
            if is_minimal_vertex_cover(G, current_cover):
                covers.append(current_cover)
            return
        
        # Pick the next edge to branch
        e = remaining_edges.pop()
        u, v = e
        
        # Branch: Include u in the cover
        search(remaining_edges[:], current_cover | {u})
        
        # Branch: Include v in the cover
        search(remaining_edges[:], current_cover | {v})
    
    # Start search with all edges
    search(list(kernel.edges()), set())
    return covers

# Example usage
if __name__ == "__main__":
    G, node_id, node_name = op.load_graph_with_compression()
    G = get_random_subgraph(G)
    
    print("Enumerating all minimal vertex covers...")
    #solutions = enumerate_minimal_vertex_covers(G)
    #print(f"Found {len(solutions)} solutions.")
    
    #min_vertex_cover = find_extreme_solution(solutions, find_minimum=True)
    
    covers = enumerate_minimal_vertex_covers(G,  101)
    print(f"Found {len(covers)} minimal vertex covers.")
    

    #print(f"Minimal Vertex Cover with minimum length: {min_vertex_cover} with length {sum(min_vertex_cover)}")


############################################################################################################################################
