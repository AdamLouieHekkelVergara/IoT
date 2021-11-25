import random
import uuid


class Node:
    # constructor
    def __init__(self, rank: float, positionX: float, positionY: float):
        self.ID: uuid = uuid.uuid4()
        self.rank: float = rank  # initial rank
        self.positionX: float = positionX
        self.positionY: float = positionY

    def get_ID(self) -> uuid:
        return self.ID

    def get_rank(self) -> float:
        return self.rank

    def get_X(self) -> float:
        return self.positionX

    def get_Y(self) -> float:
        return self.positionY
