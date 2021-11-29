import math

from Node import Node
from Messages import DIO, DAO
import random
import numpy as np
from Connection import Connection


class Network:
    # constructor
    def __init__(self, no_of_nodes: int):
        self.noOfNodes: int = no_of_nodes
        self.nodes: [] = self.__define_nodes_in_network(no_of_nodes)
        self.neighbourRadius: float = 1.5
        self.connections: [] = self.__find_neighbours()

    # assign each node a random position and rank in the network
    # ToDO: make the rank not random.
    def __define_nodes_in_network(self, no_of_nodes) -> []:
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(i / (no_of_nodes / 10))
            rank = 0 #round(np.random.uniform(1, 10), 1)
            node = Node(rank, x, y)
            nodelist.append(node)
        return nodelist

    def __find_neighbours(self) -> []:
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
        root.set_rank(0)
        dio = DIO(DAGRank=root.get_rank())
        all_connections = self.connections
        neighbours = []
        for i in all_connections:
            if i.get_node_from() == root:
                neighbours.append(i.nodeTo)
        # Nu sender vi
        for i in neighbours:
            if not i.isBusy:
                i.receive_message(dio)
        pass

        # Send_DAO creates a DAO message with a DAO rank and an instanceID
        # send_DAO can only send DAO messages upwards or to the sides.
        # if a DAO message had been received from the sides (neighbor) it can only send upwards.
        # Sends to the parent (lower rank) with the lowest ETX.
        # When a 'send' has been successful, it receives a DAO_ACK (true if successful false otherwise)
        # TODO: create "findBestParent" algorithm based on multiple factors (better objective function).

    def send_DAO(self, dao: DAO):
        # is the node the
        rank_from = dao.get_rank() # rank of the from node.
        this_node = None
        for node in self.get_nodes():
            if node.get_ID() == dao.get_node_ID():
                this_node = node

        dao_new = DAO(this_node.get_rank(), this_node.get_ID())

        print("node: ", this_node.get_ID())
        # determine who to send to!
        neighbors_ETX = []
        neighbor_connections = []
        for i in self.connections:
            if i.nodeFrom.get_ID() == this_node.get_ID() and i.nodeTo.get_rank() < rank_from:
                neighbors_ETX.append(i.get_ETX())
                neighbor_connections.append(i)
                print(f"we have a neighbor! with rank going from => {rank_from} to {i.nodeTo.get_rank()}")

        # is the sender node a neighbor (= equal rank) send to parent only
        # is the sender a child ( higher rank) send to parent OR neighbor
        for connection in neighbor_connections:
            if connection.get_ETX() == min(neighbors_ETX):
                connection.nodeTo.receive_message_DAO(dao_new)
                return connection.nodeTo
        return




    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections

# Define an ETX between each connection.
# To simplify it is set at random between 1 and 3.
