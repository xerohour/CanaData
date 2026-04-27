import os
import json
import pytest
import shutil
from cache_manager import CacheManager
from pathlib import Path

class TestCacheManagerSecurity:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        # Create a temporary directory for the cache
        self.cache_dir = "test_secure_cache_dir"
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir)

        yield

        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    def test_json_serialization_safe(self):
        """Test that CacheManager stores data using JSON correctly."""
        manager = CacheManager(cache_dir=self.cache_dir, enable_disk_cache=True)
        url = "https://api.weedmaps.com/test_json"
        data = {"safe_data": "value", "list": [1, 2, 3]}

        # Store data
        manager.set(url, data)

        # Ensure it is stored on disk
        cache_key = manager._generate_cache_key(url)
        cache_file = Path(self.cache_dir) / f"{cache_key}.cache"

        assert cache_file.exists(), "Cache file was not created on disk."

        # Verify it's actually JSON on disk
        with open(cache_file, "r", encoding="utf-8") as f:
            disk_content = json.load(f)

        assert disk_content == data, "Data on disk does not match original data."

        # Invalidate memory cache to force disk load
        manager.memory_cache.clear()

        # Retrieve data
        retrieved = manager.get(url)
        assert retrieved == data, "Retrieved data does not match original data."

    def test_no_pickle_imported(self):
        """Ensure that pickle is not used in cache_manager.py."""
        with open("cache_manager.py", "r", encoding="utf-8") as f:
            content = f.read()
            assert "import pickle" not in content, "pickle module should not be imported."
            assert "pickle.dump" not in content, "pickle.dump should not be used."
            assert "pickle.load" not in content, "pickle.load should not be used."

    def test_corrupted_json_handling(self):
        """Ensure corrupted JSON is handled gracefully."""
        manager = CacheManager(cache_dir=self.cache_dir, enable_disk_cache=True)
        url = "https://api.weedmaps.com/corrupt"
        cache_key = manager._generate_cache_key(url)
        cache_file = Path(self.cache_dir) / f"{cache_key}.cache"

        # Write corrupted JSON
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write("{invalid_json: 123")

        retrieved = manager.get(url)
        assert retrieved is None, "Should return None for corrupted JSON."
