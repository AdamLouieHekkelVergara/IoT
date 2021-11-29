from Messages import DAO
from Node import Node
from Network import Network
import matplotlib.pyplot as plt
import numpy as ns
import random
import simpy

network = Network(110)
nodes = network.get_nodes()
network.generate_ranks(root=nodes[0])

# PLOT NODES AND CONNECTIONS
for i in nodes:
    x = i.get_X()
    y = i.get_Y()
    plt.plot(x, y, 'ro')
    plt.annotate(i.get_rank(), (x,y),size=7)


def simulateDAO(dao: DAO, nrOfRecursions: int):
    print("", nrOfRecursions)
    if network.send_DAO(dao) is None or nrOfRecursions == 100:
        print("we stop")
        return
    else:
        # get the node in the dao message in order to plot the connecting line!
        nodeFrom = None
        for node in network.get_nodes():
            if node.get_ID() == dao.get_node_ID():
                nodeFrom = node
                print(f"this is the node from the dao message {nrOfRecursions}: ", node)
        # run the send_Dao message, which gives the node it sends to!
        nodeTo = network.send_DAO(dao)
        # plot the connection:

        ax = plt.subplot(111)
        lines = ax.plot([nodeFrom.get_X(), nodeTo.get_X()], [nodeFrom.get_Y(), nodeTo.get_Y()], 'k')
        plt.pause(1)
        plt.legend(lines[:1], ['Dao message route'], bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=50.5)

        ax.set_position([0.125, 0.11 + 0.693 * 0.1,0.775, 0.693 * 0.9])
        # run recursive!
        new_dao = DAO(nodeTo.get_rank(), nodeTo.get_ID())

        simulateDAO(new_dao, nrOfRecursions = nrOfRecursions + 1)


nodeFrom = network.nodes[109]  # send from a Dao from an arbitrary node.
dao = DAO(nodeFrom.get_rank(), nodeFrom.get_ID())


#plt.plot([nodeFrom.get_X(), nodeTo.get_X()], [nodeFrom.get_Y(), nodeTo.get_Y()], 'k')
#plt.plot(nodeFrom.get_X(), nodeFrom.get_Y(), 'bo')
simulateDAO(dao,0)
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
