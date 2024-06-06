import Graph
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import gzip



def open_pickle(filename = "itwiki-2013/itwiki13.pickle"):
    
    with open(filename, 'rb') as f:
        loaded_graph = pickle.load(f)
    return loaded_graph

def load_graph_with_compression(filename = 'enwiki-2023/enwiki-2023.graph.pkl.gz'):
    with gzip.open(filename, 'rb') as f:
        graph, node_id, node_name = pickle.load(f)
    return graph, node_id, node_name

