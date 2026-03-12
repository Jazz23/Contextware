import logging
import time
from .base import Broker, Task

logger = logging.getLogger(__name__)

class Worker:
    def __init__(self, broker: Broker, registry: dict):
        self.broker = broker
        self.registry = registry

    def run(self):
        logger.info("Worker started...")
        while True:
            task = self.broker.pop()
            if task:
                self.process_task(task)
            else:
                time.sleep(1)

    def process_task(self, task: Task):
        func = self.registry.get(task.name)
        if not func:
            logger.error(f"Task {task.name} not registered!")
            self.broker.nack(task.id, requeue=False)
            return

        try:
            func(*task.args, **task.kwargs)
            self.broker.ack(task.id)
        except Exception as e:
            logger.error(f"Task {task.id} failed: {e}")
            if task.retries < task.max_retries:
                task.retries += 1
                self.broker.push(task)
            else:
                # TODO: Implement Dead Letter Queue (DLQ)
                logger.warning(f"Task {task.id} exceeded max retries. Dropping...")
                self.broker.nack(task.id, requeue=False)
