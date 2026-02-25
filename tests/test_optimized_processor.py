import pytest
import pandas as pd
from optimized_data_processor import OptimizedDataProcessor

def test_flatten_basic_structure():
    """Test flattening of simple structure."""
    processor = OptimizedDataProcessor()
    data = {
        "loc1": [
            {"id": "1", "name": "Item 1", "price": 10},
            {"id": "2", "name": "Item 2", "price": 20},
        ]
    }

    result = processor.process_menu_data(data)

    assert len(result) == 2
    assert result[0]['_location_id'] == 'loc1'
    assert result[0]['name'] == 'Item 1'

def test_flatten_nested_structure():
    """Test flattening of nested dictionaries."""
    processor = OptimizedDataProcessor()
    data = {
        "loc1": [
            {
                "id": "1",
                "details": {
                    "brand": "Brand A",
                    "specs": {"thc": "20%"}
                }
            }
        ]
    }

    result = processor.process_menu_data(data)

    assert len(result) == 1
    assert result[0]['details.brand'] == 'Brand A'
    assert result[0]['details.specs.thc'] == '20%'

def test_flatten_with_mixed_keys():
    """Test when items have different keys."""
    processor = OptimizedDataProcessor()
    data = {
        "loc1": [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "price": 20},
        ]
    }

    result = processor.process_menu_data(data)

    assert len(result) == 2
    # Missing keys should be 'None' or NaN depending on normalization,
    # but _normalize_data fills na with 'None'.
    item1 = next(item for item in result if item['id'] == '1')
    item2 = next(item for item in result if item['id'] == '2')

    assert item1.get('price') == 'None'
    assert item2.get('name') == 'None'

def test_empty_data():
    """Test handling of empty data."""
    processor = OptimizedDataProcessor()
    data = {}
    result = processor.process_menu_data(data)
    assert result == []

    data = {"loc1": []}
    result = processor.process_menu_data(data)
    assert result == []

def test_location_id_preservation():
    """Test that _location_id matches the input keys."""
    processor = OptimizedDataProcessor()
    data = {
        "loc_A": [{"id": "1"}],
        "loc_B": [{"id": "2"}, {"id": "3"}]
    }

    result = processor.process_menu_data(data)

    loc_a_items = [item for item in result if item['_location_id'] == 'loc_A']
    loc_b_items = [item for item in result if item['_location_id'] == 'loc_B']

    assert len(loc_a_items) == 1
    assert len(loc_b_items) == 2
