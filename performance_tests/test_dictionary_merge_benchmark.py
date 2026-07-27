import pytest
import time
from CanaData import CanaData

@pytest.fixture
def mock_data():
    template_dict = dict.fromkeys([f"key_{i}" for i in range(50)], 'None')
    flat_list = [{f"key_{j}": j for j in range(25)} for _ in range(5000)]
    return template_dict, flat_list

def test_legacy_merge(benchmark, mock_data):
    template_dict, flat_list = mock_data

    def merge():
        ready_list = []
        for item in flat_list:
            flat_ordered_dict = template_dict.copy()
            flat_ordered_dict.update(item)
            ready_list.append(flat_ordered_dict)
        return ready_list

    result = benchmark(merge)
    assert len(result) == 5000

def test_optimized_merge(benchmark, mock_data):
    template_dict, flat_list = mock_data

    def merge():
        return [template_dict | item for item in flat_list]

    result = benchmark(merge)
    assert len(result) == 5000
