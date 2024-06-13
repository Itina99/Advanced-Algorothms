from graph_tool.all import *
from tqdm import tqdm
import gzip
import pickle

def build_graph_from_files(ids_file, arc_file, directed=True):
    # Create an empty Graph object
    g = Graph(directed=directed)

    # Create property maps to store node IDs and node names
    node_id = g.new_vertex_property("int")
    node_name = g.new_vertex_property("string")

    # Count the total number of lines in the .ids file
    with open(ids_file, 'r') as f:
        num_lines = sum(1 for line in f)

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=num_lines, desc="Building graph")

    # Read node IDs from .ids file
    with open(ids_file, 'r') as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            v = g.add_vertex()  # Add a vertex for each line in the .ids file
            node_id[v] = line_num  # Assign the line number as the ID
            node_name[v] = line  # Assign the node name

            progress_bar.update(1)  # Update progress bar

    progress_bar.close()  # Close progress bar

    # Read edges from .arc file and add them to the graph
    with open(arc_file, 'r') as f:
        num_lines_arc = sum(1 for line in f)

    # Initialize tqdm progress bar for adding edges from .arc file
    progress_bar_arc = tqdm(total=num_lines_arc, desc="Adding edges from .arc file")

    # Read edges from .arc file and add them to the graph
    with open(arc_file, 'r') as f:
        for line in f:
            u, v = map(int, line.strip().split())  # Assuming edges are space-separated
            g.add_edge(g.vertex(u), g.vertex(v))

            progress_bar_arc.update(1)  # Update progress bar

    progress_bar_arc.close()  # Close progress bar for .arc file

    return g, node_id, node_name


def print_first_5_nodes_with_successors(graph, node_id_prop, node_name_prop):
    for v in graph.vertices():
        if node_id_prop[v] < 5:  # Print only the first 5 nodes
            print("Node ID:", node_id_prop[v], "Node Name:", node_name_prop[v])
            successors = [node_name_prop[u] for u in v.out_neighbours()]  # Get successors of the current node
            print("Successors:", successors)

def save_graph_with_compression(graph, node_id, node_name, filename):
    data = (graph, node_id, node_name)
    with gzip.open(filename, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    ids_filename = 'enwiki-2023/enwiki-2023.ids'
    arcs_filename = 'enwiki-2023/enwiki-2023.arcs'
    g, node_id, node_name = build_graph_from_files(ids_filename, arcs_filename, directed=False)
    print_first_5_nodes_with_successors(g, node_id, node_name)

    # Save the graph with compression
    #save_filename = 'enwiki-2023/enwiki-2023.graph.pkl.gz'
    #save_graph_with_compression(g, node_id, node_name, save_filename)

    save_filename = 'enwiki-2023/enwiki-2023_undirected.graph.pkl.gz'
    save_graph_with_compression(g, node_id, node_name, save_filename)

# Now you can use the created graph 'g' along with node_id and node_name property maps.
