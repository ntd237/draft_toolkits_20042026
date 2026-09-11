---
name: security-scan
description: Read-only security audit skill for source code, dependencies, configuration, and secrets. Identifies OWASP Top 10 vulnerabilities, hardcoded credentials, insecure crypto/auth patterns, and misconfigurations, producing an evidence-backed, severity-ranked report.
---

# Skill: security-scan

## Language Protocol
- Respond in Vietnamese. Restate non-English requests in English first.
- Internal analysis in English; final report in Vietnamese with standard security terminology (CVE, CWE, OWASP, Severity levels).

## Trigger
User asks to audit code for security flaws, scan for hardcoded secrets or dependency vulnerabilities, review security posture, or runs `/security-scan`.

## Workflow

### Phase 1: Recon & Scope Definition
**Objective**: Identify project architecture, tech stack, and dependencies, and establish scanning boundaries.

- Identify primary languages, web frameworks, database ORMs, package managers, and deployment configurations (`Dockerfile`, CI workflows, IaC manifests).
- Determine scan scope: default to entire workspace or narrow to user-specified directories (e.g., `src/`, `api/`). Exclude build artifacts (`dist/`, `build/`), vendor libraries (`node_modules/`, `vendor/`, `.venv/`), and test mocks unless specifically requested.
- Inspect whether existing security tooling configurations are present (`.gitleaks.toml`, `.semgrep/`, `bandit.yaml`, `dependabot.yml`).

### Phase 2: Static Vulnerability & Secret Audit
**Objective**: Audit codebase, dependencies, and configuration across key threat vectors using static analysis.

- **Secrets & Sensitive Exposure**:
  - Scan for hardcoded API keys, private keys, JWT secrets, database connection strings, passwords, and cloud tokens (AWS, GCP, Stripe, GitHub).
  - Distinguish production secrets from obvious placeholders (e.g., `CHANGE_ME`, `example.com`) or unit test fixtures.
- **OWASP Top 10 & Code Injection**:
  - Audit database queries for SQL/NoSQL injection (raw string concatenation, missing parameterized queries).
  - Check command execution and system calls (`exec`, `eval`, `spawn`, `popen`, `os.system`) for unsanitized user inputs.
  - Audit web endpoints for cross-site scripting (XSS), server-side request forgery (SSRF), path traversal (`../`), and insecure deserialization.
- **Authentication, Authorization & Cryptography**:
  - Inspect auth middleware for missing access controls, broken object-level authorization (IDOR), and unauthenticated sensitive routes.
  - Verify session handling: cookie flags (`Secure`, `HttpOnly`, `SameSite`), JWT signature verification, algorithm enforcement (prevent `alg: none`), and expiration checks.
  - Review cryptographic implementations: flag deprecated ciphers/hashes (`MD5`, `SHA1`, `DES`), ECB mode, static initialization vectors (IV), and pseudo-random generators used for security tokens.
- **Configuration, Infrastructure & Supply Chain**:
  - Audit web server/framework settings: debug mode enabled in production, permissive CORS (`Access-Control-Allow-Origin: *` with credentials), missing security headers (`CSP`, `HSTS`, `X-Frame-Options`).
  - Review container/CI manifests: containers running as `root`, missing health checks, secrets passed in plaintext `ENV` or CI action arguments.
  - Inspect dependency manifests (`package.json`, `requirements.txt`, `pom.xml`, `go.mod`): flag known vulnerable package versions and unpinned dependencies.

### Phase 3: Synthesize & Severity-Ranked Reporting
**Objective**: Aggregate verified findings into a structured markdown report and present a high-level summary.

- Assign defensible severity levels:
  - **Critical**: Direct remote code execution (RCE), unauthenticated administrative bypass, active production secret exposure.
  - **High**: Exploitable injection flaws, broken authorization on sensitive user data, weak JWT verification.
  - **Medium**: CSRF on state-changing operations, sensitive info leak via error messages, unpinned high-risk dependencies.
  - **Low / Info**: Missing hardening headers, verbose non-prod logging, deprecated API usage.
- Create output directory `docs/security-scan/` if not present and write the report to `docs/security-scan/security-scan_<yyyymmdd>_<hhmmss>.md` (use real system timestamp).
- Deliver concise conversational summary in Vietnamese displaying finding counts by severity, top critical risks, and clickable file link to the report.

## Output Format

### Report File: `docs/security-scan/security-scan_<yyyymmdd>_<hhmmss>.md`
````markdown
# Security Audit Report: <project-name>

**Scan Date**: <YYYY-MM-DD HH:MM:SS>
**Scope**: `<scanned-path>`
**Total Findings**: <N> (Critical: <C>, High: <H>, Medium: <M>, Low: <L>, Info: <I>)

## Executive Summary
Brief high-level overview of the security posture and principal risks.

## Severity Distribution Table
| Severity | Count | Primary Categories |
|---|---|---|
| Critical | ... | Secrets, RCE |
| High | ... | Injection, Broken Auth |
| Medium | ... | CSRF, Outdated Deps |
| Low / Info | ... | Missing Headers |

## Detailed Findings
### [SEC-<ID>] <Title>
- **Severity**: Critical | High | Medium | Low | Info
- **Category**: OWASP Top 10 / CWE Reference
- **Location**: `path/to/file.ext:L<line>`
- **Vulnerable Code Snippet**:
  ```lang
  // code snippet
  ```
- **Impact Analysis**: Concrete description of exploitability and business risk.
- **Remediation**: Actionable, copy-pastable fix or configuration change.

## Remediation Roadmap
Prioritized action plan grouped by urgency (Immediate / Next Sprint / Backlog).
````

## Don'ts
- Do not modify, edit, patch, or delete any project files; maintain strict read-only execution.
- Do not run live payloads, active exploits, fuzzing, or network penetration tests against running services.
- Do not upload code, configs, or discovered secrets to external third-party services or cloud scanners.
- Do not print or expose raw unmasked secrets in reports or chat; always mask credentials (e.g. `AKIA****WXYZ`).
- Do not fabricate or hallucinate CVE identifiers without verified package/version matches.
- Do not assign Critical or High severity without a clear, defensible exploit path.

## Quality Checklist
- [ ] Scan remained strictly read-only with zero modifications to source files?
- [ ] Every finding contains an exact file path, line number, and verified code snippet?
- [ ] All reported secrets are masked (first 4 and last 4 characters only)?
- [ ] Severity levels are defensible and mapped to OWASP / CWE standards?
- [ ] Each finding provides concrete, actionable remediation guidance tailored to the project stack?
- [ ] Report file saved to `docs/security-scan/security-scan_<yyyymmdd>_<hhmmss>.md`?
- [ ] Conversation summary delivered in Vietnamese with severity metrics and report link?
