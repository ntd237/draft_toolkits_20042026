# Phase 6 (Part 2) — Tooling by Language & Stack

## Objective

Provide concrete, copy-pastable, **local, non-destructive, no-upload** commands for SAST and SCA tools, organized by ecosystem. Each command requires **explicit user approval per invocation** before running. Always check whether the tool is already installed before recommending installation.

---

## Pre-Flight: Tool Discovery

Before suggesting any command, check the environment:

```bash
# Verify presence of common tools (replace with rg/Glob/which equivalents)
which rg gitleaks trufflehog semgrep osv-scanner trivy bandit pip-audit safety npm yarn pnpm govulncheck gosec brakeman bundler-audit hadolint tfsec checkov kube-linter
# (use your platform's equivalent — `where` on Windows cmd, `Get-Command` on PowerShell)
```

Report which tools are available and which are not. Recommend only the available ones; for the missing ones, mention them as "available-but-not-installed" with a brief install hint.

---

## Section A — Cross-Language

### A.1 — Semgrep (multi-language SAST)

```bash
# Auto-config rule packs (uses bundled rules; no upload)
semgrep --config auto --error --metrics=off <project-root>

# Stricter, OWASP-aligned subsets:
semgrep --config p/owasp-top-ten --metrics=off <project-root>
semgrep --config p/security-audit --metrics=off <project-root>

# JSON output for inclusion in the report appendix:
semgrep --config p/security-audit --json --metrics=off <project-root> > /tmp/semgrep.json
```

`--metrics=off` disables anonymous telemetry. Use it.

### A.2 — gitleaks (secret detection in tree and history)

```bash
# Working tree only
gitleaks detect --source <project-root> --no-git --redact

# Including git history (with user approval)
gitleaks detect --source <project-root> --redact --report-format json --report-path /tmp/gitleaks.json
```

`--redact` ensures secret values are not printed — safe for chat output and logs.

### A.3 — trufflehog (verified secret detection)

```bash
# Filesystem scan (no verification = offline)
trufflehog filesystem <project-root> --no-verification

# Git history (no remote calls)
trufflehog git file://<project-root> --no-verification
```

Avoid `--only-verified` if it would trigger network calls to vendor APIs unless the user accepts that.

### A.4 — osv-scanner (multi-ecosystem SCA, by Google)

```bash
# Scan a directory (auto-detects manifests)
osv-scanner --recursive <project-root>

# Scan only manifests (faster)
osv-scanner --lockfile=<project-root>/package-lock.json
osv-scanner --lockfile=<project-root>/poetry.lock

# JSON output
osv-scanner --recursive --format=json <project-root> > /tmp/osv.json
```

`osv-scanner` queries the OSV.dev API by default. If air-gapped use is required, use `--offline-vulnerabilities` with a pre-downloaded DB.

### A.5 — Trivy (container + filesystem)

```bash
# Filesystem scan (deps + secrets + misconfig)
trivy fs --scanners vuln,secret,misconfig --no-progress <project-root>

# Specific image (works on local image only after `docker pull`)
trivy image --scanners vuln,secret --no-progress <image:tag>

# Offline DB (download once with `trivy db update`):
trivy fs --skip-update --offline-scan --no-progress <project-root>
```

---

## Section B — JavaScript / TypeScript / Node.js

### B.1 — SCA

```bash
# npm — built in
npm audit                           # JSON: npm audit --json
npm audit --omit=dev                # production only
npm audit fix --dry-run             # preview fixes (don't run real fix without approval)

# pnpm
pnpm audit
pnpm audit --prod
pnpm audit --json

# yarn classic
yarn audit
yarn npm audit                      # yarn berry

# bun
bun audit
```

### B.2 — SAST

```bash
# ESLint with security plugin (only if already configured)
npx eslint --ext .js,.jsx,.ts,.tsx <src>

# Plugins to look for in eslint config:
#   eslint-plugin-security
#   eslint-plugin-no-unsanitized
#   eslint-plugin-react/recommended (no-danger rule)

# Snyk Code (requires login; offline-by-default modes are limited; prefer Semgrep instead)

# njsscan
njsscan --json -o /tmp/njsscan.json <project-root>
```

### B.3 — Bundle Inspection

For bundlers that emit JS, inspect the output for embedded secrets:

```bash
# Grep for typical key patterns inside dist/*.js
rg -n "AKIA|sk_live_|ghp_|AIza|-----BEGIN " <project-root>/dist
```

---

## Section C — Python

### C.1 — SCA

```bash
# pip-audit (uses OSV / PyPI advisories)
pip-audit -r requirements.txt
pip-audit -P                         # use pip's resolver from pyproject.toml/setup
pip-audit --format json -o /tmp/pip-audit.json

# safety
safety check -r requirements.txt --json --output /tmp/safety.json

# poetry
poetry export -f requirements.txt -o /tmp/req.txt && pip-audit -r /tmp/req.txt
```

### C.2 — SAST

```bash
# bandit
bandit -r <src> -f json -o /tmp/bandit.json
bandit -r <src> -ll                  # only Medium and High

# Semgrep Python rules
semgrep --config p/python --config p/django --config p/flask --metrics=off <src>
```

### C.3 — Notebook-specific

```bash
# nbdefense (notebook-focused secret scan, if installed)
nbdefense scan <notebook.ipynb>

# Or grep notebooks (.ipynb is JSON)
rg -n "(?i)(api[_-]?key|password|secret|token)\s*=\s*[\"'].+[\"']" <project-root> -g "*.ipynb"
```

---

## Section D — Java / Kotlin

### D.1 — SCA

```bash
# OWASP Dependency-Check (file-based; downloads NVD data on first run)
dependency-check.sh --project <name> --scan <project-root> --format JSON --out /tmp/dc

# Maven
mvn -B org.owasp:dependency-check-maven:check
mvn versions:display-dependency-updates

# Gradle
./gradlew dependencyCheckAnalyze
./gradlew dependencyUpdates
```

### D.2 — SAST

```bash
# SpotBugs + find-sec-bugs plugin (configured in build script)
./gradlew spotbugsMain

# Semgrep Java rules
semgrep --config p/java --config p/owasp-top-ten --metrics=off <src>

# PMD with security ruleset (less common, available)
pmd -d <src> -R rulesets/java/security.xml -f text
```

---

## Section E — Go

### E.1 — SCA

```bash
# govulncheck (official, uses vuln.go.dev DB)
govulncheck ./...
govulncheck -json ./... > /tmp/govuln.json

# nancy (Sonatype OSS Index — requires registration for high rate; offline mode limited)
nancy sleuth -p go.list

# osv-scanner is also good here
osv-scanner --lockfile=go.sum
```

### E.2 — SAST

```bash
# gosec
gosec -fmt=json -out=/tmp/gosec.json ./...
gosec -severity=medium ./...

# staticcheck (broader, security-adjacent)
staticcheck ./...

# Semgrep
semgrep --config p/golang --metrics=off <src>
```

---

## Section F — Ruby

### F.1 — SCA

```bash
bundle audit check --update
bundler-audit check --update --format json --output /tmp/bundler-audit.json
```

### F.2 — SAST

```bash
brakeman -A -o /tmp/brakeman.json
brakeman --confidence-level=2        # only Medium and High confidence
```

---

## Section G — PHP

### G.1 — SCA

```bash
# composer audit (built into Composer 2.4+)
composer audit
composer audit --format=json > /tmp/composer-audit.json

# Local DB-only:
local-php-security-checker --path=composer.lock
```

### G.2 — SAST

```bash
# Psalm with TaintAnalysis
vendor/bin/psalm --taint-analysis

# PHPStan with security rule packs
vendor/bin/phpstan analyse --level=max <src>

# Semgrep
semgrep --config p/php --metrics=off <src>
```

---

## Section H — .NET (C# / F#)

### H.1 — SCA

```bash
# Built-in: list vulnerable packages (dotnet 5+)
dotnet list package --vulnerable
dotnet list package --vulnerable --include-transitive --format json > /tmp/dotnet-vuln.json

# OWASP Dependency-Check works for .NET too
dependency-check.sh --project <name> --scan <project-root>
```

### H.2 — SAST

```bash
# Roslyn analyzers via SDK
dotnet build /warnaserror

# Security Code Scan (NuGet pkg added to project)
dotnet build  # warnings appear if SCS is referenced

# Semgrep
semgrep --config p/csharp --metrics=off <src>
```

---

## Section I — Rust

### I.1 — SCA

```bash
# cargo-audit (RustSec advisory DB)
cargo audit
cargo audit --json > /tmp/cargo-audit.json

# cargo-deny (broader: licenses, advisories, sources)
cargo deny check advisories
```

### I.2 — SAST

```bash
# clippy (some security-adjacent lints)
cargo clippy -- -D warnings

# Semgrep
semgrep --config p/rust --metrics=off <src>
```

---

## Section J — Mobile

### J.1 — Android

For source code:
```bash
# MobSF (CLI mode; runs locally)
mobsfscan --json -o /tmp/mobsfscan.json <android-src>

# Semgrep mobile pack
semgrep --config p/mobsfscan --metrics=off <android-src>
```

For built APK / AAB:
- See the separate `android-app-variant` skill or use:
  ```bash
  apkleaks -f <app.apk> -o /tmp/apkleaks.txt
  trivy image --input <app.apk>     # may not work; APK is not OCI
  ```

### J.2 — iOS

```bash
# MobSF static mode for IPA
# MOBSFSCAN supports Swift/Objective-C
mobsfscan --json -o /tmp/mobsfscan-ios.json <ios-src>

# Semgrep
semgrep --config p/swift --metrics=off <src>
```

---

## Section K — Containers & IaC

### K.1 — Dockerfile

```bash
hadolint <Dockerfile>
hadolint --format json <Dockerfile> > /tmp/hadolint.json
```

### K.2 — Terraform

```bash
tfsec <terraform-dir>
tfsec --format json <terraform-dir> > /tmp/tfsec.json

checkov -d <terraform-dir>
checkov -d <terraform-dir> --output json --output-file-path /tmp/checkov.json
```

### K.3 — Kubernetes

```bash
kube-linter lint <k8s-dir>
kube-score score <pod.yaml>
kubesec scan <pod.yaml>
```

### K.4 — CloudFormation / ARM / Bicep

```bash
checkov -d <cfn-dir> --framework cloudformation
cfn-lint <template.yaml>
checkov -d <bicep-dir> --framework arm
```

---

## Section L — Recording Tool Output in the Report

For each tool you run:

1. Record the **exact command**.
2. Record the **exit code**.
3. Quote the **summary** (counts by severity), not the full output.
4. Save the full output to `/tmp/<tool>.json` (or similar) for reference, but do not paste megabytes of JSON into the report.
5. In the report's Appendix, list "Tools run, version, exit code, summary".

Example Appendix entry:

```
- semgrep 1.78.0 — `semgrep --config p/security-audit --metrics=off .` — exit 1
  Summary: 12 findings (3 ERROR, 5 WARNING, 4 INFO). Full output: /tmp/semgrep.json
- npm audit — `npm audit --json` — exit 1
  Summary: 4 vulnerabilities (1 critical, 2 high, 1 moderate). Full output: /tmp/npm-audit.json
```

---

## Approval & Safety

- Each tool invocation needs the user's per-command approval. Approve in writing or by an explicit "yes/approved" before each run.
- Tools must not transmit project source to a third-party service. If a tool's default is online (e.g., `osv-scanner` queries OSV.dev), inform the user and offer the offline mode.
- Tools must not modify source files or lockfiles. Avoid `npm audit fix`, `cargo audit fix`, `composer update`, etc., unless the user explicitly asks for remediation execution (which is out of this skill's scope).
- If a tool is missing, report it. Do not auto-install with `apt`, `brew`, `pip`, `npm i -g`, etc., without approval.

---

## Required Practices

- Always check tool availability before recommending.
- Always disable telemetry where the flag exists (`--metrics=off`, `--no-telemetry`).
- Always run in non-modifying mode (`--dry-run`, `audit` without `fix`, etc.).

## Prohibited Practices

- Do not use online services that upload source code (uncertified SaaS scanners, online linters).
- Do not run `npm audit fix`, `pip-audit --fix`, or any auto-remediation in this skill.
- Do not install missing tools without explicit user approval per install.
