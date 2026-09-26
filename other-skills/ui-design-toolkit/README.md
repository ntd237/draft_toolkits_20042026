# UI Design Toolkit

Spec-first UI/UX design toolkit for Claude Code. Six cohesive skills take a product from intent to a validated interface specification and optional static prototypes — covering Web Apps, Mobile Apps, Desktop Apps, and Game UIs, with responsive layouts (Mobile / Tablet / PC) and Vietnamese-safe typography.

## What's Inside

**6 skills with high cohesion** (`00` orchestrator + `01`–`05` specialists). Skills run as a pipeline: the orchestrator classifies the platform and workflow, routes work to specialists, and compiles every output into a single `docs/ui-design/system_design.md` specification.

```
ui-design-toolkit/
  README.md
  LICENSE
  .claude-plugin/plugin.json          <- Plugin manifest for Claude Code
  skills/                             <- Single source of truth (6 skills)
    00-ui-orchestrator/               <- Workflow coordinator & system_design.md compiler
    01-ux-flow-architecture/          <- Personas, sitemap/IA, user flows with error & recovery paths, wireframes
    02-ui-design-system/              <- Design tokens (60-30-10 color), Vietnamese-safe typography, 6-state components
    03-ui-platform-responsive/        <- Breakpoint matrix & recipes for Web / Mobile / Desktop / Game platforms
    04-ui-ux-qa-review/               <- WCAG 2.2 AA audit, Nielsen heuristics, Vietnamese diacritics stress test
    05-ui-example-generator/          <- Static sample interfaces (vanilla HTML/CSS/JS) generated on explicit opt-in
```

## Skill Catalog

| Skill | Primary Responsibility | File Access |
| :--- | :--- | :--- |
| `/00-ui-orchestrator` | Classify the target platform (Web, Mobile, Desktop, Game), coordinate specialist skills, and synthesize the unified `docs/ui-design/system_design.md` specification. | Read/write docs UI |
| `/01-ux-flow-architecture` | Personas, JTBD, information architecture (sitemap), task flows with error & recovery paths, low-fidelity wireframes, and ethical UX (no dark patterns). | Read/write |
| `/02-ui-design-system` | Design tokens (60-30-10 color palettes for Light/Dark, spacing, radius, motion), Vietnamese-safe typography (line-height 1.4–1.6 to prevent diacritic clipping), and component specs with all 6 interactive states. | Read/write |
| `/03-ui-platform-responsive` | Breakpoint matrix (Mobile <768px, Tablet 768–1024px, PC >1024px, Ultrawide >1920px), navigation adaptation (Bottom Bar → Rail → Sidebar), and platform-specific UX recipes for Web Apps, Mobile Apps, Desktop Apps, Game Desktop HUDs, and Game Mobile HUDs. | Read/write |
| `/04-ui-ux-qa-review` | Accessibility audit against WCAG 2.2 AA (color contrast, focus visibility, screen reader), the 10 Nielsen usability heuristics, Vietnamese diacritics stress testing, and P0/P1/P2 issue classification. | Read-only / QA report |
| `/05-ui-example-generator` | After explicit user opt-in (consent gate in skill `00`), generates static sample interfaces faithful to the approved `system_design.md` — vanilla HTML/CSS/JS only, saved under `docs/ui-design/examples/`. | Read spec / write `docs/ui-design/examples/` |

## Workflow

1. **Orchestrate** — `00-ui-orchestrator` analyzes product intent, classifies the platform, and plans the workflow.
2. **Architect** — `01-ux-flow-architecture` defines personas, information architecture, and user flows.
3. **Systematize** — `02-ui-design-system` produces tokens, typography, and full-state component specs.
4. **Layout** — `03-ui-platform-responsive` maps the design onto breakpoints and the target platform's idioms.
5. **Audit** — `04-ui-ux-qa-review` validates the specification against accessibility and usability standards.
6. **Prototype (optional)** — `05-ui-example-generator` renders static sample interfaces from the approved spec.

Every step writes into one specification, so the final `docs/ui-design/system_design.md` is self-contained and hand-off ready.

## Requirements

- Claude Code 2.x or later

## Installation

Via a plugin marketplace (recommended):

```bash
# In Claude Code
/plugin marketplace add <owner>/<repo>
/plugin install ui-design-toolkit@<marketplace-name>
```

Or via the CLI:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install ui-design-toolkit@<marketplace-name>
```

## Usage

Open any project in Claude Code and ask for a UI/UX design task, e.g.:

> "Design a food-delivery mobile app home screen using the UI Design Toolkit."

The orchestrator skill (`00-ui-orchestrator`) triggers automatically and drives the pipeline through its specialist skills.

## Updating

```bash
/plugin update ui-design-toolkit@<marketplace-name>
```

When releasing a new version, bump the `version` field in the plugin manifest and commit.

## Uninstalling

```bash
/plugin uninstall ui-design-toolkit@<marketplace-name>
```

Restart the runtime after uninstalling.
