import uuid
from Version2.messages import DIO, DAO



class Node:
    # constructor
    def __init__(self, env, rank: int, positionX: float, positionY: float):
        self.ID: uuid = uuid.uuid4()
        self.rank: int = rank  # initial rank
        self.positionX: float = positionX
        self.positionY: float = positionY

        self.env = env

    #
    def receive_message(self, message: DIO):
        new_rank = message.get_rank() + 1
        self.rank = new_rank

    # when called upon
    def receive_message_DAO(self, message: DAO):
        self.isBusy = True

    def send_message(self):
        new_DIO = DIO(self.rank)
        yield self.env.timeout(0.1)  # it takes 0.1 second to create a dio.
        print(f'message sent out at: {self.env.now}')
        #Network.send_to_neigbors(self.ID, new_DIO)

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
