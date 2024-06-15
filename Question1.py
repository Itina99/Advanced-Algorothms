import networkx as nx
import matplotlib.pyplot as plt
import openpickle as op
import heapq
from tqdm import tqdm
import Graph
import numpy as np


def out_degree_distribution(G, node_dict):
    num_nodes = G.number_of_nodes()
    pbar = tqdm(total=num_nodes, desc="Calculating out-degree distribution")

    out_degrees = [d for n, d in G.out_degree()]
    pbar.update(num_nodes)  

    out_degree_count = {}
    for degree in out_degrees:
        if degree in out_degree_count:
            out_degree_count[degree] += 1
        else:
            out_degree_count[degree] = 1
    
    out_degree_distribution = {k: v / num_nodes for k, v in out_degree_count.items()}

    min_heap = []
    pbar.reset(total=num_nodes)  
    for node, out_degree in G.out_degree():
        heapq.heappush(min_heap, (out_degree, node))
        if len(min_heap) > 10:
            heapq.heappop(min_heap)
        pbar.update(1)  
    
    top_out_degree_nodes = sorted(min_heap, reverse=True)

    pbar.close()  

    print("Top 10 nodes with the highest out-degree:")
    for out_degree, node in top_out_degree_nodes:
        print(f"Node: {node_dict[node]}, Out-Degree: {out_degree}")

    return out_degree_distribution

def plot_out_degree_distribution(out_degree_distribution):
    # Extracting degrees and their frequencies
    degrees = list(out_degree_distribution.keys())
    frequencies = list(out_degree_distribution.values())
    
    # Convert to numpy arrays for easier manipulation
    degrees = np.array(degrees)
    frequencies = np.array(frequencies)
    
    # Plotting the log-log plot of out-degree distribution
    plt.figure(figsize=(12, 6))
    plt.scatter(degrees, frequencies, color='blue', edgecolor='black')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Out-Degree (log scale)')
    plt.ylabel('Frequency (log scale)')
    plt.title('Out-Degree Distribution (Log-Log Plot)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plt.show()

if __name__ == '__main__': 
    G=op.open_pickle() # Apre il file pickle
    ids_filename = 'itwiki-2013/itwiki-2013.ids' 
    node_dict = Graph.read_ids_file(ids_filename)
    distribution = out_degree_distribution(G, node_dict) # Calcola la distribuzione del grado uscente
    plot_out_degree_distribution(distribution) # Plotta la distribuzione del grado uscente
    
