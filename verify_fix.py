import os
import json
from cache_manager import CacheManager

class Exploit:
    def __reduce__(self):
        return (os.system, ('echo "VULNERABILITY: Arbitrary Code Execution via Pickle"',))

def main():
    cm = CacheManager(cache_dir="test_cache", enable_disk_cache=True)
    
    # Test valid JSON caching
    cm._set_to_disk("valid_key", {"test": "data"})
    result = cm._get_from_disk("valid_key")
    assert result == {"test": "data"}, "JSON serialization failed"
    
    print("Verification script passed JSON tests.")

if __name__ == "__main__":
    main()
