import json
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData

def test_organize_clean_list_performance(benchmark):
    sample_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])
    scraper.allMenuItems = {'test_dispensary': products * 10} # Create a larger dataset

    def process_data():
        scraper._original_organize_into_clean_list()
        return len(scraper.finishedMenuItems)

    result = benchmark(process_data)
    assert result > 0
