import pytest
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
from tests.profile_canadata import generate_mock_data

@pytest.fixture
def mock_data():
    return generate_mock_data(num_locations=20, items_per_loc=50)

def test_benchmark_custom_flatten(benchmark, mock_data):
    processor = OptimizedDataProcessor(max_workers=4)
    # Extract the flat list of items
    items = [item for items_list in mock_data.values() for item in items_list]

    @benchmark
    def run_custom():
        processor._fallback_flattening(items)

def test_benchmark_pandas_flatten(benchmark, mock_data):
    processor = OptimizedDataProcessor(max_workers=4)

    @benchmark
    def run_pandas():
        processor._flatten_all_items(mock_data)
