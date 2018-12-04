import os
import sys
import networkx as nx

path_to_outputs = "./outputs"

def score_output_direct_non_destructive(input_graph, num_buses, size_bus, constraints, assignments):
    """
    Directly score without modifying the graph
    """
    bus_assignments = {}

    # assign each student to their bus
    for i in range(len(assignments)):
        for student in assignments[i]:
            bus_assignments[student] = i

    total_edges = input_graph.number_of_edges()
    # Exclude edges for rowdy groups which were not broken up
    excluded_edges = set()
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                for e in input_graph.edges(student):
                    excluded_edges.add(e)

    # score output
    score = 0
    for edge in input_graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]] and edge not in excluded_edges and edge[::-1] not in excluded_edges:
            score += 1
    score = score / total_edges

    return score

def score_output_direct(graph, num_buses, size_bus, constraints, assignments):
    """
    Score without having to create input and output files
    """
    if len(assignments) != num_buses:
        return -1, "Must assign students to exactly {} buses, found {} buses".format(num_buses, len(assignments))

    # make sure no bus is empty or above capacity
    for i in range(len(assignments)):
        if len(assignments[i]) > size_bus:
            return -1, "Bus {} is above capacity".format(i)
        if len(assignments[i]) <= 0:
            return -1, "Bus {} is empty".format(i)

    bus_assignments = {}
    attendance_count = 0

    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(assignments)):
        if not all([student in graph for student in assignments[i]]):
            return -1, "Bus {} references a non-existant student: {}".format(i, assignments[i])

        for student in assignments[i]:
            # if a student appears more than once
            if attendance[student] == True:
                print(assignments[i])
                return -1, "{0} appears more than once in the bus assignments".format(student)

            attendance[student] = True
            bus_assignments[student] = i

    # make sure each student is accounted for
    if not all(attendance.values()):
        return -1, "Not all students have been assigned a bus"

    total_edges = graph.number_of_edges()
    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

    # score output
    score = 0
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score += 1
    score = score / total_edges


    return score, "Valid output submitted with score: {}".format(score)

####################################################
# To run:
#   python3 output_scorer.py <input_folder> <output_file>
#
#   input_folder - the path to the input folder
#   output_file - the path to the output file
#
# Examples:
#   python3 output_scorer.py ./inputs/small/12 ./outputs/small/12.out
####################################################

def score_output(input_folder, output_file):
    '''
        Takes an input and an output and returns the score of the output on that input if valid

        Inputs:
            input_folder - a string representing the path to the input folder
            output_file - a string representing the path to the output file

        Outputs:
            (score, msg)
            score - a number between 0 and 1 which represents what fraction of friendships were broken
            msg - a string which stores error messages in case the output file is not valid for the given input
    '''
    graph = nx.read_gml(input_folder + "/graph.gml")
    parameters = open(input_folder + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [node.replace("'","") for node in line.split(", ")]
        constraints.append(curr_constraint)

    output = open(output_file)
    assignments = []
    for line in output:
        line = line[1: -2]
        curr_assignment = [node.replace("'","") for node in line.split(", ")]
        assignments.append(curr_assignment)

    if len(assignments) != num_buses:
        return -1, "Must assign students to exactly {} buses, found {} buses".format(num_buses, len(assignments))

    # make sure no bus is empty or above capacity
    for i in range(len(assignments)):
        if len(assignments[i]) > size_bus:
            return -1, "Bus {} is above capacity".format(i)
        if len(assignments[i]) <= 0:
            return -1, "Bus {} is empty".format(i)

    bus_assignments = {}
    attendance_count = 0

    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(assignments)):
        if not all([student in graph for student in assignments[i]]):
            print([student in graph for student in assignments[i]])
            return -1, "Bus {} references a non-existant student: {}".format(i, assignments[i])

        for student in assignments[i]:
            # if a student appears more than once
            if attendance[student] == True:
                print(assignments[i])
                return -1, "{0} appears more than once in the bus assignments".format(student)

            attendance[student] = True
            bus_assignments[student] = i

    # make sure each student is accounted for
    if not all(attendance.values()):
        return -1, "Not all students have been assigned a bus"

    total_edges = graph.number_of_edges()
    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

    # score output
    score = 0
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score += 1
    score = score / total_edges


    return score, "Valid output submitted with score: {}".format(score)

def score_all():
    total = 0
    num_inputs = 0

    for size in ["small", "medium", "large"]:
        inputs = os.listdir("all_inputs/" + size)
        if ".DS_Store" in inputs:
            inputs.remove(".DS_Store")
        for input_folder in inputs:
            score = score_output("all_inputs/" + size + "/" + input_folder, path_to_outputs + "/" + size + "/" + input_folder + ".out")
            print(score, "num scored:", num_inputs, " input: {} {}".format(size, input_folder))
            total += score[0]
            num_inputs += 1
        print("average so far:", total/num_inputs)
    print("average score:", total/num_inputs)

if __name__ == '__main__':
    #score, msg = score_output(sys.argv[1], sys.argv[2])
    #print(msg)
    #print(score_output("./all_inputs/medium/166", "./debug_outputs/medium/166.out"))
    score_all()