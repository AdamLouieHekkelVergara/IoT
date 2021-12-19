import uuid
from Version2.Messages import DIO, DAO
import random
import numpy as np
import simpy


class Node(simpy.PriorityResource):
    # constructor
    def __init__(self, env, max_capacity, rank: int, positionX: float, positionY: float):
        super().__init__(env, max_capacity)
        self.ID: uuid = uuid.uuid4()
        self.rank: int = rank  # initial rank
        self.positionX: float = positionX
        self.positionY: float = positionY
        self.env = env
        self.batteryPower: int = 9999
        self.last_transmitter_ID: Node = None  # Used for visualization of final DODAG

    # Receive message processes the received message. Change of rank and decrement of battery power happens here.
    def receive_message(self, message):
        if isinstance(message, DIO):
            processing_time = np.random.randint(3, 10)
            self.batteryPower -= processing_time
            yield self.env.timeout(processing_time)  # it takes 500 milliseconds to process/receive a message

            if message.get_rank() is None:
                pass
            else:  # The sender has a rank! Initially, we wait for root to send out rank 0.
                if self.get_rank() is None or message.get_rank() < self.get_rank():  # is it a better rank??
                    new_rank = message.get_rank() + 1
                    self.rank = new_rank
                else:
                    pass
        # TODO implement this.
        elif isinstance(message, DAO):
            self.last_transmitter_ID = message.get_node_ID()

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

    def get_battery_power(self) -> int:
        return self.batteryPower

    def set_battery_power(self, power: int):
        self.batteryPower = power

    def get_last_transmitter_ID(self):
        return self.last_transmitter_ID
