# Non-Functional Review Checklists (Accessibility / SEO / Performance)

Used in Phase 1.5 of `07-web-review` for the dimensions flagged in acceptance criteria (`01-web-brainstorm` Phase 3) or the plan (`02-web-plan` Phase 2). Severity rule from SKILL.md applies: violating a *stated* acceptance criterion is BLOCKING; gaps in dimensions never agreed on are ADVISORY.

## Accessibility (WCAG 2.1 AA — practical minimum for new/changed UI)

Check only UI touched by the change:
- **Keyboard**: every interactive element (buttons, links, inputs, modals, menus) reachable and operable by keyboard alone; no keyboard traps; focus visible at all times.
- **Semantics & labels**: native/semantic elements used for their purpose; every input has a programmatic label (`label`/`aria-label`/`aria-labelledby`); icon-only controls have accessible names; headings form a logical outline (no skipped levels).
- **Images & media**: informative images have `alt` conveying their content; decorative images are `alt=""`; video with speech has captions.
- **Contrast**: text contrast ≥ 4.5:1 (≥ 3:1 for large text and UI component boundaries) — verify with a contrast tool, not by eye.
- **Forms & errors**: errors are announced to assistive tech (`aria-live`/role=alert or equivalent) and described in text, not color alone; required fields indicated accessibly.
- **Dynamic content**: modals/drawers manage focus (moved in on open, restored on close); toasts/updates announced; loading states exposed accessibly.

## SEO (public-facing pages only)

- Unique, descriptive `<title>` and meta description per page; canonical URL where duplicates are possible.
- One `<h1>` per page, heading hierarchy sensible; meaningful anchor text (no "click here" for navigation links).
- Crawlability: no accidental `noindex`/robots blocking on public routes; key content is server-rendered or at least present without JS interaction where feasible (flag SPA-only content as ADVISORY unless SEO was a stated criterion).
- Structured data (JSON-LD, e.g., product/article/breadcrumb) on page types where the project already uses it.
- Images: descriptive filenames/alt; lazy loading without delaying LCP image.

## Performance

Verify against the targets set in `02-web-plan` Phase 2 when stated; otherwise review as ADVISORY:
- **Core Web Vitals on affected pages** (measured by `06-web-test` Phase 4): LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 at the agreed device/network profile.
- **Backend response time**: p95 within the stated target for changed endpoints.
- **Bundle/deliverable size**: new dependencies or assets meaningfully increase the route bundle — flag with measured delta; suggest code-splitting for heavy, rarely-used components.
- **Caching & payloads**: cacheable responses carry appropriate cache headers; list/detail endpoints avoid overfetching (no N+1, no full-table selects for paginated UI); large payloads paginated.
- **Regressions only vs. aspirations**: without stated targets, review flags clear regressions introduced by the change (e.g., a new full-table query on a hot path) rather than pre-existing slowness.
