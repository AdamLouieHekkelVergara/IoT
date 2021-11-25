from Node import Node
from Network import Network
import matplotlib.pyplot as plt
import numpy as ns
import random
import simpy

network = Network(50)


xs = []
ys = []
for node in network.nodes:
    xs.append(node.get_X())
    ys.append(node.get_Y())
    print("id: ", node.get_ID())
    print("rank: ", node.get_rank())
    print(f"x position: {node.get_X()}    y position: {node.get_Y}", )
    print("")



plt.plot(xs,ys ,'ro')
plt.show()


