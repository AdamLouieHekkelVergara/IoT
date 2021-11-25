import math

from Node import Node
from Messages import DIO, DAO
import random
import numpy as np


class Network:
    # constructor
    def __init__(self, no_of_nodes: int):
        self.noOfNodes: int = no_of_nodes
        self.nodes: [] = self.__define_nodes_in_network(no_of_nodes)
        self.neighbourRadius: float = 1.5

    # assign each node a random position and rank in the network
    # ToDO: make the rank not random.
    def __define_nodes_in_network(self, no_of_nodes):
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(i / (no_of_nodes / 10))
            rank = round(random.uniform(1, 4), 2)
            node = Node(rank, x, y)
            nodelist.append(node)
        return nodelist

    def find_neighbours(self):
        connections = []
        nodes = self.nodes
        for i in nodes:
            for j in nodes:
                if i.get_ID() == j.get_ID():
                    continue
                dist = math.sqrt((i.get_X() - j.get_X()) ** 2 + (i.get_Y() - j.get_Y()) ** 2)
                if dist <= self.neighbourRadius:
                    connection = Connection(ETX=1, node_from=i, node_to=j)
                    connections.append(connection)
        return connections

    def send_DIO(self):
        root = self.nodes[0]  # Just pick root as the first node for now
        dio = DIO(DAGRank=0)
        pass

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes


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
