export const config = {
  pane: {
    id: "pipeline-dashboard",
    title: "Orchestrator Pipeline Dashboard",
    columns: 48,
    hotkey_dashboard: "p",
    hotkey_close: "escape",
    hotkey_reset: "r"
  },
  command: {
    name: "pipeline",
    description: "View and reset orchestrator pipeline dashboard",
    reset_subcommand: "reset"
  },
  filesystem: {
    log_directory_relative: "docs/harness-logs",
    log_file_extension: ".md"
  },
  runtime: {
    poll_interval_ms: 5000
  },
  policy: {
    orchestrator_skill: "00-orchestrator",
    completion_markers: [
      "Pipeline Summary",
      "Pipeline Run Summary",
      "## Pipeline Summary"
    ],
    skill_gate_mapping: {
      "01-brainstorm": "Brainstorm Gate",
      "02-plan": "Plan Gate",
      "07-review": "Review Gate"
    },
    skill_tdd_mapping: {
      "06-test": "RED",
      "03-implement": "GREEN",
      "05-fix": "GREEN",
      "07-review": "REFACTOR"
    },
    default_labels: {
      no_active_skill: "None",
      no_active_tdd: "None",
      no_active_gate: "None",
      initial_log: "None"
    }
  },
  ui: {
    colors: {
      banner_prefix: "cyan",
      banner_skill_active: "yellow",
      banner_skill_idle: "gray",
      tdd_red: "red",
      tdd_green: "green",
      tdd_refactor: "yellow",
      tdd_none: "gray",
      gate_active: "magenta",
      gate_none: "gray"
    }
  }
};
