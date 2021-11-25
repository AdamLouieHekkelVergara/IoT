from Node import Node
from Network import Network
import matplotlib.pyplot as plt
import numpy as ns
import random


network = Network(50)


xs = []
ys = []
for node in network.nodes:
    xs.append(node.get_positionX())
    ys.append(node.get_Y())
    print("id: ", node.get_ID())
    print("rank: ", node.get_rank())
    print(f"x position: {node.get_positionX()}    y position: {node.positionY}", )
    print("")



plt.plot(xs,ys ,'ro')
plt.show()

