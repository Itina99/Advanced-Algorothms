import gzip
import pickle
import random
import graph_tool.all as gt
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD
import openpickle as op

def get_random_subgraph(graph, num_vertices=100):
    vertices = list(graph.vertices())
    subgraph_vertices = random.sample(vertices, num_vertices)
    subgraph = gt.Graph(directed=False)
    vertex_map = {}
    
    for v in subgraph_vertices:
        v_new = subgraph.add_vertex()
        vertex_map[v] = v_new
    
    for v in subgraph_vertices:
        for neighbor in v.out_neighbors():
            if neighbor in vertex_map:
                subgraph.add_edge(vertex_map[v], vertex_map[neighbor])
    
    return subgraph

def add_exclusion_constraint(model, x, solution):
    model += lpSum(x[i] for i in range(len(x)) if solution[i]) <= sum(solution) - 1

def enumerate_minimal_vertex_covers(graph):
    solutions = []
    num_nodes = graph.num_vertices()
    
    while True:
        # Create an ILP problem
        prob = LpProblem("Minimal_Vertex_Cover", LpMinimize)
        x = [LpVariable(f"x_{i}", 0, 1, LpBinary) for i in range(num_nodes)]
        
        # Objective function: Minimize the sum of all vertex variables
        prob += lpSum(x)
        
        # Constraints: For each edge, at least one of its vertices must be in the cover
        for e in graph.edges():
            u, v = int(e.source()), int(e.target())
            prob += x[u] + x[v] >= 1
        
        # Add exclusion constraints for all previously found solutions
        for sol in solutions:
            add_exclusion_constraint(prob, x, sol)
        
        # Solve the ILP problem
        status = prob.solve(PULP_CBC_CMD(msg=0))
        
        if status != 1:  # No more feasible solutions
            break
        
        # Extract the solution
        solution = [int(x[i].varValue) for i in range(num_nodes)]
        solutions.append(solution)
        print(f"Solution {len(solutions)}: {solution}")
    
    return solutions

def find_extreme_solution(solutions, find_minimum=True):
    if find_minimum:
        return min(solutions, key=sum)
    else:
        return max(solutions, key=sum)

# Example usage
if __name__ == "__main__":
    G, node_id, node_name = op.load_graph_with_compression()
    G = get_random_subgraph(G)
    
    print("Enumerating all minimal vertex covers...")
    solutions = enumerate_minimal_vertex_covers(G)
    print(f"Found {len(solutions)} solutions.")
    
    min_vertex_cover = find_extreme_solution(solutions, find_minimum=True)
    
    print(f"Minimal Vertex Cover with minimum length: {min_vertex_cover} with length {sum(min_vertex_cover)}")
