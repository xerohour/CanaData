import threading
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData

def test_distributed_stress_mock():
    # Mimic a system doing large concurrent ingestion, showing how time is blocked
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = []

    def worker(i):
        for j in range(200):
            # In a distributed system, a shared lock would represent network I/O or DB lock
            with scraper._menu_data_lock:
                scraper.allMenuItems.append({'id': f'{i}_{j}'})
                # Simulate tiny processing overhead
                time.sleep(0.0001)

    threads = []
    start_time = time.time()
    for i in range(20): # 20 workers
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start_time
    assert len(scraper.allMenuItems) == 4000
    print(f"Stress test completed 4000 entities in {duration:.4f} seconds.")

if __name__ == '__main__':
    test_distributed_stress_mock()
