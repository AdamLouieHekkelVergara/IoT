import simpy
import matplotlib.pyplot as plt
from Version2.Network import Network

def plot_network(nodes :[], connections: []):
    # PLOT NODES AND CONNECTIONS
    for i in nodes:
        x = i.get_X()
        y = i.get_Y()
        plt.plot(x, y, 'ro')
        plt.annotate(i.get_rank(), (x, y))
    for i in connections:
        from_x = i.get_node_from().get_X()
        from_y = i.get_node_from().get_Y()
        to_x = i.get_node_to().get_X()
        to_y = i.get_node_to().get_Y()
        plt.plot([from_x, to_x], [from_y, to_y], 'k')
    plt.show()


print("Dodag")


def main():
    NEW_MESSAGES = 5  # Total number of messages generated pr Node
    INTERVAL_MESSAGES = 10  # Generate messages roughly every x seconds
    MESSAGE_CREATE_TIME = 10  # time it takes a message to be created
    MESSAGE_PROCESS_TIME = 10  # time it takes a message to be processed.

    NUMBER_OF_NODES = 7 # amount of nodes in the network.
    NEIGHBOR_RADIUS = 7.5  # the range a node can see.


    env = simpy.Environment()
    # initialize network with number of nodes placed on a grid:
    network = Network(env, no_of_nodes= NUMBER_OF_NODES, neighbor_radius= NEIGHBOR_RADIUS)

    # plot the initial network!
    plot_network(network.get_nodes(), network.get_connections())


    env.process(network.source(NEW_MESSAGES, INTERVAL_MESSAGES))
    env.run()

    # plot network after
    plot_network(network.get_nodes(), network.get_connections())

    # for connection in network.get_connections():
    #     print("etx", connection.get_ETX())
    #     print("succ", connection.successfulTransmissions)
    #     print("failed", connection.failedTransmissions)


main()