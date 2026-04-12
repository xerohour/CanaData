import time
from optimized_data_processor import OptimizedDataProcessor

def run_benchmark():
    processor = OptimizedDataProcessor()

    # Simulate realistic hierarchical response data
    sample_data = {
        'store1': [{'id': i, 'product': {'name': f'test_{i}', 'brand': {'name': f'brand_{i}'}}, 'price': i*10} for i in range(100000)]
    }

    start = time.time()
    flattened = processor.process_menu_data(sample_data)
    end = time.time()

    print(f"Flattening 100k nested items took: {end - start:.4f} seconds")
    return end - start

if __name__ == "__main__":
    run_benchmark()
