import os
import sys

# Add parse-script to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../parse-script')))
from CanaParse import CanaParse, FlowerFilter

def test_canaparse_filtering(benchmark):
    """
    Benchmarks the CanaParse data filtering and string joining efficiency.
    """
    # Create a mock CSV dataset with many rows
    # Ensure it looks like the expected structure (at least 30 columns)
    # Price columns are at 9-15. Category at 20. Store at 29.

    num_rows = 1000
    mock_raw_data = []

    for i in range(num_rows):
        row = [str(j) for j in range(35)]  # Fill with dummy data

        # Inject realistic data for matching
        row[2] = f"Premium Flower {i}" # Name
        row[4] = f"Brand-{i%10}"       # Brand
        row[9] = str(10.0 + (i%5))     # Price Gram
        row[11] = str(35.0 + (i%10))   # Price Eighth
        row[20] = "flower" if i % 2 == 0 else "edible" # Category
        row[29] = f"Store-{i%5}"       # Store

        # Add some thc and cbd text to some rows for cannabinoid extraction
        if i % 3 == 0:
            row[1] = f"Some description THC: {20 + i%10}% CBD: {1 + i%5}%"
        else:
            row[1] = "Standard description"

        mock_raw_data.append(row)

    # Setup parser
    parser = CanaParse(no_filter=True)
    parser.raw_data = mock_raw_data

    # Create complex filters
    filter1 = FlowerFilter({
        "name": "Filter 1",
        "key": "prices.eighth",
        "price": 40.0,
        "compare": "<=",
        "categories": ["flower"],
        "brands": ["Brand-1", "Brand-2"],
        "thc_floor": 15
    })

    filter2 = FlowerFilter({
        "name": "Filter 2",
        "key": "prices.gram",
        "stores": ["Store-1", "Store-3"],
        "good_words": ["premium"],
        "bad_words": ["edible"]
    })

    parser.filters = [filter1, filter2]

    def run_filtering_benchmark():
        parser.apply_filters()
        return True

    # Run benchmark
    _ = benchmark(run_filtering_benchmark)
