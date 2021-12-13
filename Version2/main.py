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
    NEW_MESSAGES = 2 # Total number of customers
    INTERVAL_MESSAGES = 10  # Generate messages roughly every x seconds

    env = simpy.Environment()
    # initialize network with number of nodes placed on a grid:
    network = Network(env, 3)

    # plot the initial network!
    plot_network(network.get_nodes(), network.get_connections())


    env.process(network.source(NEW_MESSAGES,INTERVAL_MESSAGES))
    env.run()

    # plot network after
    plot_network(network.get_nodes(), network.get_connections())


main()

