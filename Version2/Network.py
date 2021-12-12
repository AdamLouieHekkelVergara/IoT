import uuid

from Version2.Messages import DIO
from Version2.Node import Node
from Version2.Connection import Connection
import numpy as np
import random
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
                    self.env.process(self.send_message_dio(node, i))
            t = interval # TODO implement a trickle timer function instead of using t!
            yield self.env.timeout(t)  # wait time 't' before sending a new message.

    def send_message_dio(self, node, message_number: int):
        ## Create new DIO message
        print(f'At time {self.env.now}, message {message_number} is being CREATED for node: {node.ID}')
        dio = DIO(node.get_rank(), message_number)
        yield self.env.timeout(np.random.randint(1, 10))  # it takes between 1 and 10  seconds to create a dio.
        print(f'At time {self.env.now}, message {message_number} was CREATED for node: {node.ID}')

        for i in self.__find_neighbours(node.get_ID()):  # get all neighbors
            # request neighboring Node from the environment!
            with i.request() as req:
                # Say: Get the node before we timeout!
                results = yield req | self.env.timeout(3)  ## renege after timeout time.
                if req in results:
                    # if this is not None => We got the node!!

                    # We now sent out, by calling the Nodes "receive_message method":
                    print(f'At time {self.env.now}, message {message_number} was SENT OUT for node: {node.get_ID()} to Node:   {i.get_ID()}')
                    # TODO: Calling the receive_message, should also change the rank!
                    yield self.env.process(i.receive_message(dio))


                else:
                    # We  did not succesfully get a node before timeout! => reneged
                    # TODO: Count the number of times reneged, and maybe use this for a ETX metrix?
                    print(
                        f'At time {self.env.now}, node: {node.get_ID()} RENEGED  as it could not send message to: {i.get_ID()}')


    # TODO: Implement this method also:
    def send_message_dao(self, node: Node, message_number_int):
        pass


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
                    connection = Connection(ETX=1, node_from=i, node_to=j)
                    connections.append(connection)
        return connections

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections

    def get_env(self):
        return self.env
