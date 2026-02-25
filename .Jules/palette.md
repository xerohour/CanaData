## 2024-05-22 - Static Report Accessibility
**Learning:** Custom "Glassmorphism" designs often strip default browser styles (like focus rings) without replacing them, leaving keyboard users lost.
**Action:** Always verify `:focus-visible` states when working with custom dark-mode or glass-effect CSS to ensure high contrast focus indicators.

## 2024-05-22 - Testing Static Generators
**Learning:** Python scripts generating static HTML often hardcode output paths, making them hard to test safely.
**Action:** Always refactor file generation functions to accept an `output_path` argument to enable safe testing with temporary files.
