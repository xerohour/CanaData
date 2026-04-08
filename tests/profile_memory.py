from memory_profiler import profile
from optimized_data_processor import OptimizedDataProcessor

@profile
def profile_flattening():
    test_data = [{'id': i, 'name': f'Product {i}', 'price': {'amount': 50.0, 'currency': 'USD'}, 'metadata': {'tags': ['a', 'b', 'c'], 'nested': {'deep': {'value': True}}}} for i in range(10000)]
    all_menu_items = {'loc_1': test_data}
    processor = OptimizedDataProcessor()
    processor.process_menu_data(all_menu_items)

if __name__ == '__main__':
    profile_flattening()
