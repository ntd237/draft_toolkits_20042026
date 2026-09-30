# Harness Execution Log Standard (Self-Contained)

Canonical specification for the harness execution log mechanism embedded in `00-llm-orchestrator`. This file is the single source of truth for the log mechanism of this toolkit and must be Read by the orchestrator before creating or appending any log section. The toolkit runs standalone — no reference to `plugins/toolkit-lite/` or any external skill is permitted at runtime.

## When to create a log
Create one log file per task that follows one of the 6 canonical pipelines (1–6) of this LLM toolkit. Single-skill, read-only advisory tasks (pure explanation, ad-hoc Q&A) do not require a log.

**CRITICAL INVARIANT**: The presence of in-chat YAML handoff blocks between skills DOES NOT exempt or replace creating this log file. The log file in `docs/harness-logs/` MUST still be created before the first skill runs and updated after each skill completes for every run in pipelines 1–6 without exception.

## File naming
```
docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md
```
- `category`: `new_project` | `add_feature` | `debug_fix` | `refactoring` | `migration` | `adaptation` | `optimization`
- `task_name`: short snake_case description (e.g., `rag_hybrid_search`, `fix_json_parser`)
- `yyyymmdd_hhmmss`: **actual creation time** — run a shell command to get the real timestamp, never hardcode or guess it
- If the task does not fit any of the categories above, omit the category prefix and use `<task_name>_<yyyymmdd>_<hhmmss>.md`

Example: `docs/harness-logs/add_feature_rag_hybrid_search_20260521_143022.md`

## Lifecycle rules
- **Create** the log file at the start of the pipeline, before the first skill runs.
- **Append** one skill section immediately after each skill completes — do not batch at the end.
- **One file per pipeline run** — never create a second file for the same task.
- Create `docs/harness-logs/` if it does not exist before writing the first log.

## Per-skill section template

```markdown
## Skill Execution Log: <skill-name>

- **Skill**: <skill-name> (e.g., 03-llm-implement, 05-llm-fix, 06-llm-test)
- **TDD phase**: Red | Green | Refactor | N/A — <one line; e.g. "Red — regression test fails as expected">
- **Nhiệm vụ**: <mô tả ngắn gọn nhiệm vụ được giao>
- **Đầu vào nhận được**: <context hoặc danh sách file được cung cấp>
- **Files đã sửa**: <danh sách file kèm mô tả thay đổi ngắn gọn, hoặc "Không có">
- **Files đã tạo**: <danh sách file mới, hoặc "Không có">
- **Files đã xóa**: <danh sách — phải có xác nhận của user, hoặc "Không có">
- **Kết quả kiểm tra**: PASS / FAIL — <mô tả chi tiết>
- **Số lần tự sửa lỗi**: <0 nếu pass ngay, hoặc mô tả ngắn về các lần retry>
- **Trạng thái**: COMPLETED / FAILED / PARTIAL
- **Ghi chú**: <quan sát hoặc cảnh báo nếu có, hoặc "Không có">
```

## Pipeline summary template

```markdown
## Tổng kết Pipeline

- **Pattern**: <tên pipeline theo chuẩn 6 pipeline của LLM toolkit: #1 Simple Implementation | #2 Ambiguous Implementation | #3 Complex / Multi-Agent / RAG Implementation | #4a Unknown-Cause Bug (Simple) | #4b Unknown-Cause Bug (Complex) | #5 Known-Cause Bug (Simple) | #6 Known-Cause Bug (Complex)>
- **TDD**: yes (Red → Green → Refactor) | skipped — <reason if skipped> | inverted — <prompt spike/exploratory reasoning>
- **Tổng số skills**: <số>
- **Hoàn thành**: <số>
- **Thất bại**: <số>
- **Tổng files đã sửa**: <danh sách tổng hợp từ tất cả skill logs>
- **Kết quả kiểm tra tổng thể**: PASS / FAIL / PARTIAL
- **Timeline**:
  1. <skill-name>: COMPLETED / FAILED — <mô tả ngắn>
  2. <skill-name>: COMPLETED / FAILED — <mô tả ngắn>
- **Vấn đề gặp phải**: <liệt kê các vấn đề nổi bật, hoặc "Không có">
- **Bước tiếp theo được đề xuất**: <gợi ý hành động tiếp theo cho user>
```

## Language rules
Log content in Vietnamese. Keep in English: skill names, file paths, error messages, command strings, status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL).
