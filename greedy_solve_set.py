def solve(graph, num_bus, size_bus, constraints):
    '''
    Parses the input file and then outputs an assignment of students as a list of lists.
    '''
    G = graph

    # All nodes sorted by degree
    nodes_by_degree = sorted(G.nodes, key=lambda n: G.degree(n))
    nodes_left = set(G.nodes)
    num_people = len(nodes_left)
    # The output list of bus assignments (list of sets)
    output = [set() for _ in range(num_bus)]

    # APPROACH 1: Assign equal number of people per bus
    num_people_per_bus = num_people // num_bus

    # Indices of rowdy groups that cannot form
    excluded_rowdy = set()
    # Create a dictionary tracking each node and every rowdy group that node is a part of
    # List of current states for each rowdy group, used to determine if a rowdy group has formed
    rowdy_dict, rowdy_states = map_nodes_to_rowdy(constraints, size_bus)
    # Dict of each node and its assigned bus number
    assignments = {}

    # Greedily assign students to buses, keep track of the current bus
    # we are assigning
    bus_index = 0
    # Have we gone over num_bus?
    over = False
    while nodes_left:
        max_neighbor_node_first = find_node_max_neighbors(nodes_left, output[bus_index], G, nodes_by_degree)
        max_neighbor_node = max_neighbor_node_first
        will_create_rowdy = set()
        while nodes_left and node_creates_rowdy(max_neighbor_node, bus_index, rowdy_dict, rowdy_states, excluded_rowdy):
            will_create_rowdy.add(max_neighbor_node)
            nodes_left.remove(max_neighbor_node)
            if not nodes_left:
                max_degree_node = max_neighbor_node_first
                break
            max_neighbor_node = find_node_max_neighbors(nodes_left, output[bus_index], G, nodes_by_degree)
        nodes_left |= will_create_rowdy
        update_assignments(max_neighbor_node, bus_index, assignments, rowdy_dict, rowdy_states, excluded_rowdy)
        output[bus_index].add(max_neighbor_node)
        nodes_left.remove(max_neighbor_node)

        if over:
            bus_index = (bus_index + 1) % num_bus
        elif len(output[bus_index]) >= num_people_per_bus:
            bus_index += 1
            if bus_index >= num_bus:
                bus_index = 0
                over = True

    # Return the output, which should be a list of lists
    return [list(s) for s in output]

def find_node_max_neighbors(nodes, bus, G, nodes_by_degree):
    '''
    Finds the node with the most number of neighbors in bus. If
    all nodes will form a rowdy group, then the first node will be returned.
    '''
    # If the bus is empty, return the node with the most neighbors
    if not bus:
        max_degree_node = nodes_by_degree.pop()
        while max_degree_node not in nodes:
            max_degree_node = nodes_by_degree.pop()
        return max_degree_node
    return max(nodes, key=lambda n: len(bus.intersection(G.neighbors(n))))

def map_nodes_to_rowdy(rowdy_groups, size_bus):
    """
    Returns
        dict of nodes mapped to the set of rowdy groups each node is in
        list of lists, each list holds current state of rowdy group
            (size of group, how many members in same bus, associated bus)
    Rowdy groups are only considered if their size isn't greater than the bus size
    """
    mapping = {}
    states = []
    i = 0
    for group in rowdy_groups:
        size = len(group)
        if size > size_bus:
            # excluded_rowdy.add(i)
            # i += 1
            continue
        states.append([size, 0, None])
        for node in group:
            mapping_val = mapping.get(node, set())
            mapping_val.add(i)
            mapping[node] = mapping_val
        i += 1
    return mapping, states

# Check if rowdy group will form
def node_creates_rowdy(node, bus_index, rowdy_dict, rowdy_states, excluded_rowdy):
    if rowdy_dict and node in rowdy_dict:
        for rowdy in rowdy_dict[node]:
            if rowdy not in excluded_rowdy:
                length, cur_size, bus_num = rowdy_states[rowdy]
                if bus_num == bus_index and cur_size + 1 == length:
                    return True
    return False

# Update rowdy states and assignment
def update_assignments(node, bus_index, assignments, rowdy_dict, rowdy_states, excluded_rowdy):
    assignments[node] = bus_index
    if rowdy_dict and node in rowdy_dict:
        for rowdy in rowdy_dict[node]:
            if rowdy not in excluded_rowdy:
                state = rowdy_states[rowdy]
                if state[2] == bus_index:
                    state[1] += 1
                elif state[2] == None:
                    state[1] += 1
                    state[2] = bus_index
                else:
                    excluded_rowdy.add(rowdy)

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
    
        for input_folder in input_folders:
            if str(input_folder) == "b'.DS_Store'":
                continue
            print("Solving {} {}.".format(size, str(input_folder)))
            input_name = os.fsdecode(input_folder)
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
    main()
