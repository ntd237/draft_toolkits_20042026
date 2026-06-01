---
name: grill-me
description: >-
  Interview the user about every aspect of their task until you've reached a
  shared understanding. Walk down each branch of the design tree, resolving
  dependencies between decisions one-by-one. For each question, provide your
  recommended answer.
---

# Grill-me

## Overview
Interview the user about every aspect of their task until you've reached a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

## Dependencies
This skill relies on core agent platform features:
- `default_api:ask_question`: To conduct interactive, structured, multiple-choice questions one by one.
- File system API: To write the final design plan.

## Quick Start
To trigger this skill, use a query like:
- *“Phỏng vấn tôi về việc tích hợp API thanh toán”*
- *“Hãy grill-me thiết kế hệ thống cache cho dự án”*

## Workflow

### 1. Analyze Context
- Read the codebase to understand the project structure, dependencies, existing API usage, and specific file configurations relevant to the user's task. Do not ask questions that can be answered by exploring the codebase.

### 2. Identify Key Design Decisions
- List all design decisions that need to be made (e.g., choice of databases, APIs, libraries, data schemas, error handling, performance strategies).

### 3. Conduct Interactive Interview
- Ask the questions **one at a time** using the `default_api:ask_question` tool.
- For each question:
  - Provide a clear, recommended option first based on best practices and context.
  - Detail why the recommendation is chosen.
  - If information is missing or the user is unsure, recommend the optimal solution according to industry standards/best practices for their approval.
- Do not overload the user with multiple questions in a single step.

### 4. Create Implementation Plan & Document Answers
- Once all design options and branches are clarified and agreed upon, compile:
  - A consolidated list of the agreed answers.
  - An implementation plan (`implementation_plan.md`) describing the architecture, changes, and verification plan.
- Save the plan and answers to the project directory or conversation workspace using `default_api:write_to_file`.

### 5. Report & Conclude
- Inform the user of the location of the generated plan.
- Stop and wait for further user commands (do not automatically trigger next actions/handoffs).

## Common Mistakes
- **Asking multiple questions at once**: Always ask questions one at a time to ensure a focused alignment.
- **Ignoring the codebase**: Always check the codebase first before asking the user for existing configuration details.
- **Skipping recommendations**: Never ask a question without providing a recommended choice first.
