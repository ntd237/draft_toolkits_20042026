# 3D UI Design Toolkit

Spec-first 3D and spatial UI/UX design toolkit for Claude Code. Six cohesive skills take a product from intent to a validated 3D interface specification and optional runnable prototypes — covering 3D Games, Web3D, Spatial Computing (XR), and Industrial 3D interfaces.

## What's Inside

**6 skills with high cohesion** (`00` orchestrator + `01`–`05` specialists). Skills run as a pipeline: the orchestrator classifies the 3D medium and input modalities, routes work to specialists, and compiles every output into a single `docs/3d-ui-design/3d_system_design.md` specification.

```
3d-ui-design-toolkit/
  README.md
  LICENSE
  .claude-plugin/plugin.json          <- Plugin manifest for Claude Code
  skills/                             <- Single source of truth (6 skills)
    00-3d-ui-orchestrator/            <- Workflow coordinator & 3d_system_design.md compiler
    01-3d-spatial-ux-architecture/    <- 4 UI classes (Diegetic/Spatial/Non-Diegetic/Meta), ergonomics & comfort
    02-3d-design-system-materials/    <- Spatial tokens, PBR/unlit shaders, 3D audio, SDF typography & 3D components
    03-3d-platform-engine-recipes/    <- Engine recipes: Web3D (Three.js/R3F), Unity, Unreal Engine & XR (VisionOS/Quest)
    04-3d-spatial-qa-optimization/    <- Performance QA (draw calls, overdraw), contrast against 3D light & cyber sickness
    05-3d-example-generator/          <- Runnable in-browser samples (HTML/CSS/JS + optional vendored Three.js) from 3d_system_design.md into docs/3d-ui-design/examples/
```

## Skill Catalog

| Skill | Primary Responsibility | File Access |
| :--- | :--- | :--- |
| `/00-3d-ui-orchestrator` | Classify the 3D medium and input modalities, coordinate specialist skills, and synthesize `docs/3d-ui-design/3d_system_design.md`. | Read/write docs 3D UI |
| `/01-3d-spatial-ux-architecture` | 4-tier UI classification (Diegetic, Non-diegetic, Spatial, Meta), depth-plane zoning (Near/Comfort/Far), angular FoV comfort cones, and cyber sickness prevention. | Read/write |
| `/02-3d-design-system-materials` | Metric spatial tokens (1m = 1 unit), unlit/frosted-glass/holographic shaders, 3D positional HRTF audio, SDF typography, and 6-state 3D interactive components. | Read/write |
| `/03-3d-platform-engine-recipes` | Concrete recipes for Web3D (Three.js, R3F, Babylon.js), game engines (Unity World Canvas, Unreal UMG 3D Widgets, Godot), and XR (Apple VisionOS, Meta Quest OpenXR). | Read/write |
| `/04-3d-spatial-qa-optimization` | 3D rendering budget audits (draw calls ≤ 25, transparent overdraw ≤ 2 layers, LOD), dynamic lighting contrast (≥ 4.5:1), and cyber sickness verification. | Read-only / QA report |
| `/05-3d-example-generator` | After explicit user opt-in (consent gate in skill `00`), generates runnable in-browser sample interfaces faithful to the approved `3d_system_design.md` — vanilla HTML/CSS/JS with optional locally vendored Three.js, saved under `docs/3d-ui-design/examples/`. | Read spec / write `docs/3d-ui-design/examples/` |

## Workflow

1. **Orchestrate** — `00-3d-ui-orchestrator` analyzes product intent, classifies the 3D medium, and plans the workflow.
2. **Architect** — `01-3d-spatial-ux-architecture` defines spatial journeys, UI tiers, depth planes, and comfort zones.
3. **Systematize** — `02-3d-design-system-materials` produces spatial tokens, materials, audio, and 3D component specs.
4. **Implement** — `03-3d-platform-engine-recipes` maps the specification onto the target engine or XR platform.
5. **Audit** — `04-3d-spatial-qa-optimization` validates rendering budgets, lighting contrast, and comfort standards.
6. **Prototype (optional)** — `05-3d-example-generator` renders runnable in-browser samples from the approved spec.

Every step writes into one specification, so the final `docs/3d-ui-design/3d_system_design.md` is self-contained and hand-off ready.

## Requirements

- Claude Code 2.x or later

## Installation

Via a plugin marketplace (recommended):

```bash
# In Claude Code
/plugin marketplace add <owner>/<repo>
/plugin install 3d-ui-design-toolkit@<marketplace-name>
```

Or via the CLI:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install 3d-ui-design-toolkit@<marketplace-name>
```

## Usage

Open any project in Claude Code and ask for a 3D UI/UX design task, e.g.:

> "Design a diegetic cockpit HUD for a space-sim game using the 3D UI Design Toolkit."

The orchestrator skill (`00-3d-ui-orchestrator`) triggers automatically and drives the pipeline through its specialist skills.

## Updating

```bash
/plugin update 3d-ui-design-toolkit@<marketplace-name>
```

When releasing a new version, bump the `version` field in the plugin manifest and commit.

## Uninstalling

```bash
/plugin uninstall 3d-ui-design-toolkit@<marketplace-name>
```

Restart the runtime after uninstalling.
