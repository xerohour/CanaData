import logging
import os
from concurrent.futures import ThreadPoolExecutor

import psutil
import pytest

from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

logger = logging.getLogger(__name__)


def get_memory_usage() -> float:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB


@pytest.fixture
def mock_item_data():
    return {
        "id": "item123",
        "name": "Super Silver Haze",
        "price": {"price_grams": [{"grams": 1, "price": 15.0}]},
        "thc": "25%",
        "brand": {"name": "BestBrand"},
        "category": {"name": "Flower"},
    }


def test_audit_high_concurrency(benchmark, mock_item_data):
    """
    Stress tests the `_menu_data_lock` in CanaData to ensure thread safety
    and identify "noisy neighbor" stateful bottlenecks.
    """
    scraper = CanaData()
    num_threads = 50
    items_per_thread = 500

    def concurrent_worker(worker_id):
        items = []
        for i in range(items_per_thread):
            item = mock_item_data.copy()
            item["id"] = f"item_{worker_id}_{i}"
            items.append(item)

        # Simulate network delay parsing (outside the lock)
        # We don't want artificial delay inside the lock
        # as it will falsely trigger contention issues.

        with scraper._menu_data_lock:
            scraper.allMenuItems.extend(items)

    def run_stress():
        scraper.allMenuItems = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(concurrent_worker, i) for i in range(num_threads)
            ]
            for future in futures:
                future.result()

    # Benchmark the high concurrency execution
    benchmark.pedantic(run_stress, iterations=3, rounds=3)

    assert len(scraper.allMenuItems) == num_threads * items_per_thread


def test_audit_memory_leak():
    """
    Simulates repeated execution of the OptimizedDataProcessor to detect
    memory leaks in Pandas or internal structures during large batches.
    """
    processor = OptimizedDataProcessor()

    # Create large dummy batch
    batch_size = 5000
    iterations = 20

    dummy_data = {
        "loc1": [
            {
                "id": f"item{i}",
                "name": f"Product {i}",
                "price": {"price_grams": [{"grams": 1, "price": 10.0}]},
                "brand": {"name": "Brand X"},
                "category": {"name": "Category Y"},
            }
            for i in range(batch_size)
        ]
    }

    initial_memory = get_memory_usage()

    for _ in range(iterations):
        result = processor.process_menu_data(dummy_data)
        assert len(result) == batch_size

    final_memory = get_memory_usage()
    memory_diff = final_memory - initial_memory

    # Assert memory growth is within reasonable bounds (e.g., < 50MB)
    # Pandas caching or python garbage collection might hold some, but shouldn't leak linearly
    assert memory_diff < 50.0, f"Memory leak detected: grew by {memory_diff:.2f} MB"
    logger.info(f"Memory test passed: Growth was {memory_diff:.2f} MB")


def test_audit_latency_throughput(benchmark, mock_item_data):
    """
    Benchmarks latency and throughput of the optimized batch processor.
    """
    processor = OptimizedDataProcessor()

    # Create a decently sized batch
    batch = {"loc1": [mock_item_data.copy() for _ in range(1000)]}

    def run_batch():
        return processor.process_menu_data(batch)

    # Benchmark processing
    result = benchmark(run_batch)
    assert len(result) == 1000
