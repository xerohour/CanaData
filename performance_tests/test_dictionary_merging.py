import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))


def test_dictionary_merging_legacy(benchmark):
    flatDictList = [{"id": str(i), "name": f"test{i}", "price": str(10 + i % 10)} for i in range(1000)]
    def process():
        all_keys_set = set()
        for item in flatDictList:
            all_keys_set.update(item.keys())
        all_keys = sorted(list(all_keys_set))
        template_dict = dict.fromkeys(all_keys, 'None')
        ready_list = []
        for item in flatDictList:
            flat_ordered_dict = template_dict.copy()
            flat_ordered_dict.update(item)
            ready_list.append(flat_ordered_dict)
        return ready_list
    result = benchmark(process)
    assert len(result) == 1000

def test_dictionary_merging_optimized(benchmark):
    flatDictList = [{"id": str(i), "name": f"test{i}", "price": str(10 + i % 10)} for i in range(1000)]
    def process():
        all_keys_set = set()
        for item in flatDictList:
            all_keys_set.update(item.keys())
        all_keys = sorted(list(all_keys_set))
        template_dict = dict.fromkeys(all_keys, 'None')
        ready_list = [template_dict | item for item in flatDictList]
        return ready_list
    result = benchmark(process)
    assert len(result) == 1000
