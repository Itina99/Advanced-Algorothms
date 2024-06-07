import networkx as nx
import matplotlib.pyplot as plt
import openpickle as op
import random
import numpy as np
from tqdm import tqdm

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


if __name__ == "__main__":
    G = op.open_pickle()
    greedy_cover = greedy_vertex_cover(G)
    print("Greedy Vertex Cover:", len(greedy_cover))
