# Phase 3 — Skill Quality Rubric

## Objective

Grade the **content** of every skill in the bundle, ignoring how impressive the name sounds. The output of this phase is a per-skill scorecard that feeds the *Per-Skill Content Quality* axis of the final score.

## Files Under Review

For each skill, evaluate the following set:

- `SKILL.md` (the orchestrator)
- All files under `references/` (if present)
- Any file the SKILL.md links via `@references/...` or relative paths

If a skill has no `references/` and the workflow is rich enough in `SKILL.md` alone, that's fine — do not penalize structural choice; penalize content thinness.

## The Eight Criteria (0–4 each, max 32 → normalized to /100)

For every skill, score these criteria. Each criterion accepts 0, 1, 2, 3, or 4. No half points.

### C1. Role Clarity (0–4)
Does the skill define an expert identity, focus areas, and tone?

- 0 — No role section, or generic ("you are an AI assistant").
- 2 — Role named but focus areas thin or buzzword-only.
- 4 — Senior-level identity, ≥ 3 specific focus areas, tone declared, alignment with task scope.

Evidence to cite: the `## Identity and Role` block (or equivalent) with file:line.

### C2. Scope Boundaries (0–4)
Does the skill say what is **in** and **out** of scope, with refusal handling?

- 0 — No scope section.
- 2 — In-scope listed; out-of-scope vague.
- 4 — In/out clearly enumerated; refusal protocol described; downgrade rules when env lacks tools.

### C3. Step-by-Step Workflow (0–4)
Is the work decomposed into phases/steps with objective and execution per step?

- 0 — One paragraph of advice. No steps.
- 2 — Steps present but no per-step objective + outputs.
- 4 — Numbered phases, each with explicit objective, execution, and named deliverables.

### C4. Output Contract (0–4)
Is there a precise specification of what the skill returns — paths, file naming, sections, conversation summary template?

- 0 — Output unspecified.
- 2 — Loose description ("produce a report").
- 4 — File path, naming pattern, full template structure, summary message format, all defined.

### C5. Examples / Few-Shot (0–4)
Are concrete examples or templates included that a model can pattern-match against?

- 0 — None.
- 2 — One or two short examples, mostly hand-wavy.
- 4 — Multiple worked examples across difficulty/scope, plus templates for common cases.

### C6. Anti-Patterns / Negative Prompts (0–4)
Does the skill list prohibited practices that prevent typical failure modes?

- 0 — No "do not" guidance.
- 2 — Generic warnings ("don't break things").
- 4 — Specific prohibitions tied to known failure modes, with reasoning.

### C7. Quality Checklist (0–4)
Is there a self-verification checklist before delivery?

- 0 — None.
- 2 — Generic "did you test it" line.
- 4 — Concrete checklist tied to the skill's outputs; every item is verifiable.

### C8. Evidence-Grounding & Verification (0–4)
Does the skill require the assistant to anchor claims in file paths, line numbers, command outputs, or transcripts? Does it integrate with a verification protocol?

- 0 — Vibes-based; no grounding requirement.
- 2 — Mentions evidence but does not require it.
- 4 — Mandatory file:line + snippet for findings; references a verification protocol; defines failure escalation.

## Scoring Aggregation per Skill

```
raw   = C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8     (max 32)
norm  = round(raw * 100 / 32)                     (0–100)
```

Letter per skill:
- A: 86–100 — production-grade
- B: 70–85 — solid; minor gaps
- C: 55–69 — usable but soft on contract or examples
- D: 40–54 — sketchy; needs rewrite
- F: < 40 — placeholder

## Penalty Modifiers

Apply the following after scoring the eight criteria, capped at -10 per skill:

- **-2** SKILL.md exceeds 600 lines without splitting into references (token waste).
- **-2** Frontmatter `description` is misleading (does not match the workflow content).
- **-3** Skill duplicates another in the same bundle (charge to whichever is thinner).
- **-2** Skill links to a reference file that does not exist on disk.
- **-3** Skill instructs the assistant to perform actions outside the bundle's permission boundaries (write where read-only is required, etc.).
- **-2** Skill embeds long literal code blocks (> 80 lines) that should be in references.

## Scorecard Template

```
### Skill: <relative path to SKILL.md>

| Criterion | Score | Evidence |
|---|---|---|
| C1 Role | x/4 | <file:line — quote ≤ 25 words> |
| C2 Scope | x/4 | <evidence> |
| C3 Workflow | x/4 | <evidence> |
| C4 Output | x/4 | <evidence> |
| C5 Examples | x/4 | <evidence> |
| C6 Anti-patterns | x/4 | <evidence> |
| C7 Checklist | x/4 | <evidence> |
| C8 Evidence-grounding | x/4 | <evidence> |
| Raw | xx/32 | |
| Modifiers | -x | <reason : reason> |
| **Final** | **xx/100** | Letter: <A–F> |
```

## Special-Skill Overrides (mandatory deeper read)

These five skills receive both a generic scorecard **and** a specialized review that feeds Phase 4 capability scores:

- planning skill (e.g., `05-plan`)
- debug skill (e.g., `17-debug`, `debug`)
- bugfinder skills (regular + hard variant)
- fix-bug skills (regular + hard variant)
- UI design skill (e.g., `11-ui-design`, `ui`)

For these, do not stop at C1–C8. Also evaluate against Phase 4's targeted rubrics. The Phase 3 score is the *content* score; Phase 4 adds *capability* score.

## Phase 3 Output

Per bundle, a list of skill scorecards (one per skill), plus:

- **Average normalized score** across all skills (used for Per-Skill Quality axis in Phase 7).
- **Bottom three skills** by score (with reason).
- **Top three skills** by score (with reason).
- Total penalty applied.

## Required Practices

- Always quote the criterion-defining line from the skill (e.g., the role definition) — do not paraphrase.
- Always read every linked reference file before scoring C5 (Examples) and C7 (Checklist).
- Always check that frontmatter `name` matches the file's stated identity.
- Always identify dead links (referenced files that do not exist).

## Prohibited Practices

- Do not award points for the existence of a section heading without content beneath it.
- Do not give partial credit on C4 (Output Contract) unless paths, naming, and section structure are all specified.
- Do not score a skill above 70 if any of its `references/` files are missing.
- Do not score a skill above 75 if it lacks both a checklist and explicit anti-patterns.
- Do not normalize scores upward "to be fair" — the rubric is the rubric.
