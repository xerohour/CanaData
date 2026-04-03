import pytest
import copy
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_benchmark_flatten_custom(benchmark, monkeypatch):
    monkeypatch.setenv("USE_CONCURRENT_PROCESSING", "false")
    scraper = CanaData(interactive_mode=False)
    sample_data = {"id": 1, "nested": {"key": "value"}, "list": [{"a": 1}]}
    benchmark(lambda: scraper.flatten_dictionary(copy.deepcopy(sample_data)))

def test_benchmark_flatten_pandas(benchmark):
    processor = OptimizedDataProcessor()
    sample_data = {"loc_1": [{"id": 1, "nested": {"key": "value"}, "list": [{"a": 1}]}]}
    benchmark(lambda: processor.process_menu_data(copy.deepcopy(sample_data)))
