import uuid


# DIO messages
class DIO:
    # constructor
    # has 4 variables: DAGRank, DAGID
    def __init__(self, DAGRank: int):
        self.DAGRank: int = DAGRank
        self.DAGID: uuid = uuid.uuid4()

    def get_rank(self) -> int:
        return self.DAGRank

    def get_ID(self) -> uuid:
        return self.DAGID


# Dao messages
class DAO:
    # constructor
    # has 4 variables: DAGRank, DAGID
    def __init__(self, DAORank: int, nodeID):
        self.DAORank: int = DAORank  # is the rank of the node issuing the message.
        self.InstanceID: uuid = uuid.uuid4()
        self.NodeID = nodeID

    def get_rank(self) -> int:
        return self.DAORank

    def get_ID(self) -> uuid:
        return self.InstanceID

    def get_node_ID(self) -> uuid:
        return self.NodeID