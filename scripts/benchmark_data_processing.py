import time
import tracemalloc
from optimized_data_processor import OptimizedDataProcessor

def generate_sample_data(num_items=5000):
    all_menu_items = {'loc-1': []}
    for i in range(num_items):
        item = {
            'name': f'Product {i}',
            'brand': {'name': 'Brand A'},
            'price': {'amount': 10 + i},
            'categories': [{'name': 'Flower'}],
            'locations_found_at': ['/dispensaries/loc-1'],
            'listing_id': 'loc-1'
        }
        all_menu_items['loc-1'].append(item)
    return all_menu_items

def run_benchmark():
    processor = OptimizedDataProcessor(max_workers=4)
    data = generate_sample_data(5000)

    # 1. Pandas Method
    tracemalloc.start()
    start_time = time.time()

    _ = processor._flatten_all_items(data)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    pandas_time = end_time - start_time
    pandas_mem = peak / 1024 / 1024

    # 2. Custom Method
    tracemalloc.start()
    start_time = time.time()

    items = []
    for loc_id, menu_items in data.items():
        for item in menu_items:
            item_copy = item.copy()
            item_copy['_location_id'] = loc_id
            items.append(item_copy)

    _ = processor._fallback_flattening(items)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    fallback_time = end_time - start_time
    fallback_mem = peak / 1024 / 1024

    print("--- Data Processing Benchmark (5000 items) ---")
    print(f"Pandas (json_normalize): {pandas_time:.4f}s, Peak Mem: {pandas_mem:.2f} MB")
    print(f"Custom (Fallback):       {fallback_time:.4f}s, Peak Mem: {fallback_mem:.2f} MB")

if __name__ == "__main__":
    run_benchmark()
