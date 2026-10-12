export const config = {
  dimensions: {
    min_lines: 1,
    max_lines: 8,
    fallback_columns: 80,
    column_padding: 4
  },
  enrichment: {
    skill_name: "enrich-prompt",
    skill_directory_candidates: [
      "~/.claude/skills/enrich-prompt"
    ],
    skill_main_file: "SKILL.md",
    skill_reference_mode_a: "references/mode_a_direct.md",
    skill_reference_mode_b: "references/mode_b_structured.md",
    default_mode: "A",
    supported_modes: ["A", "B"],
    max_tokens_by_mode: {
      A: 4096,
      B: 8192
    },
    model: "haiku",
    mode_b_triggers: [
      "--mode-b",
      "--structured",
      "--detailed",
      "--breakdown",
      "structured format",
      "detailed breakdown",
      "dạng cấu trúc",
      "phân rã chi tiết"
    ],
    directives: {
      enforce_language_mirroring: true
    }
  },
  command: {
    name: "enricher",
    description: "Toggle and control prompt enricher toolbar",
    subcommands: {
      toggle: "toggle",
      clear: "clear",
      enrich: "enrich",
      undo: "undo",
      submit: "submit",
      mode: "mode"
    }
  },
  hotkeys: {
    expand: "e",
    collapse: "escape",
    enrich: "r",
    undo: "u",
    submit: "s",
    clear: "c",
    scroll_up: "k",
    scroll_down: "j",
    toggle_mode: "m"
  },
  ui: {
    labels: {
      expand_button: "[+ Expand Enricher]",
      collapse_button: "[-] Collapse",
      enrich_button: "[Enrich]",
      undo_button: "[Undo]",
      submit_button: "[Submit]",
      clear_button: "[Clear]",
      mode_button_prefix: "[Mode: ",
      mode_button_suffix: "]",
      header_title: "[PROMPT ENRICHER]",
      placeholder: "Type prompt here, or run /enricher...",
      status_idle: "Idle",
      status_enriching: "Enriching via enrich-prompt...",
      status_enriched: "Enriched",
      status_restored: "Restored",
      status_empty: "Empty prompt",
      status_cleared: "Cleared",
      scroll_up: "[^]",
      scroll_down: "[v]"
    },
    colors: {
      header_prefix: "cyan",
      status_idle: "gray",
      status_busy: "yellow",
      status_success: "green",
      status_warning: "yellow",
      status_error: "red",
      border: "cyan",
      button_primary: "cyan",
      button_secondary: "gray",
      text_content: "white",
      text_dim: "gray"
    }
  }
};
