from .base import Broker, Task
from typing import Optional

class RedisBroker(Broker):
    """
    TODO: Implement the RedisBroker.
    Use Redis lists (RPUSH/LPOP) for the queue.
    Use Redis hashes for tracking task metadata if needed.
    """
    def __init__(self, host: str, port: int, db: int = 0):
        # Implementation needed
        pass

    def push(self, task: Task):
        # Implementation needed
        pass

    def pop(self) -> Optional[Task]:
        # Implementation needed
        return None

    def ack(self, task_id: str):
        # Implementation needed
        pass

    def nack(self, task_id: str, requeue: bool = True):
        # Implementation needed
        pass
