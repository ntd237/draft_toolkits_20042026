---
name: enrich-prompt
description: "Optimize, clarify, and enrich raw user prompts before execution. Combines Mode A (Direct Single-Block - default, strict language preservation, concise) and Mode B (Structured Multi-Section - detailed structural breakdown for complex technical tasks). Triggers when prompts are vague, incomplete, or missing critical context."
---

# Enrich-Prompt — Dual-Mode Context Enrichment

## Execution Directives & Constraints
- **Rewrite Only**: Do NOT execute the prompt. Do NOT answer the prompt. Only rewrite it.
- **Protected Mentions Preservation**: If the prompt contains tokens of the form `⟦PLH:N⟧` (protected @-mentions), copy each token unchanged into the rewritten prompt at the same relative position. Do not delete, translate, or reformat them.

## Language Protocol
- **Strict Language Mirroring (Universal Rule)**: All user-facing output — including the enriched prompt, section titles, headers, descriptions, clarification questions, and assumptions notes — **MUST strictly match 100% of the user's input language** across BOTH Mode A and Mode B (e.g., Vietnamese input &rarr; Vietnamese output; English input &rarr; English output; Japanese input &rarr; Japanese output).
- Never translate the user's request, intent, or output into another language unless explicitly requested by the user.
- Standard technical identifiers and terms (frameworks, APIs, functions, classes, CLI flags, file paths, error messages) must remain standard and uncorrupted in English.
- Internal processing and gap analysis may be conducted in English, but all deliverables presented to the user must strictly mirror the user's input language.

## Trigger
Activates when the user requests prompt optimization, clarification, or enrichment (`enrich-prompt`, `optimize prompt`, `rewrite prompt`, `enhance prompt`, `tối ưu prompt`, `làm rõ prompt`); or when the raw user instruction is vague, incomplete, or lacking critical technical context before execution.

## Workflow

### Phase 1: Ingest, Language Detection & Mode Selection
**Objective**: Detect the natural language of the input prompt and determine the execution mode, locking the output language and prioritizing Mode A by default.

1. Detect the primary natural language of the raw input prompt (English, Vietnamese, Japanese, etc.) and lock all subsequent generation strictly to this language.
2. Select the processing mode according to precedence:
   - **Mode A (Direct Single-Block - DEFAULT)**: Applied to all standard requests unless another mode is requested. Produces a cohesive, single-block prompt that is immediately usable without formatting friction.
   - **Mode B (Structured Multi-Section)**: Activated when explicit flags/keywords are present (`--mode-b`, `--structured`, `--detailed`, `--breakdown`, `structured format`) or when managing highly complex technical/AI-ML tasks requiring explicit separation across concern boundaries.
3. Extract core intent, domain scope, and primary target artifacts.

### Phase 2: Context Enrichment & Gap Analysis
**Objective**: Fill information gaps and enrich context according to the selected mode without distorting the user's original intent.

1. **Processing under Mode A (Default)**:
   - Apply the 5 core optimization dimensions from `references/mode_a_direct.md`:
     - *Clarity & Actionability*: Replace generic verbs with precise technical actions.
     - *Context & Scope Boundary*: Pinpoint exact target files, modules, or directories.
     - *Structured Deliverables*: Enumerate expected output artifacts and components.
     - *Output Format & Standards*: Define formatting expectations (Markdown, clean code diffs).
     - *Constraints & Guardrails*: Embed practical quality guardrails (non-breaking, error handling).
2. **Processing under Mode B (Structured)**:
   - Audit the 7 core dimensions (Role, Task, Context, Input, Output, Constraints, Goal) and 7 engineering criteria (P1–P7) from `references/mode_b_structured.md`.
   - Apply the Smart Defaults Library for low-risk gaps.
   - For high-risk gaps (e.g., conflicting tech stacks), prompt with at most 1–2 concise multiple-choice questions in the user's exact language before generating output.

### Phase 3: Prompt Generation
**Objective**: Output exactly one complete, execution-ready prompt in the detected language and the format dictated by the selected mode.

1. **Mode A Output (Default)**:
   - Synthesize a single cohesive text block with natural transitions and clear instructions in the detected user language.
   - Strictly lock output language to match 100% of the user's input language.
   - Render inside the standard Mode A output container.
2. **Mode B Output (Structured)**:
   - Render the complete multi-section layout with localized headings matching the user's language (e.g., Vietnamese headings for Vietnamese input, English headings for English input): Title, Role & Context, Task, Input, Expected Output, Constraints & Rules (Must do / Must NOT do), and Success Criteria.
   - All section contents, descriptions, and criteria must be written 100% in the user's detected language.
   - Append an inline technical assumptions note in the matching language.

### Phase 4: Quality & Integrity Verification
**Objective**: Self-audit the generated prompt against quality criteria before delivery.

1. Verify compliance against the Quality Checklist below, especially language preservation.
2. Confirm technical identifiers and terms remain accurate and standard.
3. Deliver the finalized prompt directly without superfluous meta-commentary or process explanation.

---

## Output Format

### When running Mode A (Default)

```markdown
### 🎯 Enriched Prompt ([Detected Language] - Mode A: Direct)

[Insert the complete, single-block enriched prompt here in the user's exact matching language, fully cohesive and ready to copy-paste]
```

*(Optional: If critical technical inferences were made, append a 1-line note below in the same language: `> 💡 Note on assumptions / Ghi chú giả định: [...]`).*

---

### When running Mode B (Structured)

```markdown
### 🎯 Enriched Prompt (Mode B: Structured)

## [Descriptive Task Title in User Language]

### 🎯 Role & Context 
- **Role**: [Target expert role]
- **Context**: [System background and operational rationale]

### 📋 Task 
[Clear, atomic action description in User Language]

### 📥 Input 
- **Artifacts**: [Target files, API contracts, database schemas]
- **Tech Stack**: [Languages, frameworks, runtime versions]

### 📤 Expected Output 
- **Format**: [Structured Markdown / Code blocks / Tables]
- **Deliverables**: [List of concrete components to deliver]

### ⚙️ Constraints & Rules 
**Must do:**
- [Mandatory technical requirement in User Language]

**Must NOT do:**
- [Prohibited anti-pattern / Constraint boundary in User Language]

### ✅ Success Criteria
- [Concrete, verifiable verification targets in User Language]

---
> 💡 *Assumptions made: [Inferred technical defaults and configurations in User Language]*
```

---

## Don'ts
- **Never change or translate the user's language in ANY mode**: Whether operating in Mode A or Mode B, the output language MUST strictly match 100% of the user's input language (Vietnamese input &rarr; Vietnamese prompt; English input &rarr; English prompt; Japanese input &rarr; Japanese prompt).
- Do not split the prompt into multiple discrete subheadings (Role, Task, Input...) when operating in Mode A; Mode A must remain a single cohesive text block.
- Do not automatically switch to Mode B unless explicitly requested by the user or required by high-complexity architectural scope; Mode A is always the default.
- Do not hallucinate nonexistent package names, API versions, or file paths without noting them in assumptions.
- Do not output multiple prompt variations; provide only the single highest-quality enriched prompt.
- Do not preface the output with conversational filler or lengthy explanations of the enrichment process.

---

## Quality Checklist
- [ ] Entire output (prompt content, section headings, notes, and questions) strictly matches 100% of the user's input language across both Mode A and Mode B?
- [ ] No spontaneous translation to English or another language occurred in either Mode A or Mode B?
- [ ] Mode A (Direct Single-Block) is applied by default when no Mode B indicator is present?
- [ ] Mode A output is a single, fluid, cohesive paragraph ready for direct execution?
- [ ] When Mode B is invoked, all 7 structural sections and relevant P1–P7 criteria are populated in the user's language?
- [ ] User's core objective is preserved without unintended scope creep?
- [ ] Technical terms, identifiers, and file paths are preserved accurately in standard English?
- [ ] SKILL.md and all references files remain strictly under 300 lines?
