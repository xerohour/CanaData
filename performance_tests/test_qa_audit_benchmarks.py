import pytest
from CanaData import CanaData

def test_benchmark_flatten_dictionary_latency(benchmark):
    scraper = CanaData()
    test_dict = {
        "id": "12345",
        "name": "Test Item",
        "brand": {"name": "Test Brand"},
        "prices": {"ounce": [200.0, 150.0], "gram": [10.0]}
    }
    def run_flatten():
        return scraper.flatten_dictionary(test_dict)
    result = benchmark(run_flatten)
    assert result["id"] == "12345"

def test_benchmark_organize_throughput(benchmark):
    scraper = CanaData()
    scraper.allMenuItems = {
        "loc1": [
            {"id": str(i), "name": f"Item {i}", "prices": {"ounce": [100.0]}} for i in range(100)
        ]
    }
    scraper.city_slug = "test_slug"
    def run_organize():
        scraper.organize_into_clean_list()
    benchmark(run_organize)
