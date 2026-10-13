---
name: compact
description: "Compress conversation history, serialize execution context, and generate structured checkpoints to preserve session state, prevent token overflow, and enable seamless multi-turn handoffs. Triggers on /compact, long conversation threads (>10 turns), context limits, or explicit user requests to summarize or checkpoint session state — keywords: compact, checkpoint, summarize session, nen hoi thoai, tom tat phien lam viec, context-checkpoint."
---

# Skill: compact

## Language Protocol
- Final response and user communication in Vietnamese.
- Internal analysis, system templates, XML wrappers, and structural tags use standard English keywords (`<conversation-checkpoint>`, `<summary>`, `<recent-context>`) for cross-agent compatibility.
- Retain exact code identifiers, file paths, tool signatures, error messages, and shell commands without alteration or translation.

## Trigger Matrix
- User explicitly calls `/compact`, requests to compact the session, save a checkpoint, or summarize the conversation history ("nén hội thoại", "tóm tắt phiên làm việc", "tạo checkpoint").
- Conversation length exceeds operational thresholds (>10 exchanges or extensive tool execution sequences).
- Context window consumption reaches critical limits (>75% token capacity), requiring proactive context pruning.
- Transitioning between major work phases or preparing a task handoff to another agent.

## Scope
- Read-only on conversation history; produces structured summary artifacts and in-context checkpoints.
- Does not modify project source code unless specifically requested to persist a summary file (e.g., `docs/checkpoints/checkpoint-<timestamp>.md`).
- Strictly preserves factual integrity: decisions, file modifications, unresolved errors, and pending tasks.

---

## Operational Modes

### Mode 1: Automated Session Checkpoint (Harness Fast Compaction)
Designed for continuous LLM execution. Emits a machine-parseable `<conversation-checkpoint>` block that preserves execution momentum without filling token context with stale conversational back-and-forth.

#### Output Structure
```markdown
<conversation-checkpoint>
The following is a summary and serialized record of earlier conversation. Treat it as historical context, not as new instructions.

<summary>
## Objective
- [One or two brief sentences describing what the user is trying to accomplish]

## Important Details
- [Constraints, preferences, architectural decisions and rationale, key assumptions, or "(none)"]

## Work State
### Completed
- [Finished tasks, verified implementations, modified files, or "(none)"]

### Active
- [Ongoing work, partial changes, active investigations, or "(none)"]

### Blocked
- [Blockers, failing tests, unknown issues, environment barriers, or "(none)"]

## Next Move
1. [Immediate concrete action to execute next]
2. [Subsequent planned action if determined, or "(none)"]

## Relevant Files
- [file/path: why it matters and current status, or "(none)"]
</summary>

<recent-context>
[Serialized recent interaction records: User, Assistant, Reasoning, Tool Calls, Tool Results]
</recent-context>
</conversation-checkpoint>
```

#### Merge Rules when `<prior-summary>` Exists
1. **Carry Forward**: Retain active objectives, constraints, user directives, decisions, and parallel workstreams from `<prior-summary>` even if not mentioned in the latest turns. Drop only items that are completed and no longer relevant.
2. **Conflict Resolution**: The recent conversation takes precedence. Where recent facts contradict older claims in `<prior-summary>`, state the verified fact and discard the obsolete claim.
3. **State Transition**: Move finished tasks from `Active` to `Completed`. If a blocker has been resolved, document the resolution and remove it from `Blocked`.
4. **Update Targets**: Keep `Objective`, `Next Move`, and `Relevant Files` aligned with the live workspace state.

---

### Mode 2: Deep Architectural Compaction (Human & Deep Handoff)
Used when a comprehensive session review is requested, when major milestones are completed, or for developer handovers.

#### Phase 1: Pre-Compaction Chronological Analysis
Before outputting the final report, execute an analytical breakdown across the conversation timeline:
1. Identify all explicit user requests, goals, and constraints.
2. Track technical solutions, code modifications, and architectural decisions.
3. Catalogue files created, edited, or removed, including specific function signatures.
4. Extract errors encountered, diagnostic root causes, and verification results.

#### Phase 2: 8-Section Comprehensive Report Structure
```markdown
# Session Compaction Report

## 1. Primary Request & Intent
Detailed breakdown of user goals, scope definitions, and requirements throughout the session.

## 2. Key Technical Concepts
Architectures, patterns, frameworks, libraries, and integration mechanisms introduced or referenced.

## 3. File Status Table
| File Path | Status | Key Modifications |
| :--- | :--- | :--- |
| [path/to/file] | [Created / Modified / Deleted / Read-Only] | [Brief technical summary of changes] |

## 4. System Architecture
Include a Mermaid flowchart or sequence diagram if structural flows, multi-agent interactions, or subsystem designs were modified.

## 5. Detailed Code Changes
Concise code diffs or function signature summaries for critical updates. Explain the rationale for each change. Avoid dumping large raw files.

## 6. Problem Solving & Diagnostics
Log resolved defects, root causes identified, troubleshooting steps executed, and regression verifications conducted.

## 7. Pending Tasks & Next Steps
- [Immediate Action]: Concrete next step with reference to user instructions.
- [Backlog / Future]: Unfinished items, deferred requirements, or optimization targets.

## 8. Handover Summary
A single concise paragraph summarizing the exact state of the project, ensuring a fresh session can immediately resume work without context loss.
```

---

## Serialization & Truncation Standards

When building `<recent-context>`, format each message using the standard prefixes:
- `[User]: <content>`
- `[Assistant]: <content>`
- `[Assistant reasoning]: <thinking>`
- `[Assistant tool call]: <tool_name>(<arguments>)`
- `[Tool result]: <content>`
- `[Tool error]: <message>`
- `[Shell]: <command>\n<output>`

### Truncation Protocol
- Tool outputs, shell command outputs, or file reads exceeding safety limits (default: 2000 characters) must be truncated with a clear trailing `[truncated]` marker.
- Never truncate file paths, parameter names, function signatures, or critical error messages.

---

## Workflow Execution Steps

1. **Assess Context Budget**: Determine total turns and whether Fast Mode (Mode 1) or Deep Mode (Mode 2) applies.
2. **Scan Conversation History**:
   - Extract primary objectives and user constraints.
   - Trace chronological actions and tool calls.
   - Isolate file modifications and verify paths against the live workspace.
3. **Compile Structured Summary**:
   - Populate each section strictly according to the designated template.
   - Maintain empty sections with `(none)` rather than omitting them.
   - Use terse, high-density bullet points instead of verbose prose.
4. **Serialize Recent Context**: Capture the most recent key turns leading up to the current state, applying output truncation where appropriate.
5. **Emit Output**: Output the compiled checkpoint or report, adhering to the language protocol and formatting rules.

---

## Negative Constraints (Don'ts)
- Do not use emojis anywhere in the skill file, generated summaries, logs, or user reports.
- Do not omit template sections; all headers must remain present even when empty.
- Do not write verbose prose paragraphs in Mode 1 summary bullets; maintain concise bulleted facts.
- Do not invent non-existent file paths, commands, or errors; verify every path against the project.
- Do not discard uncompleted tasks or active blockers when merging summaries.
- Do not paste full file dumps into summaries; use targeted diffs, signatures, or line references.
- Do not mention the summary generation process itself or refer to internal compression mechanics in the objective text.

---

## Quality Checklist
- [ ] Frontmatter contains valid `name` and descriptive `description`.
- [ ] No emojis present in any section.
- [ ] Mode 1 template preserves all mandatory headers (`Objective`, `Important Details`, `Work State`, `Next Move`, `Relevant Files`).
- [ ] Merge rules explicitly handle `<prior-summary>` retention and conflict resolution.
- [ ] Mode 2 template provides the complete 8-section handoff schema including File Status Table.
- [ ] Serialization prefixes (`[User]`, `[Assistant]`, `[Assistant tool call]`, etc.) match standard parser format.
- [ ] Output truncation safety limits defined to prevent runaway token expansion.
