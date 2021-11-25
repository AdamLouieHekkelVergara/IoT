import numpy as np
import matplotlib.pyplot as plt
import math
from Node import Node

no_of_nodes = 110
neighbour_radius = 1.5
# GENERATE NODES
nodes = []
for i in range(no_of_nodes):
    x = round(np.random.uniform(0, 10), 1)
    y = round(i/(no_of_nodes/10))
    nodes.append(Node(0, x, y))


# GENERATE CONNECTIONS BY FINDING NEIGHBOURS
dictionary = {}
for i in nodes:
    connections = []
    for j in nodes:
        if i.get_ID() == j.get_ID():
            continue
        dist = math.sqrt((i.get_X() - j.get_X())**2 + (i.get_Y() - j.get_Y())**2)
        if dist <= neighbour_radius:
            connections.append(j)
    dictionary[i] = connections


# PLOT NODES AND CONNECTIONS
for i in dictionary:
    plt.plot(i.get_X(), i.get_Y(), 'ro')
    for j in dictionary[i]:
        plt.plot([i.get_X(), j.get_X()], [i.get_Y(), j.get_Y()], 'k')
plt.show()
