## 2026-02-24 - List Comprehension Optimization in CanaParse
**Learning:** In `CanaParse.apply_filters`, proactively creating a shallow copy of every row (`row[:]`) before checking conditions causes severe memory allocation overhead and performance regressions.
**Action:** Pre-calculate `row_str` for all rows beforehand to avoid redundant string joins inside `is_match`. Pass the original row to `is_match` to be evaluated and mutated, and only construct the copied list of items that passed the test (`filtered.append(original_row[:])`), preserving memory efficiency.
