import json
import os
import sys
import psutil
import time

# Ensure root directory is in path for imports to work during CI
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData


def test_memory_and_cpu_utilization(benchmark):
    sample_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    # We will simulate processing multiple batches to see memory jump
    workload = [data] * 5  # Simulate processing 5 large menu payloads

    def run_workload():
        process = psutil.Process()

        # Take initial snapshots
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_times()

        scraper = CanaData(interactive_mode=False)

        for payload in workload:
            # Note: Memory instructs capturing returned dict and calling _merge_menu_result.
            # However, the current code in CanaData mutates state directly and doesn't return a dict.
            # We will call it directly but we add the hook just in case the architecture shifts during testing.
            result = scraper.process_menu_items_json(payload, {'slug': 'test-location'})
            if result is not None and hasattr(scraper, '_merge_menu_result'):
                scraper._merge_menu_result(result)

        end_memory = process.memory_info().rss
        end_cpu = process.cpu_times()

        mem_diff_mb = (end_memory - start_memory) / (1024 * 1024)
        cpu_diff_user = end_cpu.user - start_cpu.user

        print(f"\nResource Utilization:")
        print(f"Memory increase: {mem_diff_mb:.2f} MB")
        print(f"CPU User Time increase: {cpu_diff_user:.4f} seconds")

        return mem_diff_mb

    result = benchmark(run_workload)
    # Just checking it doesn't crash
    assert result is not None
