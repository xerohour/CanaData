## 2024-05-29 - [Optimize Dictionary Flattening]
**Learning:** In hot loops processing deep recursive structures (like `flatten_dictionary`), repeated implicit string method lookups (like `'.'.join(keys)`) and generating keys early can add significant overhead.
**Action:** Pre-cache repetitive built-in methods (`join_keys = '.'.join`), add early loop continues for common primitives (`isinstance(v, (str, int, float, bool))`), and defer string key compilation until necessary. However, avoid replacing `isinstance` with exact `type()` checks to preserve structural robustness.
