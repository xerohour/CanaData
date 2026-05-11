## 2026-05-11 - [O(n) Cache Pruning Bottleneck]
**Learning:** Using `min()` to find the oldest entry in a dictionary for eviction causes O(n) cache pruning time. Under high load, this causes an O(n^2) bottleneck.
**Action:** Always use `collections.OrderedDict` for LRU caching patterns in Python, as `popitem(last=False)` provides O(1) time complexity for eviction.
