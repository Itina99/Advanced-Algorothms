import graph_tool.all as gt
import gzip
import pickle
import random
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

if __name__ == "__main__":
    G,node_id, node_name = op.load_graph_with_compression()
    print("Graph Loaded")
    greedy_cover = greedy_vertex_cover(G)
    print("Greedy Vertex Cover:", len(greedy_cover))
