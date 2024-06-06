import networkx as nx
from tqdm import tqdm
import random
import pickle


def read_ids_file(filename):
    dict_node = {}
    with open(filename, 'r') as f:
        for i, line in tqdm(enumerate(f), desc="Reading IDs"):
            line = line.strip()
            if line:
                node_id, node_name = (i, line)
                try:
                    node_id = int(node_id)
                    dict_node[node_id] = node_name
                except ValueError:
                    print(f"Skipping line with invalid ID: {line}")
    return dict_node

def read_nodes_file(filename):
    with open(filename, 'r') as f:
        for node_id, line in enumerate(tqdm(f, desc="Reading Nodes"), start=1):
            if line.strip():  # if line is not empty
                yield node_id


def read_arcs_file(filename):
    # First pass to count the lines
    with open(filename, 'r') as f:
        total_lines = sum(1 for _ in f)

    # Second pass to read the lines with a progress bar
    with open(filename, 'r') as f:
        for line in tqdm(f, desc="Reading Edges", total=total_lines, unit=" lines"):
            parts = line.strip().split()
            if len(parts) != 2:
                print(f"Warning: Malformed line: {line.strip()}")
                continue
            try:
                u, v = map(int, parts)
                yield u, v
            except ValueError:
                print(f"Warning: Invalid edge in line: {line.strip()}")


def create_graph_from_files(nodes_filename, arcs_filename):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes from the nodes file
    for node_id in read_nodes_file(nodes_filename):
        G.add_node(node_id)

    # Add edges
    for u, v in read_arcs_file(arcs_filename):
        G.add_edge(u, v)

    return G

def print_random_subset_of_nodes(G, node_name_dict, num_samples=5):
    nodes = list(G.nodes())
    sampled_nodes = random.sample(nodes, min(num_samples, len(nodes)))
    
    for node_id in sampled_nodes:
        successors = list(G.successors(node_id))
        successor_names = [(succ, node_name_dict.get(succ, 'Unknown')) for succ in successors]
        node_name = node_name_dict.get(node_id, 'Unknown')
        
        print(f"Node {node_id} ({node_name}):")
        print("  Successors:")
        for succ_id, succ_name in successor_names:
            print(f"    {succ_id} ({succ_name})")
        print()

def print_first_10_lines_ids_file(filename):
    with open(filename, 'r') as f:
        print("First 10 lines of", filename, ":\n")
        for i, line in enumerate(f, 1):  # Start enumeration from 1
            if i > 10:
                break
            print(f"ID {i}: {line.strip()}")  # Print line number along with line content

if __name__ == '__main__':
    # Usage
    ids_filename = 'itwiki-2013/itwiki-2013.ids' 
    arcs_filename = 'itwiki-2013/itwiki-2013.arcs'  
    node_dict = read_ids_file(ids_filename)
    G = create_graph_from_files(node_dict, arcs_filename)
    filename = "itwiki-2013/itwiki13.pickle"  
    with open(filename, 'wb') as f:
        pickle.dump(G, f)
    print_random_subset_of_nodes(G, node_dict)