💡 What: Added `aria-hidden="true"` to the decorative sort icon (`↕`, `▲`, `▼`) in the interactive table headers within the generated HTML report.

🎯 Why: Screen readers read out the visible sorting symbols (like "up down arrow" or "upwards pointing triangle") alongside the table header text. This creates a noisy and clunky experience, especially since the header already includes a descriptive `aria-label` (e.g., "Sort by Price"). Hiding the decorative icon from screen readers ensures a cleaner, more focused auditory experience.

📸 Before/After: Visual appearance remains identical, but the screen reader output for table headers changes from "Sort by Price, up down arrow" to simply "Sort by Price".

♿ Accessibility: Improves screen reader navigation and comprehension by reducing unnecessary auditory noise and relying on proper `aria-label` descriptions for interactive sorting headers.
