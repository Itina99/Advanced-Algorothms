import Graph
import pickle

filename = "itwiki-2013/itwiki13.pickle"
with open(filename, 'rb') as f:
    loaded_graph = pickle.load(f)

Graph.print_random_subset_of_nodes(loaded_graph)
