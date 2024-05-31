import networkx as nx
import matplotlib.pyplot as plt
import pickle
import heapq
from tqdm import tqdm

def out_degree_distribution(G):
    # Initialize tqdm progress bar
    num_nodes = G.number_of_nodes()
    pbar = tqdm(total=num_nodes, desc="Calculating out-degree distribution")

    # Calculate the out-degrees of all nodes
    out_degrees = [d for n, d in G.out_degree()]
    pbar.update(num_nodes)  # Update progress bar for out-degree calculation

    # Calculate the distribution of out-degrees
    out_degree_count = {}
    for degree in out_degrees:
        if degree in out_degree_count:
            out_degree_count[degree] += 1
        else:
            out_degree_count[degree] = 1
    
    # Normalize to get the probability distribution
    out_degree_distribution = {k: v / num_nodes for k, v in out_degree_count.items()}

    # Find the top 10 nodes with the highest out-degree using a Min-Heap
    min_heap = []
    pbar.reset(total=num_nodes)  # Reset progress bar for heap calculation
    for node, out_degree in G.out_degree():
        heapq.heappush(min_heap, (out_degree, node))
        if len(min_heap) > 10:
            heapq.heappop(min_heap)
        pbar.update(1)  # Update progress bar for each node processed
    
    # Get the nodes with the highest out-degree from the Min-Heap
    top_out_degree_nodes = sorted(min_heap, reverse=True)
    print("Top 10 nodes with the highest out-degree:", top_out_degree_nodes)

    pbar.close()  # Close the progress bar

    return out_degree_distribution

if __name__ == '__main__': 
    filename = "itwiki-2013/itwiki13.pickle"
    with open(filename, 'rb') as f:
        G = pickle.load(f) # Carica il grafo da un file pickle
    
    distribution = out_degree_distribution(G) # Calcola la distribuzione del grado uscente
    print("Distribuzione del grado uscente:", distribution) # Stampa la distribuzione del grado uscente
