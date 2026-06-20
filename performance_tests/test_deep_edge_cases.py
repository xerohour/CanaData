import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData  # noqa: E402

def test_deep_edge_cases_flattening():
    scraper = CanaData(interactive_mode=False)

    edge_cases = {
        'empty_dict': {},
        'empty_list': [],
        'nested_empty_dict': {'a': {}},
        'nested_empty_list': {'a': []},
        'list_of_dicts': {'items': [{'id': 1}, {'id': 2}]},
        'deeply_nested': {'a': {'b': {'c': {'d': 'value'}}}},
        'mixed_types': {'a': 1, 'b': None, 'c': 'string', 'd': [1, 2, 3]}
    }

    result = scraper.flatten_dictionary(edge_cases)

    assert result['empty_dict'] == 'None'
    assert result['empty_list'] == 'None'
    assert result['nested_empty_dict.a'] == 'None'
    assert result['nested_empty_list.a'] == 'None'
    assert result['list_of_dicts.items.id'] == '2' # Behavior of existing system
    assert result['list_of_dicts.id'] == '1' # Behavior of existing system
    assert result['deeply_nested.a.b.c.d'] == 'value'
    assert result['mixed_types.a'] == '1'
    assert result['mixed_types.b'] == 'None'
    assert result['mixed_types.c'] == 'string'
    assert result['mixed_types.d'] == '1.2.3'