---
name: 04-bugfinder
description: "Investigates and identifies root causes of defects across frontend (UI/state/rendering), backend (logic/API/service), or database (query/transaction/connection pooling), including performance issues. Mandatorily triggered when 00-orchestrator determines the defect cause is unknown (Scenarios #4a, #4b) — before transitioning to 05-fix is permitted. Read-only by default — investigates and reports root causes only; transient debug probes are strictly regulated and must be verified clean before handoff."
---

# 04-bugfinder — Multi-Tier Root Cause Investigation

## Trigger
Mandatorily invoked by `00-orchestrator` when defect causes are unknown (no concrete evidence pointing directly to the failure location). Must not be skipped in such cases, even if the user conjectures a cause without verified evidence.

## Workflow

### Phase 1: Reproduce & Localize
**Objective**: Identify reproduction conditions and localize the offending layer.

1. Collect symptoms: issue description, logs, tracebacks, network request/response payloads (if involving frontend-backend), query logs / execution plans (if suspecting database).
2. Localize the layer: determine whether errors manifest in the frontend (console errors, corrupt state, rendering bugs), backend (error logs, erroneous responses, unhandled exceptions), database (slow queries, deadlocks, incorrect result sets), or inter-layer interactions (contract mismatches, race conditions).
3. If reproduction information is insufficient, explicitly specify the missing details (do not guess root causes without evidence).

### Phase 2: Root Cause Analysis & Diagnostic Ladder
**Objective**: Trace from symptoms to the true root cause, refusing to stop at surface-level descriptions.

1. For backend/database: apply appropriate diagnostics (trace stack traces, EXPLAIN ANALYZE for slow queries, verify transaction isolation / connection pool configs) to pinpoint the exact line of code, query, or configuration causing the fault.
2. For frontend: trace state flow, component lifecycles, root re-renders, or asynchronous race conditions.
3. For cross-layer bugs: pinpoint contract breakages (e.g., backend modified response fields but frontend was not updated).
4. Distinguish genuine root causes from symptoms — never report "API returned 500 error" as a root cause when the actual cause is "query timeout due to a missing index".
5. **Transient Instrumentation Protocol (Debug Probes)**:
   - Prioritize non-invasive observation first (stack traces, server logs, network inspect).
   - If and only if non-invasive methods cannot isolate the fault (e.g., asynchronous race conditions, intermittent state corruption, complex query bindings), temporary probe logging is permitted.
   - Every temporary probe statement MUST be clearly tagged with `// [DEBUG-PROBE]` or `<!-- [DEBUG-PROBE] -->` (or language comment equivalent).
   - Probes must remain strictly read-only (observing variable state, timestamps, call sequence); never mutate state or alter logic.

### Phase 3: Impact Scoping
**Objective**: Determine blast radius to enable `00-orchestrator` to assess complexity (simple vs complex).

1. Enumerate other modules/layers potentially affected by the same root cause (e.g., the same flawed query pattern reused across multiple endpoints).
2. Assess whether the defect is single-layer/single-module (→ branch 4a) or multi-tier/multi-module (→ branch 4b) for proper orchestrator routing.

### Phase 4: Cleanup Gate & Handoff Preparation
**Objective**: Guarantee that 100% of temporary probe instrumentation is completely removed prior to handoff.

1. Search the codebase for `[DEBUG-PROBE]` to locate all injected instrumentation statements.
2. Remove all probe statements, reverting files to their exact pre-investigation state.
3. Verify via diff / inspection that zero residual debug probes remain (`cleanup_verified: true`).

## Output Format
Report containing: Symptoms & reproduction conditions → Offending layer → Specific root cause (exact location: file/line/query/config) → Blast radius (simple/complex, single-tier/multi-tier) → Recommended fix approach (do not write fix code). 

Additionally, output the structured YAML handoff block for `06-test` or `02-plan`:
```yaml
handoff:
  from_skill: "04-bugfinder"
  to_skill: "06-test" # or "02-plan"
  offending_layer: "backend" # frontend | backend | database | multi-tier
  exact_location: "src/db/queries/order.ts:42"
  root_cause: "N+1 query loop when fetching order items without JOIN"
  blast_radius: "simple" # simple | complex
  recommended_fix: "Use INNER JOIN with items table and eager load"
  cleanup_verified: true # confirms all temporary debug instrumentation was removed
```

## Don'ts
- Do not edit production logic to "see if the bug goes away" — investigative transient instrumentation is permitted only when tagged with `[DEBUG-PROBE]`, and must be completely removed before handoff.
- Do not leave temporary probe code in the repository — leaving any `[DEBUG-PROBE]` in files is a critical cleanup violation.
- Do not report symptoms as root causes (e.g., "database error" without specifying the exact query, table, or missing index).
- Do not skip Phase 3 (impact scoping) — this is mandatory input for the orchestrator to branch into 4a vs 4b.
- Do not guess root causes without sufficient reproduction evidence — articulate missing information instead of speculating.

## Quality Checklist
- [ ] Were non-invasive observation methods prioritized before inserting any transient instrumentation?
- [ ] Was all transient instrumentation tagged with `[DEBUG-PROBE]` completely removed and verified clean (Cleanup Gate) prior to handoff?
- [ ] Is the root cause pinpointed to a specific location (file/line/query/config) rather than a vague symptom?
- [ ] Has the offending layer (frontend/backend/database/multi-tier) been clearly identified?
- [ ] Has the blast radius (simple/complex) been evaluated to guide proper orchestrator branching?
- [ ] Is the structured YAML handoff block populated with `cleanup_verified: true`?
