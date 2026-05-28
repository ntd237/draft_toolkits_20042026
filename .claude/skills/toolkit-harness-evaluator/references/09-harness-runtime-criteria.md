# Phase 9 — Harness-Runtime Governance Criteria

## Objective

Skills are the muscles. The harness is the spine. A bundle without governance — verification, retry, permission boundaries, runtime enforcement — is a prompt collection, not a harness-engineering toolkit. This phase audits the spine.

## Six Governance Pillars

A complete harness-runtime contract must address every pillar below.

### G1. Rule Loading & Bootstrap Contract
**What to look for**:
- A top-level `CLAUDE.md` (or equivalent root) that declares which rule files are mandatory.
- Explicit `@rules/*.md` imports OR a documented loader that reads `rules/00-index.md`.
- A clear precedence statement: which root wins when multiple roots exist (user/global vs. project).

**Audit checklist**:
- [ ] `CLAUDE.md` present.
- [ ] Bootstrap contract names every required rule file.
- [ ] Each named rule file exists on disk.
- [ ] Precedence between roots stated.
- [ ] Failure mode declared if a rule file is missing (e.g., "stop and report").

### G2. Verification Protocol
**What to look for**: a protocol file (e.g., `harness/verification-protocol.md`) that defines:
- Verification tiers per agent type (basic / standard / strict).
- Required steps per tier (build, lint, test, regression, proof-of-fix).
- Verdict template (`PASS / FAIL`, `Verdict: VERIFIED / FAILED`).
- Tier downgrade rule when tooling is missing.
- Same-error early-stop rule.

**Audit checklist**:
- [ ] File exists.
- [ ] Tiers explicitly assigned to each agent type.
- [ ] Verdict template is concrete and copy-pasteable.
- [ ] Downgrade rule present.
- [ ] Same-error rule present.

### G3. Retry / Self-Correction Policy
**What to look for**: a policy file that defines:
- Per-agent retry limits.
- Self-correction loop steps (read error → root cause → revert → fix → re-verify).
- No-patch-stacking rule (revert before retrying).
- Diagnostic Summary template for escalation when limit is reached.
- Reset semantics (per-task vs. per-session).

**Audit checklist**:
- [ ] File exists.
- [ ] Per-agent limits specified.
- [ ] Same-error early stop documented.
- [ ] Diagnostic Summary template present.
- [ ] Reset semantics declared.

### G4. Execution Log Schema
**What to look for**:
- Storage location and naming convention (e.g., `docs/harness-logs/<pattern>_<yyyymmdd>_<hhmmss>.md`).
- Per-agent execution log section.
- Pipeline-level summary section.
- Language rule for the log content.
- Rule that **only the orchestrator** writes the log (sub-agents do not).
- Rule that logs live in the project, not the toolkit.

**Audit checklist**:
- [ ] File exists.
- [ ] Path and naming canonical.
- [ ] Per-agent + pipeline templates concrete.
- [ ] Language rule stated.
- [ ] Orchestrator-only writer rule stated.
- [ ] Logs scoped to project, not toolkit.

### G5. Permission Boundaries
**What to look for**:
- Scope declaration template every agent must produce before writing.
- Per-agent allow/deny matrix on file-system actions.
- High-risk action list (delete, schema change, CI change, dep change, env change).
- Confirmation request template for high-risk actions.
- Out-of-scope file request template.

**Audit checklist**:
- [ ] File exists.
- [ ] Scope declaration template present.
- [ ] Allow/deny matrix complete for declared agents.
- [ ] High-risk list and confirmation template defined.
- [ ] Read-only agents flagged explicitly.

### G6. Runtime Enforcement
**What to look for**:
- A runner script (e.g., `harness-runtime/harness_runner.py`) with subcommands like `validate`, `semantic-validate`, `run-pipeline`, `gateway`, `install-ci`.
- Config files driving the runtime (e.g., `harness-runtime/config/*.json`).
- Validation tests (unit tests for the runtime).
- A documented invocation path (in `rules/06-runtime-enforcement.md` or equivalent).
- A gateway that mediates file writes / shell commands during pipeline runs.

**Audit checklist**:
- [ ] Runner script exists and is executable.
- [ ] Subcommands documented.
- [ ] Config files exist and parse.
- [ ] Tests exist (even minimal smoke tests).
- [ ] Pipelines define phase order and approval gates.
- [ ] Gateway pattern exists for write/shell mediation.

## Per-Pillar Score (0–1.5 each, total 0–9)

For each pillar:

- **0** — Pillar absent.
- **0.5** — Pillar partially present (file exists but is shallow, or missing key elements).
- **1.0** — Pillar present, complete, but lacks one of: examples, failure modes, integration with other pillars.
- **1.5** — Pillar fully complete with examples, failure modes, integrated with other pillars.

Total governance score: **sum of six pillars, max 9**, contributes to the *Harness-Runtime Governance Completeness* axis in the final scoring rubric.

## Integration Cross-Checks

Award **+0** but log the following as findings if integration is broken:

- Verification Protocol references retry limits → those limits must match Retry Policy.
- Retry Policy escalation message → must point to Diagnostic Summary defined in Verification or Retry file.
- Permission Boundaries high-risk list → must align with what `runtime-enforcement` actually gates.
- Execution Log Schema → orchestrator's instructions in commands must require log writes per the schema.
- Rule Loading → if `CLAUDE.md` `@-imports` a path, that file must exist.

Each integration break is a -0.5 modifier (capped at -2 across all integration breaks).

## Runtime Enforcement Live Smoke (deep mode, optional)

If the bundle has a runner and the user approves:

1. Run `<runner> validate` and capture exit code.
2. Run `<runner> semantic-validate` and capture exit code.
3. Run `<runner> run-pipeline --workflow <known-workflow> --task "smoke" --dry-run` and capture exit code.
4. Run any unit tests under `harness-runtime/tests/` and capture results.

Successful exits add +0.5 to G6 (cap pillar at 1.5). Failures are findings, not deductions on G6 — the documentation is graded; runtime correctness is supplementary.

## Reporting

```
### Harness-Runtime Governance

| Pillar | File reviewed | Score (0–1.5) | Notes |
|---|---|---:|---|
| G1 Rule Loading | <path> | x.x | <reason> |
| G2 Verification | <path> | x.x | <reason> |
| G3 Retry | <path> | x.x | <reason> |
| G4 Execution Log | <path> | x.x | <reason> |
| G5 Permissions | <path> | x.x | <reason> |
| G6 Runtime | <path> | x.x | <reason> |
| Subtotal | | xx.x/9 | |
| Integration modifiers | | -x.x | |
| **Final** | | **xx.x/9** | |
```

## Required Practices

- Always look for each pillar's **own** file before concluding it is missing — do not rely on the orchestrator's prose.
- Always check disk for `@-imported` paths.
- Always run integration cross-checks; this is where "harness-shaped" but actually-broken bundles fail.
- Always note whether the runtime can run on the user's OS (Windows vs. Unix).

## Prohibited Practices

- Do not award full credit for a pillar that exists but contradicts another.
- Do not run the bundle's runner without explicit per-command approval.
- Do not extend governance pillars beyond the six listed; new candidate pillars belong in a follow-up version of this rubric, not this audit.
