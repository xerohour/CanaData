from optimized_data_processor import OptimizedDataProcessor
import pandas as pd

def test_optimized_data_processor(benchmark):
    """
    Benchmarks the DataFrame cleaning and flattening string representation overhead.
    """
    # Generate mock nested data
    num_items = 2000

    mock_data = []
    for i in range(num_items):
        item = {
            "id": i,
            "name": f"Product {i}",
            "price": {"amount": 50 + i, "currency": "USD"},
            "metadata": {
                "tags": ["premium", "indica" if i % 2 == 0 else "sativa"],
                "lab_results": [{"test": "thc", "value": 20}, {"test": "cbd", "value": 1}]
            },
            "locations": [f"loc-{j}" for j in range(3)],
            "simple_list": [1, 2, 3]
        }
        mock_data.append(item)

    processor = OptimizedDataProcessor(max_workers=4)

    def run_processor_benchmark():
        # First step of _flatten_all_items to get initial df
        df = pd.json_normalize(mock_data, sep='.')
        # Target the specific method we are optimizing
        df = processor._handle_remaining_nesting(df)
        return df

    # Run benchmark
    _ = benchmark(run_processor_benchmark)
