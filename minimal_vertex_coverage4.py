import graph_tool.all as gt
from tqdm import tqdm
import openpickle as op
import pulp


def is_vertex_cover(graph, cover):
    for e in graph.edges():
        u, v = int(e.source()), int(e.target())
        if u not in cover and v not in cover:
            return False
    return True

def greedy_vertex_cover(graph):
    cover = set()
    uncovered_edges = set((int(e.source()), int(e.target())) for e in graph.edges())
    
    with tqdm(total=len(uncovered_edges), desc="Greedy Vertex Cover") as pbar:
        while uncovered_edges:
            u, v = uncovered_edges.pop()
            cover.add(u)
            cover.add(v)
            incident_edges = list((int(e.source()), int(e.target())) for e in graph.edges([u, v]))
            for e in incident_edges:
                if e in uncovered_edges:
                    uncovered_edges.remove(e)
                    pbar.update(1)
    
    return cover

################################################# TEST SECONDO ALGORITMO #################################################


def minimal_vertex_cover_ilp(graph):
    print("Formulating ILP...")
    # Initialize ILP problem
    prob = pulp.LpProblem("MinimalVertexCover", pulp.LpMinimize)

    # Create a binary variable for each vertex
    vertex_vars = {v: pulp.LpVariable(f"v_{v}", cat='Binary') for v in graph.vertices()}

    # Objective: Minimize the sum of the vertex variables
    prob += pulp.lpSum(vertex_vars[v] for v in graph.vertices()), "TotalVertices"

    # Constraint: For each edge, at least one of its endpoints must be in the vertex cover
    for e in graph.edges():
        v1, v2 = int(e.source()), int(e.target())
        prob += vertex_vars[graph.vertex(v1)] + vertex_vars[graph.vertex(v2)] >= 1, f"Edge_{v1}_{v2}"

    print("Solving ILP...")
    # Solve the ILP problem
    prob.solve()

    # Extract the solution
    vertex_cover = [v for v in graph.vertices() if pulp.value(vertex_vars[v]) == 1]

    return vertex_cover

################################################################################################



if __name__ == "__main__":
    G,node_id, node_name = op.load_graph_with_compression()
    print("Graph Loaded")
    #greedy_cover = greedy_vertex_cover(G)
    #print("Greedy Vertex Cover:", len(greedy_cover))

    ##################################################
    #TODO: per lollo come prima fai girare entrambi i metodi e confronta i risultati
    #probabilmente il greedy farà schifo e non so quanto tempo ci metterà. L'altro dovrebbe essere molto più veloce
    #ma potrebbe riempire la memoria. 
    ####################################################

    vertex_cover = minimal_vertex_cover_ilp(G)
    print(f"Vertex Cover Size: {len(vertex_cover)}")

    #covers = enumerate_minimal_vertex_covers(G)
    #for cover in covers:
        #print([G.vertex_index[v] for v in cover])
    #min_cover = find_minimal_vertex_cover(G)
    #print("Minimum Vertex Cover:", [G.vertex_index[v] for v in min_cover])

