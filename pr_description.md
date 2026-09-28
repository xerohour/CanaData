🚨 Severity: MEDIUM
💡 Vulnerability: Probable use of insecure hash functions in `hashlib`: `md5`
🎯 Impact: Using `md5` can make the application vulnerable to collision attacks. Although here it is used for caching, an attacker could potentially force cache collisions to serve incorrect data.
🔧 Fix: Replaced the use of `hashlib.md5()` with the more secure `hashlib.sha256()` algorithm.
✅ Verification: Review the source code and run `pytest tests/` to make sure caching still works as expected.