import pytest
import copy
from CanaData import CanaData

def test_flatten_performance(benchmark):
    bot = CanaData(cache_enabled=False, interactive_mode=False)
    menu_item = {'id': '1', 'name': 'Item', 'prices': {'gram': 10, 'eighth': 30}}
    menu_items = [copy.deepcopy(menu_item) for _ in range(100)]
    all_menu_items = {f'dispensary-{i}': copy.deepcopy(menu_items) for i in range(10)}

    bot.allMenuItems = all_menu_items
    bot.totalLocations = [{'slug': f'dispensary-{i}', 'name': f'Dispo {i}'} for i in range(10)]

    def run_optimized():
        bot.optimize_processing = True
        bot.organize_into_clean_list()

    benchmark(run_optimized)
