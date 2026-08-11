import subprocess
with open('.jules/bolt.md', 'a') as f:
    f.write('''\n## 2026-08-11 - [Optimize dict flattening initialization]
**Learning:** In CPython, `dict.copy()` and `dict.update()` execute entirely at the C level and are extraordinarily fast. Do not attempt to optimize C-level dictionary merging or updating operations by replacing them with manual Python loops (e.g., explicit iteration to assign keys), as evaluating keys in Python-space is slower despite avoiding secondary dictionary allocations.
**Action:** Use list comprehensions when constructing arrays of merged dicts `[{**item, "_location_id": location_id} ...]`, they are significantly faster than appending copied dicts in a python `for` loop.
''')

subprocess.run(["rm", "benchmarks.json"])
subprocess.run(["git", "restore", "."])
