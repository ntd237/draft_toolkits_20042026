# OWASP Top 10 Security Audit Checklist

Used in Phase 1 of `07-web-review` whenever the reviewed change touches security-sensitive code (auth, payments, user data, file/input handling). Every check must yield a concrete verdict (pass / finding with file:line evidence) — "probably fine" is not a verdict. All findings in this domain are classified per the standard severity rules; actual injection/authz flaws are always BLOCKING.

## A01 — Broken Access Control
- Every new endpoint/handler has an explicit authorization decision (public / authenticated / role-scoped) enforced server-side — not merely hidden in the UI.
- Object access is scoped to the requesting user (no IDOR: `/orders/123` verifies ownership/permission on the object, not just the session).
- Admin/sensitive routes are not discoverable or guessable via predictable IDs without authz checks.
- CORS configuration matches the documented origin policy; no wildcard credentials combinations.

## A02 — Cryptographic Failures
- Passwords hashed with a modern adaptive hash (bcrypt/argon2/scrypt) — never md5/sha1/plain/reversible encoding.
- Sensitive data encrypted in transit (TLS assumed) and at rest where the data classification requires it; no secrets in logs, error messages, or client-exposed payloads.
- No homegrown crypto; tokens are high-entropy and have expiry.

## A03 — Injection
- All SQL built via parameterized queries/ORM — no string interpolation of user input (also check for second-order injection via stored values).
- No `eval`/`exec`/raw command construction from user input (shell injection).
- Frontend: no rendering of user input as raw HTML (`dangerouslySetInnerHTML`, `v-html`, `innerHTML` without sanitization) — stored/reflected XSS.
- LDAP/OS/path traversal: user input never concatenated into file paths or directory operations without normalization + allowlisting.

## A04 — Insecure Design
- Critical flows have server-side validation of business rules (price, quantity, discount computed server-side; client-sent totals never trusted).
- Rate limiting / abuse controls exist on auth, OTP, and payment endpoints (or a documented plan-level decision defers it).

## A05 — Security Misconfiguration
- No debug/dev modes, verbose stack traces, or default credentials enabled in production config paths touched by the change.
- Error responses expose no internals (stack traces, SQL, file paths) to clients.
- Security headers set where the project manages them (CSP, X-Content-Type-Options, HSTS) — flag absence as ADVISORY unless the change makes it worse.

## A06 — Vulnerable Components
- New dependencies added by the change: pinned versions, from trusted sources, no known-advisory versions if a lockfile audit (`npm audit`/`pip-audit`/equivalent) is available to run — run it and report output when dependencies changed.

## A07 — Identification & Authentication Failures
- Session/login logic: credentials checked server-side with constant-time comparison where applicable; session invalidation on logout/password change; no session token in URLs.
- Login endpoints respond generically on failure (no user-enumeration oracle) and throttle repeated attempts.
- JWT/API tokens: algorithm and audience validated; secrets not embedded client-side.

## A08 — Software & Data Integrity Failures
- Deserialized/untrusted data (webhooks, CI inputs, serialized blobs) verified via signature/allowlist before processing.
- CI/deploy steps touched by the change do not execute untrusted code from external sources without pinning.

## A09 — Logging & Monitoring Failures
- Auth failures, authorization denials, and payment anomalies are logged with enough context to investigate (user id, ip, action) — without logging secrets or full card/PII values.
- Logged events reach the project's monitoring/error-tracking pipeline.

## A10 — Server-Side Request Forgery (SSRF)
- Any feature fetching URLs from user input (webhooks, importers, previews) validates against an allowlist of schemes/hosts and blocks internal/private address ranges.

## Verdict Handling
- Any confirmed instance of A01–A03, A07 (broken auth), or SSRF reaching internal targets → **BLOCKING** → FAIL.
- Missing hardening without a live exploit path (headers, rate limiting where no abuse surface changed, advisory-level items) → **ADVISORY** → may PASS, listed for future maintenance.
