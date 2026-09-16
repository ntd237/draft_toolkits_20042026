---
description: Optimize, clarify, and enrich user prompts or instructions to maximize AI execution quality, strictly matching the user's input language
argument-hint: [raw-user-request-or-prompt]
---

# Command: optimize-input

## Context & Scope
- **Raw Input**: $ARGUMENTS
- **Permission Scope**: Read-only (transform and optimize input prompts; do not mutate source files or configurations).

## Execution Directives & Constraints
- **Rewrite Only**: Do NOT execute the prompt. Do NOT answer the prompt. Only rewrite it.
- **Protected Mentions Preservation**: If the prompt contains tokens of the form `⟦PLH:N⟧` (protected @-mentions), copy each token unchanged into the rewritten prompt at the same relative position. Do not delete, translate, or reformat them.

## Mandatory Language Rule
- **Strict Language Preservation**: The final optimized prompt **MUST** be written in the exact same language as the user's input (e.g., English input &rarr; English output, Vietnamese input &rarr; Vietnamese output, Japanese input &rarr; Japanese output).
- Do not translate the user's request into another language unless explicitly requested by the user.
- Technical identifiers (file extensions, function names, library names, CLI commands) should remain standard and uncorrupted.

---

## Optimization Engine & Dimensions

When processing `$ARGUMENTS`, analyze and enrich across 5 core dimensions:

1. **Clarity & Actionability**:
   - Replace vague or generic verbs (*"read"*, *"check"*, *"make"*, *"help me with"*, *"fix"*) with precise, concrete action statements (*"read and analyze"*, *"inspect and locate"*, *"implement with comprehensive error handling"*, *"isolate root cause and fix"*).
2. **Context & Scope Boundary**:
   - Explicitly identify target files, directories, components, or scope (e.g. `README.md in the project root directory`, specific config files, API routes, database models).
3. **Structured Deliverables**:
   - Detail the exact components expected in the response (e.g. purpose, architecture/structure, key features, step-by-step installation, usage examples, edge cases, error handling).
4. **Output Format & Standards**:
   - Specify the desired response format (e.g. structured Markdown with headings, tables, clean code blocks with syntax highlighting, step-by-step plans).
5. **Constraints & Guardrails**:
   - Add practical quality constraints (e.g. non-breaking changes, clean code, handling edge cases, avoiding unnecessary external dependencies).

---

## Execution Workflow

### Phase 1: Ingest & Language Detection
**Objective**: Detect the input language and extract the user's core intent.

1. Detect the primary natural language of `$ARGUMENTS` (e.g., English, Vietnamese, French, etc.).
2. Extract the core intent, goal, and domain (General QA, Code Exploration, Feature Implementation, Bug Fixing, Code Review, Testing, Documentation, Architecture).
3. Identify missing context, ambiguities, or unstated assumptions.

### Phase 2: Context Enrichment & Structuring
**Objective**: Expand the raw prompt into an execution-ready, high-signal instruction.

1. Clarify the target object (e.g. `"the README file"` &rarr; `"the README.md file in the project root directory"`).
2. Enumerate explicit requirements and breakdown points.
3. Formulate clear quality criteria and formatting guidelines.
4. Ensure the scope remains faithful to the user's original intent without adding unwanted fluff or speculative scope creep.

### Phase 3: Generate Direct Optimized Prompt
**Objective**: Deliver a clean, ready-to-use, single-block optimized prompt in the detected language.

1. Construct a unified, complete, and self-contained prompt ready to copy-paste or execute directly.
2. Seamlessly blend the enriched context, target files/scope, concrete action verbs, and explicit deliverables into natural, flowing instructions.
3. Keep the prompt cohesive in a single direct text block without breaking it into complex multi-section boilerplate.

---

## Output Format

Present the response cleanly:

```markdown
### 🎯 Optimized Prompt ([Detected Language])

[Insert the complete, single-block optimized prompt here in the matching language]
```

*(Optional: If high-risk ambiguities exist, append a brief 1-line note with assumptions made in the same language).*

---

## Examples & Reference Transformations

### Example 1: Documentation & Overview (English)
- **User Input**: `Read the README file and give me information about this project.`
- **Optimized Output**:
> Please read the README.md file in the project root directory and provide a comprehensive summary of this project. Include details about its purpose, key features, structure, installation steps, usage guidelines, and any other relevant information found in the documentation.

### Example 2: Bug Fixing (Vietnamese)
- **User Input**: `Sửa lỗi đăng nhập giúp tôi.`
- **Optimized Output**:
> Vui lòng kiểm tra và khắc phục lỗi đăng nhập trong module xác thực (authentication). Trước tiên, hãy phân tích các tệp mã nguồn và log lỗi liên quan để xác định chính xác nguyên nhân gốc rễ (root cause). Sau đó, hãy triển khai giải pháp sửa lỗi tối ưu, xử lý đầy đủ các trường hợp ngoại lệ (edge cases), bảo toàn tính tương thích và cung cấp các bước hoặc test case để kiểm chứng lỗi đã được khắc phục hoàn toàn.

---

## Don'ts
- **Never change the language**: Do not output English when the user asked in Vietnamese, and do not output Vietnamese when the user asked in English.
- **Do not distort intent**: Keep the core goal intact; do not introduce unrelated requirements or change the user's actual objective.
- **Do not overcomplicate**: For simple requests, provide a clean, direct prompt rather than an overly bloated, unnecessary multi-page document.
- **Do not invent false details**: Do not hallucinate nonexistent paths, libraries, or APIs when they are not specified or inferred from context.

---

## Quality Checklist
- [ ] Language of the output matches the language of the user input 100%?
- [ ] Core intent accurately captured and made specific and actionable?
- [ ] Scope, target files, and deliverables explicitly detailed?
- [ ] Output is immediately usable without requiring manual rewrites?
- [ ] Technical terms and identifiers preserved accurately?
