
## 2026-03-27 - Pre-compiling regexes in tight loops
**Learning:** Calling `re.search(rf"{pattern}")` with an f-string forces Python to dynamically compile the regex on every single invocation. In tight loops (like iterating over thousands of rows x multiple filters in `CanaParse`), this creates a massive performance bottleneck because the regex engine throws away and recompiles the identical pattern each time.
**Action:** Always pre-compile regex patterns (e.g., using `re.compile`) at the class instantiation level (`__init__`) or module level, and reuse the compiled pattern objects.
