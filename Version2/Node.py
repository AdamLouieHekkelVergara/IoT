import uuid
from Version2.Messages import DIO, DAO
import random
import numpy as np
import simpy


class Node(simpy.Resource):
    # constructor
    def __init__(self, env, max_capacity, rank: int, positionX: float, positionY: float):
        super().__init__(env, max_capacity)
        self.ID: uuid = uuid.uuid4()
        self.rank: int = rank  # initial rank
        self.positionX: float = positionX
        self.positionY: float = positionY
        self.env = env

    #
    def receive_message_DIO(self, message: DIO):
        # new_rank = message.get_rank() + 1
        # self.rank = new_rank
        yield self.env.timeout(np.random.randint(3, 10))  # it takes 500 milliseconds to process/receive a message
        print(f'At time {self.env.now}, message {message.get_ID()} was PROCESSED for node:    {self.get_ID()}')

    # when called upon
    def receive_message_DAO(self, message: DAO):
        self.isBusy = True

    def get_ID(self) -> uuid:
        return self.ID

    def get_rank(self) -> int:
        return self.rank

    def set_rank(self, rank):
        self.rank = rank

    def get_X(self) -> float:
        return self.positionX

    def get_Y(self) -> float:
        return self.positionY

    def set_status(self, is_busy: bool):
        self.isBusy = is_busy
