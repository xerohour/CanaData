import os
import sys
import psutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_memory_growth():
    scraper = CanaData(interactive_mode=False)
    process = psutil.Process(os.getpid())

    initial_mem = process.memory_info().rss

    # Simulate adding data in loop
    for i in range(5000):
        with scraper._menu_data_lock:
            scraper.allMenuItems.setdefault("test_listing", []).append({'item_id': i, 'price': 10})

    final_mem = process.memory_info().rss
    mem_diff_mb = (final_mem - initial_mem) / (1024 * 1024)

    print(f"\nMemory growth: {mem_diff_mb:.2f} MB")
    assert mem_diff_mb < 20.0
