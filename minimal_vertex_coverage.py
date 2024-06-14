import networkx as nx
import matplotlib.pyplot as plt
import openpickle as op
import random
import numpy as np
from tqdm import tqdm
import pulp

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
def minimal_vertex_cover_ilp(graph):
    print("Formulating ILP...")
    # Initialize ILP problem
    prob = pulp.LpProblem("MinimalVertexCover", pulp.LpMinimize)

    # Create a binary variable for each vertex
    vertex_vars = {v: pulp.LpVariable(f"v_{v}", cat='Binary') for v in graph.nodes()}

    # Objective: Minimize the sum of the vertex variables
    prob += pulp.lpSum(vertex_vars[v] for v in graph.nodes()), "TotalVertices"

    # Constraint: For each edge, at least one of its endpoints must be in the vertex cover
    for u, v in graph.edges():
        prob += vertex_vars[u] + vertex_vars[v] >= 1, f"Edge_{u}_{v}"

    print("Solving ILP...")
    # Solve the ILP problem
    prob.solve()

    # Extract the solution
    vertex_cover = [v for v in graph.nodes() if pulp.value(vertex_vars[v]) == 1]

    return vertex_cover




if __name__ == "__main__":
    G = op.open_pickle()
    #vertex_cover = minimal_vertex_cover_ilp(G)
    #print(f"Vertex Cover Size: {len(vertex_cover)}")
    ##############################################################
    #TODO: Per lollo, esegui entrambi gli algoritmi separatamente e confronta i risultati
    ##############################################################
    
    greedy_cover = greedy_vertex_cover(G)
    print("Greedy Vertex Cover:", len(greedy_cover))
