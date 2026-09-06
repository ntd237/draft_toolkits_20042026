# Phase 6 (Part 1) — Dependencies & Supply Chain

## Objective

Identify direct and transitive dependencies that have known vulnerabilities, suspicious origins, or supply-chain risks. Pair each finding with version-accurate remediation guidance.

This phase covers the data and methodology. The companion file `references/07-tooling-by-language.md` covers the per-ecosystem tools and commands.

---

## Section A — Inventory

### A.1 — Manifest Files to Read

| Ecosystem | Manifest | Lockfile |
|---|---|---|
| Node.js | `package.json` | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb` |
| Python | `requirements.txt`, `requirements/*.txt`, `pyproject.toml`, `Pipfile`, `setup.py`, `setup.cfg` | `Pipfile.lock`, `poetry.lock`, `uv.lock`, `pdm.lock` |
| Java | `pom.xml`, `build.gradle(.kts)` | `gradle.lockfile`, dependency-locking enabled? |
| Go | `go.mod` | `go.sum` |
| Rust | `Cargo.toml` | `Cargo.lock` |
| Ruby | `Gemfile`, `*.gemspec` | `Gemfile.lock` |
| PHP | `composer.json` | `composer.lock` |
| .NET | `*.csproj`, `*.fsproj`, `Directory.Packages.props` | `packages.lock.json`, `paket.lock` |
| Swift | `Package.swift` | `Package.resolved` |
| Dart | `pubspec.yaml` | `pubspec.lock` |
| Container | `Dockerfile` (`FROM` lines) | `image-digest@sha256:...` if pinned |
| GitHub Actions | `.github/workflows/*.yml` (`uses: ...@<ref>`) | none — pin by SHA |

### A.2 — Lockfile Discipline Check

- Manifest present + lockfile **missing** → reproducibility risk; flag as **Low** unless this is a library project where it is acceptable.
- Lockfile present but **stale** relative to manifest (e.g., manifest version updated without lockfile regenerated) → flag as **Low** and point at the discrepancy.
- Multiple lockfiles for the same ecosystem (`package-lock.json` + `yarn.lock`) → ambiguous resolution; flag as **Info** with cleanup recommendation.

### A.3 — Pinning Discipline

For each dependency, classify how it is pinned:

| Pin style | Risk |
|---|---|
| Exact (`1.2.3`) | Lowest risk, but you must keep up with security updates |
| Caret/tilde (`^1.2.3`, `~1.2.3` in npm; `>=1.2.3,<2` in pip) | Acceptable when paired with a lockfile |
| Range (`>=1.2.3`) | Acceptable with lockfile; hazardous without |
| Wildcard (`*`, `latest`) | High risk — flag as **Medium** |
| Git URL / GitHub tarball | Supply-chain risk; flag as **Medium** unless pinned by commit SHA |
| Local path (`file:../foo`) | Acceptable for monorepos; flag if used in published library |

---

## Section B — Vulnerability Matching (SCA)

### B.1 — Methodology

Run a local SCA tool with user approval (see `07-tooling-by-language.md`). Use the tool's report as the primary source. Map each advisory to:

- Direct vs. transitive dependency
- Affected version range
- Fixed version (if available)
- Severity (use the tool's CVSS-derived severity, mapped to this skill's five-level model)
- Reachability (best-effort heuristic)

### B.2 — Severity Mapping

Tools usually report `Critical / High / Medium / Low` with a CVSS score. Map them like this in the report:

| Tool severity | This skill's severity | Adjust by reachability |
|---|---|---|
| Critical (CVSS 9.0+) | Critical → High if dep is dev-only or transitive-without-call-path | |
| High (7.0–8.9) | High → Medium if dep is dev-only or unreachable | |
| Medium (4.0–6.9) | Medium | |
| Low (< 4.0) | Low | |

Reachability heuristic (without full call-graph):
- If the vulnerable function is not imported anywhere in `[SOURCE]`, downgrade by one level and label "likely unreachable".
- If the vulnerable code path requires a configuration the project does not enable, downgrade and explain.
- Be honest about heuristic limits — never claim "unreachable" without grep evidence.

### B.3 — Avoid Fabrication

- Do not invent CVE IDs, advisory URLs, or version ranges.
- Always quote the exact tool output line for each advisory.
- If the tool was not run (user declined or tool missing), say so and downgrade the entire dependency section to "manual review only — SCA recommended".

### B.4 — Reporting Pattern

```
### [High] Vulnerable Dependency: lodash@4.17.10 (transitive via webpack@4)
**Category**: Vulnerable & Outdated Components (OWASP A06:2021)
**Source**: package-lock.json:1234 (transitive: webpack@4.46.0 → terser@4 → lodash@4.17.10)
**Advisory**: GHSA-jf85-cpcp-j695  (Prototype pollution via _.set / _.merge)
**Affected**: lodash < 4.17.21
**Fixed in**: 4.17.21
**Reachability**: lodash._.merge is not imported in src/; usage only inside webpack build pipeline.
**Severity adjustment**: Critical (CVSS 9.1) → reported as **High** because the vulnerable path runs only at build time, not at request time.
**Remediation**:
  1. Update webpack toolchain: `npm i -D webpack@5 webpack-cli@5` (which pulls a fixed lodash transitive).
  2. Or pin lodash directly via overrides:
     {
       "overrides": { "lodash": "4.17.21" }
     }
  3. Run `npm audit` after update to confirm zero remaining advisories for this CVE.
```

---

## Section C — Suspicious Package Indicators

### C.1 — Typosquatting

Compare suspicious-looking package names against a known list of popular packages. Common typosquat patterns:

- One-character substitution: `colors` vs `color`, `axiios` vs `axios`, `expreess` vs `express`
- Concatenation: `react-dom-router` (real: `react-router-dom`)
- Hyphen/underscore swaps: `body_parser` vs `body-parser`
- Capital-letter / locale tricks: `cróss-env`, `cross_env`

If a dependency has < 1k weekly downloads and a name suspiciously similar to a popular one, flag as **Medium** for manual review. Provide the user with a download/popularity check command:

```
npm view <pkg> --json | jq '.versions | length, ."dist-tags".latest'
pip show <pkg>; pip index versions <pkg> 2>/dev/null | head
```

### C.2 — Recently Published Packages

Recently created or recently published packages (< 30 days) that show up as direct deps deserve a manual look. The risk is supply-chain compromise via newly registered or transferred names.

### C.3 — Postinstall Scripts (npm)

Search `package.json` for `scripts.postinstall`, `scripts.preinstall`, `scripts.install`:

- Postinstall that downloads from a URL → **High** review-required.
- Postinstall that runs an obfuscated script (base64 / hex blobs) → **Critical**.
- Postinstall that exec's a binary in the package → review for legitimacy (some native libs need compilation).

If `--ignore-scripts` is set in `.npmrc`, mention as a positive control.

### C.4 — Unsigned / Unverified Sources

- npm packages are generally unsigned but the registry verifies provenance for newer publishes (look for `"_npmPublishProvenance"` in package metadata).
- Maven Central artifacts should match published GPG signatures.
- Go modules: `go.sum` ensures content addressing.
- Python: PEP 458/480 signing is rare in practice; use hash-pinning (`pip install --require-hashes`).

### C.5 — Abandoned / Unmaintained

A dep with no commits in 2+ years and known open vulnerabilities → **High** to **Critical** depending on usage. Recommend a fork, replacement, or vendoring with patches.

---

## Section D — License & Compliance Adjacent (Light Touch)

This skill is not a license audit, but flag obvious red flags:

- GPL / AGPL deps in a closed-source project where compliance would require source disclosure → **Info** with a note to consult legal.
- "Source-available but not OSS" licenses (BSL, SSPL) used in violation of their terms.

Do not produce a license report; defer to dedicated tools.

---

## Section E — Dockerfile Base Image Versions

### E.1 — Base Image Vulnerability

A `FROM python:3.7` is itself a dependency. Treat the base image as a dependency:

- Is the tag pinned by major+minor (`python:3.11-slim`) and ideally by digest (`@sha256:...`)?
- Is the base image still receiving security updates? (e.g., Python 3.7 is end-of-life since 2023; flag as **High**.)
- Run `trivy image <name:tag>` (offline DB) if approved for a list of CVEs in the image.

### E.2 — `apt`/`apk` packages installed in image

Inspect `RUN apt-get install ...` lines for outdated package pinning. Generally rely on the base image's package manager freshness; no action unless the user pinned a specific old package version.

---

## Section F — GitHub Actions / Composite Action Dependencies

Each `uses: <repo>@<ref>` line is a dependency:

- `uses: actions/checkout@v4` (tag) → readable but mutable; recommend SHA pinning for security-sensitive workflows.
- `uses: third-party/action@v1` (unknown maintainer) → **High** review; recommend SHA pin or fork.
- Star metric and maintainer reputation are not visible here; default to caution.

Recommended pinned form:

```yaml
- uses: actions/checkout@8e5e7e5ab8b370d6c329ec480221332ada57f0ab  # v4.2.2
```

---

## Section G — Vendored / Bundled Dependencies

If the repo contains a `vendor/` directory or copies of third-party code:

- Run grep for known signature-bearing files (`@license`, `@version`).
- For each vendored library, confirm whether the project is tracking upstream patches.
- A pinned vendored copy with a known unfixed CVE is **High** to **Critical**.

---

## Required Practices

- Always run an SCA tool (with approval) when a manifest is present and a tool exists for that ecosystem.
- Always cite advisory IDs (CVE / GHSA / OSV) directly from tool output.
- Always describe reachability honestly — heuristic if you didn't trace, definitive only if you did.
- Always recommend a concrete update command (not "upgrade lodash" but `npm i lodash@4.17.21`).

## Prohibited Practices

- Do not invent CVE numbers, GHSA IDs, or advisory text.
- Do not claim "no vulnerabilities" unless the tool was actually run and returned zero.
- Do not auto-run package upgrades; this skill is read-only.
- Do not infer vulnerabilities from version numbers alone without an advisory database.
