## 2026-08-12 - Vestibular Disorders and Smooth Scrolling
**Learning:** Adding global `scroll-behavior: smooth;` can trigger motion sickness and nausea for users with vestibular disorders. It is critical to always wrap smooth scrolling in a `@media (prefers-reduced-motion: no-preference)` media query.
**Action:** Always test animations and smooth scrolling by enabling 'Prefers reduced motion' in OS accessibility settings and ensure they are disabled.
