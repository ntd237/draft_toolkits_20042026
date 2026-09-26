---
name: 05-ui-example-generator
description: "Generate static sample interfaces (vanilla HTML/CSS/JS only) from the synthesized system_design.md specification. Triggered after 00-ui-orchestrator completes and the user explicitly opts in."
---

# UI Example Generator

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.

## Trigger
Activates only when the user consents to sample interface generation after `00-ui-orchestrator` has delivered an approved `system_design.md`, or when the user explicitly asks to build sample UI/mockup pages from an existing specification.

Skip when no `system_design.md` exists, when the specification has not been approved, or when the user asks for production frontend code with a framework (React/Vue/...) — that is outside this skill's scope.

## Workflow

### Phase 1: Spec Intake & Screen Inventory
**Objective**: Extract every implementable decision from the specification before writing a single line of markup.

1. Read `docs/ui-design/system_design.md` and extract: design tokens (60-30-10 palette Light/Dark, spacing, radius, elevation), Vietnamese typography scale (font stack, line-height 1.4–1.6), IA sitemap, component specifications with their 6 states, responsive breakpoint matrix, and target platform(s).
2. If the spec is missing, incomplete (no tokens or no sitemap), or unapproved, stop and report what is missing — never invent unspecified design decisions.
3. Build a screen inventory: one example page per Level-1/Level-2 sitemap entry, prioritizing the critical task flows defined in section 2 of the spec.

### Phase 2: Static Page Generation
**Objective**: Implement the inventoried screens as standalone static pages that faithfully render the spec.

1. Write all output to `docs/ui-design/examples/` (create the directory if missing), one folder or file set per page, with `index.html` as the entry point listing links to all sample pages.
2. Author markup and styles in **vanilla HTML, CSS, and JavaScript only**:
   - Express every token from the spec as CSS variables (`:root` / `[data-theme="dark"]`), including Light/Dark switching if the spec defines a dark theme.
   - Apply the type scale and mandatory line-height 1.4–1.6 so Vietnamese diacritics never clip.
   - Implement the responsive matrix with the spec's breakpoints; adapt navigation per platform recipe (Bottom Bar → Rail → Sidebar) where applicable.
   - Demonstrate all 6 interactive states for each primary component using CSS (`:hover`, `:active`, `:focus-visible`, `:disabled`) and minimal JS for loading/error states.
   - Use semantic HTML landmarks and the spec's accessibility constraints (contrast, focus visibility).
3. Reference assets relatively only (no absolute paths, no CDN, no external fonts — fall back to the spec's system font stack if a webfont cannot be bundled locally).

### Phase 3: Verification & Delivery
**Objective**: Confirm the samples open and behave standalone, then hand back a file report.

1. Verify each page has no broken relative links and no dependency on a dev server (openable via `file://`).
2. Cross-check every page against the spec: token values match, breakpoints match, required states present, Vietnamese text renders with correct line-height.
3. Report to the user: list of created files under `docs/ui-design/examples/`, which spec sections each page demonstrates, and any spec decisions that could not be represented in static HTML.

## Output Format
- `docs/ui-design/examples/index.html` — gallery entry point linking all sample pages
- One static page (HTML + CSS + JS) per inventoried screen, plus a short `docs/ui-design/examples/README.md` describing how to open the samples and which spec sections they demonstrate

## Don'ts
- Do not use any framework, library, bundler, build tool, or CDN resource — output must run by opening `index.html` directly in a browser.
- Do not introduce colors, spacing values, fonts, or components absent from `system_design.md`.
- Do not modify `system_design.md` or any skill file while generating examples.
- Do not generate sample pages for screens outside the approved sitemap.

## Quality Checklist
- [ ] `system_design.md` exists and was read in full before generation
- [ ] All output files live under `docs/ui-design/examples/` with an `index.html` entry point
- [ ] Every page uses only vanilla HTML/CSS/JS with zero external requests
- [ ] Tokens, typography (line-height 1.4–1.6), breakpoints, and 6-state components match the spec exactly
- [ ] `docs/ui-design/examples/README.md` explains how to view the samples
- [ ] Final report lists every created file and its corresponding spec section
