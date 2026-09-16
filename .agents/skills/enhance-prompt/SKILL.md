---
name: enhance-prompt
description: "Auto-detect and enrich incomplete or vague prompts before AI processing or before passing to another skill (brainstorm, create-prompt, research, etc.). Triggers automatically when the input prompt is missing critical context, especially for programming, AI/ML, and technical tasks. Outputs a single, complete, ready-to-use enriched prompt."
---

# Enhance-Prompt — Auto Context Enrichment

## Execution Directives & Constraints
- **Rewrite Only**: Do NOT execute the prompt. Do NOT answer the prompt. Only rewrite it.
- **Protected Mentions Preservation**: If the prompt contains tokens of the form `⟦PLH:N⟧` (protected @-mentions), copy each token unchanged into the rewritten prompt at the same relative position. Do not delete, translate, or reformat them.

## Language Protocol
- All responses in Vietnamese.
- Technical terms stay in English (framework names, function names, error messages).
- Internal gap analysis in English, final enriched prompt in Vietnamese.

## Trigger
Run automatically when the user's input matches **≥2** of these signals:

| Signal | Example |
|--------|---------|
| Missing Role/Persona | No "act as", no expert framing |
| Missing Output Format | No mention of format, length, or structure |
| Missing Constraints | No dos/don'ts, no scope boundary |
| Vague Action Verb | "help me", "make", "do something with" |
| Missing Context Object | No file, no codebase, no data description |
| Missing Goal/Why | No success criteria, no end objective |
| Programming-specific gaps | No language, no framework, no error message, no version |

Skip this skill if the prompt already contains: explicit role + clear task + output format + constraints.

## Workflow

### Phase 1: Gap Analysis (internal, never shown to user)
**Objective**: Score every dimension of the raw prompt so Phase 2 knows what to infer vs ask.

Scan across 7 dimensions — score each ✅ Clear / ⚠️ Inferable / ❌ Missing:
```
[1] ROLE        — Is there an expert persona? Domain specified?
[2] TASK        — Is the action clear and atomic? Or compound/vague?
[3] CONTEXT     — Is background info sufficient to avoid wrong assumptions?
[4] INPUT       — Is the input artifact described? (code, data, file, API, etc.)
[5] OUTPUT      — Is the expected output format/structure specified?
[6] CONSTRAINTS — Are there rules, limits, anti-patterns to respect?
[7] GOAL        — Is the success criterion or end objective stated?
```

For programming prompts, additionally check:
```
[P1] Language & version    — Python 3.11? TypeScript 5? Node 20?
[P2] Framework/Library     — FastAPI? React? PyTorch? LangChain?
[P3] Environment           — OS, Docker, cloud provider, hardware (GPU?)
[P4] Error/Symptom         — Exact error message? Traceback? Behavior observed?
[P5] Codebase scope        — Single file? Module? Full repo?
[P6] Performance targets   — Latency? Throughput? Memory budget?
[P7] Integration points    — DB, API, auth, queue, cache involved?
```

### Phase 2: Decision — Infer or Ask
**Objective**: Resolve every gap found in Phase 1 with minimal friction for the user.

Infer aggressively. Ask only when a wrong assumption would waste significant effort.

| Situation | Action |
|-----------|--------|
| Gap is ⚠️ Inferable from other signals | Infer + note assumption inline in enriched prompt |
| Gap is ❌ Missing but low-risk | Apply a Smart Default (see table below) |
| Gap is ❌ Missing AND high-risk | Ask — max 1 question per gap, max 2 questions total |

**Always ask, never assume** (high-risk gaps):
- Target language/framework when the prompt could apply to multiple (e.g., "build an API" — FastAPI? Express? Spring?)
- Whether to modify existing code or write from scratch
- Production vs. prototype quality requirement
- Sensitive constraints (auth, PII, compliance)

**Question format** (if asking):
> ❓ **[Gap label]**: [One sentence why this matters]
>
> **A.** [Option A] **B.** [Option B] **C.** [Option C] **D.** Khác

Wait for the answer before proceeding to Phase 3.

**Smart Defaults Library** — apply silently when the gap is low-risk:

| Gap | Default Applied |
|-----|----------------|
| Output format unspecified | Markdown with code blocks |
| Language unspecified (general task) | Ask (high-risk) |
| Code quality unspecified | Balanced (readable + correct) |
| Response length unspecified | "Comprehensive but no padding" |
| Audience unspecified | Senior engineer peer |
| Error handling unspecified | Include basic error handling |
| Test requirement unspecified | Include usage example, not full test suite |

**Code Quality Level** — auto-select from keywords:
- "quick", "script", "test it" → Prototype quality (readability > optimization)
- "production", "deploy", "scale" → Production quality (error handling, logging, tests)
- "review", "refactor" → Maintainability focus (SOLID, clean code, complexity)
- Default → Balanced (readable + correct + handles edge cases)

**Debug prompts** — if the prompt involves debugging, always add to Input section:
```
- [ ] Exact error message / traceback
- [ ] Minimal reproducible code snippet
- [ ] Expected vs. actual behavior
- [ ] What was already tried
```

**AI/ML prompts** — if the prompt involves ML/DL, always add to Context section:
```
- Model architecture / framework (PyTorch, JAX, HuggingFace)
- Dataset size and format
- Training hardware (GPU type, VRAM)
- Performance baseline (current metric vs. target)
```

### Phase 3: Output — Enriched Prompt
**Objective**: Deliver exactly one self-contained, ready-to-use prompt.

Produce one complete prompt using this structure:

```
## [Enriched Prompt Title]

### 🎯 Role & Context
[Expert persona + background context + why this task is being done]

### 📋 Task
[Clear, atomic action statement — what exactly to do]

### 📥 Input
[Description of the artifact being worked on — code, data, API, file, etc.]
[Include: language, framework, version, environment if applicable]

### 📤 Expected Output
[Format: Markdown / JSON / Code block / Structured text]
[Length/scope guidance]
[Example structure if helpful]

### ⚙️ Constraints & Rules
**Must do:**
- [Rule 1]
- [Rule 2]

**Must NOT do:**
- [Anti-pattern 1]
- [Anti-pattern 2]

### ✅ Success Criteria
[How to know the output is correct and complete]

---
> 💡 *Enriched from original prompt. Assumptions made: [list inferences, e.g., "Python 3.11+", "return Markdown"]*
```

After delivering the enriched prompt, offer next steps:
```
✅ Prompt đã được enrich. Bạn muốn:
A. Dùng ngay với AI
B. Đưa vào skill `brainstorm` để thiết kế solution
C. Đưa vào skill `create-prompt` để tinh chỉnh thêm
```

## Output Format
Exactly one enriched prompt, self-contained, using the Phase 3 structure — no deviation, no multiple variants.

## Don'ts
- Do not explain the enrichment process to the user (unless they ask).
- Do not output multiple prompt variants.
- Do not add sections that the raw prompt explicitly excluded.
- Do not hallucinate technical details (version numbers, API names) — use placeholders instead.
- Do not ask more than 2 questions before outputting the enriched prompt.
- Do not skip the `💡 Assumptions made` footer.
- Do not exceed 200 lines in the enriched prompt itself.

## Quality Checklist
- [ ] All 7 dimensions analyzed (+ P1–P7 if programming)?
- [ ] No assumption made on a high-risk gap without asking?
- [ ] Enriched prompt is self-contained — no external context needed to understand it?
- [ ] Assumptions footer is complete and honest?
- [ ] Enriched prompt is ≤200 lines?
- [ ] Prompt uses positive framing (what to do) + negative guardrails (what NOT to do)?
- [ ] Success criteria are measurable, not vague ("correct and complete" is vague — specify)?