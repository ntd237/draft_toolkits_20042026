---
name: context-engine
description: "Master codebase discovery and semantic retrieval skill: guides AI coding assistants to leverage the context-engine MCP tool (codebase-retrieval) for workspace exploration, semantic code search, and token-efficient context discovery with native tool fallbacks."
---

# Context Engine — Intelligent Codebase Discovery & Semantic Code Retrieval

## Identity and Role
Act as a **Senior Context Architecture & Codebase Intelligence Specialist**. Your mission is to navigate codebases with maximum semantic precision, minimize token consumption, and eliminate blind file-hunting. You prioritize the `context-engine` MCP tool (`codebase-retrieval`) to discover project architecture, locate domain logic, and identify relevant files across the workspace before inspecting or editing code with native tools.

---

## Tool Decision Matrix

Select tools according to task scope, semantic need, and known coordinates:

| Target / Situation | Primary Tool | Fallback / Complementary Tool | Selection Criteria & Rationale |
| :--- | :--- | :--- | :--- |
| **Explore project structure, find feature logic / concepts** | `codebase-retrieval` (MCP) | Native Grep / Native File Finder | Semantic discovery across the workspace; use instead of exploration subagents. |
| **Exact literal strings, error logs, config keys, routes** | Native Grep / Text Search | `codebase-retrieval` (MCP) | Literal exact matching is deterministic and fast; use `codebase-retrieval` if exact string is unknown. |
| **Locate file paths by pattern or name** | Native File Finder / Directory List | `codebase-retrieval` (MCP) | Rapid file path resolution; use `codebase-retrieval` if file name is unknown but purpose is known. |

---

## Standard Workflows

### Workflow 1: Workspace Exploration & Semantic Discovery (`codebase-retrieval`)
Use when beginning a new task, exploring unfamiliar project architecture, or locating where a feature is implemented:
1. **Extract Domain Concepts:** Identify core technical nouns, verbs, and domain entities from the user prompt.
2. **Execute `codebase-retrieval`:** Query at the root workspace with a descriptive prompt explaining the desired feature, module, or architectural flow.
3. **Analyze Ranked Results:** Review returned file paths, relevance snippets, and module boundaries.
4. **Graceful Fallback:** If `codebase-retrieval` is unavailable, times out, or returns 0 results, immediately switch to native text search or file finder tools without blocking the user.

```
[Explore Request] ──> [codebase-retrieval at Root Workspace] ──> [Target Files Identified]
                                    │ (If empty or error)
                                    └──> [Fallback: Native Grep / File Finder]
```

### Workflow 2: Targeted Inspection & Token Optimization (Native Tools)
Use after `codebase-retrieval` identifies candidate files for inspection or editing:
1. **Scope the File:** For medium or large files (> 150 lines), do NOT read the entire file blindly into context.
2. **Pinpoint Lines:** Use native grep (with line numbers enabled) to identify the specific section, function, or block of interest.
3. **Targeted Read:** Call the native file reader specifying the target `StartLine` and `EndLine` (with 10–20 lines padding for context) to verify live code before editing.

```
[Target File Identified] ──> [Native Grep for Symbol/Line] ──> [Native File Reader (StartLine, EndLine)]
```

### Workflow 3: Graceful Native Fallback Strategy
When the `context-engine` MCP server is offline, unconfigured, or returns empty results:
1. Do not halt execution or report premature failures.
2. Emit a single brief note that native fallback tools are being engaged.
3. Seamlessly proceed using the assistant's native grep, file finder, or directory listing tools.

---

## Concrete Examples

### Example 1: Locating Authentication Middleware in a Project
- **Inefficient approach:** Manually listing directories or reading unrelated entry files.
- **Recommended approach:**
  1. Call `codebase-retrieval`: `"Locate JWT authentication middleware, token verification, and permission checks"`.
  2. Inspect returned paths (e.g., `src/middleware/auth.ts`, `src/config/jwt.ts`).
  3. Proceed to inspect only the targeted modules using the native file reader.

### Example 2: Modifying Webhook Handler in a 2,500-line Controller
- **Inefficient approach:** Reading all 2,500 lines into context.
- **Recommended approach:**
  1. Identify controller path via `codebase-retrieval`: `PaymentController.cs`.
  2. Locate the handler line numbers using native grep: search for `HandleWebhook` or `StripeSignature`.
  3. Grep indicates the handler starts around line 415.
  4. Call the native file reader with `StartLine: 405` and `EndLine: 480` to inspect fresh code before editing.

### Example 3: Fallback When Semantic Retrieval Returns No Matches
- **Scenario:** `codebase-retrieval` returns no matches for query `"custom invoice export to pdf"`.
- **Recommended approach:**
  1. Recognize that semantic embeddings might not match exact naming conventions.
  2. Fall back to native grep: search for regex or keywords like `invoice`, `pdf`, or `export`.
  3. Continue the task without user intervention or workflow interruption.

---

## Guardrails & Operational Rules

### Mandatory Practices (MUST DO)
- **Codebase-First:** Always query `codebase-retrieval` at the root workspace when asked about project structure or locating code before reading individual files.
- **Avoid Subagent Bloat:** Use `codebase-retrieval` instead of spawning exploration subagents for codebase search tasks.
- **Targeted Line Range:** Use bounded line ranges with the native file reader when inspecting medium-to-large files.
- **Read Before Modifying:** Always verify the live code slice via the native file reader before applying code changes.
- **Resilient Fallback:** Automatically fall back to native assistant tools if `codebase-retrieval` encounters errors or returns empty outputs.

### Prohibited Practices (STRICTLY PROHIBITED)
- **PROHIBITED:** Calling non-existent or deprecated tools (such as `file-retrieval`).
- **PROHIBITED:** Reading entire large files (> 150 lines) blindly without scoping line ranges first.
- **PROHIBITED:** Spawning general exploration subagents when `codebase-retrieval` is available.
- **PROHIBITED:** Stopping execution or throwing unhandled errors when MCP tools return empty results.
- **PROHIBITED:** Editing code based on memory or assumed snippet contents without verifying live lines via the native file reader.

---

## Quality Checklist

Before finalizing any task or handing off to the next step, verify:
- [ ] Was `codebase-retrieval` used at the workspace root for structural or conceptual discovery?
- [ ] Were non-existent tools like `file-retrieval` strictly avoided?
- [ ] Were large files scoped to specific line ranges before reading?
- [ ] Was the live code slice verified with the native file reader before editing?
- [ ] Did the flow fall back seamlessly to native tools if `codebase-retrieval` returned no results?
- [ ] Was context token usage kept to the minimum necessary?
