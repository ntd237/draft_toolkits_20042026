import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'
import { config } from '../config/config.js'

const state = {
  isExpanded: false,
  draftText: '',
  undoSnapshot: null,
  isLoading: false,
  status: config.ui.labels.status_idle,
  scrollOffset: 0,
  activeMode: config.enrichment.default_mode || 'A'
}

let cachedSkillSpecs = {
  main: '',
  modeA: '',
  modeB: ''
}

function resolvePath(targetPath) {
  if (!targetPath) return ''
  if (targetPath.startsWith('~')) {
    return path.join(os.homedir(), targetPath.slice(1))
  }
  return path.resolve(targetPath)
}

function loadSkillFiles() {
  if (cachedSkillSpecs.main) {
    return cachedSkillSpecs
  }

  const candidates = config.enrichment.skill_directory_candidates || []

  for (const candidate of candidates) {
    const baseDir = resolvePath(candidate)
    const mainPath = path.join(baseDir, config.enrichment.skill_main_file)
    const modeAPath = path.join(baseDir, config.enrichment.skill_reference_mode_a)
    const modeBPath = path.join(baseDir, config.enrichment.skill_reference_mode_b)

    if (fs.existsSync(mainPath)) {
      try {
        cachedSkillSpecs.main = fs.readFileSync(mainPath, 'utf-8')
        if (fs.existsSync(modeAPath)) {
          cachedSkillSpecs.modeA = fs.readFileSync(modeAPath, 'utf-8')
        }
        if (fs.existsSync(modeBPath)) {
          cachedSkillSpecs.modeB = fs.readFileSync(modeBPath, 'utf-8')
        }
        break
      } catch {
        // Continue fallback search
      }
    }
  }

  return cachedSkillSpecs
}

function detectEffectiveMode(inputText, currentSelectedMode) {
  const lower = String(inputText || '').toLowerCase()
  const triggers = config.enrichment.mode_b_triggers || []
  const hasModeBTrigger = triggers.some(trig => lower.includes(trig))
  if (hasModeBTrigger) {
    return 'B'
  }
  return currentSelectedMode || 'A'
}

function extractEnrichedText(rawOutput) {
  if (!rawOutput) return ''
  let text = String(rawOutput).trim()

  if (text.startsWith('```') && text.endsWith('```')) {
    text = text.replace(/^```[a-zA-Z]*\n/, '').replace(/\n```$/, '').trim()
  }

  const headerRegex = /^###\s+Enriched Prompt[^\n]*\n+/i
  if (headerRegex.test(text)) {
    text = text.replace(headerRegex, '').trim()
  }

  return text
}

async function executeEnrichment($, inputPrompt, mode) {
  const skillName = config.enrichment.skill_name
  const maxTokens = config.enrichment.max_tokens_by_mode[mode] || 4096

  if ($.tool && typeof $.tool.call === 'function') {
    try {
      const modeFlag = mode === 'B' ? ' --mode-b' : ''
      const toolResult = await $.tool.call({
        tool: 'Skill',
        skill: skillName,
        args: `${inputPrompt}${modeFlag}`
      })
      const extracted = extractEnrichedText(toolResult?.text || toolResult?.result || toolResult)
      if (extracted && extracted.length > 0) {
        return extracted
      }
    } catch {
      // Fallback to model completion if tool invocation fails
    }
  }

  const specs = loadSkillFiles()
  const modeSpec = mode === 'B' ? specs.modeB : specs.modeA
  const modeDescription = mode === 'B'
    ? 'Mode B (Structured Multi-Section Context Enrichment)'
    : 'Mode A (Direct Single-Block Prompt Optimization)'

  const systemPrompt = [
    `You are the execution engine for the '${skillName}' skill running in '${modeDescription}'.`,
    `Official Skill Specification:`,
    specs.main,
    `Mode Reference Guidelines:`,
    modeSpec
  ].filter(Boolean).join('\n\n')

  const modeInstructions = mode === 'B'
    ? [
        `Execution requirements for Mode B:`,
        `1. Rewrite Only: Do NOT answer or execute the prompt.`,
        `2. Strict Language Mirroring: The entire prompt narrative and section descriptions MUST match 100% of the input language.`,
        `3. Structured Multi-Section Layout: Produce Title, Role & Context, Task, Input, Expected Output, Constraints & Rules (Must do / Must NOT do), and Success Criteria.`,
        `4. Clean Output: Output the structured prompt directly without conversational filler or surrounding markdown fence wrappers.`
      ].join('\n')
    : [
        `Execution requirements for Mode A:`,
        `1. Rewrite Only: Do NOT answer or execute the prompt.`,
        `2. Strict Language Mirroring: Output language MUST match 100% of the input language.`,
        `3. 5 Dimensions: Elevate clarity, define scope, enumerate deliverables, specify format, and embed guardrails.`,
        `4. Single-Block Output: Output only the finalized prompt directly as a single cohesive text block without section headings or conversational filler.`
      ].join('\n')

  const userInstruction = [
    `Raw prompt to enrich:`,
    inputPrompt,
    ``,
    modeInstructions
  ].join('\n')

  const res = await $.model.complete({
    model: config.enrichment.model,
    system: systemPrompt,
    prompt: userInstruction,
    maxTokens: maxTokens
  })

  const rawResult = typeof res === 'string' ? res : (res?.text || '')
  return extractEnrichedText(rawResult)
}

function calculateContentLines(text, bodyColumns) {
  if (!text || text.length === 0) return 1
  const cols = Math.max(20, bodyColumns - config.dimensions.column_padding)
  const paragraphs = text.split('\n')
  let totalLines = 0
  for (const paragraph of paragraphs) {
    if (paragraph.length === 0) {
      totalLines += 1
    } else {
      totalLines += Math.max(1, Math.ceil(paragraph.length / cols))
    }
  }
  return Math.max(1, totalLines)
}

function getStatusColor(status, colors) {
  if (status.startsWith('Enriching')) return colors.status_busy
  if (status.startsWith('Enriched') || status === config.ui.labels.status_restored) {
    return colors.status_success
  }
  if (status === config.ui.labels.status_empty) return colors.status_warning
  if (status.startsWith('Error')) return colors.status_error
  return colors.status_idle
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: config.command.name,
      description: config.command.description,
      immediate: true
    })
    return next(e)
  })

  on('command.run', { command: config.command.name }, async ($, e) => {
    const rawArg = String(e?.args || '').trim().toLowerCase()
    const subs = config.command.subcommands

    if (rawArg === subs.mode) {
      state.activeMode = state.activeMode === 'A' ? 'B' : 'A'
      $.ui.invalidate('ui.render')
      return {}
    }

    if (rawArg === subs.clear) {
      state.undoSnapshot = state.draftText
      state.draftText = ''
      state.status = config.ui.labels.status_cleared
      state.scrollOffset = 0
      $.ui.invalidate('ui.render')
      return {}
    }

    if (rawArg === subs.undo) {
      if (state.undoSnapshot !== null) {
        state.draftText = state.undoSnapshot
        state.undoSnapshot = null
        state.status = config.ui.labels.status_restored
        state.scrollOffset = 0
        $.ui.invalidate('ui.render')
      }
      return {}
    }

    if (rawArg === subs.submit) {
      if (state.draftText.trim().length > 0) {
        const textToSubmit = state.draftText
        state.draftText = ''
        state.undoSnapshot = null
        state.isExpanded = false
        state.status = config.ui.labels.status_idle
        state.scrollOffset = 0
        $.ui.invalidate('ui.render')
        await $.prompt.submit({ text: textToSubmit })
      }
      return {}
    }

    state.isExpanded = !state.isExpanded
    $.ui.invalidate('ui.render')
    return {}
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const nextTree = await next(e)
    const { Box, Text, Button, Input } = $.ui.resolve(e)
    const colors = config.ui.colors
    const labels = config.ui.labels
    const hotkeys = config.hotkeys

    if (!state.isExpanded) {
      const collapsedRow = Box({
        flexDirection: 'row',
        padding: 0,
        children: [
          Button({
            key: 'btn-expand-enricher',
            label: labels.expand_button,
            hotkey: hotkeys.expand,
            plain: true,
            onPress: async () => {
              state.isExpanded = true
              $.ui.invalidate('ui.render')
            }
          })
        ]
      })

      return Box({
        flexDirection: 'column',
        children: nextTree ? [collapsedRow, nextTree] : [collapsedRow]
      })
    }

    const termColumns = typeof process !== 'undefined' && process.stdout && process.stdout.columns
      ? process.stdout.columns
      : config.dimensions.fallback_columns

    const contentLines = calculateContentLines(state.draftText, termColumns)
    const minLines = config.dimensions.min_lines
    const maxLines = config.dimensions.max_lines
    const computedHeight = Math.max(minLines, Math.min(contentLines, maxLines))
    const isScrollable = contentLines > maxLines
    const maxScroll = isScrollable ? contentLines - maxLines : 0

    if (state.scrollOffset > maxScroll) {
      state.scrollOffset = maxScroll
    }

    const effectiveMode = detectEffectiveMode(state.draftText, state.activeMode)

    const headerChildren = [
      Text({ children: [labels.header_title], bold: true, color: colors.header_prefix }),
      Text({ children: ['|'], dimColor: true }),
      Text({ children: [`Status: ${state.status}`], color: getStatusColor(state.status, colors) }),
      Text({ children: ['|'], dimColor: true }),
      Text({ children: [`Active: Mode ${effectiveMode}`], bold: true, color: colors.header_prefix })
    ]

    if (isScrollable) {
      headerChildren.push(
        Text({ children: ['|'], dimColor: true }),
        Text({
          children: [`Line ${state.scrollOffset + 1}-${Math.min(state.scrollOffset + maxLines, contentLines)}/${contentLines}`],
          dimColor: true
        }),
        Button({
          key: 'btn-scroll-up',
          label: labels.scroll_up,
          hotkey: hotkeys.scroll_up,
          plain: true,
          onPress: async () => {
            if (state.scrollOffset > 0) {
              state.scrollOffset -= 1
              $.ui.invalidate('ui.render')
            }
          }
        }),
        Button({
          key: 'btn-scroll-down',
          label: labels.scroll_down,
          hotkey: hotkeys.scroll_down,
          plain: true,
          onPress: async () => {
            if (state.scrollOffset < maxScroll) {
              state.scrollOffset += 1
              $.ui.invalidate('ui.render')
            }
          }
        })
      )
    }

    const headerRow = Box({
      flexDirection: 'row',
      columnGap: 1,
      children: headerChildren
    })

    const inputRow = Box({
      flexDirection: 'column',
      height: computedHeight,
      minHeight: minLines,
      maxHeight: maxLines,
      borderStyle: 'single',
      borderColor: colors.border,
      padding: 0,
      children: [
        Input({
          key: 'input-prompt-draft',
          value: state.draftText,
          placeholder: labels.placeholder,
          onInput: (val) => {
            state.draftText = String(val || '')
            state.status = config.ui.labels.status_idle
            $.ui.invalidate('ui.render')
          }
        })
      ]
    })

    const actionRow = Box({
      flexDirection: 'row',
      columnGap: 2,
      children: [
        Button({
          key: 'btn-enrich',
          label: state.isLoading ? labels.status_enriching : labels.enrich_button,
          hotkey: hotkeys.enrich,
          dimColor: state.isLoading,
          onPress: async () => {
            if (state.isLoading) return
            const trimmed = state.draftText.trim()
            if (trimmed.length === 0) {
              state.status = labels.status_empty
              $.ui.invalidate('ui.render')
              return
            }

            state.undoSnapshot = state.draftText
            state.isLoading = true
            const targetMode = detectEffectiveMode(state.draftText, state.activeMode)
            state.status = `Enriching via enrich-prompt (Mode ${targetMode})...`
            $.ui.invalidate('ui.render')

            try {
              const enriched = await executeEnrichment($, state.draftText, targetMode)
              state.draftText = enriched
              state.status = `${labels.status_enriched} (Mode ${targetMode})`
              state.scrollOffset = 0
            } catch (err) {
              state.status = `Error: ${err?.message || 'Enrichment failed'}`
            } finally {
              state.isLoading = false
              $.ui.invalidate('ui.render')
            }
          }
        }),
        Button({
          key: 'btn-toggle-mode',
          label: `${labels.mode_button_prefix}${state.activeMode}${labels.mode_button_suffix}`,
          hotkey: hotkeys.toggle_mode,
          plain: true,
          onPress: async () => {
            state.activeMode = state.activeMode === 'A' ? 'B' : 'A'
            $.ui.invalidate('ui.render')
          }
        }),
        Button({
          key: 'btn-undo',
          label: labels.undo_button,
          hotkey: hotkeys.undo,
          dimColor: state.undoSnapshot === null,
          onPress: async () => {
            if (state.undoSnapshot !== null) {
              state.draftText = state.undoSnapshot
              state.undoSnapshot = null
              state.status = labels.status_restored
              state.scrollOffset = 0
              $.ui.invalidate('ui.render')
            }
          }
        }),
        Button({
          key: 'btn-submit',
          label: labels.submit_button,
          hotkey: hotkeys.submit,
          onPress: async () => {
            const trimmed = state.draftText.trim()
            if (trimmed.length === 0) {
              state.status = labels.status_empty
              $.ui.invalidate('ui.render')
              return
            }

            const promptToSubmit = state.draftText
            state.draftText = ''
            state.undoSnapshot = null
            state.isExpanded = false
            state.status = labels.status_idle
            state.scrollOffset = 0
            $.ui.invalidate('ui.render')

            await $.prompt.submit({ text: promptToSubmit })
          }
        }),
        Button({
          key: 'btn-collapse',
          label: labels.collapse_button,
          hotkey: hotkeys.collapse,
          plain: true,
          onPress: async () => {
            state.isExpanded = false
            $.ui.invalidate('ui.render')
          }
        }),
        Button({
          key: 'btn-clear',
          label: labels.clear_button,
          hotkey: hotkeys.clear,
          plain: true,
          onPress: async () => {
            if (state.draftText.length > 0) {
              state.undoSnapshot = state.draftText
              state.draftText = ''
              state.status = labels.status_cleared
              state.scrollOffset = 0
              $.ui.invalidate('ui.render')
            }
          }
        })
      ]
    })

    const expandedToolbar = Box({
      flexDirection: 'column',
      rowGap: 1,
      padding: 0,
      children: [
        headerRow,
        inputRow,
        actionRow
      ]
    })

    return Box({
      flexDirection: 'column',
      children: nextTree ? [expandedToolbar, nextTree] : [expandedToolbar]
    })
  })
}
