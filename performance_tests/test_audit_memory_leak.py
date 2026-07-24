import gc
import os

import psutil

from optimized_data_processor import OptimizedDataProcessor


def test_memory_leak_processor():
    process = psutil.Process(os.getpid())
    gc.collect()
    start_memory = process.memory_info().rss

    processor = OptimizedDataProcessor(max_workers=2)
    large_menu = {
        "loc1": [
            {"id": str(i), "name": f"Item {i}", "nested": {"level1": {"level2": {"value": i}}}} for i in range(10000)
        ]
    }

    processor.process_menu_data(large_menu)

    gc.collect()
    end_memory = process.memory_info().rss

    memory_diff = end_memory - start_memory
    print(f"Memory diff: {memory_diff / 1024 / 1024} MB")
    assert memory_diff < 200 * 1024 * 1024
