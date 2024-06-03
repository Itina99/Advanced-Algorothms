import networkx as nx
import matplotlib.pyplot as plt
import openpickle as op
import random
import numpy as np
from tqdm import tqdm

def is_vertex_cover(graph, cover):
    for u, v in graph.edges():
        if u not in cover and v not in cover:
            return False
    return True


def greedy_vertex_cover(graph):
    cover = set()
    uncovered_edges = set(graph.edges())
    
    with tqdm(total=len(uncovered_edges), desc="Greedy Vertex Cover") as pbar:
        while uncovered_edges:
            u, v = uncovered_edges.pop()
            cover.add(u)
            cover.add(v)
            incident_edges = list(graph.edges([u, v]))
            for e in incident_edges:
                if e in uncovered_edges:
                    uncovered_edges.remove(e)
                    pbar.update(1)
    
    return cover

def two_approx_vertex_cover(graph):
    cover = set()
    uncovered_edges = set(graph.edges())
    
    with tqdm(total=len(uncovered_edges), desc="2-Approximation Vertex Cover") as pbar:
        while uncovered_edges:
            u, v = uncovered_edges.pop()
            cover.add(u)
            cover.add(v)
            incident_edges = list(graph.edges([u, v]))
            for e in incident_edges:
                if e in uncovered_edges:
                    uncovered_edges.remove(e)
                    pbar.update(1)
    
    return cover

def simulated_annealing_vertex_cover(graph, initial_temp=100, cooling_rate=0.99, iterations=1000):
    current_solution = greedy_vertex_cover(graph)
    best_solution = current_solution
    temperature = initial_temp

    def cost(solution):
        return len(solution)

    def neighbor(solution):
        new_solution = solution.copy()
        if random.random() < 0.5:
            new_solution.add(random.choice(list(graph.nodes())))
        else:
            if new_solution:
                new_solution.remove(random.choice(list(new_solution)))
        return new_solution

    with tqdm(total=iterations, desc="Simulated Annealing Vertex Cover") as pbar:
        for i in range(iterations):
            candidate_solution = neighbor(current_solution)
            if is_vertex_cover(graph, candidate_solution) and cost(candidate_solution) < cost(current_solution):
                current_solution = candidate_solution
                if cost(candidate_solution) < cost(best_solution):
                    best_solution = candidate_solution
            else:
                delta = cost(candidate_solution) - cost(current_solution)
                if random.random() < np.exp(-delta / temperature):
                    current_solution = candidate_solution
            temperature *= cooling_rate
            pbar.update(1)

    return best_solution




if __name__ == "__main__":
    G = op.open_pickle()
    greedy_cover = greedy_vertex_cover(G)
    print("Greedy Vertex Cover:", len(greedy_cover))
    approx_cover = two_approx_vertex_cover(G)
    print("2-Approximation Vertex Cover:", len(approx_cover))
    sa_cover = simulated_annealing_vertex_cover(G)
    print("Simulated Annealing Vertex Cover:", len(sa_cover))
