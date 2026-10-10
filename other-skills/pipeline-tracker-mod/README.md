# pipeline-tracker-mod

Persistent pipeline HUD and Approval/Review Gate monitoring mod for `00-orchestrator` in Claude Code.

## 1. Directory Structure

```text
pipeline-tracker-mod/
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

## 2. Configuration Settings (`config/config.js`)

All operational rules, mappings, and UI color palettes are declared centrally in `config/config.js`:
- `policy.orchestrator_skill`: Main orchestrator entrypoint (`00-orchestrator`).
- `policy.completion_markers`: Markers in execution logs signaling workflow completion.
- `policy.skill_gate_mapping`: Mappings from child skills to approval gates.
- `policy.skill_tdd_mapping`: Mappings from child skills to TDD phases (`RED`, `GREEN`, `REFACTOR`).
- `policy.default_labels`: Default idle text (`None` for skill, TDD, and gate).
- `ui.colors`: Precise terminal TUI color schemes for active and idle components.

## 3. Display and Lifecycle Behavior

### Always Visible HUD
The `[PIPELINE]` HUD banner is persistent above the prompt input across the entire session.

### Accurate Skill Tracking
- **When a skill is executing**: Shows the exact active skill name (e.g., `Skill: 00-orchestrator`, `Skill: 06-test`, `Skill: advisor`) in yellow bold text. Handles nested skills via an execution stack.
- **When no skill is executing**: Automatically returns to `Skill: None` (dim gray) as soon as the skill finishes.

### Context-Aware TDD Phase
- **Inside 00-orchestrator pipeline**: Displays active phase (`RED`, `GREEN`, `REFACTOR`) with corresponding status colors (red, green, yellow).
- **Outside 00-orchestrator pipeline (standalone or automated execution)**: Displays `TDD: None` (neutral gray).

### Gate Checkpoints
- Tracks active approval gates (`Brainstorm Gate`, `Plan Gate`, `Review Gate`) during `00-orchestrator` runs. Returns to `Gate: None` outside or when completed.

### Reset and Completion
- **Automatic**: Resets pipeline status to `None` when `Pipeline Summary` is appended to `docs/harness-logs/*.md`.
- **Manual**: Run `/pipeline reset` or press `r` in the Dashboard (`p`) to reset pipeline tracking at any time.

## 4. Testing and Global Installation

### Session Testing
```powershell
claude --plugin-dir ".\other-skills\pipeline-tracker-mod"
```

### Global Installation
```powershell
Copy-Item -Recurse ".\other-skills\pipeline-tracker-mod" "$HOME\.claude\plugins\pipeline-tracker-mod"
```
