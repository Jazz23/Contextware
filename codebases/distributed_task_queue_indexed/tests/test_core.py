import pytest
from unittest.mock import MagicMock
from codebases.distributed_task_queue.src.core.base import Task, Broker
from codebases.distributed_task_queue.src.core.engine import Worker

def test_worker_processes_task():
    broker = MagicMock(spec=Broker)
    task = Task(id="1", name="add", args=[1, 2])
    broker.pop.side_effect = [task, None]
    
    registry = {"add": lambda x, y: x + y}
    worker = Worker(broker, registry)
    
    # Run one iteration manually
    worker.process_task(task)
    
    broker.ack.assert_called_with("1")

def test_worker_retries_on_failure():
    broker = MagicMock(spec=Broker)
    task = Task(id="1", name="fail", retries=0, max_retries=1)
    broker.pop.side_effect = [task, None]
    
    def fail_task():
        raise Exception("Failure")
    
    registry = {"fail": fail_task}
    worker = Worker(broker, registry)
    
    worker.process_task(task)
    
    # Should push back to broker for retry
    broker.push.assert_called()
    assert task.retries == 1
