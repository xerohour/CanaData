import time
from unittest.mock import patch
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
from concurrent_processor import ConcurrentMenuProcessor

def generate_mock_locations(num_locations=100):
    locations = []
    for i in range(num_locations):
        locations.append({
            'id': f'loc-{i}',
            'wmid': f'wmid-{i}',
            'slug': f'test-slug-{i}',
            'type': 'dispensary',
            'name': f'Dispensary {i}'
        })
    return locations

def mock_process_menu_items(location):
    # Simulate processing time for fetching and parsing menu items
    time.sleep(0.01) # Simulate network latency
    return {
        'id': location['id'],
        'items_count': 1000
    }

def test_menu_fetching_latency_sequential():
    """Benchmark sequential menu fetching"""
    cana = CanaData()
    cana.locations = generate_mock_locations(20) # 20 locations
    cana.NonGreenState = False

    start_time = time.time()

    with patch.object(cana, '_fetch_and_process_menu', side_effect=mock_process_menu_items):
        with patch.object(cana, 'organize_into_clean_list'): # Skip organizing for this test
            cana._getMenusSequential()

    sequential_time = time.time() - start_time
    print(f"\nSequential Fetching Time: {sequential_time:.4f}s")

def test_menu_fetching_latency_concurrent():
    """Benchmark concurrent menu fetching"""
    cana = CanaData(max_workers=10, rate_limit=0) # No rate limit for benchmark
    cana.locations = generate_mock_locations(20)
    cana.NonGreenState = False

    start_time = time.time()

    with patch.object(cana, '_fetch_and_process_menu', side_effect=mock_process_menu_items):
        with patch.object(cana, 'organize_into_clean_list'): # Skip organizing for this test
            cana._getMenusConcurrent()

    concurrent_time = time.time() - start_time
    print(f"\nConcurrent Fetching Time: {concurrent_time:.4f}s")

def test_flattening_throughput_original():
    """Benchmark original flattening algorithm"""
    cana = CanaData()

    # Generate mock data
    all_menu_items = {}
    for i in range(50): # 50 locations
        items = []
        for j in range(200): # 200 items each = 10,000 items
            items.append({
                'id': f'item-{i}-{j}',
                'name': f'Test Product {j}',
                'price': {'amount': 50, 'currency': 'USD'},
                'tags': ['indica', 'flower'],
                'strain': {'name': 'OG', 'slug': 'og-kush'}
            })
        all_menu_items[f'loc-{i}'] = items

    cana.allMenuItems = all_menu_items

    start_time = time.time()
    cana._original_organize_into_clean_list()
    original_time = time.time() - start_time

    print(f"\nOriginal Flattening Time (10k items): {original_time:.4f}s")

def test_flattening_throughput_optimized():
    """Benchmark optimized flattening algorithm"""
    processor = OptimizedDataProcessor(max_workers=4)

    # Generate mock data
    all_menu_items = {}
    for i in range(50):
        items = []
        for j in range(200):
            items.append({
                'id': f'item-{i}-{j}',
                'name': f'Test Product {j}',
                'price': {'amount': 50, 'currency': 'USD'},
                'tags': ['indica', 'flower'],
                'strain': {'name': 'OG', 'slug': 'og-kush'}
            })
        all_menu_items[f'loc-{i}'] = items

    start_time = time.time()
    _ = processor.process_menu_data(all_menu_items)
    optimized_time = time.time() - start_time

    print(f"\nOptimized Flattening Time (10k items): {optimized_time:.4f}s")

def test_high_concurrency_workers():
    """Test behavior with high concurrency limits to identify thread contention"""
    # 50 workers, no rate limiting
    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0)

    locations = generate_mock_locations(100) # 100 locations

    def process_func(location):
        time.sleep(0.01) # Small sleep to simulate minimal IO
        return {'status': 'success', 'slug': location['slug']}

    start = time.time()
    results = processor.process_locations(locations, process_func)
    duration = time.time() - start

    assert len(results) == 100
    assert len(processor.errors) == 0
    # Expected duration is roughly ~0.02s since 100 tasks on 50 workers taking 0.01s each is ~2 waves
    print(f"\nHigh Concurrency Processing Time (100 items on 50 workers): {duration:.4f}s")


def test_retry_backoff_recovery():
    """Simulate API rate limits, 500 errors, and timeouts for retry_with_backoff"""
    from concurrent_processor import retry_with_backoff

    attempts = {'count': 0}

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=0.5)
    def flacky_request():
        attempts['count'] += 1
        if attempts['count'] < 3:
            raise Exception("Simulated 500 error")
        return "success"

    result = flacky_request()

    assert result == "success"
    assert attempts['count'] == 3


def test_thread_safety_fine_grained_locks():
    """Verify thread-safety of fine-grained locks in CanaData when updating shared state"""
    cana = CanaData()
    total_locations = 200
    items_per_location = 10

    import concurrent.futures
    import random

    def simulate_menu_processing(loc_id):
        # We construct a dummy JSON structure for process_menu_items_json
        dummy_json = {
            'data': {
                'menu_items': []
            }
        }

        # Add some items
        for i in range(items_per_location):
            dummy_json['data']['menu_items'].append({
                'name': f'Item {i} at {loc_id}',
                'strain_data': {'slug': f'strain-{random.randint(1, 10)}', 'name': 'Strain'}
            })

        location = {'id': loc_id, 'wmid': f'w-{loc_id}', 'slug': f'slug-{loc_id}', 'type': 'dispensary'}
        cana.process_menu_items_json(dummy_json, location)

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(simulate_menu_processing, f'loc-{i}') for i in range(total_locations)]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Verify state consistency
    assert len(cana.allMenuItems) == total_locations
    assert cana.menuItemsFound == total_locations * items_per_location
    assert len(cana.totalLocations) == total_locations
    # Ensure strains lock functioned correctly and deduped them
    assert len(cana.extractedStrains) <= 10
