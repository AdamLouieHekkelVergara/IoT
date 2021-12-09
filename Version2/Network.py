from Version2.Messages import DIO
from Version2.Node import Node
import numpy as np
import random



class Network:
    # constructor
    def __init__(self, env, no_of_nodes: int):
        self.noOfNodes: int = no_of_nodes
        self.env = env
        self.nodes: [] = self.__define_nodes_in_network(no_of_nodes)
        self.neighbourRadius: float = 1.5
        # self.connections = self.__initialize_neighbours()

    def source(self, amountOfMessages, interval):
        """Source generates messages randomly"""
        for i in range(amountOfMessages):
            print(f'message {i} was created at time: {self.env.now}')
            # make a random node from the network send a random message.
            node = random.choice(self.nodes)
            self.env.process(node.send_message())
            t = random.expovariate(1.0 / interval)
            yield self.env.timeout(t)

    def send_to_neigbors(self, node_id: int, dio: DIO):
        print(f'A message was to neighbors send at time: {self.env.now}')

    # assign each node a random position and rank in the network
    def __define_nodes_in_network(self, no_of_nodes) -> []:
        nodelist = []
        for i in range(no_of_nodes):
            x = round(np.random.uniform(0, 10), 1)
            y = round(i / (no_of_nodes / 10))
            rank = 0
            node = Node(self.env, rank, x, y)
            nodelist.append(node)
        return nodelist

    def get_nodes(self) -> list:
        return self.nodes

    def get_nr_of_nodes(self) -> int:
        return self.noOfNodes

    def get_connections(self) -> list:
        return self.connections

    def get_env(self):
        return self.env
