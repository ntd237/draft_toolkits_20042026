# Phase 12 — Final Report Template

## Objective

Consolidate every phase output into a single, predictable Markdown file at:

```
docs/toolkit-evaluation/toolkit-eval_<yyyymmdd>_<hhmmss>.md
```

The file lives in the **project**, not the toolkit. Create `docs/toolkit-evaluation/` if it does not exist.

The conversation message back to the user must be a short Vietnamese summary including the per-bundle final score, letter grade, top-3 strengths, top-3 weaknesses, and a clickable path to the report.

---

## File Naming

- Format: `toolkit-eval_<yyyymmdd>_<hhmmss>.md`
- Example: `toolkit-eval_20260526_143000.md`
- Use the local time at the moment the report is generated.

---

## Full Report Template

Use this exact structure. Empty sections must still appear with "Không có" / "None" so the structure is preserved across runs.

```markdown
# Toolkit & Harness Engineering Evaluation

- **Generated**: <yyyy-mm-dd hh:mm local>
- **Mode**: read-only (audited bundles unchanged)
- **Bundles evaluated**: <list of labels>
- **Depth**: quick | standard | deep
- **Auditor**: toolkit-harness-evaluator skill (Claude)

---

## 1. Executive Summary

<3–8 câu tiếng Việt. Tóm tắt: số bundle được đánh giá, kết quả tổng quan (xếp hạng nếu N ≥ 2), bundle mạnh nhất ở axis nào, các điểm đáng lo nhất, có cap nào bị kích hoạt không.>

### Top-Line Numbers

| Bundle | Total | Letter | Tier ceiling | Critical gaps | Cap triggered |
|---|---:|:---:|:---:|---|:---|
| <name> | xx.x | <L> | <T> | <list or None> | <if any> |
| ... |

---

## 2. Bundle Profiles

> One subsection per bundle, copied from Phase 1 outputs.

### 2.1 <Bundle label>

- Root: <path>
- Skills: <n> · Agents: <n> · Commands: <n>
- Hooks: <count or None>
- Harness protocol files: <list>
- Runtime enforcement: <runner present? validate works?>
- Self-claimed scope: "<verbatim quote>"
- Detected language: <Vietnamese / English / mixed>

#### Inventories

<Skills, Agents, Commands tables from Phase 1.>

#### Cross-Reference Findings

- Orphan commands: <list or None>
- Dangling skill references: <list or None>
- Missing imports: <list or None>

#### Self-Claim vs. Reality Diff

<List of claimed-but-missing capabilities, or "None">

<repeat for each bundle>

---

## 3. Coverage

### 3.1 Canonical 11-Category Matrix

| # | Category | <bundle A> | <bundle B> | ... |
|---|---|:---:|:---:|---|
| 1 | Planning | Present (file:line) | Partial (file:line) | ... |
| 2 | Init | ... |
| ... |

### 3.2 Project Archetype Breadth

| Archetype | <A> | <B> | ... |
|---|:---:|:---:|---|
| Web frontend | ✓ | ✓ | |
| Web backend  | ✓ | ✗ | |
| Mobile       | ✓ | ✓ | |
| Desktop      | ✗ | ✓ | |
| AI/ML        | ✓ | ✗ | |
| Data pipeline| ✓ | ✓ | |
| CLI/Library  | ✓ | ✓ | |
| Infra/IaC    | ✗ | ✓ | |
| Game/Graphics| ✗ | ✗ | |

### 3.3 Bloat & Overlap

- <Bundle>: <skill A> overlaps with <skill B> (file paths, reason)
- ...

---

## 4. Per-Skill Content Quality

> One subsection per bundle, condensed from Phase 3 scorecards.

### 4.1 <Bundle label>

| Skill | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Mod | Final /100 | Letter |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| <skill> | x | x | x | x | x | x | x | x | -x | xx | <A–F> |
| ... |

- Average normalized score: xx
- Top three skills: <list>
- Bottom three skills: <list>
- Total penalty applied: -x

<repeat for each bundle>

---

## 5. Specialized Capability Tests

> Per-bundle table of capability scores plus evidence.

| Bundle | Plan /8 | Debug /7 | Bugfinder /10 | Fix-Bug /8 | UI /5 | Sum /38 |
|---|---:|---:|---:|---:|---:|---:|

### 5.1 Evidence Citations

- <Bundle>: Plan = x — <quote / file:line>
- <Bundle>: Debug = x — <quote / file:line>
- ...

### 5.2 Live Execution Transcripts (deep mode)

- <Bundle>: see `docs/toolkit-evaluation/transcripts/<bundle>/<skill>.md`
- (or "Not run; static analysis only")

---

## 6. Bug Difficulty Tier Coverage

| Bundle | Easy /4 | Medium /4 | Hard /4 | Very Hard /4 | Super Hard /4 | Tier total /20 | Ceiling |
|---|---:|---:|---:|---:|---:|---:|:---:|

### 6.1 Notes per tier

- <Bundle> tier H: <evidence quote / shortcoming>
- <Bundle> tier V: <evidence>
- <Bundle> tier S: <evidence>

---

## 7. Non-Functional Axes

### 7.1 Token Economy

| Bundle | Avg load | Max load | Heaviest skill | Modifiers | Score /8 |
|---|---:|---:|---|---|---:|

### 7.2 Latency / Round-trip Cost

| Bundle | Round-trips (typical) | Read budget | Approval gates | Score /5 |
|---|---:|---:|---|---:|

### 7.3 Live Measurements (deep mode)

> CSV path or "Not measured."

---

## 8. Behavioral Axes & Governance

### 8.1 Parallel Execution Capability (A12)

| Bundle | P1 Tool-batch | P2 Sub-agent fanout | P3 Pipeline concurrency | P4 Map-reduce | P5 Independence | P6 Conflict | Subtotal /6 | Mod | A12 /5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| <bundle A> | x.x | x.x | x.x | x.x | x.x | x.x | x.x | -x.x | x.x |

### 8.2 Orchestrator Coordination Quality (A13)

| Bundle | O1 Routing | O2 Pipelines | O3 Handoff | O4 Gates | O5 Retry | O6 Log | O7 Convergence | Subtotal /7 | Mod | A13 /7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| <bundle A> | x.x | x.x | x.x | x.x | x.x | x.x | x.x | x.x | -x.x | x.x |

### 8.3 Harness-Runtime Governance

| Pillar | <bundle A> /1.5 | <bundle B> /1.5 | ... |
|---|---:|---:|---|
| G1 Rule Loading | x.x | x.x | |
| G2 Verification | x.x | x.x | |
| G3 Retry        | x.x | x.x | |
| G4 Execution Log| x.x | x.x | |
| G5 Permissions  | x.x | x.x | |
| G6 Runtime      | x.x | x.x | |
| Subtotal        | xx.x| xx.x| |
| Integration mod | -x.x| -x.x| |
| **Final /9**    | **xx.x** | **xx.x** | |

> A11 = round(Final /9 × 8/9), capped at 8.

### 8.4 Integration Cross-Check Findings

- <Bundle>: <break>
- ...

---

## 9. Final Scores

> One subsection per bundle, from Phase 10.

### 9.1 <Bundle label>

| Axis | Weight | Score | Notes |
|---|---:|---:|---|
| A1 Coverage Completeness | 13 | xx.x | |
| A2 Coverage Breadth      |  8 | x.x  | |
| A3 Skill Content Quality | 12 | xx.x | |
| A4 Plan                  |  8 | x.x  | |
| A5 Debug                 |  7 | x.x  | |
| A6 Bugfinder             |  9 | x.x  | tier ceiling = <X> |
| A7 Fix-Bug               |  8 | x.x  | |
| A8 UI Design             |  5 | x.x  | |
| A9 Token Economy         |  6 | x.x  | |
| A10 Latency              |  4 | x.x  | |
| A11 Governance           |  8 | x.x  | |
| A12 Parallel             |  5 | x.x  | |
| A13 Orchestrator         |  7 | x.x  | |
| **Total**                | **100** | **xx.x** | |
| **Letter (after caps)**  | | **<L>** | <cap or "no cap"> |

<repeat for each bundle>

---

## 10. Comparative Ranking (only when N ≥ 2)

> Insert outputs O1–O7 from `11-comparative-analysis.md` here.

### 10.1 Leaderboard
### 10.2 Per-Axis Head-to-Head
### 10.3 Strengths / Weaknesses Cards
### 10.4 Pairwise Delta Matrix (or Top/Bottom-3 callout if N > 4)
### 10.5 Use-Case Recommendations
### 10.6 Anti-Recommendations
### 10.7 Migration Notes (if applicable)

---

## 11. Remediation Roadmap

> Per bundle. Group by impact on score.

### 11.1 <Bundle label>

#### Tier 1 — Score-critical (≥ 5 points if fixed)
- <action> — <axis impacted> — <expected delta>

#### Tier 2 — Important (2–5 points)
- ...

#### Tier 3 — Hygiene (< 2 points)
- ...

---

## 12. Appendix

### 12.1 Methodology

- Phases run: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, (11 if N ≥ 2), 12
- Token estimation: 1 token ≈ 4 chars (prose), 1 token ≈ 3.5 chars (code)
- Live execution: <Yes / No>, with per-prompt approval

### 12.2 Files Audited

- <Bundle>: <count> skill files, <count> reference files, <count> agent files, <count> command files

### 12.3 Tools Used

| Tool | Command | Exit | Summary |
|---|---|---:|---|
| <runner> validate | `...` | 0 | <result> |
| <runner> semantic-validate | `...` | 0 | <result> |

### 12.4 Statement of Limitations

- This is a **read-only** audit. No bundle file was modified.
- Static analysis substitutes for live execution unless explicitly approved.
- Tokens labelled `estimated` were computed from byte length, not from the live tokenizer.
- The audit covers Claude-Code surfaces only; non-Claude variants under `.codex/`, `.cursor/`, `.aider/` were inventoried but not graded.
- Capability scores reflect what the skill content **forces** the assistant to do, not what a clever assistant might do despite the skill.
```

---

## Conversation Summary Template (Vietnamese)

After the file is written, post a short message in chat. Keep it brief — the report is the artifact.

```
Đã hoàn tất đánh giá toolkit ở chế độ READ-ONLY trên: <bundle paths>

Tổng điểm theo bundle:
- <bundle A>: xx.x — <Letter> (tier ceiling: <X>)
- <bundle B>: xx.x — <Letter> (tier ceiling: <X>)
- ...

Top 3 điểm mạnh chung: <axis>, <axis>, <axis>
Top 3 điểm yếu chung: <axis>, <axis>, <axis>

Cap đã kích hoạt: <list or "Không có">
Xếp hạng (nếu N ≥ 2): 1) <name>  2) <name>  3) <name>

Báo cáo đầy đủ: [docs/toolkit-evaluation/toolkit-eval_<yyyymmdd>_<hhmmss>.md](docs/toolkit-evaluation/toolkit-eval_<yyyymmdd>_<hhmmss>.md)

Lưu ý: Đây là rà tĩnh dựa trên nội dung file; không thực thi tool nào của bundle ngoài các lệnh validate được user duyệt.
```

---

## Required Practices

- Always create `docs/toolkit-evaluation/` if it does not exist.
- Always include every section header even if a section is empty (`Không có` / `None`).
- Always preserve per-bundle scorecards in Section 9, even when comparative ranking is shown in Section 10.
- Always include the Statement of Limitations.
- Always link the report path with `[path](path)` so the user can click it in the IDE.
- Always show the math for the final score in Section 9.

## Prohibited Practices

- Do not write the report file outside `docs/toolkit-evaluation/`.
- Do not omit Section 10 when N ≥ 2; comparative ranking is mandatory in that case.
- Do not paste full transcripts inline; link to persisted files.
- Do not rewrite axis labels or weights from `08-scoring-rubric.md`.
- Do not produce more than one report file per evaluation run.
- Do not silently drop a bundle from the leaderboard for any reason; if a bundle could not be scored, document why and place it at the bottom marked "Unscored — reason."
