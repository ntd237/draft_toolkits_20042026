---
name: repo-onboarding
description: "Onboard into an unfamiliar repository: scan structure, detect the tech stack, trace entry points and main execution flows, then write an ONBOARDING.md in the target repo's root so a new developer can start contributing after one read. Triggers when the user opens a new/unfamiliar repo and asks to explore, understand, onboard, or document it — keywords: repo-onboarding, onboard, understand this repo, explore repo, project overview, repo map, new dev onboarding, hiểu repo, tìm hiểu dự án, dev mới vào dự án."
---

# Skill: repo-onboarding

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English first.
- Internal analysis in English; final response in Vietnamese.
- ONBOARDING.md content in Vietnamese (keep original code identifiers, file paths, shell commands, and established technical terms).

## Trigger
Activates when the user opens or mentions a repo (usually new or unfamiliar) and wants to understand or document it: "onboard this repo", "help me understand this project", "how does this repo run", "write docs for a new dev". Does not activate when the user already knows the repo and just needs a specific bug fixed (that belongs to debug/fix workflows).

## Scope
- Analysis is **read-only** across all source; **write exactly one file** `ONBOARDING.md` at the target repo's root. Do not modify any code or config file.
- Medium depth: structure, stack, entry points, main flows, build/test/run commands, feature map. Do not go into detailed dependency graphs or historical design decisions (git archaeology) unless the user explicitly asks for a "deep onboarding".

## Workflow

### Phase 1 — Surface survey (Stack & Structure)
**Objective**: Determine stack, build tooling, and directory layout from declaration files only.

1. List the repo root. Read declaration files in priority order: `package.json`, `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`/`build.gradle`, `pubspec.yaml`, `*.csproj`, `Gemfile`, `composer.json` — stop once the primary stack is identified.
2. Read config files that shape the project: lockfile, `tsconfig.json`, `vite/webpack/next.config`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `Makefile`, CI config (`.github/workflows/`).
3. Draw a 2-level directory tree (exclude `node_modules`, `.git`, build artifacts, `dist`, `__pycache__`). For each level-1 directory, determine its role from the name plus 2-3 representative files inside.
4. Record available scripts/commands from the manifest (`build`, `dev`, `test`, `lint`, `start`...) — never guess commands.

### Phase 2 — Trace the main flow (Entry Points & Flows)
**Objective**: Find the launch points and the 1-3 most important business flows of the app.

1. Identify actual entry points: `main`/`bin`/`scripts` fields in the manifest, route indexes (`app/`, `src/pages/`, `cmd/*/main.go`, `manage.py`, `main.py`), Docker/CI config if present.
2. Starting from an entry point, read up to 3 hops inward (file → import → import): which functions are called, what gets initialized, which services are connected (DB, API, cache).
3. Pick 1-3 flows that represent the project's core purpose (e.g., one HTTP request from route to response; one CLI command completing a task). Describe each flow as a chain of actual file:function pairs you read.
4. Note "newcomer gotchas": generated vs hand-written directories, codegen steps, migrations, required environment variables from `.env.example`.

### Phase 3 — Synthesize & write ONBOARDING.md
**Objective**: Write `ONBOARDING.md` at the target repo's root using the template below, containing only facts verified in Phase 1-2.

```markdown
# ONBOARDING — <repo name>
> Documentation for new developers. Generated <YYYY-MM-DD> by repo-onboarding.

## 1. What this project is
2-4 sentences: purpose, target users, main deliverable.

## 2. Tech stack
| Layer | Technology | Verified from |
|---|---|---|
(runtime, framework, DB, infra as needed — each row cites the file it was read from)

## 3. Directory structure
2-level tree with a role note per directory.

## 4. Running the project
Install / dev / test / lint commands — copied verbatim from the manifest, with prerequisites (versions, .env, external services).

## 5. Main flows
1-3 flows, each: entry point → steps → endpoint, citing file:function paths.

## 6. Feature map
Table: feature | primary module/directory responsible.

## 7. Notes for newcomers
Codegen, migrations, environment variables, generated code areas, gotchas actually observed in the code (no speculation).
```

- If the repo already has an `ONBOARDING.md` or a `README.md` with similar dev documentation: read it first, keep their correct content, only add or correct what is wrong — never overwrite blindly. If the README is product marketing (not a dev doc), still create a separate `ONBOARDING.md`.
- For anything that could not be verified (e.g., tests could not run), mark it explicitly "unverified" instead of inventing content.

### Phase 4 — Self-check & report
**Objective**: Ensure every path and command in ONBOARDING.md is real, then summarize for the user.

1. Verify each cited file/function path in ONBOARDING.md exists on disk. Verify each command in section 4 exists in a manifest/config — no invented commands.
2. Remove any statement not traced to specific code you read.
3. Report in chat (Vietnamese): 5-8 line summary (stack, entry point, main flows), link to `ONBOARDING.md`, and list any "unverified" items.

## Don'ts
- Do not invent run commands or tool versions — every command must be quoted from a read `package.json`/`Makefile`/`Dockerfile`/CI config.
- Do not describe "typical framework architecture" instead of what the code actually does (common pitfall: assuming a Next.js app uses SSR because an `app/` directory exists).
- Do not paste large file contents or a full file listing into ONBOARDING.md — the doc is a map, not a dump.
- Do not modify code or run state-changing repo commands (install, migration, build) while onboarding — read-only; run `build`/`test` only if the user explicitly asks for live verification.
- Do not overwrite an existing `ONBOARDING.md`/README without reading and reconciling it first.

## Quality Checklist
- [ ] Stack and every command in section 4 of ONBOARDING.md trace back to a specific declaration file.
- [ ] Each flow in section 5 cites at least one file:function path that exists on disk.
- [ ] The directory tree in section 3 matches the disk (build-generated directories excluded).
- [ ] ONBOARDING.md sits at the target repo's root and no other file changed.
- [ ] No section contains invented or speculative content without an "unverified" label.
- [ ] Chat ends with a 5-8 line Vietnamese summary + link to ONBOARDING.md.
