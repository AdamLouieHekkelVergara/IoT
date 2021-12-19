from Version2.Node import Node


class Connection:
    # constructor
    def __init__(self, node_from: Node, node_to: Node):
        self.ETX: float = 2
        self.nodeFrom: Node = node_from
        self.nodeTo: Node = node_to
        self.successfulTransmissions = 0
        self.failedTransmissions = 0

    # Successful/failed transmission are used to calculate ETX of connection
    def successful_transmission(self):
        self.successfulTransmissions += 1
        self.__calculate_ETX()

    def failed_transmission(self):
        self.failedTransmissions += 1
        if self.successfulTransmissions > 0:  # To avoid division with 0
            self.__calculate_ETX()

    def __calculate_ETX(self):
        self.ETX = (self.successfulTransmissions + self.failedTransmissions) / self.successfulTransmissions

    def set_ETX(self, etx):
        self.ETX = etx

    def get_ETX(self) -> float:
        return self.ETX

    def get_node_from(self) -> Node:
        return self.nodeFrom

    def get_node_to(self) -> Node:
        return self.nodeTo
