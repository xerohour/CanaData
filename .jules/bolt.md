## 2026-03-16 - Pre-calculating string representations in nested loops
**Learning:** In heavily nested loops, calling `join` and `lower` on rows generates significant overhead when performed repeatedly (O(N*M)). Moving the calculation outside the inner loop to generate pre-calculated `row_strs` yields measurable performance gains (~57% improvement).
**Action:** When filtering or comparing large datasets across multiple parameters or configurations (like `CanaParse.apply_filters`), pre-compute list-comprehension based string conversions and mappings before iterating.
