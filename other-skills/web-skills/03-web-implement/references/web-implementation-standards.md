# Tier Implementation Standards for Web Code

Applied by `03-web-implement` (and `05-web-fix` where a fix touches the same concerns). These are minimum standards, not a license to expand scope beyond the targeted tests — apply what the current unit demands and flag conflicts with existing project conventions instead of silently overriding either side.

## Frontend

- **Component structure**: one component per file, colocate component-specific styles/tests; keep components presentational where feasible and push data fetching/state orchestration up to containers/hooks; extract a component only on second use or when it exceeds ~100 lines.
- **State management**: server data belongs in a query/cache layer (e.g., TanStack Query/SWR) when the project uses one; local UI state stays local (`useState`/composable/signal); reach for a global store (Redux/Zustand/Pinia) only when state is genuinely cross-tree — never introduce a store because "it might be needed".
- **Styling & responsive**: follow the project's styling system (CSS modules, Tailwind, styled-components, plain CSS) — do not mix paradigms; use relative units/flex/grid rather than fixed pixel widths; verify the layout at mobile (~375px), tablet (~768px), and desktop (~1280px) widths for any new UI.
- **Semantic HTML & accessibility in code**: use semantic elements (`button` for actions, `a` for navigation, `label` for inputs); every interactive element reachable by keyboard; images carry `alt`; icon-only buttons carry `aria-label`; visible focus states are not removed.
- **Frontend hygiene**: clean up subscriptions/listeners/timers in teardown; never render user input as raw HTML (XSS); derived values are computed, not duplicated in state.

## Backend

- **Input validation at the boundary**: validate and normalize every external input (HTTP body/query/params, webhooks) at the entry point with the project's validation library — route handlers deeper in the stack must not trust data already handled elsewhere.
- **Error handling**: fail loudly with typed/appropriate status codes; never swallow exceptions silently; return consistent error shapes per the project's error contract; log the server-side detail, expose the client-safe message.
- **Authorization at the resource**: check permissions per resource/per request (never assume "the UI hides it"); every new endpoint gets an explicit authz decision (public / authenticated / role-scoped) even if the decision is "public".
- **Secrets & config**: no credentials in code; read configuration from environment variables validated at startup.

## API Design (REST conventions unless the project dictates otherwise)

- Nouns for resources, plural collection paths (`/orders/42/items`); standard methods and status codes (200/201/204/400/401/403/404/409/422/500); idempotency preserved for GET/PUT/DELETE.
- Consistent pagination/filtering/sorting pattern with existing endpoints; consistent field naming (pick camelCase or snake_case per project, never mixed).
- Contract changes follow the plan's versioning decision (`02-web-plan` Phase 2); deprecate before removing; document payloads where the project keeps API docs (OpenAPI/README).

## Database Access

- Parameterized queries only — never interpolate user input into SQL (injection).
- Transactions around multi-statement invariants (debit+credit patterns); pick explicit isolation only when a documented race exists, not by default.
- New/changed queries consider indexing: check the query matches an existing index or propose one in the handoff to review; avoid N+1 patterns via joins/eager loading.
- Migrations follow the sequencing decided in `02-web-plan` (backward-compatible first, cleanup later).

## Observability

- Log key business events and failures with structured fields (event name, entity id, outcome) at the project's logging level conventions — never log secrets or full personal data.
- Wire errors into the project's error-tracking hook (e.g., Sentry) where one exists; a new feature must be diagnosable in production without attaching a debugger.

## App-Level Deployment & Config

- New behavior requiring configuration gets an environment variable with a sane default and documentation in the project's env sample file.
- Build/CI changes (new test steps, build flags) keep the pipeline green-first: tests run before deploy stages; failed stages block.
- Hosting config changes (Dockerfile, serverless config, static host settings) must state their rollback path in the handoff summary.
