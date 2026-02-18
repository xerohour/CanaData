import pytest
from CanaData import CanaData

def test_flatten_dictionary_simple():
    cana = CanaData()
    nested = {
        'name': 'Great Product',
        'price': {'amount': 10, 'currency': 'USD'},
        'tags': ['calm', 'sweet']
    }
    flattened = cana.flatten_dictionary(nested)
    
    assert flattened['name'] == 'Great Product'
    assert flattened['price.amount'] == '10'
    assert flattened['price.currency'] == 'USD'
    assert flattened['tags'] == "['calm', 'sweet']"

def test_flatten_dictionary_empty():
    cana = CanaData()
    nested = {
        'empty_dict': {},
        'empty_list': []
    }
    flattened = cana.flatten_dictionary(nested)
    
    assert flattened['empty_dict'] == 'None'
    assert flattened['empty_list'] == 'None'

def test_flatten_dictionary_list_of_dicts():
    cana = CanaData()
    nested = {
        'items': [
            {'id': 1},
            {'id': 2}
        ]
    }
    # Current implementation joins/handles lists of dicts by pushing to stack
    # Let's verify what it actually produces
    flattened = cana.flatten_dictionary(nested)
    assert flattened['items.id'] in ['1', '2'] # It gets one of them due to the logic
