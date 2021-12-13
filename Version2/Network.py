import random
import uuid

from Version2.Messages import DIO, DAO
from Version2.Node import Node
from Version2.Connection import Connection
import numpy as np
import math


class Network:
    # constructor
    def __init__(self, env, no_of_nodes: int):
        self.noOfNodes: int = no_of_nodes
        self.env = env
        self.nodes: [] = self.__define_nodes_in_network(no_of_nodes)
        self.neighbourRadius: float = 15  # 1.5
        self.connections = self.__initialize_neighbours()

    def source(self, amountOfMessages, interval):
        """Source generates messages randomly"""
        for i in range(amountOfMessages):
            # make a random node from the network send a random message.
            for node in self.nodes:
                # Request the node : wait for the node to become available
                with node.request() as req:
                    yield req
                    ## TODO (maybe randomly) shift between call 'send_message_dio' and 'send_message_dao'!
                    booleans: [] = [self.send_message_DIO(node, i), self.send_message_DAO(node, i)]
                    send_message = random.choice(booleans)
                    self.env.process(random.choice(send_message))
            t = interval  # TODO implement a trickle timer function instead of using t!
            yield self.env.timeout(t)  # wait time 't' before sending a new message.

    def send_message_DIO(self, node, message_number: int):
        ## Create new DIO message
        print(f'At time {self.env.now}, DIO message {message_number} is being CREATED for node: {node.ID}')
        message = DIO(node.get_rank(), message_number)
        yield self.env.timeout(np.random.randint(1, 10))  # it takes between 1 and 10  seconds to create a dio.
        print(f'At time {self.env.now}, DIO message {message_number} was CREATED for node: {node.ID}')

        for neighbor in self.__find_neighbours(node.get_ID()):  # get all neighbors
            # request neighboring Node from the environment!
            with neighbor.request() as req:
                # Say: Get the node before we timeout!
                results = yield req | self.env.timeout(3)  ## renege after timeout time.
                if req in results:
                    # if this is not None => We got the node!!
                    self.__get_connection_between(node, neighbor).successful_transmission()

                    # We now sent out, by calling the Nodes "receive_message method":
                    print(
                        f'At time {self.env.now}, {type(message).__name__} message {message_number} was SENT OUT for node: {node.get_ID()} to Node:   {neighbor.get_ID()}')
                    print(
                        f'At time {self.env.now}, {type(message).__name__} message {message_number} was SENT OUT for node: {node.get_ID()} to '
                        f'Node:   {neighbor.get_ID()}')
                    # TODO: Calling the receive_message, should also change the rank!
                    yield self.env.process(neighbor.receive_message(message))

                else:
                    # We  did not succesfully get a node before timeout! => reneged
                    # TODO: Count the number of times reneged, and maybe use this for a ETX metrix?
                    self.__get_connection_between(node, neighbor).failed_transmission()
                    print(
                        f'At time {self.env.now}, node: {node.get_ID()} RENEGED  as it could not send message to: {neighbor.get_ID()}')

    # TODO: Implement this method also:
    def send_message_dao(self, node: Node, message_number: int):
        # Check for Node rank.
        if node.get_rank() is None:
            print(
                f'At time {self.env.now}, Node {node.get_ID()} has no parents to send to')
            pass  # if Node doesnt have a rank, it does not know who to send to, as no parents are present.
        else:
            dao = DAO(node.get_rank(),message_number)
            # determine who to sent to based on objective function in Connection:
            node_to: Node = self.objective_function(node)
            node_to.receive_message(dao)
            pass

    ## return the best node, based on some routing metrix.
    def objective_function(self, node) -> Node:
        neighbor_nodes: [] = self.__find_neighbours(node.get_ID())

    ## returns a list of nodes containing neighbors.
    def __find_neighbours(self, node_id: uuid) -> []:
        all_connections = self.connections
        neighbours = []
        for i in all_connections:
            if i.get_node_from().get_ID() == node_id:
                neighbours.append(i.nodeTo)
        return neighbours

    # assign each node a random position and rank in the network
    def __define_nodes_in_network(self, no_of_nodes) -> []:
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(i / (no_of_nodes / 10))
            rank = None
            max_capacity = 1
            node = Node(self.env, max_capacity, rank, x, y)
            nodelist.append(node)
        nodelist[0].set_rank(0)  # define node 0 to be root
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
                    connection = Connection(node_from=i, node_to=j)
                    connections.append(connection)
        return connections

    def __find_nodes_with_rank(self, rank: int):
        nodes_with_rank = []
        for i in self.nodes:
            if i.get_rank() == rank:
                nodes_with_rank.append(i)
        return nodes_with_rank

    def __find_nodes_with_id(self, node_ID: uuid):
        for node in self.get_nodes():
            if node.get_ID() == node_ID:
                return node
        return

    def __get_connection_between(self, node1: Node, node2: Node) -> Connection:
        for connection in self.connections:
            if connection.get_node_from().get_ID() == node1.get_ID() and connection.get_node_to().get_ID() == node2.get_ID():
                return connection

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections

    def get_env(self):
        return self.env
