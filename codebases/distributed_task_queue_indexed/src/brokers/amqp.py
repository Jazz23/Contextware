import json
import pika
from .base import Broker, Task
from typing import Optional

class AMQPBroker(Broker):
    def __init__(self, host: str, queue_name: str):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name)

    def push(self, task: Task):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=task.model_dump_json()
        )

    def pop(self) -> Optional[Task]:
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            return Task.model_validate_json(body)
        return None

    def ack(self, task_id: str):
        # basic_get requires manual ack but we don't have delivery_tag here in this simple mock
        pass

    def nack(self, task_id: str, requeue: bool = True):
        pass
