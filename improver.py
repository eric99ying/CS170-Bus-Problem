from output_scorer import score_output_direct_non_destructive as score
from io_helper import parse_input, parse_output
import networkx as nx
import random

path_to_output = "./improved_outputs"
path_to_input = "./all_inputs"
path_to_prev_output = "./outputs"

def random_improve(input_folder, output_file, swaps, repeats, iters):
    """
    Does random swaps between nodes in current assignment.
    Then tries to do local improvement until local maximum is reached.
    """
    graph, num_buses, size_bus, constraints = parse_input(input_folder)
    assignments = parse_output(output_file)

    best_score = score(graph, num_buses, size_bus, constraints, assignments)
    best_assign = assignments

    curr_assign = list(assignments)
    for _ in range(swaps):
        bus1 = random.randint(0, num_buses - 1)
        bus2 = random.randint(0, num_buses - 1)
        bus1_size = len(curr_assign[bus1])
        bus2_size = len(curr_assign[bus2])
        # Get random student from buses
        student1 = random.randint(0, bus1_size - 1)
        student2 = random.randint(0, bus2_size - 1)
        assign_swap(curr_assign, student1, student2, bus1, bus2)

    curr_score = score(graph, num_buses, size_bus, constraints, curr_assign)
    iter_assign = list(curr_assign)
    for bus1 in range(len(assignments)):
        for student1 in range(len(assignments[bus1])):
            for bus2 in set(range(len(assignments))) - {bus1}:
                for student2 in range(len(assignments[bus2])):
                    assign_swap(iter_assign, student1, student2, bus1, bus2)
                    if score(graph, num_buses, size_bus, constraints, iter_assign) > curr_score:


def assign_swap(assign, b1, b2, s1, s2):
    temp = assign[b1][s1]
    curr_assign[b1][s1] = curr_assign[b2][s2]
    curr_assign[b2][s2] = temp