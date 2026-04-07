import pytest
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def generate_mock_data(size):
    return {
        "location1": [
            {
                "id": str(i),
                "name": f"Product {i}",
                "price": {"amount": 50, "currency": "USD"},
                "category": {"name": "Flower", "tags": ["sativa", "hybrid"]},
                "stock": [{"location": "A", "quantity": 10}, {"location": "B", "quantity": 5}]
            } for i in range(size)
        ]
    }

@pytest.mark.benchmark(group="flattening")
def test_benchmark_custom_flattening(benchmark):
    cana = CanaData(optimize_processing=False, interactive_mode=False)
    data = generate_mock_data(1000)

    def run_flattening():
        cana.allMenuItems = data
        cana.organize_into_clean_list()

    benchmark(run_flattening)

@pytest.mark.benchmark(group="flattening")
def test_benchmark_optimized_flattening(benchmark):
    cana = CanaData(optimize_processing=True, interactive_mode=False)
    data = generate_mock_data(1000)

    def run_flattening():
        cana.allMenuItems = data
        cana.organize_into_clean_list()

    benchmark(run_flattening)
