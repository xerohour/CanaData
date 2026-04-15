import threading
from CanaData import CanaData

def test_concurrent_processing_stress():
    cana = CanaData(interactive_mode=False)

    def worker(worker_id):
        sample_json = {'data': {'menu_items': [{'id': i, 'name': f'Item {i}'} for i in range(100)]}}
        sample_location = {'slug': f'test-slug-{worker_id}', 'type': 'dispensary', 'id': f'test-id-{worker_id}', 'wmid': f'test-wmid-{worker_id}'}
        cana.process_menu_items_json(sample_json, sample_location)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(cana.allMenuItems) == 10
    # Process menu updates self.menuItemsFound += menu_items_count inside the _menu_data_lock block
    assert cana.menuItemsFound == 1000
