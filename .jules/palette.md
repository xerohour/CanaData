## 2024-06-08 - Added accessible ARIA labels to fancybox galleries
**Learning:** When using data-fancybox image galleries inside dynamically generated HTML tables, the `a` wrapper often lacks an `aria-label` and the `img` itself misses an `alt` text. This makes screen readers announce the link as empty or fall back to announcing the raw URL, which is terrible for accessibility.
**Action:** Ensure all dynamically generated images and their parent interactive wrappers have contextually relevant `alt` texts and `aria-labels` using data from the dataset.
