# Phase 2 — Secrets & Sensitive Data Exposure

## Objective

Find hardcoded credentials, API keys, tokens, private keys, and PII in tracked files. Optionally, with explicit user approval, scan git history. Categorize each match as a **confirmed secret**, **likely placeholder**, or **test fixture**, and define a remediation per category.

A leaked production secret in a tracked file is automatically **Critical** severity.

---

## Step 2.1 — Define the Search Surface

In scope:
- All files in `[SOURCE]` and `[CONFIG]` buckets from Phase 1
- Dotfiles at the project root (`.env`, `.env.*`, `.npmrc`, `.netrc`, `.aws/credentials` if checked in)
- README, docs, and example files (frequently contain real keys "for the demo")
- Build artifacts only if checked into VCS (e.g., compiled Android `*.apk`, JS `*.bundle.js`)

Out of scope (unless user approves):
- `.git/` history (requires `git log -p` or `gitleaks`)
- Vendor / `node_modules/` / `venv/` (third-party code, not your secrets)
- Encrypted blobs (sealed-secrets, sops, age, vault-wrapped)

---

## Step 2.2 — Pattern Inventory

Run patterns in this order — high-precision provider tokens first, generic credential patterns last. Use the `Grep` tool (`rg`) with file-type filters when possible to keep noise low.

### High-precision provider tokens

| Pattern | Provider | Severity if real |
|---|---|---|
| `AKIA[0-9A-Z]{16}` | AWS Access Key ID | Critical |
| `aws_secret_access_key\s*=\s*["']?[A-Za-z0-9/+=]{40}["']?` | AWS Secret Key | Critical |
| `ASIA[0-9A-Z]{16}` | AWS STS temporary key | High |
| `AIza[0-9A-Za-z_\-]{35}` | Google API key | High–Critical depending on scope |
| `ya29\.[0-9A-Za-z_\-]+` | Google OAuth access token | High |
| `ghp_[0-9A-Za-z]{36}` | GitHub personal access token | Critical |
| `gho_[0-9A-Za-z]{36}` | GitHub OAuth token | Critical |
| `ghs_[0-9A-Za-z]{36}` | GitHub server-to-server token | Critical |
| `github_pat_[0-9A-Za-z_]{82}` | GitHub fine-grained PAT | Critical |
| `glpat-[0-9A-Za-z_\-]{20}` | GitLab PAT | Critical |
| `xox[baprs]-[0-9A-Za-z\-]{10,}` | Slack token | High |
| `https://hooks\.slack\.com/services/T[A-Z0-9/]+` | Slack webhook | Medium–High |
| `sk_live_[0-9A-Za-z]{24,}` | Stripe live secret key | Critical |
| `sk_test_[0-9A-Za-z]{24,}` | Stripe test secret key | Medium |
| `rk_live_[0-9A-Za-z]{24,}` | Stripe restricted key | High |
| `SG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}` | SendGrid API key | High |
| `key-[0-9a-zA-Z]{32}` | Mailgun key | High |
| `npm_[0-9A-Za-z]{36}` | NPM token | High–Critical |
| `dop_v1_[a-f0-9]{64}` | DigitalOcean PAT | Critical |
| `do[a-z]{1}_v1_[a-f0-9]{64}` | DigitalOcean token (variants) | Critical |
| `EAACEdEose0cBA[0-9A-Za-z]+` | Facebook access token | High |
| `sk-[A-Za-z0-9]{20,}` | OpenAI / Anthropic-style API key | High–Critical |
| `nvapi-[A-Za-z0-9_\-]{20,}` | NVIDIA API key | High |
| `hf_[A-Za-z0-9]{30,}` | Hugging Face token | High |
| `gho?_[0-9A-Za-z]{36,}` (broad) | GitHub family | Critical |
| `-----BEGIN (RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----` | Private key blocks | Critical |
| `-----BEGIN ENCRYPTED PRIVATE KEY-----` | Encrypted private key | High |
| `-----BEGIN CERTIFICATE-----` (in source/config, not in `certs/`) | Cert leakage | Low–Medium |

### Generic credential patterns

These produce noise. Always inspect the surrounding line before reporting.

```
(?i)(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|auth[_-]?token|bearer)\s*[=:]\s*["'][^"'\s]{6,}["']
(?i)(database|db)[_-]?(url|uri|connection)\s*[=:]\s*["'][^"']+://[^"']*:[^@]+@[^"']+["']
(?i)(client[_-]?secret|consumer[_-]?secret)\s*[=:]\s*["'][^"'\s]{8,}["']
```

### Connection strings with embedded credentials

```
postgres://[^:/\s]+:[^@\s]+@
mysql://[^:/\s]+:[^@\s]+@
mongodb(\+srv)?://[^:/\s]+:[^@\s]+@
redis://[^:/\s]+:[^@\s]+@
amqp://[^:/\s]+:[^@\s]+@
```

### PII patterns (lower priority, document only when they appear in code/config rather than test data)

- Email addresses concatenated with passwords (`user@example.com:password`)
- Phone numbers + names hardcoded in seed scripts (sample/demo only is fine)
- Credit-card-like sequences (`\b(?:\d[ -]*?){13,19}\b`) — flag and request review

---

## Step 2.3 — Triage Each Match

For every hit, classify it before reporting:

| Class | Indicators | Action |
|---|---|---|
| **Confirmed secret** | Tracked file, value matches a strict provider pattern, no nearby `example`/`fake`/`test`/`changeme` markers, file not in a tests directory | Report as Critical; remediation: rotate + remove from history |
| **Likely placeholder** | Strings like `your-key-here`, `<API_KEY>`, `xxx`, `changeme`, `REPLACE_ME`, default `admin/admin`, all-caps env-name patterns | Report as Info or Low if it teaches developers a bad habit; recommend env-loader |
| **Test fixture** | Inside `tests/`, `__tests__/`, `*_test.go`, `spec/` and value is clearly a test double | No finding unless the same string also appears in production paths |
| **Encrypted blob** | `sops:` header, age headers, vault prefixes, sealed-secret CRDs | No finding; note that the project uses a secret-management tool |

When in doubt, ask the user before assigning Critical.

---

## Step 2.4 — `.env` and Environment Files

Inspect every `.env`, `.env.*`, `*.envrc`, and similar files:

- Tracked in git? Run `git ls-files -- .env .env.*` (or use the search tool). If yes, **Critical**.
- Are they listed in `.gitignore`? If yes but a copy was committed earlier, recommend a history scan.
- Are values templated (`${VAR}` or `your_key_here`)? If yes, classify as placeholder.
- Are there parallel `.env.example` files? Good practice; verify the example file does not also contain real values.

For framework-specific config files (`application.properties`, `application.yml`, `appsettings.json`, `web.config`), grep for password/secret keys and follow the same triage.

---

## Step 2.5 — Build Artifacts and Bundles

If the repo has built artifacts checked in (rarely a good idea):

- `*.bundle.js`, `*.min.js`, `dist/*.js` — search for embedded API keys
- Android `*.apk` — out of scope here (covered by `android-app-variant` skill); flag if present
- iOS `*.ipa`, `*.app` — flag if present
- `*.jar`, `*.war`, `*.ear` — list manifests; do not extract unless approved

A bundled secret is just as exploitable as a source secret.

---

## Step 2.6 — Git History Scan (Approval Required)

This step is **opt-in**. Ask:

```
Bạn có cho phép tôi quét git history không? Tôi sẽ chạy ở chế độ chỉ đọc:
- gitleaks detect --no-git --redact (nếu gitleaks có sẵn)
- hoặc git log -p (chỉ đọc, không sửa)
Quét lịch sử có thể tốn vài phút trên repo lớn.
```

If approved:

```bash
# Preferred: gitleaks (offline, no upload)
gitleaks detect --source <project-root> --redact --report-path /tmp/gitleaks-report.json --report-format json

# Fallback: pure git
git -C <project-root> log -p --all -S "<token-prefix>"   # search for additions of a specific pattern
git -C <project-root> log --all --diff-filter=A -- '.env'  # commits that added .env
```

If a secret is found in history but **not** in HEAD, it is still considered Critical (the commit is reachable on any clone, including any fork). Remediation: rotate the secret immediately; rewriting history is an organizational decision.

---

## Step 2.7 — Suppress Known Test Doubles

Common test-double values that are safe and should not be reported:

- AWS test keys: `AKIAIOSFODNN7EXAMPLE`, `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` (these are in AWS docs)
- JWT example header `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0In0.<sig>` with `secret`/`secretkey`/`your-256-bit-secret`
- Stripe test keys (`sk_test_`) when found inside test files
- `password = "password"`, `password = "test"`, `password = "12345"` inside test fixtures

Add a brief note in the report's Appendix listing suppressions, so reviewers can see what was deliberately filtered.

---

## Step 2.8 — Reporting Each Finding

Mask the secret in the report. Show only the first 4 and last 4 chars; replace the middle with asterisks. Examples:

```
- AKIA****WXYZ        (AWS Access Key ID)
- ghp_****abcd        (GitHub PAT)
- -----BEGIN PRIVATE KEY----- (key body redacted)
```

Each finding should look like:

```
### [Critical] Hardcoded AWS Access Key in src/config/aws.ts:14
**Category**: Secret Exposure (CWE-798: Use of Hard-coded Credentials)
**Evidence**:
  src/config/aws.ts:14
  const ACCESS_KEY_ID = "AKIA****WXYZ";
**Impact**: A user with read access to the repo can authenticate to AWS as <role>; depending on the role's IAM policy, this may grant full account access.
**Remediation**:
  1. Rotate the key immediately in AWS IAM Console.
  2. Remove the literal from source; load from environment via process.env.AWS_ACCESS_KEY_ID.
  3. Confirm .env is in .gitignore and not in git history (run gitleaks if not yet done).
  4. Consider OIDC federation for CI/CD instead of long-lived keys.
```

---

## Deliverables

- List of confirmed-secret findings (each Critical/High with masked value)
- List of placeholder/test findings noted for awareness
- Git history result (if approved)
- Suppression list documented
- All findings ready to be merged into the final report

---

## Required Practices

- Always mask secret values in the report.
- Always classify each match before promoting to Critical.
- Always recommend rotation in the remediation, not just removal.
- Always check both HEAD and (with approval) history.

## Prohibited Practices

- Do not paste full secret values into the report or chat output.
- Do not run secret scanners that upload data to a third-party service.
- Do not auto-rotate or auto-revoke any key — that is a user-side action.
- Do not delete `.env` files or rewrite history; report and let the user decide.
