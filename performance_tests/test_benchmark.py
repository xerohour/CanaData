import pytest
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_benchmark_processing(benchmark):
    # Mock data setup
    mock_data = {"loc_1": [{"id": 1, "name": "Test Item"}] * 1000}
    processor = OptimizedDataProcessor()

    def run_processing():
        return processor.process_menu_data(mock_data)

    result = benchmark(run_processing)
    assert len(result) == 1000
