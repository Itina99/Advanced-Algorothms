import Graph
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm


def open_pickle(filename = "itwiki-2013/itwiki13.pickle"):
    
    with open(filename, 'rb') as f:
        loaded_graph = pickle.load(f)
    return loaded_graph

def open_ids(filename = "itwiki-2013/itwiki13.ids"):
    
    with open(filename, 'r') as f:
        ids = f.readlines()
    return ids