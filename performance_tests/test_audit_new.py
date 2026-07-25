import pytest
import threading
import time
import psutil
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

def test_memory_leak_flattening(benchmark):
    def run_memory_leak():
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        scraper = CanaData(interactive_mode=False)
        # simulate large memory assignment
        for i in range(100):
            scraper.allMenuItems[f"loc_{i}"] = [{"id": j, "price": 10.0, "amount": 1, "nested": {"a": 1, "b": 2}} for j in range(100)]
        from optimized_data_processor import OptimizedDataProcessor
        processor = OptimizedDataProcessor(max_workers=4)
        processor.process_menu_data(scraper.allMenuItems)
        mem_after = process.memory_info().rss
        return mem_after - mem_before

    result = benchmark(run_memory_leak)
    assert result is not None

def test_horizontal_scaling_concurrency(benchmark):
    def run_concurrency():
        processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)
        locations = [{'slug': f'loc_{i}'} for i in range(100)]
        def mock_process(loc):
            time.sleep(0.01) # Simulate network/IO
            return {"status": "ok"}

        results = processor.process_locations(locations, mock_process)
        return len(results)

    result = benchmark(run_concurrency)
    assert result == 100
