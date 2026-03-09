## 2026-03-09 - Dictionary Flattening Overhead
**Learning:** The pure-Python stack-based iterative dictionary unpacking (`_flatten_dictionary`) significantly outperforms the Pandas `json_normalize` implementation for heavily nested but small-scoped structures due to overhead with constructing/manipulating DataFrames and handling inner nested fallbacks.
**Action:** When working on flattening implementations, prioritize the existing iterative pure-Python fallback. Deprecate or re-evaluate Pandas overhead prior to assuming `json_normalize` optimization.

## 2026-03-09 - Noisy Neighbor Data Locks
**Learning:** `CanaData` currently utilizes a single shared `self._menu_data_lock` when mapping data in threads. This creates a noisy neighbor bottleneck when executing at massive horizontal concurrency scales, effectively throttling processing down to the speed of lock aquisition.
**Action:** Before increasing horizontal scaling to extreme loads, consider segmenting dictionaries per-worker and merging sequentially outside of the lock, eliminating the lock requirement entirely during runtime.

## 2026-03-09 - Stateful Cache Distribution Issue
**Learning:** `CacheManager` stores local state in RAM, which fails to scale effectively when orchestrating multiple independent containerized replicas. Local caches result in fragmented memory cache and duplicate requests across container boundaries.
**Action:** For distributed deployments, prioritize implementing a centralized remote caching solution like Redis or Memcached to normalize state across instances.