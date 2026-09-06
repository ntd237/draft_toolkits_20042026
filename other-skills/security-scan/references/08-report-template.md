# Phase 7 — Report Template

## Objective

Consolidate every finding into a single, predictable Markdown document at:

```
docs/security-scan/security-scan_<yyyymmdd>_<hhmmss>.md
```

The file lives in the **project**, not the toolkit. Create the `docs/security-scan/` directory if it does not exist.

The conversation message back to the user must be a short Vietnamese summary that includes severity counts and a clickable path to the report.

---

## File Naming

- Format: `security-scan_<yyyymmdd>_<hhmmss>.md`
- Example: `security-scan_20260518_143000.md`
- Use the local time at the moment the report is generated.

---

## Full Report Template

Use this exact structure. Sections may be empty (write "Không có" / "None") but must be present.

```markdown
# Security Scan Report — <project name or root path>

- **Generated**: <yyyy-mm-dd hh:mm local>
- **Mode**: read-only
- **Scope**: <paths included>
- **Excluded**: <paths excluded>
- **Auditor**: security-scan skill (Claude)

---

## 1. Executive Summary

<2–6 câu tiếng Việt: tóm tắt tình trạng tổng thể, các nhóm rủi ro chính, mức độ khẩn của remediation.>

### Severity Counts

| Severity | Count |
|---|---|
| Critical | <n> |
| High     | <n> |
| Medium   | <n> |
| Low      | <n> |
| Info     | <n> |
| **Total**| <n> |

### Top 3 Issues to Address First

1. <Title — file:line — one-line impact>
2. <Title — file:line — one-line impact>
3. <Title — file:line — one-line impact>

---

## 2. Scope & Methodology

### 2.1 Project Profile

- Languages: <list>
- Frameworks: <list>
- Application type: <web frontend | backend | mobile | library | CLI | data pipeline | mixed>
- Package managers: <list>
- Container / IaC present: <yes/no — list>

### 2.2 Files Audited

- Source directories: <list>
- Config files: <list>
- Manifests / lockfiles: <list>
- IaC files: <list>
- CI files: <list>

### 2.3 Out-of-Scope

- Vendored: <list>
- Generated: <list>
- Tests: <included | excluded — reason>
- Other exclusions: <list>

### 2.4 Methodology

- Phases run: 1 — Recon, 2 — Secrets, 3 — Injection, 4 — Auth/Crypto, 5 — Config/Infra, 6 — Dependencies
- Manual review only (where SCA tools were not run): <list>
- Tools run with user approval: <see Appendix>

---

## 3. Findings

> Findings are grouped by severity. Within a severity, sort by category (Secret → Injection → Auth → Crypto → Config → Dep).

### 3.1 Critical

#### CR-01: <Title>
- **Category**: <e.g., A03:2021 Injection / CWE-89>
- **File**: `<path>:<line>` (or range)
- **Source → Sink**: <if injection-class>
- **Evidence**:
  ```<lang>
  <minimal snippet, ≤ 10 lines, secrets masked>
  ```
- **Impact**: <one paragraph; concrete attacker capability>
- **Remediation**:
  1. <step>
  2. <step>
  3. <verification step>
- **References**: <CVE / CWE / OWASP link>

<repeat CR-02, CR-03, ...>

### 3.2 High
<same structure with HI-01, HI-02, ...>

### 3.3 Medium
<same structure with ME-01, ME-02, ...>

### 3.4 Low
<same structure with LO-01, LO-02, ...>

### 3.5 Info
<same structure with IN-01, IN-02, ...>

---

## 4. Remediation Roadmap

A prioritized plan the team can execute, grouped by effort.

### 4.1 Immediate (within 24–72 hours)
- All Critical findings
- Active secret rotations

### 4.2 Short-Term (within 2 weeks)
- All High findings
- Dependency updates with confirmed exploitability

### 4.3 Medium-Term (within 1 quarter)
- All Medium findings
- Hardening: security headers, CSP, rate limiting

### 4.4 Hygiene & Process
- All Low / Info findings
- Tooling: enable Dependabot/Renovate, add pre-commit hooks for secret scanning, integrate Semgrep into CI

---

## 5. Suppressions & Known False-Positive Filters

<List anything the auditor deliberately did not flag, with reason. Examples: AWS docs example keys, test fixtures with synthetic credentials.>

---

## 6. Appendix

### 6.1 Tools Used

| Tool | Version | Command | Exit | Summary |
|---|---|---|---|---|
| <tool> | <ver> | `<command>` | <code> | <counts> |

> Full tool outputs (if persisted) are at the paths listed in this table. They are not included inline because of size.

### 6.2 Routes / Entry Points Inventory

<For backend audits: list of HTTP routes / handlers / RPC methods. Mark each with: requires-auth (Y/N), authorization-check (present/missing), method.>

### 6.3 Cryptographic Primitives Detected

<List of hash/cipher/HMAC calls found, with verdict (OK / Weak / Broken). This grounds Section 4 (Auth/Crypto) findings.>

### 6.4 Environment / Config Files Inspected

<List, with sensitivity rating: contains-secret-pattern / placeholder-only / encrypted.>

### 6.5 Dependency Manifest Snapshot

<Top-line counts: total deps, direct vs. transitive (when known), oldest dep major version, count of deps with known advisories.>

---

## 7. Statement of Limitations

- This is a **static, read-only audit**. No live exploitation, fuzzing, or DAST was performed.
- SAST and SCA tools find a subset of real vulnerabilities; absence of findings is not absence of vulnerabilities.
- Reachability claims labeled "heuristic" were not verified by full call-graph analysis.
- The auditor did not modify any source, config, or build files.
- The auditor did not transmit project content to any third-party service.
```

---

## Conversation Summary Template (Vietnamese)

After the file is written, post a short message in chat. Keep it brief — the report is the artifact.

```
Đã hoàn tất security scan ở chế độ READ-ONLY trên: <path>

Số phát hiện theo mức độ:
- Critical: <n>
- High:     <n>
- Medium:   <n>
- Low:      <n>
- Info:     <n>

Top 3 cần xử lý ngay:
1. <title> — <file:line>
2. <title> — <file:line>
3. <title> — <file:line>

Báo cáo đầy đủ: [docs/security-scan/security-scan_<yyyymmdd>_<hhmmss>.md](docs/security-scan/security-scan_<yyyymmdd>_<hhmmss>.md)

Lưu ý: Đây là rà quét tĩnh, không phải pentest. Tôi không thực thi exploit, không upload mã nguồn ra ngoài, và không sửa file nào.
```

---

## Finding ID Convention

Use a short prefix per severity so findings can be referenced in conversation:

| Prefix | Severity |
|---|---|
| CR-NN | Critical |
| HI-NN | High |
| ME-NN | Medium |
| LO-NN | Low |
| IN-NN | Info |

NN is two-digit, zero-padded, restarts per severity.

---

## Inclusion Rules per Finding

Every finding must include all of these fields. If any is missing, the finding is not ready for the report:

- ID and Title
- Severity
- Category (OWASP / CWE reference where possible)
- File path with line (or precise range)
- Evidence snippet (≤ 10 lines, secrets masked)
- Impact (one paragraph, concrete)
- Remediation (numbered steps, including a verification step)
- References (CVE / GHSA / CWE / OWASP, if any)

---

## Required Practices

- Always create the `docs/security-scan/` directory if it does not exist.
- Always include severity counts in the summary table and the chat reply.
- Always include the "Statement of Limitations" section.
- Always link the report path with the relative-path Markdown link form `[path](path)` so the user can click it in IDE.
- Always include a Tools Used table even when no tools were run (use "None — manual review only").

## Prohibited Practices

- Do not include raw secret values anywhere in the report. Mask everything.
- Do not paste tool outputs > 50 lines into the report; summarize and reference.
- Do not omit the limitations statement; it sets expectations correctly.
- Do not write the report file outside `docs/security-scan/`.
- Do not write more than one report per scan run.
