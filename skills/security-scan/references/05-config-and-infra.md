# Phase 5 — Configuration, Infrastructure & CI/CD

## Objective

Most exploited breaches start at a misconfiguration, not a clever code bug. This phase audits framework configs, server configs, container manifests, IaC files, and CI/CD pipelines for hardening gaps.

---

## Section A — Framework Configuration

### A.1 — Debug Mode in Production

| Stack | Indicator |
|---|---|
| Django | `DEBUG = True` in `settings.py` (or `settings/prod.py`) |
| Flask | `app.run(debug=True)`, `FLASK_ENV=development` |
| Rails | `config.consider_all_requests_local = true` in `production.rb` |
| Laravel | `APP_DEBUG=true` in `.env` (prod) |
| Spring | `spring.boot.admin.enable=true`, `management.endpoints.web.exposure.include=*` exposing `/env`, `/heapdump` |
| Express | `app.set('env', 'development')`, verbose error middleware in prod |
| ASP.NET Core | `app.UseDeveloperExceptionPage()` outside `IsDevelopment()` |

If a config file is named `production.*` or `prod.*` and has debug enabled → **High** to **Critical** depending on what is exposed (e.g., Spring `/env` leaks env vars).

### A.2 — Permissive CORS

```
Access-Control-Allow-Origin: *
cors({ origin: true })           // reflects any origin
cors({ origin: req.headers.origin })   // identical effect
CORS_ALLOWED_ORIGINS = ['*']
```

- `*` with `Access-Control-Allow-Credentials: true` is invalid in browsers but a clear policy mistake → **High**.
- `*` without credentials on an API that returns sensitive data → **Medium** to **High**.
- Reflecting any origin without an allowlist → **High**.

### A.3 — Missing Security Headers

For browser-facing apps, check for:

- `Content-Security-Policy` (any policy is better than none)
- `Strict-Transport-Security` (HSTS, with `max-age` ≥ 6 months for production)
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy` (e.g., `strict-origin-when-cross-origin`)
- `Permissions-Policy` (where applicable)
- Removal of `Server`, `X-Powered-By` (info disclosure)

Missing each is **Low** individually, but a wholly unset bundle is **Medium** for any app handling sensitive data.

### A.4 — Verbose Error Pages / Stack Traces

- Stack traces returned in HTTP response body in prod → **Medium** to **High** depending on what they leak.
- Error responses that include SQL queries or file paths → **Medium**.

### A.5 — Open Admin Panels

- `phpMyAdmin`, `Adminer`, `RailsAdmin`, `Django admin` exposed without auth wall or IP allowlist.
- Spring `actuator` endpoints (`/actuator/env`, `/actuator/heapdump`) exposed publicly.
- Next.js / Nuxt dev server hot-reload endpoints in production builds.

---

## Section B — Web Server / Reverse Proxy

### B.1 — Nginx

Look for:

```
ssl_protocols TLSv1 TLSv1.1;          # weak
ssl_ciphers HIGH:!aNULL:!MD5;         # OK but inspect
add_header X-Frame-Options ...        # check exists
server_tokens on;                     # info disclosure
location ~ /\.git { ... allow ...; }  # exposes .git
client_max_body_size 0;               # unlimited upload
proxy_pass http://internal;           # behind TLS-only setup?
```

### B.2 — Apache `httpd.conf` / `.htaccess`

- `ServerSignature On`, `ServerTokens Full` → info disclosure.
- `Options +Indexes` → directory listing.
- `Options +ExecCGI` in user-writable dirs → RCE risk.

### B.3 — IIS `web.config`

- `<httpErrors errorMode="Detailed" />` in prod → info disclosure.
- `<directoryBrowse enabled="true" />` → directory listing.

---

## Section C — Container Hardening

### C.1 — Dockerfile Review

Findings to flag with severity:

| Pattern | Severity | Finding |
|---|---|---|
| `FROM image:latest` | Low | Unpinned base image; non-reproducible builds |
| `FROM image` (no tag) | Medium | Same as above, with implicit `latest` |
| `USER root` (or no `USER` directive at all, default is root) | Medium | Container runs as root |
| `RUN curl ... | sh` | Medium | Unverified install; supply-chain risk |
| `ADD http://...` | Low | Use `RUN curl + checksum verify` instead |
| `COPY .ssh /root/.ssh` | Critical | Secrets baked into image |
| `ENV SECRET=...`, `ENV PASSWORD=...` | High | Secrets in image layers |
| Missing `HEALTHCHECK` | Info | Operational, not security |
| `apt-get install` without `--no-install-recommends` and no `apt-get clean` | Low | Image bloat, larger attack surface |
| `RUN chmod 777` | Low | Loose permissions |

Multi-stage builds that copy a small binary into a `distroless`/`scratch`/`alpine` final image are good signals of a hardened workflow.

### C.2 — docker-compose / compose.yaml

- `privileged: true` → **High**.
- `network_mode: host` → **Medium** (depends on workload).
- `volumes: - /:/host` (or similar root mounts) → **Critical**.
- Plain-text passwords in `environment:` → **High**; use secrets/`*_FILE` references.
- `cap_add: [SYS_ADMIN, ALL]` → **High**.

### C.3 — Kubernetes Manifests

| Pattern | Severity |
|---|---|
| `runAsUser: 0` or no `securityContext.runAsNonRoot: true` | Medium |
| `privileged: true` | High |
| `allowPrivilegeEscalation: true` (or missing — defaults to true) | Medium |
| `hostNetwork: true`, `hostPID: true`, `hostIPC: true` | High |
| `hostPath:` mounting sensitive paths (`/`, `/var/run/docker.sock`) | Critical |
| `serviceAccountName: default` and the default has bindings | Medium |
| `imagePullPolicy: Always` with `:latest` tag | Low |
| Secrets in plain ConfigMap rather than Secret | Medium |
| Missing `resources.limits` (CPU/memory) | Low (DoS / noisy-neighbor) |
| Missing NetworkPolicy for sensitive namespaces | Medium |
| `automountServiceAccountToken: true` (default) on workloads that don't call the API | Low–Medium |

### C.4 — Helm Charts

- `values.yaml` with embedded credentials → flag like `.env`.
- Templates that produce overly broad RBAC (`ClusterRoleBinding` for `cluster-admin`) → **High**.

---

## Section D — Infrastructure as Code (Terraform / CloudFormation / Pulumi)

### D.1 — Cloud Provider Patterns (mostly AWS-flavored, similar in GCP/Azure)

| Resource | Misconfig | Severity |
|---|---|---|
| `aws_security_group` | Ingress `0.0.0.0/0` to port 22 / 3389 / 3306 / 5432 / 6379 | High–Critical |
| `aws_s3_bucket` | `acl = "public-read"`, missing `block_public_acls = true` | High |
| `aws_s3_bucket_public_access_block` | All four flags must be `true` | n/a (the safe pattern) |
| `aws_s3_bucket_server_side_encryption_configuration` | Missing | Medium |
| `aws_iam_policy_document` | `Action = "*"`, `Resource = "*"` together | High |
| `aws_db_instance` | `publicly_accessible = true`, `storage_encrypted = false` | High |
| `aws_kms_key` | `enable_key_rotation = false` | Low |
| `aws_lb_listener` | Protocol `HTTP` (not HTTPS) on prod | Medium |
| `aws_cloudtrail` | Missing or `enable_log_file_validation = false` | Medium |

For GCP: `iam_policy` with `roles/owner` to a broad principal, public Cloud Storage buckets (`allUsers`, `allAuthenticatedUsers`).

For Azure: `azurerm_storage_account` with `public_network_access_enabled = true`, NSGs allowing `*` source on management ports.

### D.2 — Terraform State

- `terraform.tfstate` checked into VCS → **Critical** (state often contains plaintext secrets).
- Backend not configured with encryption / state-locking.

### D.3 — Recommended Tools

If approved, run:
- `tfsec <dir>` — Terraform-focused
- `checkov -d <dir>` — multi-IaC
- `kube-linter lint <dir>` — Kubernetes
- `kubesec scan <pod.yaml>` — per-manifest scoring

---

## Section E — CI/CD Pipelines

### E.1 — GitHub Actions

| Pattern | Severity |
|---|---|
| `pull_request_target` on a workflow that runs untrusted PR code (`actions/checkout@v3` of `${{ github.event.pull_request.head.sha }}` followed by build/test) | Critical (token-leak / RCE on runner) |
| Third-party action used by tag (`actions/checkout@v4`) instead of SHA | Low–Medium for trusted actions, **High** for unknown maintainers |
| `secrets:` passed to workflow runs triggered by forks | High |
| Permissions left at default for `GITHUB_TOKEN` (often `write-all`) | Medium |
| Inline `bash -c "${{ inputs.x }}"` or echo of untrusted env into a script | Critical (script injection via context expressions) |
| Self-hosted runner + public repo + no isolation | High |
| Caches keyed by branch name only (cache poisoning across forks) | Medium |
| `actions/upload-artifact` of build outputs containing secrets | High |

Required GitHub Actions hardening:

```
permissions:
  contents: read
# scope-up only what's needed per job
```

### E.2 — GitLab CI

- `image: <untrusted>` without digest pinning → Medium.
- `before_script` with `eval $(cat .env)` exposing secrets → High.
- Predefined CI/CD variables marked "Protected" but referenced in unprotected branches.

### E.3 — Jenkins

- `Jenkinsfile` with credential printed to console (`sh "echo $PASSWORD"`).
- Script Security plugin disabled / `groovy.lang.GroovyShell` use of untrusted strings.

### E.4 — Common Across CI

- Secrets stored as plain env vars in pipeline definition → **High**.
- Workflow that publishes artifacts to PyPI/npm/Maven with long-lived tokens (instead of OIDC) → **Medium** to **High**.
- Build matrix that sources untrusted forks without restricting secret access.

---

## Section F — Logging & Monitoring

### F.1 — Logging Hygiene

- Logs that include passwords, tokens, full request bodies of auth endpoints → **High** (depending on retention).
- Logs at DEBUG level in production → **Low** (info disclosure if logs aren't tightly controlled).

### F.2 — Monitoring Gaps

- No security-relevant logging on auth events, privilege changes, admin actions → **Medium** (defense-in-depth).
- Alerts not configured for repeated failures → **Info**.

---

## Section G — Storage / Data

### G.1 — At-Rest Encryption

- DBs without `storage_encrypted = true` (cloud) or filesystem-level encryption (on-prem) for sensitive data → **Medium**.
- Backups stored unencrypted in S3/GCS/Azure Blob → **Medium**.

### G.2 — Backup Exposure

- Backup endpoints (`/backup`, `/db.sql.gz`) reachable from the public internet → **Critical** if found.

---

## Reporting Pattern

```
### [High] Container Runs as Root in Dockerfile:1
**Category**: Security Misconfiguration (OWASP A05:2021)
**Evidence**:
  Dockerfile (no USER directive)
  FROM python:3.11
  COPY . /app
  CMD ["python", "/app/main.py"]
**Impact**: A vulnerability inside the application that yields shell access immediately yields root inside the container, increasing the blast radius of any container escape.
**Remediation**:
  1. Add a non-root user near the end of the Dockerfile:
     RUN useradd -r -u 1000 appuser && chown -R appuser /app
     USER appuser
  2. In Kubernetes, set securityContext.runAsNonRoot: true and runAsUser: 1000.
  3. Ensure the application does not require root privileges (no binding to ports < 1024 inside the container).
```

---

## Required Practices

- Always note whether the project is web-facing, internal, or air-gapped — config severity depends on exposure.
- Always check for an existing `SECURITY.md` or hardening checklist in the project.
- Always recommend pinning third-party CI actions by SHA when severity warrants it.

## Prohibited Practices

- Do not actively probe deployed infrastructure (cloud APIs, port scans).
- Do not enumerate cloud account resources (`aws s3 ls`, `gcloud projects list`).
- Do not write infra-modifying commands; only read and audit.
