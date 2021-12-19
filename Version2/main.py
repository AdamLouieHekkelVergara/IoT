import math
import simpy
import matplotlib.pyplot as plt
from Version2.Network import Network


def plot_network(nodes: [], connections: [], network: Network):
    # PLOT NODES AND CONNECTIONS
    for i in connections:
        from_x = i.get_node_from().get_X()
        from_y = i.get_node_from().get_Y()
        to_x = i.get_node_to().get_X()
        to_y = i.get_node_to().get_Y()
        plt.plot([from_x, to_x], [from_y, to_y], 'k', linewidth=0.1 / math.log10(i.get_ETX() + 0.05))

    for i in nodes:
        x = i.get_X()
        y = i.get_Y()
        plt.plot(x, y, 'ro', markersize=10)
        plt.annotate(i.get_rank(), (x + .07, y + .07), size=16, color="Orange")
        parents = network.find_parents(i)
        # Draw arrow
        for parent in parents:
            if parent.get_battery_power() >= 0:
                plt.annotate("", xytext=(x, y), xy=(parent.get_X(), parent.get_Y()),
                             arrowprops=dict(arrowstyle="-|>, head_length = 0.8, head_width = .3", lw=.0001, color='k'))
    plt.xticks([])
    plt.yticks([])


def test_local_repair(network: Network):
    # Define node with no battery left
    dead_node = network.get_nodes()[3]
    children = network.find_children(dead_node)
    dead_node.set_battery_power(-1)
    network.local_repair(children)
    network.remove_node_from_network(dead_node)

    # plot resulting network
    surviving_nodes = [x for x in network.get_nodes() if x not in network.get_removed_nodes()]
    surviving_connections = [x for x in network.get_connections() if x not in network.get_removed_connections()]
    plt.title("Full network")
    plt.xticks([])
    plt.yticks([])

    plt.figure(2)
    plot_network(surviving_nodes, surviving_connections, network)
    plt.title("Local repair executed")
    plt.xticks([])
    plt.yticks([])


def test_different_routing_metrics(network: Network):
    dao_messages = network.get_dao_messages()
    connections = dao_messages.values()
    for i in connections:
        connection = i[1]
        from_x = connection.get_node_from().get_X()
        from_y = connection.get_node_from().get_Y()
        to_x = connection.get_node_to().get_X()
        to_y = connection.get_node_to().get_Y()
        plt.plot([from_x, to_x], [from_y, to_y], 'k', linewidth=0.1 / math.log10(connection.get_ETX() + 0.03))
    for i in network.get_nodes():
        x = i.get_X()
        y = i.get_Y()
        plt.plot(x, y, 'ro', markersize=10)
        plt.annotate(i.get_rank(), (x + .07, y + .07), size=16, color="Orange")
    for node in dao_messages.keys():
        # Draw arrow
        receiver = dao_messages.get(node)[0]
        plt.annotate("", xytext=(node.get_X(), node.get_Y()), xy=(receiver.get_X(), receiver.get_Y()),
                     arrowprops=dict(arrowstyle="-|>, head_length = 0.8, head_width = .3", lw=1, color='k'))
    plt.xticks([])
    plt.yticks([])


def main():
    NEW_MESSAGES = 40  # Total number of customers
    INTERVAL_MESSAGES = 10  # Generate messages roughly every x seconds
    NUMBER_OF_NODES = 100  # amount of nodes in the network.
    NEIGHBOR_RADIUS = 1.5  # the range a node can see.
    net_type = 'rand'  # Type of network
    env = simpy.Environment()

    # initialize network with number of nodes placed on a grid:
    network = Network(env, no_of_nodes=NUMBER_OF_NODES, neighbor_radius=NEIGHBOR_RADIUS, network_type=net_type)

    # Run the simulation!
    env.process(network.source(NEW_MESSAGES, INTERVAL_MESSAGES))
    env.run()

    # Plot network!
    plt.figure(1)
    plot_network(network.get_nodes(), network.get_connections(), network)
    plt.show()


main()
