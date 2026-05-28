# Phase 2 — Required Skill Coverage

## Objective

Decide whether the bundle's skill surface is **sufficient** for general-purpose Claude Code work — across web, AI/ML, mobile, desktop, data, infra, and CLI projects — without rewarding bloat or padding.

## Coverage Floor: The Canonical 11 Categories

A complete bundle must cover every category below. *Coverage* means at least one skill (or agent that the bundle's commands route to) whose **content** delivers the capability — not just a matching name.

| # | Category | Capability the bundle must deliver |
|---|---|---|
| 1 | **Planning / Spec design** | Convert requirements into a phased, verifiable plan with success criteria; supports re-planning on new info. |
| 2 | **Project Initialization / Scaffolding** | Stand up a new project with a chosen stack: directory layout, config, baseline tests, README. |
| 3 | **Feature Implementation** | Add a feature into an existing codebase coherently with the project's style and architecture. |
| 4 | **Refactoring / Migration / Adaptation** | Change shape without changing behaviour; replace tech A with tech B; wrap legacy with adapters. (Sub-categories may be one skill or three; one is acceptable if rich.) |
| 5 | **Bug Diagnosis (Bugfinder)** | Read-only root-cause analysis from a symptom to a precise file:line + explanation. Must scale across difficulty tiers (see Phase 5). |
| 6 | **Bug Fixing (Fix-Bug)** | Apply a targeted, verified fix with regression checks; must work for hard/super-hard bugs, not only typos. |
| 7 | **Test / Verification** | Create or run tests that confirm a change behaves as specified; verify a PR or feature manually when tests are absent. |
| 8 | **Optimization / Performance** | Profile, locate hot paths, propose and apply non-functional improvements (CPU, memory, latency, token usage). |
| 9 | **Code Review / Quality** | Review uncommitted changes for correctness, security, and quality; PASS/FAIL with severity. |
| 10 | **UI / UX Design** | Multi-platform (web, desktop, mobile) design with tokens, layouts, components, accessibility. |
| 11 | **Documentation / Project Knowledge** | Generate or update README/spec/architecture docs; explain code; build project overview. |

### Optional but Common (no penalty if absent; bonus if present and good)

- Security review / hardening
- Dockerization / deployment
- Meta-skills: prompt creation, skill creation, command creation
- Compaction / summarization
- Agent / orchestration helpers (`run`, `loop`, `verify`)

## Coverage Decision Procedure

For each canonical category 1–11:

1. **Search** the bundle for any skill, agent, or command whose **content** matches the capability description. Do not match on name alone — open the file.
2. **Classify** the result:
   - `Present` — content covers the capability with role, workflow, output contract, examples.
   - `Partial` — capability acknowledged but workflow is thin, missing output contract or examples.
   - `Absent` — no content found.
3. **Record** the matching file path(s) and the strongest evidence quote.

## Coverage Matrix Output

```
| # | Category | Status | Evidence (file path + ≤ 30-word quote) |
|---|---|---|---|
| 1 | Planning | Present | `.claude/skills/05-plan/SKILL.md:42` — "..." |
| 2 | Init | Partial | `.claude/skills/init/SKILL.md:10` — "..." |
| ... |
```

## Project Archetype Breadth

A bundle should be useful across project archetypes. For each archetype below, mark whether the bundle's skills/agents acknowledge or address it.

| Archetype | Signal of support |
|---|---|
| Web frontend | Mentions of React/Vue/Svelte, browser dev server, accessibility |
| Web backend | Routes/handlers, ORM, auth, API testing |
| Mobile | Flutter / RN / SwiftUI / Jetpack Compose mentioned in UI/feature/test skills |
| Desktop | Electron / Tauri / PyQt / WPF mentioned, packaging guidance |
| AI/ML | Training/eval loops, dataset prep, model serving, prompt engineering |
| Data pipeline | ETL, orchestration, schema, observability |
| CLI / Library | Argument parsing, packaging, semver, distribution |
| Infra / IaC | Docker, K8s, Terraform, CI/CD |
| Game / Graphics | Game loops, shaders, asset pipelines, frame budget |

A bundle does not need every archetype to score well, but the breadth count feeds Phase 7's *Coverage Breadth* score.

## Bloat & Overlap Detection

Bundles often pad their skill count. Flag the following:

- **Two skills covering the same scope** (e.g., `bugfinder` and `bugfinder-hard` are acceptable as a tier split; `bugfinder` and `find-bugs` and `bug-finder` are bloat).
- **Empty / placeholder skills** (SKILL.md ≤ 30 lines with no workflow).
- **Wrappers** that only invoke another skill without adding rules or context.
- **Fan-out commands** that route to non-existent agents or skills.

Each bloat instance is a soft deduction in Phase 3 (per-skill quality) and a hard deduction in Phase 7's Coverage Completeness sub-score.

## Sufficiency vs. Quantity Guidance

- **Lean (≤ 12 skills, full coverage)**: a strong sign — usually means each skill is dense.
- **Mid (13–25 skills)**: typical for established bundles; check for overlap.
- **Heavy (26+ skills)**: scrutinize for bloat. A heavy bundle that fails coverage on any category 1–11 is a worse signal than a lean one with full coverage.

## Phase 2 Output

Per bundle:

1. The 11-row Coverage Matrix.
2. The Project Archetype Breadth checklist (count of supported archetypes / 9).
3. Bloat & Overlap list with file paths and reason.
4. **Critical gaps**: any of categories 1–11 marked `Absent` — these cap the final grade at D (see scoring rubric).
5. Important gaps: categories marked `Partial`.

## Required Practices

- Always read at least 50 lines of a skill before deciding `Present` vs. `Partial`.
- Always cite the strongest evidence line for `Present`; cite the weakness for `Partial`; cite the absence search performed for `Absent`.
- Always prefer one rich skill to two thin ones in the same category.

## Prohibited Practices

- Do not award `Present` because a skill **claims** to cover the category in its frontmatter description; require workflow content to back it.
- Do not penalise a bundle for not including optional categories.
- Do not double-credit a skill across categories unless the content explicitly covers both with separate workflow phases.
