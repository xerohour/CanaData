import json
import os
import sys
import threading
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def test_extreme_concurrency_race_condition():
    """
    Simulates severe load from numerous concurrent workers modifying
    global state.
    """
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}
    lock = threading.Lock()

    def worker(worker_id):
        # Emulate rapid incoming API data writes
        local_data = {f"item_{worker_id}_{i}": [{"id": i}] for i in range(100)}
        with scraper._menu_data_lock:
            scraper.allMenuItems.update(local_data)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]

    for t in threads: t.start()
    for t in threads: t.join()

    # Verify no data is lost during rapid race conditions
    assert len(scraper.allMenuItems) == 10000

def test_memory_limit_edge_case():
    """
    Simulates a memory exhaustion scenario by sending exceptionally
    large recursive dictionaries to the custom flattening algorithm.
    """
    processor = OptimizedDataProcessor(max_workers=2)

    # Create an absurdly deep nested dictionary
    deep_dict = {"level_0": "val"}
    current = deep_dict
    for i in range(100):
        current[f"level_{i+1}"] = {}
        current = current[f"level_{i+1}"]
    current["end"] = "leaf"

    # Should not trigger RecursionError because it uses an iterative stack.
    result = processor._flatten_dictionary_custom(deep_dict)

    assert "level_0" in result
    assert result["level_0"] == "val"
    expected_key = ".".join([f"level_{i+1}" for i in range(100)]) + ".end"
    assert expected_key in result
    assert result[expected_key] == "leaf"

def test_malformed_data_recovery():
    """
    Test how the system recovers when encountering malformed JSON data,
    such as unexpected lists instead of dicts, or None values.
    """
    processor = OptimizedDataProcessor()

    bad_data = {
        "valid": {"id": 1},
        "none_value": None,
        "unexpected_list": ["a", "b"],
        "unexpected_int": 5,
        "empty_dict": {}
    }

    result = processor._flatten_dictionary_custom(bad_data)

    # Ensure it didn't crash and processed valid parts
    assert result["valid.id"] == "1"
    assert result["none_value"] == "None"
    assert "unexpected_list" in result
    assert result["unexpected_int"] == "5"
