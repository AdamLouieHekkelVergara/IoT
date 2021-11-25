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

plt.plot(xs, ys, 'ro')
plt.show()

SIMULATION_TIME = 120


def DODAG(env):
    """A DODAG first initializes a network with a defined set of nodes and connections.
       The Node with Rank 0, then sends out messages (DIO) to all its connected Nodes.
    """
    pass

# when a message arrives it processes the message, which takes some time 1-200 ms for both DIO and DAO messages.
def message_arrival(env):
    # receive message.
    # some time 'xx' pass.
    # return true if processed correctly
    pass


# when a message is being sent from a Node we first looks for neighbouring Nodes / children(DIO)/ parents(DAO).
# it then checks if the To-Node is busy, if not it simply sends to that Node, making it process the message.
# Otherwise it finds another Node.
# The lookup To-Node is defined as the objective function and is first only based on the ETX.
def message_send(env):
    pass
