import graph_tool.all as gt
from tqdm import tqdm
import openpickle as op


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


def preprocess_graph(graph):
    """Preprocess the graph by removing isolated vertices."""
    # Convert to graph-tool graph
    g = gt.Graph(directed=False)
    vprop_id = g.new_vertex_property("int")
    vertex_map = {}  # Map node_id to graph-tool vertex descriptor
    for node, idx in graph.items():
        v = g.add_vertex()
        vertex_map[node] = v
        vprop_id[v] = idx
    
    # Add edges
    for node, neighbors in tqdm(graph.items(), desc="Adding edges"):
        for neighbor in neighbors:
            g.add_edge(vertex_map[node], vertex_map[neighbor])
    
    # Remove isolated vertices
    gt.remove_isolated_vertices(g)
    
    return g

def minimal_vertex_cover(graph):
    # Preprocess the graph to reduce its size
    graph = preprocess_graph(graph)
    
    # Create a property map for vertex cover
    vc = graph.new_vertex_property("bool")
    vc.a = False  # Initialize all vertices as not in the cover
    
    # Get the number of edges for tqdm progress bar
    total_edges = graph.num_edges()
    
    # Adding constraints to the vertex cover problem
    for edge in tqdm(graph.edges(), desc="Adding constraints", total=total_edges):
        u, v = edge.source(), edge.target()
        vc[u] = True
        vc[v] = True
    
    # Solve the problem (in this case, just use the constructed vertex cover)
    vertex_cover = [v for v in graph.vertices() if vc[v]]
    return vertex_cover

################################################################################################


""" def enumerate_minimal_vertex_covers(graph):
    def is_vertex_cover(cover, graph):
        for e in graph.edges():
            if e.source() not in cover and e.target() not in cover:
                return False
        return True

    def is_minimal(cover, graph):
        for v in list(cover):
            new_cover = set(cover)
            new_cover.remove(v)
            if is_vertex_cover(new_cover, graph):
                return False
        return True

    def search(current_cover, remaining_vertices):
        if is_vertex_cover(current_cover, graph):
            if is_minimal(current_cover, graph):
                result.append(current_cover)
            return

        for vertex in list(remaining_vertices):
            new_cover = set(current_cover)
            new_cover.add(vertex)
            new_remaining = set(remaining_vertices)
            new_remaining.remove(vertex)
            search(new_cover, new_remaining)

    result = []
    search(set(), set(graph.vertices()))
    return result """


""" def find_minimal_vertex_cover(graph, num_nodes=100):
    nodes_to_consider = set(graph.get_vertices()[:num_nodes])
    covers = enumerate_minimal_vertex_covers(graph, nodes_to_consider)
    min_cover = min(covers, key=len)
    return min_cover
 """

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

    vertex_cover = minimal_vertex_cover(G)
    print(f"Vertex Cover Size: {len(vertex_cover)}")

    #covers = enumerate_minimal_vertex_covers(G)
    #for cover in covers:
        #print([G.vertex_index[v] for v in cover])
    #min_cover = find_minimal_vertex_cover(G)
    #print("Minimum Vertex Cover:", [G.vertex_index[v] for v in min_cover])

