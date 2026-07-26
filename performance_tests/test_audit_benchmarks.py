import os
import threading

import psutil

from CanaData import CanaData


def test_flatten_benchmark(benchmark):
    scraper = CanaData()
    data = {"a": {"b": "c"}, "d": [{"e": "f"}]}
    result = benchmark(scraper.flatten_dictionary, data)
    assert result == {"a.b": "c", "d.e": "f"}

def test_memory_leak():
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss
    scraper = CanaData()
    for _ in range(100):
        scraper.flatten_dictionary({"a": {"b": "c" * 1000}, "d": [{"e": "f" * 1000}]})
    end_mem = process.memory_info().rss
    assert end_mem - start_mem < 10 * 1024 * 1024  # Less than 10MB growth

def test_concurrent_processing(benchmark):
    scraper = CanaData()
    scraper.allMenuItems = {}

    def worker():
        for i in range(100):
            with scraper._menu_data_lock:
                scraper.allMenuItems[f"worker_{threading.get_ident()}_{i}"] = [{"id": i, "val": "test"}]

    def run_workers():
        threads = []
        for _ in range(10):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    benchmark(run_workers)
