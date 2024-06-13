import networkx as nx
import matplotlib.pyplot as plt
import openpickle as op
import random
import numpy as np
from tqdm import tqdm
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD

def is_vertex_cover(graph, cover):
    for u, v in graph.edges():
        if u not in cover and v not in cover:
            return False
    return True


def greedy_vertex_cover(graph):
    cover = set()
    uncovered_edges = set(graph.edges())
    
    with tqdm(total=len(uncovered_edges), desc="Greedy Vertex Cover") as pbar:
        while uncovered_edges:
            u, v = uncovered_edges.pop()
            cover.add(u)
            cover.add(v)
            incident_edges = list(graph.edges([u, v]))
            for e in incident_edges:
                if e in uncovered_edges:
                    uncovered_edges.remove(e)
                    pbar.update(1)
    return cover



#################################### SECONDO TEST ####################################
def preprocess_graph(graph):
    """Preprocess the graph by removing isolated vertices and applying reduction rules."""
    # Remove isolated vertices
    graph.remove_nodes_from(list(nx.isolates(graph)))
    # Additional reduction rules can be added here
    return graph

def minimal_vertex_cover_ilp(graph):
    # Preprocess the graph to reduce its size
    print("Preprocessing the graph...")
    graph = preprocess_graph(graph)
    
    # Create an ILP problem
    prob = LpProblem("Minimal_Vertex_Cover", LpMinimize)
    
    # Create a binary variable for each vertex in the graph
    x = LpVariable.dicts("x", graph.nodes(), 0, 1, LpBinary)
    
    # Objective function: Minimize the sum of all vertex variables
    prob += lpSum(x[v] for v in graph.nodes())
    
    # Constraints: For each edge, at least one of its vertices must be in the cover
    edges = list(graph.edges())
    for u, v in tqdm(edges, desc="Adding constraints"):
        prob += x[u] + x[v] >= 1
    
    # Solve the problem with a progress bar
    print("Solving the ILP problem...")
    prob.solve(PULP_CBC_CMD(msg=1))  # msg=1 enables verbose solver output
    
    # Extract the vertex cover
    vertex_cover = [v for v in graph.nodes() if x[v].varValue == 1]
    return vertex_cover


if __name__ == "__main__":
    G = op.open_pickle()
    vertex_cover = minimal_vertex_cover_ilp(G)
    print(f"Vertex Cover Size: {len(vertex_cover)}")
    ##############################################################
    #TODO: Per lollo, esegui entrambi gli algoritmi separatamente e confronta i risultati
    ##############################################################
    
    #greedy_cover = greedy_vertex_cover(G)
    #print("Greedy Vertex Cover:", len(greedy_cover))
