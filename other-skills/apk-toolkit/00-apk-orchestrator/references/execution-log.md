# Harness Execution Log Standard (Self-Contained — apk-toolkit)

Canonical specification for the harness execution log mechanism of this toolkit, embedded in the orchestrator skill (`00-apk-orchestrator`). This file is the single source of truth for logging: it is fully self-contained and runs standalone — no runtime reference to any external skill, plugin, or meta-skill path is permitted.

## When to create a log
Create one log file per task that follows one of the 6 canonical pipelines (1–6) of this toolkit. Single-skill, read-only advisory tasks (pure explanation, ad-hoc Q&A) do not require a log.

**CRITICAL INVARIANT**: The presence of in-chat YAML handoff blocks between skills DOES NOT exempt or replace creating this log file. The log file in `docs/harness-logs/` MUST still be created before the first skill runs and updated after each skill completes for every run in pipelines 1–6 without exception.

## File naming
```
docs/harness-logs/<category>_<task_name>_<yyyymmdd>_<hhmmss>.md
```
- `category`: `new_project` | `add_feature` | `debug_fix` | `refactoring` | `migration` | `adaptation` | `optimization`
- `task_name`: short snake_case description (e.g., `user_auth`, `fix_null_pointer`, `appx_free2paid`)
- `yyyymmdd_hhmmss`: **actual creation time** — run a shell command to get the real timestamp, never hardcode or guess it
- If the task does not fit any of the categories above, omit the category prefix and use `<task_name>_<yyyymmdd>_<hhmmss>.md`

Example: `docs/harness-logs/add_feature_appx_free2paid_20260521_143022.md`

## Lifecycle rules
- **Create** the log file at the start of the pipeline, before the first skill runs.
- **Append** one skill section immediately after each skill completes — do not batch at the end.
- **One file per pipeline run** — never create a second file for the same task.
- Create `docs/harness-logs/` if it does not exist before writing the first log.

## Per-skill section template

```markdown
## Skill Execution Log: <skill-name>

- **Skill**: <skill-name> (e.g., 03-apk-implement, 05-apk-fix, 06-apk-test)
- **TDD phase**: Red | Green | Refactor | N/A — <one line; e.g. "Red — S3 edition assertion fails as expected">
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

- **Pattern**: <tên pipeline theo chuẩn 6 pipeline của domain toolkit>
- **TDD**: yes (Red → Green → Refactor) | skipped — <reason if skipped> | inverted — <spike/exploratory>
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

The 6 canonical pipeline names of this toolkit (valid values for **Pattern**):
- Pipeline 1 — Simple Conversion
- Pipeline 2 — Ambiguous Conversion
- Pipeline 3 — Complex / Multi-Split Conversion
- Pipeline 4a — Unknown Bug (Simple) / Pipeline 4b — Unknown Bug (Complex)
- Pipeline 5 — Known Bug (Simple)
- Pipeline 6 — Known Bug (Complex)

## Language rules
Log content in Vietnamese. Keep in English: skill names, file paths, error messages, command strings, status keywords (COMPLETED, FAILED, PARTIAL, PASS, FAIL).
