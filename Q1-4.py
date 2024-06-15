from graph_tool.all import *
import heapq
from tqdm import tqdm
import openpickle as op
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def out_degree_distribution(graph, node_name_prop):
    num_nodes = graph.num_vertices()
    pbar = tqdm(total=num_nodes, desc="Calculating out-degree distribution")
    out_degrees = [v.out_degree() for v in graph.vertices()]
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
    for v in graph.vertices():
        out_degree = v.out_degree()
        heapq.heappush(min_heap, (out_degree, v))
        if len(min_heap) > 10:
            heapq.heappop(min_heap)
        pbar.update(1) 
    
    top_out_degree_nodes = sorted(min_heap, reverse=True)
    pbar.close()  

    print("Top 10 nodes with the highest out-degree:")
    for out_degree, v in top_out_degree_nodes:
        print(f"Node: {node_name_prop[v]}, Out-Degree: {out_degree}")

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
    # Load the graph and node properties from a file (assuming you've saved it in a similar way)
    g, node_id, node_name = op.load_graph_with_compression()
    
    # Calculate the out-degree distribution
    distribution = out_degree_distribution(g, node_name)
    plot_out_degree_distribution(distribution)