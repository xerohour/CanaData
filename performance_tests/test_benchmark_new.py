import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def test_benchmark_high_volume_throughput(benchmark):
    cana = CanaData(optimize_processing=False, interactive_mode=False)
    # Simulate a high-volume deeply nested dictionary
    nested_data = {
        'id': '12345',
        'brand': {'name': 'BrandA', 'id': 'b1'},
        'category': {'name': 'CategoryA'},
        'pricing': {'price': 100, 'discount': 10},
        'tags': ['thc', 'cbd', 'indica'],
        'metadata': {'views': 1000, 'rating': 4.5}
    }

    def process_high_volume():
        for _ in range(100):
            cana.flatten_dictionary(nested_data)

    benchmark(process_high_volume)
