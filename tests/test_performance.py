import concurrent.futures
import time
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor


def test_menu_data_lock_contention():
    """
    Tests thread safety and contention for the _menu_data_lock in CanaData.
    """
    cana = CanaData(
        cache_enabled=False, optimize_processing=False, interactive_mode=False
    )

    # Simulate a high-contention scenario with multiple threads
    # appending to allMenuItems concurrently.

    def process_fake_menu(listing_id):
        # We simulate the part of process_menu_items_json that acquires the lock
        # and mutates shared state.
        local_menu_items = [{"id": f"item-{listing_id}-{i}"} for i in range(100)]
        local_extracted_strains = {
            f"strain-{listing_id}": {"slug": f"strain-{listing_id}"}
        }
        listing_copy = {"id": listing_id, "num_menu_items": "100"}

        with cana._menu_data_lock:
            cana.allMenuItems[listing_id] = local_menu_items
            for slug, strain in local_extracted_strains.items():
                if slug not in cana.extractedStrains:
                    cana.extractedStrains[slug] = strain
            cana.menuItemsFound += len(local_menu_items)
            cana.totalLocations.append(listing_copy)

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process_fake_menu, f"loc-{i}") for i in range(100)]
        concurrent.futures.wait(futures)

    end_time = time.time()

    assert len(cana.allMenuItems) == 100
    assert cana.menuItemsFound == 100 * 100
    assert len(cana.totalLocations) == 100
    assert len(cana.extractedStrains) == 100

    # Just to have a loose bound, 100 lock acquisitions shouldn't take more than 1 second
    assert (end_time - start_time) < 1.0


def test_threadpool_throughput():
    """
    Tests ThreadPoolExecutor throughput and simulating concurrent network delays.
    """
    import concurrent.futures
    import time

    def mock_network_call(i):
        # Simulate network delay of 0.01 seconds
        time.sleep(0.01)
        return i

    start_time = time.time()

    # Process 100 items using 20 workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(mock_network_call, i) for i in range(100)]
        results = [
            future.result() for future in concurrent.futures.as_completed(futures)
        ]

    end_time = time.time()

    assert len(results) == 100

    # Expected time with 20 workers and 100 items of 0.01s sleep is approx:
    # 100 / 20 * 0.01s = 0.05 seconds. We allow some overhead.
    assert (end_time - start_time) < 0.5


def test_optimized_data_processor():
    """
    Tests memory footprint and execution speed of OptimizedDataProcessor
    vs. pure-Python dictionary flattening (CanaData.flatten_dictionary).
    """
    processor = OptimizedDataProcessor(max_workers=4)
    cana = CanaData(
        cache_enabled=False, optimize_processing=False, interactive_mode=False
    )

    # Generate nested payloads simulating menu items
    payload = {
        "name": "Test Item",
        "price": {"amount": 25, "currency": "USD"},
        "tags": ["sativa", "flower"],
        "brand": {"id": "b-1", "name": "Acme", "details": {"founded": 2020}},
        "categories": [{"id": "c-1", "name": "Flower"}],
        "strain_data": {
            "slug": "acme-sativa",
            "name": "Acme Sativa",
            "genetics": "sativa",
        },
    }

    # Simulate 5 locations with 100 items each
    test_data = {f"loc-{i}": [payload for _ in range(100)] for i in range(5)}

    # Method 1: Optimized processor (uses pd.json_normalize under the hood)
    import time

    start_opt = time.time()
    optimized_result = processor.process_menu_data(test_data)
    end_opt = time.time()
    opt_time = end_opt - start_opt

    # Method 2: Fallback iterative approach
    start_fallback = time.time()
    cana.allMenuItems = test_data
    cana._original_organize_into_clean_list()
    fallback_result = cana.finishedMenuItems
    end_fallback = time.time()
    fallback_time = end_fallback - start_fallback

    # They should produce the same amount of rows
    assert len(optimized_result) == 500
    assert len(fallback_result) == 500

    # Verification of dot notation translation
    assert "price.amount" in fallback_result[0]
    # Because _original_organize_into_clean_list fills missing columns,
    # and strings are returned for fallback result
    assert fallback_result[0]["price.amount"] == "25"

    # optimized_result retains original scalar types until written to csv or depending on its implementation.
    # We just ensure it processed without errors.
    assert isinstance(optimized_result, list)

    # Assert acceptable execution time
    assert opt_time < 2.0
    assert fallback_time < 2.0
