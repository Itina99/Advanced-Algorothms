import Graph
import pickle
import networkx as nx
from tqdm import tqdm
import random
import numpy as np
import Diameter as dm
import minimal_vertex_coverage as mvc
import Question1 as q1


def repeat_pipeline(G):
    distribution = q1.out_degree_distribution(G)
    print("Distribuzione del grado uscente:", distribution)
    dm.pipeline(G)
    greedy_cover = mvc.greedy_vertex_cover(G)
    print("Greedy Vertex Cover:", len(greedy_cover))
    approx_cover = mvc.two_approx_vertex_cover(G)
    print("2-Approximation Vertex Cover:", len(approx_cover))
    sa_cover = mvc.simulated_annealing_vertex_cover(G)
    print("Simulated Annealing Vertex Cover:", len(sa_cover))

    



if __name__ == '__main__': 
    ids_filename = 'enwiki-2023/enwiki-2023.ids'
    arcs_filename = 'enwiki-2023/enwiki-2023.arcs'  
    #node_dict = Graph.read_ids_file(ids_filename)
    G = Graph.create_graph_from_files(ids_filename, arcs_filename)
    #repeat_pipeline(G)