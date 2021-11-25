import numpy as ns
from Node import Node
import random


class Network:
    # constructor
    def __init__(self, nr_of_nodes: int):
        self.nrOfNodes = nr_of_nodes
        self.nodes: [] = self.__define_nodes_in_network(nr_of_nodes)

    # assign each node a random position and rank in the network
    # ToDO: make the rank not random.
    def __define_nodes_in_network(self, nr_of_nodes):
        nodelist = []
        for i in range(nr_of_nodes):
            position_x: int = random.randint(0, 100)
            position_y: int = random.randint(0, 100)
            rank: float = round(random.uniform(1, 4), 2)
            node = Node(rank, position_x, position_y)
            nodelist.append(node)
        return nodelist

    def get_nr_of_nodes(self) -> int:
        return self.nrOfNodes


# Define an ETX between each connection.
# To simplify it is set at random between 1 and 3.


class Connection:
    # constructor
    def __init__(self, ETX: float, node_from: Node, node_to: Node):
        self.ETX: float = ETX  # should probably be random => round(random.uniform(1, 3), 2)
        self.nodeFrom: Node = node_from
        self.nodeTo: Node = node_to

    def get_ETX(self) -> float:
        return self.ETX

    def get_node_from(self) -> Node:
        return self.nodeFrom

    def get_node_to(self) -> Node:
        return self.nodeTo
