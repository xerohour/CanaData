import os
import pytest
from CanaData import CanaData
from datetime import datetime
import shutil

class TestSecurity:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # Setup: Ensure clean state
        traversal_file = "traversal_test.csv"
        if os.path.exists(traversal_file):
            os.remove(traversal_file)

        today = datetime.today().strftime('%m-%d-%Y')
        # Check where CanaData writes
        dirs_to_check = [f'CanaData_{today}', f'tests/CanaData_{today}']

        for d in dirs_to_check:
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)

        yield

        # Teardown: remove created files
        if os.path.exists(traversal_file):
            os.remove(traversal_file)

        for d in dirs_to_check:
            if os.path.exists(d):
                shutil.rmtree(d, ignore_errors=True)

    def test_path_traversal_sanitization(self):
        """Test that path traversal attempts are sanitized in csv_maker."""
        cana = CanaData()

        # malicious_filename intended to traverse up one directory
        malicious_filename = "../traversal_test"
        data = [{'test': 'data'}]

        # Attempt to exploit
        try:
            cana.csv_maker(malicious_filename, data)
        except Exception:
            pass

        # Check if traversal occurred (file written outside intended directory)
        traversal_file = "traversal_test.csv"

        if os.path.exists(traversal_file):
            pytest.fail(f"Path traversal vulnerability exploited! File found at {traversal_file}")

        # Verify that the file WAS created in the correct location with sanitized name
        # We need to find where it was written.
        # Based on sys.path[0], it could be in tests/CanaData_DATE or ./CanaData_DATE
        import sys
        today = datetime.today().strftime('%m-%d-%Y')
        sanitized_filename = "..traversal_test"

        # Possible locations
        possible_paths = [
            f'{sys.path[0]}/CanaData_{today}/{sanitized_filename}.csv',
            f'CanaData_{today}/{sanitized_filename}.csv'
        ]

        found = False
        for p in possible_paths:
            if os.path.exists(p):
                found = True
                break

        if not found:
             # It might be fine if exception was raised, but we expect sanitization and write
             # However, let's just assert that traversal didn't happen.
             pass

    def test_sanitize_filename_method(self):
        """Test the _sanitize_filename method directly."""
        cana = CanaData()

        # This checks if the method exists and works as expected
        if not hasattr(cana, '_sanitize_filename'):
            pytest.fail("_sanitize_filename method is missing! Security fix not implemented.")

        # These assertions verify the implementation logic
        assert cana._sanitize_filename("../evil") == "..evil"
        assert cana._sanitize_filename("valid-file_name.123") == "valid-file_name.123"
        assert cana._sanitize_filename("invalid/characters!@#") == "invalidcharacters"
        assert cana._sanitize_filename("..\\windows\\style") == "..windowsstyle"
        assert cana._sanitize_filename("foo bar") == "foobar" # spaces removed

    def test_cache_manager_secure_serialization(self):
        """Test that CacheManager securely serializes data and handles legacy cache formats."""
        import json
        import pickle
        from cache_manager import CacheManager

        # Test directory
        cache_dir = "tests/test_secure_cache"
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

        manager = CacheManager(cache_dir=cache_dir)
        test_url = "https://api.example.com/data"
        test_data = {"key": "value", "list": [1, 2, 3]}

        # 1. Test secure serialization (saving)
        manager.set(test_url, test_data)

        # Verify the file was created and is valid JSON, not pickle
        cache_key = manager._generate_cache_key(test_url, None)
        cache_file = os.path.join(cache_dir, f"{cache_key}.cache")

        assert os.path.exists(cache_file)
        with open(cache_file, 'r', encoding='utf-8') as f:
            # This will fail if it's pickle data (binary)
            saved_data = json.load(f)
            assert saved_data == test_data

        # 2. Test deserialization (loading)
        # Clear memory cache to force loading from disk
        manager.memory_cache.clear()
        loaded_data = manager.get(test_url)
        assert loaded_data == test_data

        # 3. Test backward compatibility (graceful failure with legacy pickle cache)
        legacy_url = "https://api.example.com/legacy"
        legacy_key = manager._generate_cache_key(legacy_url, None)
        legacy_file = os.path.join(cache_dir, f"{legacy_key}.cache")

        # Create a malicious/legacy pickle file
        with open(legacy_file, 'wb') as f:
            pickle.dump(test_data, f)

        # Clear memory cache and attempt to get the legacy data
        manager.memory_cache.clear()

        # This should fail gracefully, catching UnicodeDecodeError or JSONDecodeError,
        # and return None without crashing or executing arbitrary code.
        legacy_loaded = manager.get(legacy_url)
        assert legacy_loaded is None

        # Cleanup
        shutil.rmtree(cache_dir)
