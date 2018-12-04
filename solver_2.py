import networkx as nx
import os

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
path_to_outputs = "./outputs_2"
path_to_debug_outputs = "./debug_outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def create_rowdy_dict(nodes_left, constraints):
    '''
    Creates a dictionary rowdy groups. 
    '''
    rowdy_dict = {n : [] for n in nodes_left}
    for c in constraints:
        for i in range(len(c)):
            r = c[0:i] + c[i + 1:]
            rowdy_dict[c[i]].append(r)
    return rowdy_dict

def find_node_max_neighbors(nodes, adj_list, bus, rowdy_dict, nodes_used):
    '''
    Finds the node with the most number of neighbors in bus. If 
    all nodes will form a rowdy group, then the first node will be returned.
    '''
    # If the bus is empty, return the node with the most neighbors
    max_neighbors, max_node = -1, nodes[0]
    if len(bus) == 0:
        return max(nodes, key=lambda n: len(__intersection(adj_list[n], 
                                            [x for x in nodes_used.keys() if nodes_used[x]])))

    # Check for rowdy group violation nodes and remove them
    for n in list(nodes):
        for group in rowdy_dict[n]:
            rowdy_group_exist = all([nodes_used[r] for r in group])
            if rowdy_group_exist:
                nodes.remove(n)
                break

    for n in nodes:        
        # Find best person to put in bus
        num_neighbors = len(__intersection(adj_list[n], bus))
        if num_neighbors > max_neighbors:
            max_neighbors = num_neighbors
            max_node = n

    return max_node

def __intersection(lst1, lst2): 
    '''
    Returns the intersection of two lists. 
    '''
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def solve(graph, num_bus, size_bus, constraints):
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    '''
    Parses the input file and then outputs an assignment of students as a list of lists. 
    '''
    G, num_bus, size_bus, contraints = graph, num_bus, size_bus, constraints

    # Keeps track of the nodes that need to be assigned
    nodes_left = list(G.nodes())
    # Total number of nodes
    num_people = len(nodes_left)
    # The output list of bus assignments (list of list)
    output = [[] for i in range(num_bus)]
    # Tracks if a given node is used in a bus. Used to prevent rowdy groups. 
    nodes_used_dicts = [{n: False for n in nodes_left} for i in range(num_bus)] 
    # APPROACH 1: Assign equal number of people per bus
    num_people_per_bus = num_people // num_bus

    # Create a dictionary tracking each node and every rowdy group that node is part of
    rowdy_dict = create_rowdy_dict(nodes_left, constraints)

    # Create adjacency list of the graph object
    adj_list = {}
    for node in nodes_left:
        adj_list[node] = list(G.neighbors(node))

    # Greedily assign students to buses, keep track of the current bus we are assigning. 
    bus_index = 0
    left_over = num_people % num_bus
    while nodes_left and bus_index < num_bus:
        empty_buses = [i for i in range(len(output)) if not output[i]]
        if len(empty_buses) == len(nodes_left):
            it = iter(nodes_left)
            for i in empty_buses:
                output[i].append(next(it))
            break

        max_neighbor_node = find_node_max_neighbors(list(nodes_left), adj_list, 
            output[bus_index], rowdy_dict, nodes_used_dicts[bus_index])
        output[bus_index].append(max_neighbor_node)
        nodes_used_dicts[bus_index][max_neighbor_node] = True
        nodes_left.remove(max_neighbor_node)

        if len(output[bus_index]) >= size_bus:
            # Removes all rowdy groups that have already been broken up
            for n_assigned in output[bus_index]:
                for c in list(constraints):
                    if n_assigned in c:
                        if c in constraints:
                            constraints.remove(c)
            # Create the rowdy dict again, with entries
            rowdy_dict = create_rowdy_dict(nodes_left, constraints)
            bus_index += 1

    # Return the output, which should be a list of list
    return output

# Runs the solver with a optional starting input
def main(starting_size="", starting_file=""):
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    # Jump to specific size
    if starting_size != "":
        size_categories = size_categories[size_categories.index(starting_size):]

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)
        
        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        input_folders = os.listdir(category_dir)
        print(input_folders)
        # Jump to specific file
        if starting_file != "":
            input_folders = input_folders[[str(x) for x in input_folders].index(starting_file):]

        num_solved = 0
        for input_folder in input_folders:
            if str(input_folder) == "b'.DS_Store'":
                continue
            print("Solving {} {}.".format(size, str(input_folder)))
            input_name = os.fsdecode(input_folder) 
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")
            num_solved += 1
            print("num solved: ", num_solved)

            #TODO: modify this to write your solution to your 
            #      file properly as it might not be correct to 
            #      just write the variable solution to a file
            # Convert the solution to a string and writes to output file
            write_string = ""
            for b in solution:
                write_string += str(b) + "\n"
            output_file.write(write_string)

            output_file.close()

def main_on_specific_input(size, input_f):
    ''' 
    Run solver on one specific file
    '''
    print("Solving input {} {}.".format(size, input_f))
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    category_path = path_to_inputs + "/" + size
    output_category_path = path_to_debug_outputs + "/" + size
    category_dir = os.fsencode(category_path)
    
    if not os.path.isdir(output_category_path):
        os.mkdir(output_category_path)

    input_name = os.fsdecode(input_f)
    graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
    solution = solve(graph, num_buses, size_bus, constraints)
    output_file = open(output_category_path + "/" + input_name + ".out", "w")

    #TODO: modify this to write your solution to your 
    #      file properly as it might not be correct to 
    #      just write the variable solution to a file
    # Convert the solution to a string and writes to output file
    write_string = ""
    for b in solution:
        write_string += str(b) + "\n"
    output_file.write(write_string)

    output_file.close()

if __name__ == '__main__':
    main(starting_size="", starting_file="")
    #main_on_specific_input("medium", "103")


