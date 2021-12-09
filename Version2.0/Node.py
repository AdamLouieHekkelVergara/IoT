import uuid
from .Messages import DIO,DAO
import simpy


class Node(simpy.Resource):
    # constructor
    def __init__(self, rank: int, positionX: float, positionY: float, env, max_capacity: int):
        super().__init__(env, max_capacity)
        self.ID: uuid = uuid.uuid4()
        self.rank: int = rank  # initial rank
        self.positionX: float = positionX
        self.positionY: float = positionY
        self.isBusy: bool = False

    #
    def receive_message(self, message: DIO):
        self.isBusy = True
        new_rank = message.get_rank() + 1
        self.rank = new_rank
        # time_delay = np.random.uniform(0, 5/1000)
        # time.sleep(time_delay)
        self.isBusy = False

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
