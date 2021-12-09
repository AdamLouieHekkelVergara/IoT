import math
from Connection import Connection
from Node import Node
from Messages import DIO, DAO
import numpy as np
import uuid


class Network():
    # constructor
    def __init__(self, env, no_of_nodes: int):
        self.noOfNodes: int = no_of_nodes
        self.env = env
        self.nodes: [] = self.__define_nodes_in_network(no_of_nodes)
        self.neighbourRadius: float = 1.5
        self.connections = self.__initialize_neighbours()


    # assign each node a random position and rank in the network
    # ToDO: make the rank not random.
    def __define_nodes_in_network(self, no_of_nodes) -> []:
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(i / (no_of_nodes / 10))
            rank = 0
            node = Node(rank, x, y, self.get_env(), 1)
            nodelist.append(node)
        return nodelist

    # Neighbour finding algorithm
    def __initialize_neighbours(self) -> []:
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
        current_rank: int = 0
        nodes_with_current_rank = [root]
        while len(nodes_with_current_rank) > 0:
            for i in nodes_with_current_rank:
                dio = DIO(DAGRank=i.get_rank())
                neighbours = self.__find_neighbours(i.get_ID())
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

    def __find_neighbours(self, node_id: uuid):
        all_connections = self.connections
        neighbours = []
        for i in all_connections:
            if i.get_node_from().get_ID() == node_id:
                neighbours.append(i.nodeTo)
        return neighbours

    def __find_nodes_with_id(self, node_ID: uuid):
        for node in self.get_nodes():
            if node.get_ID() == node_ID:
                return node
        return
        # Send_DAO creates a DAO message with a DAO rank and an instanceID
        # send_DAO can only send DAO messages upwards or to the sides.
        # if a DAO message had been received from the sides (neighbor) it can only send upwards.
        # Sends to the parent (lower rank) with the lowest ETX.
        # When a 'send' has been successful, it receives a DAO_ACK (true if successful false otherwise)
        # TODO: create "findBestParent" algorithm based on multiple factors (better objective function).

    def send_DAO(self, dao: DAO):
        # find the Node from the DAO-message.
        this_node = self.__find_nodes_with_id(dao.get_node_ID())

        # determine who to send to from connections!
        neighbors_ETX = []
        neighbor_connections = []
        for i in self.connections:
            # name booleans
            is_rank_of_DAOReceiver_smaller: bool = i.nodeTo.get_rank() < this_node.get_rank()
            is_NodeID_equal: bool = i.nodeFrom.get_ID() == this_node.get_ID()
            if is_NodeID_equal and is_rank_of_DAOReceiver_smaller:
                neighbors_ETX.append(i.get_ETX())
                neighbor_connections.append(i)
                print(f"we have a neighbor! with rank: {i.nodeTo.get_rank()} and ETX: {i.get_ETX()}")

        # is the sender node a neighbor (= equal rank) send to parent only
        # is the sender a child ( higher rank) send to parent OR neighbor
        for connection in neighbor_connections:
            is_connection_with_lowest_ETX: bool = connection.get_ETX() == min(neighbors_ETX)
            if is_connection_with_lowest_ETX:
                with connection.nodeTo.request() as req:
                    results = yield req
                    if req in results:
                        # We got to Node
                        dao_new = DAO(this_node.get_rank(), this_node.get_ID())
                        connection.nodeTo.receive_message_DAO(dao_new)
                        print(
                        f"We choose the neighbor with rank: {connection.nodeTo.get_rank()} and ETX {connection.get_ETX()}")
                    return connection.nodeTo ## return the node we send to!
        return

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections

    def get_env(self):
        return self.env

