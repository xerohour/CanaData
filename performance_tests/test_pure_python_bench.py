import pytest
from optimized_data_processor import OptimizedDataProcessor
import time

def test_pure_python_performance(benchmark):
    processor = OptimizedDataProcessor()

    def generate_data(size=1000):
        return {
            'loc1': [
                {
                    'id': i,
                    'name': f'Product {i}',
                    'brand': {'name': f'Brand {i}', 'id': i % 10},
                    'price': {'amount': i * 1.5, 'currency': 'USD'},
                    'tags': ['indica', 'flower'],
                    'variants': [{'id': 1}, {'id': 2}]
                }
                for i in range(size)
            ]
        }

    data = generate_data(1000)

    @benchmark
    def process():
        return processor.process_menu_data(data)
