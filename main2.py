import matplotlib.pyplot as plt
from Network import Network

no_of_nodes = 110
network = Network(no_of_nodes)
nodes = network.get_nodes()
connections = network.get_connections()


print("x",nodes[0].get_X())
print("y",nodes[0].get_Y())
neighbours = network.send_DIO()
for i in neighbours:
    print(i.get_X())
    print(i.get_Y())

# PLOT NODES AND CONNECTIONS
for i in nodes:
    plt.plot(i.get_X(), i.get_Y(), 'ro')
for i in connections:
    from_x = i.get_node_from().get_X()
    from_y = i.get_node_from().get_Y()
    to_x = i.get_node_to().get_X()
    to_y = i.get_node_to().get_Y()
    plt.plot([from_x, to_x], [from_y, to_y], 'k')
plt.show()

