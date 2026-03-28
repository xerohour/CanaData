## 2024-03-28 - Regex Compilation Bottleneck
**Learning:** Dynamically compiling regex patterns using f-strings inside tight loops (e.g., `re.search(rf'{pattern}', text)`) causes measurable performance bottlenecks, especially when evaluating thousands of rows in CanaParse.
**Action:** Always pre-compile regex patterns using `re.compile()` at the class or module level for operations executed inside loops.
