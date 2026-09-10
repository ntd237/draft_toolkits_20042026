---
name: code-search-expert
description: "Expert code retrieval and navigation: uses CodeGraph AST intelligence, ripgrep lexical search, and vector semantic retrieval with automatic Vietnamese-to-English query expansion to locate logic, symbols, and call hierarchies across complex codebases without token waste or search misses. Triggers when the user asks to find, locate, trace, or analyze code — functions, classes, call graphs, error messages, config keys, or architectural flows."
---

# Skill: code-search-expert

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English before proceeding.
- Internal analysis in English; final response in Vietnamese.

## Trigger
User asks to find, locate, trace, or analyze code — business logic, functions, classes, call hierarchies, error messages, log text, API routes, config keys, or architectural flows across a codebase.

## Tool Decision Matrix

Choose the primary tool based on target nature:

| Target Type | Primary Tool | Fallback | Why |
| :--- | :--- | :--- | :--- |
| Logic flow, architecture, function/class implementation | `codegraph_explore` | `codegraph_search` + `codegraph_node` | Returns AST-connected symbol source in one round-trip |
| Call hierarchy ("who calls X?", "what does X call?") | `codegraph_callers` / `codegraph_callees` | `grep_search` | Uses graph edges; handles callbacks & dynamic dispatch |
| Refactor blast radius ("what breaks if I change X?") | `codegraph_impact` | `codegraph_callers` | Traverses dependency tree up to N levels |
| Exact strings, error messages, log text, API routes, config keys | `grep_search` (ripgrep) | `find_by_name` | Literal strings are NOT AST symbols; CodeGraph will miss them |
| Abstract concept / CodeGraph returns empty | `codebase-retrieval` (Semantic RAG) | `grep_search` (root stems) | Neural embeddings bridge vocabulary gaps |

## Workflow

### Phase 1: Query Expansion
**Objective**: Bridge the semantic gap between Vietnamese prompts and English codebase identifiers.

- Extract the core concept from the user request — strip conversational phrasing, keep business nouns and verbs.
- Generate 4–6 English technical synonyms (domain jargon, CRUD conventions, noun/verb variants).
- Combine into a space-separated query bag for `codegraph_explore` (e.g., `"payout withdraw disbursement billing"`).
- Common semantic mappings:
  - Rút tiền / Trả tiền: `[payout, withdraw, disbursement, cashout, debit, transfer, settlement]`
  - Hủy đơn / Hủy thao tác: `[cancel, abort, revoke, terminate, void, rollback, dismiss]`
  - Lưu tạm / Nháp: `[draft, pending, temp, stash, staging, uncommitted]`
  - Hoa hồng / Giảm giá: `[commission, fee, discount, coupon, voucher, rebate, tariff]`
  - Xác thực / Đăng nhập: `[auth, login, signin, credential, token, session, authenticate]`
  - Phân quyền / Vai trò: `[permission, role, grant, access_control, acl, policy, authority]`
  - Đồng bộ / Cập nhật: `[sync, reconcile, refresh, poll, mutate, ingest, replicate]`

### Phase 2: Pre-Flight Check & Targeted Search
**Objective**: Verify CodeGraph readiness, then call the right tool for the target type.

- Before calling CodeGraph tools, verify `.codegraph/` is initialized (call `codegraph_status` if needed). If missing, fall back to `codebase-retrieval` / `grep_search` — do not spam CodeGraph tools on an uninitialized database.
- For logic/flows: run `codegraph_explore` with the expanded query bag.
- For exact symbols: run `codegraph_search` with candidate symbol names.
- For logs/routes/configs: run `grep_search` with exact literal patterns or regex.

### Phase 3: Fallback Ladder (If Initial Query Returns 0 Matches)
**Objective**: Exhaust all search tiers before concluding a target is absent.

Never stop or guess after an initial empty result. Execute the cascading fallback:
1. `codegraph_explore` with primary query bag.
2. If empty: `codegraph_explore` with alternative synonyms.
3. If still empty: `codebase-retrieval` with the natural-language query.
4. If still empty: `grep_search` with partial word roots (e.g. `pay`, `draw`, `settle`) scoped to relevant subdirectories.

### Phase 4: Synthesis & Targeted Reading
**Objective**: Report exact locations without token waste.

- Return exact file paths (with markdown file links), symbol signatures, and line ranges.
- When viewing code, avoid reading unbounded entire files (>500 lines); use `StartLine` and `EndLine` based on discovered positions.

## Output Format
- File path as markdown link: `[filename.ts](file:///absolute/path/to/file.ts#L10-L30)`
- Include function/class name and exact line numbers.
- Brief explanation of what the found code does, tied to the user's original question.

## Don'ts
- Do not pass raw Vietnamese sentences directly into `codegraph_search` or `grep_search` — always expand to English synonyms first.
- Do not give up after 1 search attempt without trying the Fallback Ladder.
- Do not run repeated `view_file` calls across dozens of files without using search tools first.
- Do not call CodeGraph tools repeatedly when `codegraph_status` reports `.codegraph/` is not initialized.
- Do not re-grep code already returned by `codegraph_explore` — trust the AST result.

## Quality Checklist
- [ ] Has the target logic/symbol been located with exact file path and line numbers?
- [ ] Were 4–6 technical synonyms considered if the original prompt was Vietnamese?
- [ ] Did the search use the appropriate tool tier (CodeGraph vs Grep vs Semantic Search)?
- [ ] If initial search missed, was the Fallback Ladder executed before concluding?
- [ ] Are file paths returned as clickable markdown links?
