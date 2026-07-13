import threading
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_stress_locking():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = []

    def worker(i):
        for j in range(100):
            with scraper._menu_data_lock:
                scraper.allMenuItems.append({'id': i * 100 + j})
            time.sleep(0.001)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(scraper.allMenuItems) == 1000
