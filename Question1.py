import networkx as nx
import matplotlib.pyplot as plt
import pickle
import heapq

def out_degree_distribution(G):
    # Calcola i gradi uscenti di tutti i nodi
    out_degrees = [d for n, d in G.out_degree()]

    # Calcola la distribuzione del grado uscente
    out_degree_count = {}
    for degree in out_degrees:
        if degree in out_degree_count:
            out_degree_count[degree] += 1
        else:
            out_degree_count[degree] = 1
    
    # Normalizza per ottenere la distribuzione di probabilità
    num_nodes = G.number_of_nodes()
    out_degree_distribution = {k: v / num_nodes for k, v in out_degree_count.items()}

    # Trova i top 10 nodi con il grado uscente più alto usando un Min-Heap
    min_heap = []
    for node, out_degree in G.out_degree():
        heapq.heappush(min_heap, (out_degree, node))
        if len(min_heap) > 10:
            heapq.heappop(min_heap)
    
    # Ottiene i nodi con il grado uscente più alto dal Min-Heap
    top_out_degree_nodes = sorted(min_heap, reverse=True)
    print("Top 10 nodi con il grado uscente più alto:", top_out_degree_nodes)

    return out_degree_distribution

if __name__ == '__main__': 
    filename = "itwiki-2013/itwiki13.pickle"
    with open(filename, 'rb') as f:
        G = pickle.load(f) # Carica il grafo da un file pickle
    
    distribution = out_degree_distribution(G) # Calcola la distribuzione del grado uscente
    print("Distribuzione del grado uscente:", distribution) # Stampa la distribuzione del grado uscente
