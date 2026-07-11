import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

def test_deep_nesting_processing():
    processor = OptimizedDataProcessor(max_workers=2)
    deep_data = {
        'disp1': [
            {'id': 1, 'deep': {'level1': {'level2': {'price': 100}}}},
            {'id': 2, 'deep': {'level1': {'level2': {'price': '200.5'}}}}
        ]
    }
    result = processor.process_menu_data(deep_data)
    assert len(result) == 2
    assert result[0].get('deep.level1.level2.price') == 100
    assert result[1].get('deep.level1.level2.price') == 200.5
