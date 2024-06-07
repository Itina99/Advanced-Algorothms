from graph_tool.all import *
import heapq
from tqdm import tqdm
import gzip
import pickle

def out_degree_distribution(graph, node_name_prop):
    # Initialize tqdm progress bar
    num_nodes = graph.num_vertices()
    pbar = tqdm(total=num_nodes, desc="Calculating out-degree distribution")

    # Calculate the out-degrees of all nodes
    out_degrees = [v.out_degree() for v in graph.vertices()]
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
    for v in graph.vertices():
        out_degree = v.out_degree()
        heapq.heappush(min_heap, (out_degree, v))
        if len(min_heap) > 10:
            heapq.heappop(min_heap)
        pbar.update(1)  # Update progress bar for each node processed
    
    # Get the nodes with the highest out-degree from the Min-Heap
    top_out_degree_nodes = sorted(min_heap, reverse=True)

    pbar.close()  # Close the progress bar

    # Print the top 10 nodes with the highest out-degree
    print("Top 10 nodes with the highest out-degree:")
    for out_degree, v in top_out_degree_nodes:
        print(f"Node: {node_name_prop[v]}, Out-Degree: {out_degree}")

    return out_degree_distribution

if __name__ == '__main__':
    # Load the graph and node properties from a file (assuming you've saved it in a similar way)
    with gzip.open('enwiki-2023/enwiki-2023.graph.pkl.gz', 'rb') as f:
        g, node_id, node_name = pickle.load(f)
    
    # Calculate the out-degree distribution
    distribution = out_degree_distribution(g, node_name)
    print("Out-Degree Distribution:", distribution)
