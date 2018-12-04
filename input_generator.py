import networkx as nx
import networkx.readwrite.gml as gml
import os
import random
from random_word import RandomWords

# 34 "students"
nodes_small = [
    'ohno',
    'Exerciseforthereader',
    'PequalsNP',
    'PnotequalNP',
    'Woohoo',
    'Efficientalgorithms',
    'Justnegatetheedges',
    'Bruteforce',
    'Consider',
    'Proofisobvious',
    'Infinteloopifhalt',
    'Coping',
    'Quantumcomputing',
    'OHYEAH',
    'f',
    'Anaccountingscheme',
    'Italianlessons',
    'Readsofftheslides',
    'Proofbyinduction',
    'Thisisacontradiction',
    'Reducesto3SAT',
    'Gadget',
    'Maxflowmincut',
    'Duality',
    'Basecases',
    'DP',
    'LP',
    'Greedy',
    'Divideandconquer',
    'Knapsack',
    'FFT',
    'TSP',
    'plus1',
    'Perfectmatching'
]

nodes_medium = []
med_choice = [i for i in range(300)]
for _ in range(300):
    val = random.choice(med_choice)
    nodes_medium.append(val)
    med_choice.remove(val)

nodes_large = []
large_choice = [i for i in range(700)]
for _ in range(700):
    val = random.choice(large_choice)
    nodes_large.append(val)
    large_choice.remove(val)

# create graph from nodes. each node has randomized degree up to k
def graph_from_nodes(nodes, j=1, k=6):
    if k < j:
        raise ValueError("k less than j")

    G = nx.Graph()

    G.add_nodes_from(nodes)

    # go through each vertex and add up to k vertices
    for i in range(len(nodes)):
        degree = random.randint(j, k)
        node = nodes[i]
        indices = {i}
        for _ in range(degree):
            v = random.randint(0, len(nodes) - 1)

            # randomly select vertex that is not self to connect to
            # while v == i:
            #     v = random.randint(0, len(nodes) - 1)

            # add edge if not to self
            node_v = nodes[v]
            if v not in indices and G.degree(node_v) < k:
                G.add_edge(node, node_v)
                indices.add(v)

    return G

# create n subsets from list, each of random size up to k
def rand_subsets(nodes, n, j=2, k=6):
    if k < j:
        raise ValueError("k less than j")

    subsets = []

    for _ in range(n):
        subset = []
        indices = set()
        size = random.randint(j, k)
        for __ in range(size):
            i = random.randint(0, len(nodes) - 1)
            if i not in indices:
                subset += [nodes[i]]
                indices.add(i)
        subsets += [subset]

    return subsets

def create_input(G, k, s, L, name):
    if type(name) != str:
        raise ValueError("name must be string")
    if len(G.nodes()) > k * s:
        raise AssertionError("Buses must fit all students. {} students, {} buses, {} students per bus.".format(len(G.nodes()), k, s))
    directory = "inputs/" + name
    if not os.path.exists(directory):
        os.makedirs(directory)
    gml.write_gml(G, directory + "/graph.gml")
    f = open(directory + "/parameters.txt", "w")
    f.write(str(k) + "\n")
    f.write(str(s) + "\n")
    for group in L:
        f.write("{}\n".format(group))
    f.close()


# SMALL INPUT/OUTPUT
# test_graph = graph_from_nodes(nodes_small, 1, 5)
k = 5
s = 10
test_graph = graph_from_nodes(nodes_small, 1, 100)
print("graph generated")

# import matplotlib.pylab as plt
# nx.draw(test_graph)
# plt.savefig('test_graph.png')
# print("graph drawn")

rowdy = rand_subsets(nodes_small, 10, 2, 4)
print("rowdy groups generated")

create_input(test_graph, k, s, rowdy, "small")
print("inputs created")

from output_generator import *

part = create_partitions(test_graph, k, s)
print("partitions created")

create_output(part, "small")
print("output created")

#################################################
# MEDIUM INPUT/OUTPUT
# test_graph = graph_from_nodes(nodes_small, 1, 5)
k = 10
s = 35
test_graph = graph_from_nodes(nodes_medium, 1, 5)
print("graph generated")

# import matplotlib.pylab as plt
# nx.draw(test_graph)
# plt.savefig('test_graph.png')
# print("graph drawn")

rowdy = rand_subsets(nodes_medium, 100, 2, 10)
print("rowdy groups generated")

create_input(test_graph, k, s, rowdy, "medium")
print("inputs created")

from output_generator import *

part = create_partitions(test_graph, k, s)
print("partitions created")

create_output(part, "medium")
print("output created")


#################################################
# LARGE INPUT/OUTPUT
# test_graph = graph_from_nodes(nodes_small, 1, 5)
k = 30
s = 30
test_graph = graph_from_nodes(nodes_large, 1, 6)
print("graph generated")

# import matplotlib.pylab as plt
# nx.draw(test_graph)
# plt.savefig('test_graph.png')
# print("graph drawn")

rowdy = rand_subsets(nodes_large, 500, 2, 15)
print("rowdy groups generated")

create_input(test_graph, k, s, rowdy, "large")
print("inputs created")

from output_generator import *

part = create_partitions(test_graph, k, s)
print("partitions created")

create_output(part, "large")
print("output created")

'''
# test_graph = graph_from_nodes(nodes_small, 1, 5)
nodes = [i for i in range(1000)]
k = 20
s = 55
test_graph = graph_from_nodes(nodes, 1, 100)
print("graph generated")

# import matplotlib.pylab as plt
# nx.draw(test_graph)
# plt.savefig('test_graph.png')
# print("graph drawn")

rowdy = rand_subsets(nodes, 300, 2, 3)
print("rowdy groups generated")

create_input(test_graph, k, s, rowdy, "small")
print("inputs created")

from output_generator import *

part = create_partitions(test_graph, k, s)
print("partitions created")

create_output(part, "test")
print("output created")
'''