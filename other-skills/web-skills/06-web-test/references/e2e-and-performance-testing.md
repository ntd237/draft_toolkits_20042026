# E2E & Performance Testing Guidance

Supports Phase 4 of `06-web-test`. Tests authored here follow the same integrity rules as all tests in this toolkit: real assertions, no fake passes, failures reported honestly.

## E2E Testing

**When mandatory**: the change touches a critical user flow (auth/login, payments/checkout, onboarding, data-destroying actions) or a cross-tier contract visible to the user. **When optional but recommended**: any new multi-step user journey.

**Framework selection**:
- If the project already has an E2E setup, use it as-is — never introduce a second framework.
- If none exists, default to Playwright unless the project's stack clearly favors something else (e.g., an existing Cypress config abandoned mid-setup — surface that and ask).

**Authoring rules**:
- Drive the app as a user would: real browser, real navigation; mock only third-party externals that cannot run in CI (payment gateways, email delivery) — never mock the system under test.
- Selectors: prefer accessible roles/labels (`getByRole`, `getByLabel`); CSS/XPath chains tied to styling are fragile and forbidden unless nothing else exists.
- Cover the happy path plus the failure paths named in acceptance criteria (invalid input, declined payment, session expiry).
- Keep each E2E scenario independent (no ordering dependencies) and gated on visible outcomes, not internal state.
- Auth helpers (storage state, seeded sessions) belong in fixtures; do not script the full login in every spec.

## Load / Stress Testing

**When mandatory**: an acceptance criterion states a load or response-time target (set in `02-web-plan` Phase 2).

- Use the project's existing tool if present (k6, autocannon, artillery, JMeter); otherwise k6 or autocannon are lightweight defaults that script easily.
- Exercise the target endpoint(s) at the specified profile (concurrent users, ramp-up, duration) against a representative environment — a local dev DB with 10 rows does not validate a production load target; state the data-volume assumption in the report.
- Report measured percentiles (p50/p95/p99) and throughput against the target — never a single average only.
- A miss against target is a finding for `00-web-orchestrator` (likely routing back through `04-web-bugfinder` for profiling), not something to paper over with re-runs until a lucky pass.

## Frontend Performance (Core Web Vitals)

**When mandatory**: public-facing pages, or when page-load targets are acceptance criteria.

- Measure on the affected pages: **LCP** (largest contentful paint), **INP** (interaction to next paint), **CLS** (cumulative layout shift).
- Tooling: Lighthouse CI or Playwright + web-vitals collection; record environment (device/CPU throttling, network condition) alongside every number.
- Common levers to check before reporting failure as unfixable: image sizing/format, font loading strategy, bundle size of the changed route, layout stability of late-loading content.
- Report measured values vs. targets; misses route through the orchestrator like any other failing criterion.
