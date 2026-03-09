import abc
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Task(BaseModel):
    id: str
    name: str
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}
    retries: int = 0
    max_retries: int = 3
    priority: int = 0

class Broker(abc.ABC):
    @abc.abstractmethod
    def push(self, task: Task):
        pass

    @abc.abstractmethod
    def pop(self) -> Optional[Task]:
        pass

    @abc.abstractmethod
    def ack(self, task_id: str):
        pass

    @abc.abstractmethod
    def nack(self, task_id: str, requeue: bool = True):
        pass
