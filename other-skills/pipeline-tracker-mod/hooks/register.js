import { config } from '../config/config.js'

const PANE_ID = config.pane.id
const PANE_TITLE = config.pane.title
const PANE_COLUMNS = config.pane.columns
const HOTKEY_DASHBOARD = config.pane.hotkey_dashboard
const HOTKEY_CLOSE = config.pane.hotkey_close
const HOTKEY_RESET = config.pane.hotkey_reset

let isIn00Pipeline = false
const activeSkillStack = []

const state = {
  currentSkill: config.policy.default_labels.no_active_skill,
  tddPhase: config.policy.default_labels.no_active_tdd,
  pendingGate: config.policy.default_labels.no_active_gate,
  activeLogFile: config.policy.default_labels.initial_log
}

function resetPipelineStatus() {
  isIn00Pipeline = false
  state.tddPhase = config.policy.default_labels.no_active_tdd
  state.pendingGate = config.policy.default_labels.no_active_gate
  state.activeLogFile = config.policy.default_labels.initial_log
}

function getTddColor(phase, colors) {
  if (phase === 'RED') return colors.tdd_red
  if (phase === 'GREEN') return colors.tdd_green
  if (phase === 'REFACTOR') return colors.tdd_refactor
  return colors.tdd_none
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

  on('tool.call', async ($, e, next) => {
    const toolName = e.toolName || ''
    const toolInput = e.toolInput || {}

    const isSkillCall = toolName === 'Skill' && Boolean(toolInput.skill)
    const invokedSkill = isSkillCall ? String(toolInput.skill) : null

    if (isSkillCall && invokedSkill) {
      activeSkillStack.push(invokedSkill)
      state.currentSkill = invokedSkill

      if (invokedSkill === config.policy.orchestrator_skill) {
        isIn00Pipeline = true
      }

      if (isIn00Pipeline) {
        const mappedGate = config.policy.skill_gate_mapping[invokedSkill]
        state.pendingGate = mappedGate || config.policy.default_labels.no_active_gate

        const mappedTdd = config.policy.skill_tdd_mapping[invokedSkill]
        if (mappedTdd) {
          state.tddPhase = mappedTdd
        }
      } else {
        state.tddPhase = config.policy.default_labels.no_active_tdd
        state.pendingGate = config.policy.default_labels.no_active_gate
      }

      $.ui.invalidate('ui.render')
    }

    if ((toolName === 'Write' || toolName === 'Edit') && toolInput.file_path) {
      const targetPath = String(toolInput.file_path)
      const content = String(toolInput.content || toolInput.new_string || '')

      if (targetPath.includes('harness-logs') && targetPath.endsWith('.md')) {
        const parts = targetPath.split(/[/\\]/)
        state.activeLogFile = parts[parts.length - 1]

        const isComplete = config.policy.completion_markers.some(marker => content.includes(marker))
        if (isComplete) {
          resetPipelineStatus()
        }
      }
    }

    let result
    try {
      result = await next(e)
    } finally {
      if (isSkillCall) {
        activeSkillStack.pop()
        state.currentSkill = activeSkillStack.length > 0
          ? activeSkillStack[activeSkillStack.length - 1]
          : config.policy.default_labels.no_active_skill

        $.ui.invalidate('ui.render')
      }
    }

    return result
  })

  on('command.run', { command: config.command.name }, async ($, e) => {
    const rawArgs = String(e?.args || '').trim().toLowerCase()

    if (rawArgs === config.command.reset_subcommand) {
      resetPipelineStatus()
      await $.ui.close({ id: PANE_ID })
      $.ui.invalidate('ui.render')
      return {}
    }

    await $.ui.open({
      id: PANE_ID,
      title: PANE_TITLE,
      focus: true,
      closeOnEscape: true,
      columns: PANE_COLUMNS
    })
    return {}
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const nextTree = await next(e)
    const { Box, Text, Button } = $.ui.resolve(e)
    const colors = config.ui.colors

    const isSkillActive = state.currentSkill !== config.policy.default_labels.no_active_skill
    const skillColor = isSkillActive ? colors.banner_skill_active : colors.banner_skill_idle

    const tddColor = getTddColor(state.tddPhase, colors)
    const isGateActive = state.pendingGate !== config.policy.default_labels.no_active_gate
    const gateColor = isGateActive ? colors.gate_active : colors.gate_none

    const hudBanner = Box({
      flexDirection: 'row',
      columnGap: 2,
      borderStyle: 'single',
      padding: 0,
      children: [
        Text({ children: ['[PIPELINE]'], bold: true, color: colors.banner_prefix }),
        Text({ children: [`Skill: ${state.currentSkill}`], color: skillColor, bold: isSkillActive }),
        Text({ children: ['|'], dimColor: true }),
        Text({ children: [`TDD: ${state.tddPhase}`], color: tddColor }),
        Text({ children: ['|'], dimColor: true }),
        Text({ children: [`Gate: ${state.pendingGate}`], color: gateColor }),
        Button({
          key: 'open-pipeline-dashboard',
          label: `[Dashboard (${HOTKEY_DASHBOARD})]`,
          hotkey: HOTKEY_DASHBOARD,
          plain: true,
          onPress: async () => {
            await $.ui.open({
              id: PANE_ID,
              title: PANE_TITLE,
              focus: true,
              closeOnEscape: true,
              columns: PANE_COLUMNS
            })
          }
        })
      ]
    })

    return Box({
      flexDirection: 'column',
      children: nextTree ? [hudBanner, nextTree] : [hudBanner]
    })
  })

  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    if (e.requestId !== PANE_ID) return next(e)

    const { Box, Text, Button } = $.ui.resolve(e)
    const colors = config.ui.colors

    return Box({
      flexDirection: 'column',
      rowGap: 1,
      padding: 1,
      children: [
        Text({ children: [`--- ${PANE_TITLE} ---`], bold: true, color: colors.banner_prefix }),
        Text({ children: [`Active Skill  : ${state.currentSkill}`] }),
        Text({ children: [`In 00-Flow    : ${isIn00Pipeline ? 'Yes' : 'No'}`] }),
        Text({ children: [`TDD Phase     : ${state.tddPhase}`] }),
        Text({ children: [`Active Gate   : ${state.pendingGate}`] }),
        Text({ children: [`Harness Log   : ${state.activeLogFile}`], dimColor: true }),
        Box({
          flexDirection: 'row',
          columnGap: 2,
          children: [
            Button({
              key: 'btn-reset-pipeline',
              label: `Reset [${HOTKEY_RESET}]`,
              hotkey: HOTKEY_RESET,
              onPress: async () => {
                resetPipelineStatus()
                await $.ui.close({ id: PANE_ID })
                $.ui.invalidate('ui.render')
              }
            }),
            Button({
              key: 'btn-close-pane',
              label: `Close Panel [${HOTKEY_CLOSE}]`,
              hotkey: HOTKEY_CLOSE,
              onPress: async () => {
                await $.ui.close({ id: PANE_ID })
              }
            })
          ]
        })
      ]
    })
  })
}
