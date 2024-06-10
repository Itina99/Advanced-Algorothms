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

def enumerate_minimal_vertex_covers(graph):
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
    return result

def find_minimal_vertex_cover(graph):
    covers = enumerate_minimal_vertex_covers(graph)
    min_cover = min(covers, key=len)
    return min_cover


if __name__ == "__main__":
    G,node_id, node_name = op.load_graph_with_compression()
    print("Graph Loaded")
    greedy_cover = greedy_vertex_cover(G)
    print("Greedy Vertex Cover:", len(greedy_cover))
    #covers = enumerate_minimal_vertex_covers(G)
    #for cover in covers:
        #print([G.vertex_index[v] for v in cover])
    #min_cover = find_minimal_vertex_cover(G)
    #print("Minimum Vertex Cover:", [G.vertex_index[v] for v in min_cover])

