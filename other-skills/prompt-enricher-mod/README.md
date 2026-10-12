# prompt-enricher-mod

Interactive prompt drafting and enrichment toolbar mod for Claude Code with native `enrich-prompt` skill integration.

## 1. Overview

`prompt-enricher-mod` integrates directly into Claude Code's `AbovePrompt` toolbar region. It provides an in-place draft editor with prompt enrichment, automatic dimensional scaling, and prompt submission.

### Key Capabilities

- **Direct `enrich-prompt` Skill Integration**:
  - Automatically locates and reads the canonical `enrich-prompt` specification (`SKILL.md` and `references/mode_a_direct.md`).
  - Executes Mode A (Direct Single-Block) optimization across the 5 core dimensions: Clarity & Actionability, Context & Scope Boundary, Structured Deliverables, Output Format & Standards, and Constraints & Guardrails.
  - Strictly enforces 100% language mirroring (Vietnamese input -> Vietnamese prompt, English input -> English prompt).
  - First attempts invocation via `$.tool.call({ tool: 'Skill', skill: 'enrich-prompt' })`, falling back to background model completion preloaded with the full skill instructions.
- **Minimal Footprint**: When collapsed, occupies only 1 terminal line with a compact `[+ Expand Enricher]` button.
- **Dynamic Auto-Sizing**: The input container automatically grows and shrinks between 1 line (`min_lines`) and 8 lines (`max_lines`). Content beyond 8 lines enters scrollable mode.
- **In-Place Enrichment**: The `[Enrich]` button rewrites and enriches the draft prompt without polluting conversation history.
- **Instant Undo**: The `[Undo]` button restores the original prompt text snapshot and shrinks the container back down.
- **Direct Submission**: The `[Submit]` button sends the current prompt directly to Claude Code via `$.prompt.submit`, resets draft buffers, and collapses the toolbar.
- **Persistent State**: Collapsing preserves any unsubmitted draft in memory so no work is lost.
- **Config-Driven**: Zero hardcoded values for boundaries, models, hotkeys, or labels.

## 2. Directory Structure

```text
prompt-enricher-mod/
├── .claude-plugin/
│   └── plugin.json
├── config/
│   ├── config.js
│   └── config.json
├── hooks/
│   ├── hooks.json
│   └── register.js
└── README.md
```

## 3. Configuration (`config/config.json`)

All runtime options are declared centrally in `config/config.json` and mirrored in `config/config.js`:

- `dimensions.min_lines`: Minimum input box height (default: `1`).
- `dimensions.max_lines`: Maximum input box height before scrolling activates (default: `8`).
- `dimensions.fallback_columns`: Fallback terminal column width when stdout is unavailable (default: `80`).
- `enrichment.skill_name`: Target skill (`enrich-prompt`).
- `enrichment.skill_directory_candidates`: Priority paths searched for the skill (`~/.claude/skills/enrich-prompt`, `.agents/skills/enrich-prompt`).
- `enrichment.model`: Model utilized for background completion (default: `haiku`).
- `enrichment.max_tokens`: Maximum tokens allocated for enrichment (default: `2048`).
- `command.name`: Registered slash command (default: `enricher`).
- `hotkeys`: Keyboard navigation bindings (`e`, `escape`, `r`, `u`, `s`, `c`, `k`, `j`).
- `ui.labels`: English UI display strings for all buttons and status notices.
- `ui.colors`: Terminal color tokens for header, borders, buttons, and status indicators.

## 4. Usage Workflow

1. **Expand Toolbar**:
   - Click `[+ Expand Enricher]` or press hotkey `e`.
2. **Draft Prompt**:
   - Type or paste your prompt into the input field. The box height automatically expands up to 8 lines.
3. **Enrich Prompt**:
   - Click `[Enrich]` (or press `r`). The status changes to `Enriching via enrich-prompt...`.
   - The mod processes the prompt against the canonical `enrich-prompt` Mode A specification.
   - Upon completion, the input field updates in-place with the enriched prompt.
4. **Choose Action**:
   - **Send Enriched**: Click `[Submit]` (or press `s`).
   - **Revert to Original**: Click `[Undo]` (or press `u`). The prompt reverts to your original draft and the box shrinks back down.
   - **Clear**: Click `[Clear]` (or press `c`).
   - **Collapse**: Click `[-] Collapse` (or press `escape`).

## 5. Testing and Global Installation

### Testing in Current Session

```powershell
claude --plugin-dir ".\other-skills\prompt-enricher-mod"
```

### Global Installation

To make the mod available globally across all Claude Code workspaces on your machine, copy the folder into your user plugins directory:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\plugins"
Copy-Item -Recurse -Force "E:\Workspace\Draft\project\2026\draft_toolkits_20042026\other-skills\prompt-enricher-mod" "$HOME\.claude\plugins\prompt-enricher-mod"
```
