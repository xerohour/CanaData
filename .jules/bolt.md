
## 2026-03-19 - Pre-calculating derived string values in nested loops
**Learning:** Redundant string joining (`" ".join(row).lower()`) within the inner loop of `apply_filters` (filters x rows) creates a massive performance bottleneck. The `CanaParse` script takes > 2.5 seconds because `is_match` computes this for every single row/filter combination.
**Action:** In Pandas or pure Python processing, when rows are immutable across operations (like filters), pre-calculate derived representations (like lower-cased row strings) for each row *before* the filter iteration begins, rather than dynamically inside `is_match`. Passing rows by reference corrupts `self.raw_data` for subsequent filters because `is_match` mutates the row by appending THC/CBD tags, so always copy (`row[:]`).
