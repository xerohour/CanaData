import os
import sys
import time
import threading
import json
import responses

# Ensure root directory is in path for imports to work during CI
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData

@responses.activate
def test_concurrent_network_failures_and_retries():
    scraper = CanaData(interactive_mode=False)

    # We'll test the actual endpoint scraper uses for legacy fallback:
    # f'https://weedmaps.com/api/web/v1/listings/{location_slug}/menu?type={location_type}'

    # Setup mock responses
    responses.add(
        responses.GET,
        "https://weedmaps.com/api/web/v1/listings/success-slug/menu?type=dispensary",
        json={"listing": {"id": "1", "slug": "success-slug", "_type": "dispensary"}, "categories": []},
        status=200
    )

    responses.add(
        responses.GET,
        "https://weedmaps.com/api/web/v1/listings/fail-slug/menu?type=dispensary",
        json={"error": "Internal Server Error"},
        status=500
    )

    # Because _fetch_discovery_menu_items uses discovery API and we want to test fallback,
    # we need to ensure the discovery API fails so it falls back to the legacy endpoint above.
    responses.add(
        responses.GET,
        "https://api-g.weedmaps.com/discovery/v1/listings/dispensary/success-slug/menu_items?page_size=100&size=100",
        json={"error": "Not Found"},
        status=404
    )

    responses.add(
        responses.GET,
        "https://api-g.weedmaps.com/discovery/v1/listings/dispensary/fail-slug/menu_items?page_size=100&size=100",
        json={"error": "Not Found"},
        status=404
    )

    success_location = {"slug": "success-slug", "type": "dispensary", "id": "1"}
    fail_location = {"slug": "fail-slug", "type": "dispensary", "id": "2"}

    results = []

    def worker(location):
        res = scraper._fetch_and_process_menu(location)
        results.append(res)

    threads = []
    for _ in range(10):
        t1 = threading.Thread(target=worker, args=(success_location,))
        t2 = threading.Thread(target=worker, args=(fail_location,))
        threads.append(t1)
        threads.append(t2)
        t1.start()
        t2.start()

    for t in threads:
        t.join()

    # We expect 10 True (successes) and 10 False (failures)
    successes = [r for r in results if r is True]
    failures = [r for r in results if r is False]

    assert len(successes) == 10
    assert len(failures) == 10


def test_stateful_noisy_neighbor_lock_contention():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = []

    def worker(i, sleep_time):
        for j in range(50):
            with scraper._menu_data_lock:
                # Simulate some small work holding the lock
                scraper.allMenuItems.append({'id': i * 100 + j})
                time.sleep(sleep_time)

    def run_stress_test(num_threads, lock_hold_time):
        scraper.allMenuItems = []
        threads = []
        start_time = time.time()
        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i, lock_hold_time))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return time.time() - start_time

    # Baseline with 5 threads
    baseline_duration = run_stress_test(5, 0.0001)

    # High contention with 50 threads
    high_contention_duration = run_stress_test(50, 0.0001)

    print(f"\nLock Contention Test:")
    print(f"Baseline (5 threads) duration: {baseline_duration:.4f} seconds")
    print(f"High contention (50 threads) duration: {high_contention_duration:.4f} seconds")
    print(f"Degradation factor: {high_contention_duration / baseline_duration:.2f}x")

    # The high contention duration should be significantly longer due to waiting on locks
    assert high_contention_duration > baseline_duration
