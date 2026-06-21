🛡️ Sentinel: [CRITICAL] Fix insecure deserialization vulnerability

## 🚨 Severity
CRITICAL

## 💡 Vulnerability
The `CacheManager` class in `cache_manager.py` used the insecure `pickle` library for disk caching (`pickle.load()`). If an attacker could modify the cache files on disk, they could achieve Arbitrary Code Execution (RCE) when the application loaded the cache, as `pickle` can execute arbitrary Python objects upon deserialization.

## 🎯 Impact
High. Since the cache is loaded back into memory from disk, any user or process with write access to the cache directory could place a maliciously crafted payload to execute arbitrary code with the privileges of the application.

## 🔧 Fix
Migrated the cache storage mechanism from binary `pickle` to text-based `json` by replacing `pickle.load()` with `json.load()` and `pickle.dump()` with `json.dump()`. Exception handling was updated appropriately to catch `json.JSONDecodeError` and `UnicodeDecodeError` to handle malformed or legacy cache files securely without crashing.

## ✅ Verification
Executed `pytest` and confirmed all 18 test cases pass, verifying that caching functionality continues to operate effectively under the JSON format.
