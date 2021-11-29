from Node import Node
import numpy as np

# Define an ETX between each connection.
# To simplify it is set at random between 1 and 3.


class Connection:
    # constructor
    def __init__(self, ETX: float, node_from: Node, node_to: Node):
        self.ETX: float = round(np.random.uniform(1, 3),
                                2)  # should probably be random => round(random.uniform(1, 3), 2)
        self.nodeFrom: Node = node_from
        self.nodeTo: Node = node_to

    def get_ETX(self) -> float:
        return self.ETX

    def get_node_from(self) -> Node:
        return self.nodeFrom

    def get_node_to(self) -> Node:
        return self.nodeTo
