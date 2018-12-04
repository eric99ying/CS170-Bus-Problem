import os

def create_partitions(G, k, s):
    """
    Graph G, k buses, s students per bus
    """
    ret = [[] for _ in range(k)]
    nodes = list(G.nodes())
    # Initially adds one student to every bus
    for b in range(len(ret)):
        ret[b].append(nodes[b])
    i = len(ret)
    while i < len(nodes):
        for j in range(k):
            if i >= len(nodes):
                break
            ret[j].append(nodes[i])
            i += 1
    return ret

def create_output(partitions, name):
    if type(name) != str:
        raise ValueError("name must be string")

    directory = "outputs/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory + name + ".out", "w")
    for p in partitions:
        f.write("{}\n".format(p))
    f.close()
