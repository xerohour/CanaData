1. **Apply memory-efficient optimization in `optimized_data_processor.py`**
   - Use `first_valid_index()` instead of `dropna()` to check for nested structures, avoiding O(N) memory overhead.
   - Replace `.apply(lambda)` with a list comprehension for faster JSON dumping on object columns.
2. **Run Tests and Verification**
   - Run linter on `optimized_data_processor.py`.
   - Run the test suite and benchmark to verify the improvements don't break anything and show actual speedups.
3. **Log the performance learning**
   - Append to `.jules/bolt.md` detailing the optimizations (if not routine, though memory states to record only CRITICAL, so maybe I don't need a journal entry if it's routine, but I will check if it fits). Actually, I'll write the PR.
4. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.**
5. **Submit the changes with a descriptive PR title and body**
   - Title: `⚡ Bolt: [performance improvement] Optimize nested column detection and flattening`
   - Include 💡 What, 🎯 Why, 📊 Impact, 🔬 Measurement.
