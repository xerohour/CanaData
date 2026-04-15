import pytest
from CanaData import CanaData

def test_benchmark_flatten(benchmark):
    cana = CanaData(interactive_mode=False)
    sample_item = {'id': 132352, 'name': 'Marionberry Indica Enhanced Gummies 100mg', 'slug': 'wyld-marionberry-indica-enhanced-gummies-100mg', 'brand': {'avatar_image_url': 'https://images.weedmaps.com/brands/000/000/898/avatar/1654546712-wyld_logo_black.png', 'name': 'WYLD', 'description': '...'}}

    def run_flatten():
        cana.flatten_dictionary(sample_item)

    benchmark(run_flatten)

def test_benchmark_process_menu(benchmark):
    cana = CanaData(interactive_mode=False)
    menu_items_list = [{'id': i, 'name': f'Item {i}'} for i in range(50)]
    sample_json = {'data': {'menu_items': menu_items_list}}
    sample_location = {'slug': 'test-slug', 'type': 'dispensary', 'id': 'test-id', 'wmid': 'test-wmid'}

    def run_process():
        cana.process_menu_items_json(sample_json, sample_location)

    benchmark(run_process)
