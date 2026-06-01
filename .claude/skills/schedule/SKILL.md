---
name: schedule
description: >-
  Schedule a one-shot timer or a recurring cron job that sends notifications in
  the background.
---

# Schedule

## Overview
Schedule a one-shot timer or a recurring cron job that sends notifications in the background.

**NOTE**: This tool call returns immediately and does not pause execution. To wait for the timer to fire, you must stop calling tools to end your turn.

## Modes

### 1. One-shot timer
This should be used when there are tasks happening asynchronously (either background tasks, or other subagents) and you plan to go idle. This timer ensures you will wake up by this time if no other updates are received. If it expires, a notification with your Prompt is sent. If you receive any message (from ANY task or subagent) before the timer expires, the timer is cancelled silently.

#### Examples:
- Set a 60-second reminder while waiting for a long build: DurationSeconds=60, Prompt="Check if the build has completed"
- Set a 3-minute reminder after delegating a task to a group of subagents: DurationSeconds=180, Prompt="Check if the subagents have completed their tasks"

### 2. Recurring cron
Set CronExpression to a standard 5-field cron expression (e.g., '*/5 * * * *' for every 5 minutes). Each time the cron triggers, a notification with your Prompt is sent. The cron runs as a background task. Optionally set MaxIterations to limit the number of triggers.

#### Examples:
- Poll deployment status every 5 minutes: CronExpression="*/5 * * * *", Prompt="Check deployment status and report progress"
- Run a health check every hour, up to 3 times: CronExpression="0 * * * *", MaxIterations=3, Prompt="Run the health check script and report results"

## Guidelines
- You must specify exactly one of DurationSeconds or CronExpression.
- Always provide a Prompt describing what the notification should say.
- Never run a background 'sleep' command to set a timer, use this tool instead.
- To cancel a running timer or cron schedule, use the manage_task tool with the task ID returned by this tool.
