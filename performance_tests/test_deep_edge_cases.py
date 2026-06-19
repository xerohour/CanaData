import pytest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

def test_malformed_json_resilience():
    cana = CanaData(interactive_mode=False)
    malformed_payload = {"listing": None, "categories": "not a list"}

    # Should not crash, should handle gracefully
    result = cana.process_menu_json(malformed_payload)
    assert result is None or (result.get('is_empty_menu') is True)

def test_processor_timeout_handling():
    processor = ConcurrentMenuProcessor(max_workers=2, rate_limit=0)

    def slow_process(location):
        if location['id'] == 1:
            raise TimeoutError("Simulated API Timeout")
        return {"listing_id": location['id'], "data": "success"}

    locations = [{"id": 1, "slug": "a"}, {"id": 2, "slug": "b"}]
    results = processor.process_locations(locations, slow_process)

    assert "b" in results
    assert "a" not in results
    assert len(processor.errors) == 1
    assert "Timeout" in processor.errors[0]['error']
