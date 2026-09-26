💡 What:
Added `aria-label` to pagination buttons ("Previous" and "Next") to make their purpose clear to screen reader users, since the visual text is not enough. Added `aria-live="polite"` to the dynamic pagination text showing current records, ensuring screen readers announce updates when pagination changes. Added `aria-disabled="true"` to visually disabled pagination buttons. Applied `aria-hidden="true"` to the decorative emoji ("✨") in the PROMO block.

🎯 Why:
The generated HTML report contained interactive controls (pagination) that lacked adequate screen reader context and dynamic status updates. The promo block had a decorative emoji that a screen reader might read aloud ("sparkles"), disrupting the content flow.

📸 Before/After:
N/A (Visuals remain the same, changes only affect semantic/accessible markup)

♿ Accessibility:
Improved keyboard and screen reader accessibility for pagination controls and cleaner structure for the promo block.
