import pickle
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import gzip
import os   



def open_pickle(filename = "itwiki-2013/itwiki13.pickle"):
    print("Opening graph...")
    with open(filename, 'rb') as f:
        loaded_graph = pickle.load(f)
    return loaded_graph

def load_graph_with_compression(filename = 'enwiki-2023/enwiki-2023.graph.pkl.gz'):
    print("Loading graph from pickle file...")
    with gzip.open(filename, 'rb') as f:
        graph, node_id, node_name = pickle.load(f)
    return graph, node_id, node_name

def open_undirected(filename = "itwiki-2013/itwiki13_undirected.pickle"):
    print("Opening undirected graph...")
    with open(filename, 'rb') as f:
        loaded_graph = pickle.load(f)   
    return loaded_graph

def load_undirected_graph_with_compression(filename = 'enwiki-2023/enwiki-2023_undirected.graph.pkl.gz'):
    print("Loading undirected graph from pickle file...")
    with gzip.open(filename, 'rb') as f:
        graph, node_id, node_name = pickle.load(f)
    return graph, node_id, node_name

def open_lcc(filename = "enwiki-2023/largest_cc.pickle"):
    print("Opening largest connected component...")
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            largest_cc = pickle.load(f)
        return largest_cc
    else:
        return None