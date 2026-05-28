# Phase 1 — Recon & Inventory

## Objective

Before grading anything, build a complete, verifiable picture of what each bundle actually contains. Names lie; files don't. The deliverable for this phase is a per-bundle inventory and profile that subsequent phases reference.

## Inputs

- One or more bundle root paths (absolute).
- Optional bundle labels (`bundle-A`, `bundle-B`).

## Required Discovery Steps

1. **Resolve bundle root.** Confirm the path exists and contains at least one of: `.claude/`, `harness/`, `harness-runtime/`, `rules/`, `agents/`, `commands/`, `skills/`, `CLAUDE.md`.
2. **List top-level governance files**: `CLAUDE.md`, `README.md`, `LICENSE`, version files. Note presence/absence.
3. **Walk `.claude/` if present**, recording every subtree:
   - `.claude/agents/*.md` — sub-agent definitions
   - `.claude/commands/*.md` — slash commands
   - `.claude/skills/*/SKILL.md` and `.claude/skills/*/references/`
   - `.claude/hooks/*` — pre/post hooks
   - `.claude/settings.json` / `settings.local.json`
4. **Walk harness layer if present**: `harness/`, `harness-runtime/`, `rules/` — record protocol files, runtime config (e.g., `pipelines.json`), validators, tests.
5. **Detect non-Claude-Code variants** (`.codex/`, `.cursor/`, `.aider/`) — note presence as informational; they do not contribute to the Claude-Code score.
6. **Read each `SKILL.md` frontmatter** to extract `name` and `description`. These are the bundle's self-claims.
7. **Read each agent/command file's first 30 lines** for declared purpose, model, and tool list.

## Bundle Profile Template

Produce per bundle:

```
### Bundle Profile: <label>
- Root: <absolute path>
- Top-level governance: CLAUDE.md (Y/N), README.md (Y/N), LICENSE (Y/N)
- Skills count: <n> (paths: <list>)
- Agents count: <n> (paths: <list>)
- Commands count: <n> (paths: <list>)
- Hooks: <list of hook scripts or "None">
- Harness protocol files: <list under harness/ or "None">
- Runtime enforcement: <harness-runtime/* present? entry script? validate command? "None">
- Rules files: <list under rules/ or "None">
- Non-Claude variants: <.codex / .cursor / .aider — informational only>
- Detected language(s) of prose: <Vietnamese / English / mixed>
- Self-claimed scope (from CLAUDE.md or README): <one-paragraph quote or "Unstated">
```

## Inventory Tables

For each bundle produce three tables.

### Skills Inventory

| File | Declared name | Declared description (first 120 chars) | Has references/ subdir? | SKILL.md size (lines) |
|---|---|---|---|---|

### Agents Inventory

| File | Agent purpose (≤ 1 line) | Tools allowed | Read-only? |
|---|---|---|---|

### Commands Inventory

| File | Slash command | Routes to (agents/skills) | Pause/review gates declared? |
|---|---|---|---|

## Cross-Reference Checks

- Every `command` should route to either an `agent`, a `skill`, or another command. List orphan commands (route to nothing).
- Every `skill` referenced in `MEMORY.md`, `CLAUDE.md`, or `commands/*.md` must exist on disk. List dangling references.
- Every harness protocol file imported via `@harness/*.md` in `CLAUDE.md` must exist. List missing imports.

## Self-Claim vs. Reality Diff

Record any discrepancy where the bundle's `README.md` or `CLAUDE.md` claims a capability that has no backing skill or agent. Examples:
- "Includes hard-bug diagnosis" but no `bugfinder-hard` skill or equivalent.
- "Multi-stage verification" but no `verification-protocol.md` or no `verify` command.
- "Runtime enforcement" but no executable runner script.

This diff feeds Phase 2 (coverage) and Phase 7 (governance scoring).

## Output of Phase 1

For each bundle, produce:

1. The Bundle Profile block.
2. Skills, Agents, Commands inventory tables.
3. Cross-reference findings (orphans, dangling references, missing imports).
4. Self-Claim vs. Reality diff.

Save these as a structured fragment that the final report (Phase 7) will quote verbatim.

## Required Practices

- Always count files by walking the filesystem, never by trusting `README.md`.
- Always record both **count** and **paths**, not just count.
- Always quote the bundle's self-description verbatim — do not paraphrase the claim that you intend to challenge later.
- Always check for hidden indicators of automation: `pre-commit`, `husky/`, `.github/workflows/`, `Makefile`, `package.json scripts`.

## Prohibited Practices

- Do not start grading skills in Phase 1. Discovery only.
- Do not skip a subtree because the directory is unfamiliar; either inventory it or explicitly mark it out-of-scope with reason.
- Do not modify any file (no `touch`, no normalization, no auto-format).
- Do not run any executable scripts under the bundle without explicit user approval.
