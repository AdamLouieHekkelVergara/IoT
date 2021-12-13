import matplotlib.pyplot as plt
import simpy
from Network import Network
from Node import Node


env = simpy.Environment()
no_of_nodes: int = 110
network = Network(env, no_of_nodes)
nodes = network.get_nodes()
connections = network.get_connections()

node = simpy.Resource(env, capacity=1)
env.process(Node.source(self=nodes[0], env=env, number=5, interval=10))
env.run()


# PLOT NODES AND CONNECTIONS
# for i in nodes:
#     x = i.get_X()
#     y = i.get_Y()
#     plt.plot(x, y, 'ro')
#     plt.annotate(i.get_rank(), (x, y))
# for i in connections:
#     from_x = i.get_node_from().get_X()
#     from_y = i.get_node_from().get_Y()
#     to_x = i.get_node_to().get_X()
#     to_y = i.get_node_to().get_Y()
#     plt.plot([from_x, to_x], [from_y, to_y], 'k')
# plt.show()
