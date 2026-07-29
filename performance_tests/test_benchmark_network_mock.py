import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CanaData import CanaData


def test_benchmark_network_mock(benchmark):
    def run_network():
        scraper = CanaData(interactive_mode=False)
        scraper.locations = [
            {"slug": f"test-loc-{i}", "type": "dispensary", "id": i} for i in range(10)
        ]

        # We mock the actual network call to simulate how the lock handles concurrent network tasks
        def mock_fetch(location):
            time.sleep(0.01)  # simulated network I/O
            with scraper._menu_data_lock:
                scraper.allMenuItems[location["id"]] = [{"name": "item"}]
            return True

        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            list(executor.map(mock_fetch, scraper.locations))

        return len(scraper.allMenuItems)

    result = benchmark(run_network)
    assert result == 10
