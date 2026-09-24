import json
import os
import sys
import threading
import time
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_scaling_mock_message_queue(benchmark):
    """
    Simulates a message queue architecture where workers don't share a global lock for writing to memory.
    Workers write results to local queues, and a central consumer aggregates them asynchronously.
    """

    class MessageQueue:
        def __init__(self):
            self.queue = []
            self.lock = threading.Lock()

        def publish(self, item):
            with self.lock:
                self.queue.append(item)

        def consume_all(self):
            with self.lock:
                items = self.queue[:]
                self.queue = []
                return items

    def run_distributed_stress():
        mq = MessageQueue()
        aggregated_results = {}

        def stateless_worker(worker_id):
            local_results = {}
            for i in range(500):
                # Simulating work and local aggregation
                local_results[f"{worker_id}_{i}"] = [{'id': worker_id * 1000 + i, 'name': 'test'}]
            # Publish batch to queue
            mq.publish(local_results)

        threads = []
        for i in range(50):
            t = threading.Thread(target=stateless_worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Simulate consumer pulling from queue
        for batch in mq.consume_all():
            aggregated_results.update(batch)

        assert len(aggregated_results) == 25000
        return len(aggregated_results)

    result = benchmark(run_distributed_stress)
    assert result == 25000
