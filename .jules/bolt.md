
## 2024-05-15 - Optimize duplicate row_str computation in apply_filters
**Learning:** In `CanaParse.py`, redundant string joining within the inner loop of `apply_filters` (filters x rows) is a significant bottleneck, accounting for excessive redundant processing of `row_str` in `is_match`.
**Action:** Pre-calculate `row_str` representations for each row prior to the filter loop. Store them in a tuple along with the original row `(row, row_str)` and pass the pre-calculated string to `is_match`.
