import networkx as nx
import random

# Step 1: Construct a random graph
def create_random_graph(num_nodes, num_edges):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    while len(G.edges) < num_edges:
        u, v = random.sample(list(G.nodes()), 2)  # Convert G.nodes() to a list
        G.add_edge(u, v)
    return G


def is_vertex_cover(G, cover):
    return all(u in cover or v in cover for u, v in G.edges)

def find_minimal_vertex_covers(G):
    nodes = list(G.nodes)
    covers = []
    
    def backtrack(cover, index):
        if index == len(nodes):
            if is_vertex_cover(G, cover):
                covers.append(cover[:])
            return
        
        cover.append(nodes[index])
        backtrack(cover, index + 1)
        cover.pop()
        
        if not any(v in cover for u, v in G.edges(nodes[index])):
            backtrack(cover, index + 1)
    
    backtrack([], 0)
    return covers

# Step 3: Print and select the minimum vertex cover
def main():
    num_nodes = 30
    num_edges = 60
    G = create_random_graph(num_nodes, num_edges)
    
    minimal_vertex_covers = find_minimal_vertex_covers(G)
    for cover in minimal_vertex_covers:
        print(f"Minimal Vertex Cover: {cover}")
    
    min_cover = min(minimal_vertex_covers, key=len)
    print(f"Minimum Vertex Cover: {min_cover} with size {len(min_cover)}")

if __name__ == "__main__":
    main()

