import simpy
import matplotlib.pyplot as plt
from Version2.Network import Network


def plot_network(nodes: [], connections: []):
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

def test_local_repair(network: Network):
    dead_node = network.get_nodes()[3]
    children = network.find_children(dead_node)
    print("død x", dead_node.get_X())
    print("død y", dead_node.get_Y())
    print("no of children", len(children))
    for child in children:
        print("child x", child.get_X())
        print("child y", child.get_Y())

    dead_node.set_battery_power(-1)
    network.local_repair(children)
    network.remove_node_from_network(dead_node)

    # plot surviving network
    surviving_nodes = [x for x in network.get_nodes() if x not in network.removedNodes]
    surviving_connections = [x for x in network.get_connections() if x not in network.removedConnections]
    plt.figure(1)
    plot_network(surviving_nodes, surviving_connections)

    plt.show()


print("Dodag")


def main():
    NEW_MESSAGES = 40  # Total number of customers
    INTERVAL_MESSAGES = 10  # Generate messages roughly every x seconds
    MESSAGE_CREATE_TIME = 10  # time it takes a message to be created
    MESSAGE_PROCESS_TIME = 10  # time it takes a message to be processed.

    NUMBER_OF_NODES = 40  # amount of nodes in the network.
    NEIGHBOR_RADIUS = 3  # the range a node can see.

    env = simpy.Environment()
    # initialize network with number of nodes placed on a grid:
    network = Network(env, no_of_nodes=NUMBER_OF_NODES, neighbor_radius=NEIGHBOR_RADIUS)

    # Run the simulation!
    env.process(network.source(NEW_MESSAGES, INTERVAL_MESSAGES))
    env.run()

    plt.figure(0)
    plot_network(network.get_nodes(), network.get_connections())

    test_local_repair(network)


main()
