import pytest
import threading
import time
import os
import psutil
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

@pytest.fixture
def mock_menu_data():
    """Generates a large realistic payload representing menus for a state."""
    return {
        f"loc_{i}": [
            {
                "id": f"item_{j}",
                "name": f"Strain {j}",
                "price": {"amount": 10 + j, "currency": "USD"},
                "brand": {"name": f"Brand {j%3}", "id": j%3},
                "strain": {"type": "Indica", "slug": f"indica-{j}"}
            }
            for j in range(500)
        ]
        for i in range(10)
    }

def test_audit_high_concurrency(mock_menu_data):
    """
    STRESS TEST: High Concurrency
    Simulates many concurrent worker threads writing to the shared CanaData state.
    """
    scraper = CanaData(max_workers=50, interactive_mode=False)

    # Flatten mock data to simulate individual location responses
    items_to_process = []
    for loc_id, items in mock_menu_data.items():
        items_to_process.append((loc_id, {"data": {"menu_items": items}}))

    # Multiply to simulate high load
    items_to_process = items_to_process * 5 # 50 simulated locations

    def worker_task(loc_data_tuple):
        loc_id, data = loc_data_tuple
        location = {"id": loc_id, "slug": f"slug-{loc_id}", "type": "dispensary"}
        scraper.process_menu_items_json(data, location)

    threads = []
    start_time = time.time()

    for item in items_to_process:
        t = threading.Thread(target=worker_task, args=(item,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    # Verify data integrity
    assert len(scraper.allMenuItems) == 10 # We re-used 10 loc_ids
    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 5000 # 10 locs * 500 items (assignments overwrite rather than append)

    print(f"\nConcurrency test processed {total_items} items in {end_time - start_time:.2f}s")


def test_audit_memory_leak(mock_menu_data):
    """
    STRESS TEST: Memory Leak Detection
    Processes multiple large batches to ensure memory doesn't continuously grow.
    """
    processor = OptimizedDataProcessor(max_workers=4)
    process = psutil.Process(os.getpid())

    # Warmup
    _ = processor.process_menu_data(mock_menu_data)

    initial_memory = process.memory_info().rss

    for _ in range(20):
        # We need to deep copy or regenerate to avoid optimizing away
        data = {k: v[:] for k, v in mock_menu_data.items()}
        result = processor.process_menu_data(data)
        assert len(result) == 5000

    final_memory = process.memory_info().rss
    memory_diff_mb = (final_memory - initial_memory) / (1024 * 1024)

    print(f"\nMemory growth over 20 iterations: {memory_diff_mb:.2f} MB")

    # Allow small growth for caching/interning, but shouldn't be massive
    assert memory_diff_mb < 50.0


def test_audit_latency_throughput(benchmark, mock_menu_data):
    """
    BENCHMARK: Latency and Throughput of Data Flattening
    """
    processor = OptimizedDataProcessor(max_workers=4)

    # Ensure it's working
    res = processor.process_menu_data(mock_menu_data)
    assert len(res) == 5000

    # Benchmark the processing pipeline
    result = benchmark(processor.process_menu_data, mock_menu_data)

    assert len(result) == 5000
