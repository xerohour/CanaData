## 2024-05-22 - [Optional Dependency Import Crash]
**Learning:** Top-level imports of optional dependencies (like pandas) cause immediate crashes even if the code has fallback logic.
**Action:** Always wrap optional imports in try-except blocks or place them inside methods/functions where they are used.

## 2024-05-22 - [Sparse Data CSV Export]
**Learning:** Expanding sparse dictionaries to dense ones (filling missing keys with None) before export is extremely memory inefficient ($O(N \cdot M)$).
**Action:** Use `csv.DictWriter` with `restval` to handle sparse data efficiently without pre-expansion.
