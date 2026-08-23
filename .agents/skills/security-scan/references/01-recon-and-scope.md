# Phase 1 — Recon & Scope

## Objective

Build a complete picture of the project before scanning. Skipping recon leads to false negatives (you scanned for the wrong patterns) and wasted effort (you scanned files that do not exist or are out of scope).

By the end of this phase, you must know:

- What languages and frameworks are in use
- What package managers and lockfiles are present
- Where source code lives, where tests live, where vendored code lives
- What configuration files, secrets-bearing files, and IaC files exist
- What CI/CD pipelines exist
- Which paths are in scope and which are excluded

---

## Step 1.1 — Confirm Scope With the User

**Before reading anything**, restate the scope back to the user and ask for confirmation:

```
Tôi sẽ thực hiện security scan ở chế độ READ-ONLY trên project root: <path>
- Loại trừ mặc định: node_modules/, vendor/, dist/, build/, .git/, *.min.js, *.lock (chỉ đọc, không phân tích cú pháp)
- Có phần nào cần loại trừ thêm không? (ví dụ: thư mục test, sample data, third-party fork)
- Có cho phép tôi đọc git history để dò secret không?
- Có cho phép tôi chạy SCA tool cục bộ (npm audit, pip-audit, ...) khi gặp manifest tương ứng không?
```

Wait for the user's reply. Do not proceed until scope is confirmed.

---

## Step 1.2 — Inventory: Top-Level Layout

Use a single non-recursive listing to understand the project's shape:

```bash
ls -la <project-root>
```

Look for:

- `package.json`, `pnpm-lock.yaml`, `yarn.lock` → JS/TS Node project
- `requirements.txt`, `pyproject.toml`, `Pipfile`, `poetry.lock` → Python project
- `pom.xml`, `build.gradle(.kts)` → Java/Kotlin project
- `go.mod`, `go.sum` → Go project
- `Cargo.toml`, `Cargo.lock` → Rust project
- `Gemfile`, `Gemfile.lock` → Ruby project
- `composer.json`, `composer.lock` → PHP project
- `*.csproj`, `*.sln`, `packages.lock.json` → .NET project
- `Dockerfile`, `docker-compose.yml`, `compose.yaml` → containerized
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`, `azure-pipelines.yml` → CI
- `terraform/`, `*.tf`, `cloudformation/`, `k8s/`, `helm/`, `charts/` → IaC
- `.env`, `.env.*`, `secrets.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks` → secret-bearing
- `nginx.conf`, `httpd.conf`, `web.config`, `application.yml`, `application.properties` → server / framework config

Record what you found. The combination drives subsequent phases.

---

## Step 1.3 — Identify Languages With File Counts

Count source files by extension to confirm primary languages:

```bash
# Use Glob to find files; do not run rg/grep for counting if a faster tool exists.
# Example patterns:
#   **/*.py
#   **/*.{ts,tsx,js,jsx}
#   **/*.{java,kt}
#   **/*.go
#   **/*.{rs}
#   **/*.{rb}
#   **/*.php
#   **/*.{cs,vb}
```

A project may be polyglot. Note the distribution and prioritize the language(s) with the most code in writeable scope (skip vendored/third-party trees).

---

## Step 1.4 — Map Source vs. Non-Source Trees

Identify and tag each top-level directory:

| Tag | Examples | Action |
|---|---|---|
| **Source** | `src/`, `app/`, `api/`, `lib/`, `pkg/`, `cmd/`, `internal/`, `web/` | In scope for SAST patterns |
| **Tests** | `test/`, `tests/`, `__tests__/`, `*_test.go`, `spec/` | Lower priority; may contain test fixtures with fake creds |
| **Generated** | `dist/`, `build/`, `out/`, `target/`, `*.min.js` | Out of scope (read-only sanity check only) |
| **Vendor** | `node_modules/`, `vendor/`, `venv/`, `.venv/`, `Pods/`, `external/` | Out of scope (covered by SCA, not SAST) |
| **Config** | `config/`, `conf/`, `etc/`, root-level `*.yml`/`*.yaml`/`*.toml` | In scope for misconfig review |
| **IaC** | `terraform/`, `cdk/`, `k8s/`, `helm/`, `ansible/` | In scope for Phase 5 |
| **CI** | `.github/`, `.gitlab/`, `.circleci/`, `Jenkinsfile` | In scope for Phase 5 |
| **Docs** | `docs/`, `README.md` | Skim only — sometimes contains leaked example creds |

---

## Step 1.5 — Identify Existing Security Tooling

Before suggesting tools, check what the project already configures:

| File | Purpose |
|---|---|
| `.semgrep.yml`, `.semgrepignore` | Existing Semgrep rules |
| `.bandit`, `bandit.yml`, `pyproject.toml [tool.bandit]` | Bandit config |
| `.eslintrc*`, `eslint.config.*` | ESLint (may include `eslint-plugin-security`) |
| `.gitleaks.toml`, `.gitleaksignore` | Existing gitleaks config |
| `.dependabot/`, `.github/dependabot.yml` | Dependabot |
| `renovate.json` | Renovate |
| `.pre-commit-config.yaml` | pre-commit hooks (may include security linters) |
| `.github/workflows/*security*`, `*codeql*` | Existing security workflows |
| `SECURITY.md` | Project's own security policy |

If `SECURITY.md` exists, read it. It often contains the project's threat model and disclosure process.

---

## Step 1.6 — Detect Application Type & Trust Boundaries

Classify the project to focus the audit:

- **Web frontend (SPA)**: focus on XSS, CSP, secret-in-bundle, SSRF via dev proxy, auth flow
- **Web backend / API**: focus on injection, auth/authz, IDOR, rate limiting, CSRF, SSRF
- **Mobile app**: focus on secrets in bundle, insecure storage, weak TLS pinning, exported components
- **CLI tool / library**: focus on argument injection, dependency CVEs, path traversal in file ops
- **Microservice / serverless**: focus on IAM permissions, env var handling, untrusted event sources
- **ML / data pipeline**: focus on deserialization (`pickle`, `joblib`), notebook secrets, dataset access keys

A project may belong to several categories — list all relevant ones.

---

## Step 1.7 — Identify Entry Points

For backends and APIs, list HTTP routes / GraphQL schemas / RPC handlers. These are the trust boundary where user input enters the system. Use framework-aware patterns:

| Framework | Pattern to grep |
|---|---|
| Express (JS) | `app.(get|post|put|delete|patch|use)\(`, `router.(get|post|...)\(` |
| Fastify | `fastify.(get|post|...)\(` |
| NestJS | `@Get\(`, `@Post\(`, `@Controller\(` |
| Django | `urlpatterns`, `path\(`, `re_path\(`, `@api_view`, viewsets |
| Flask | `@app.route\(`, `@blueprint.route\(` |
| FastAPI | `@app.(get|post|...)\(`, `APIRouter` |
| Spring | `@(Get|Post|Put|Delete|Patch|Request)Mapping`, `@RestController` |
| Gin (Go) | `r.(GET|POST|...)\(`, `router.Group\(` |
| Rails | `routes.rb`, `resources :`, `resource :` |
| Laravel | `routes/web.php`, `Route::(get|post|...)` |

Save a route inventory; you will revisit it in Phase 3 (Injection) and Phase 4 (AuthZ).

---

## Step 1.8 — Build the Working File List

Produce four buckets. Each subsequent phase reads from these buckets only.

```
[SOURCE]      — application code in writeable scope
[CONFIG]      — configuration, env, framework, server
[MANIFEST]    — package.json, requirements.txt, lockfiles, Dockerfile
[CI]          — pipeline files
[IAC]         — terraform, k8s, helm, ansible
```

Do not include vendored or generated code in `[SOURCE]`. Their security is handled by `[MANIFEST]` (Phase 6 — SCA).

---

## Deliverables

By the end of Phase 1, you must have:

- A confirmed scope (paths included / excluded), recorded in your working notes
- A list of detected languages and frameworks
- An application-type classification
- A route / entry-point inventory (if applicable)
- Existing security tooling noted (so you do not duplicate effort)
- The four-bucket working file list ready for Phases 2–6

Move to Phase 2 only after the user confirms scope and the inventory is complete.

---

## Required Practices

- Always confirm scope before reading source.
- Always exclude generated and vendored trees from SAST scope.
- Always read `SECURITY.md` if it exists.
- Always check existing tooling configs before recommending tools.

## Prohibited Practices

- Do not deep-read every file in this phase. Inventory only.
- Do not run any analyzer in this phase; recon is read + classify only.
- Do not assume framework from filename alone — confirm with imports or config.
