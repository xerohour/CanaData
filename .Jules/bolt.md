
## 2026-05-29 - Optimize flatten_dictionary Bottleneck
**Learning:** The `flatten_dictionary` function suffered performance bottlenecks due to repetitive O(n) checks (e.g., `len(v.keys()) < 1`) and string joining overhead in tight loops. Pre-caching `join_keys = '.'.join` and evaluating empty collections implicitly (`if not v:`) provides a measurable throughput gain. While `type(v) is dict` provided marginal improvements over `isinstance(v, dict)`, it was avoided due to the strict constraint prohibiting exact type checking in this codebase to prevent regression with custom subclasses.
**Action:** Refactored `flatten_dictionary` to cache `.join`, use implicit boolean evaluation for empty collections, and reorder conditionals to check primitive types first, as they are most common.
