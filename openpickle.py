import Graph
import pickle

def open_pickle(filename = "itwiki-2013/itwiki13.pickle"):
    
    with open(filename, 'rb') as f:
        loaded_graph = pickle.load(f)
    return loaded_graph
