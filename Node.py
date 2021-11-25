import simpy
import random
import uuid

class Node:
    # constructor
    def __init__(self, rank: float, positionX: int, positionY: int):
        self.ID: uuid = uuid.uuid4()
        self.rank: float = rank  # initial rank
        self.positionX: int = positionX
        self.positionY: int = positionY

    def get_ID(self) -> uuid:
        return self.ID

    def get_rank(self) -> float:
        return self.rank

    def get_positionX(self) -> int:
        return self.positionX

    def get_positionY(self) -> int:
        return self.positionY

