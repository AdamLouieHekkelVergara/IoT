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
        self.connections = self.__initialize_neighbours()

    # assign each node a random position and rank in the network
    # ToDO: make the rank not random.
    def __define_nodes_in_network(self, no_of_nodes):
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(i / (no_of_nodes / 10))
            rank = 0  # round(random.uniform(1, 4), 2)
            node = Node(rank, x, y)
            nodelist.append(node)
        return nodelist

    # Neighbour finding algorithm
    def __initialize_neighbours(self):
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

    def generate_ranks(self, root: Node):
        current_rank = 0
        nodes_with_current_rank = [root]
        while len(nodes_with_current_rank) > 0:
            for i in nodes_with_current_rank:
                dio = DIO(DAGRank=i.get_rank())
                neighbours = self.__find_neighbours(i)
                for j in neighbours:
                    if j.get_rank() == 0:   # Only send DIO if receiver have not yet received a DIO
                        j.receive_message(dio)
            current_rank += 1
            nodes_with_current_rank = self.__find_nodes_with_rank(current_rank)
        root.set_rank(0)

    def __find_nodes_with_rank(self, rank: int):
        nodes_with_rank = []
        for i in self.nodes:
            if i.get_rank() == rank:
                nodes_with_rank.append(i)
        return nodes_with_rank

    def __find_neighbours(self, node: Node):
        all_connections = self.connections
        neighbours = []
        for i in all_connections:
            if i.get_node_from() == node:
                neighbours.append(i.nodeTo)
        return neighbours

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections


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
