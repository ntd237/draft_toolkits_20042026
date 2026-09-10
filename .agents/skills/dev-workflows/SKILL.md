---
name: dev-workflows
description: "Orchestrator for 6 development workflows: bug-fix, code-review, documentation, performance-optimization, security-review, and tests. Auto-routes user requests to the correct workflow by keyword and coordinates multi-step tasks in dependency order. Triggers when the user asks to fix a bug, review code, generate docs, optimize performance, run a security review, or generate test cases."
---

# Skill: dev-workflows

## Language Protocol
- Respond in Vietnamese.
- Restate non-English requests in English before proceeding.
- Internal analysis in English; final response in Vietnamese.

## Trigger
User asks for one of: bug fix, code review, documentation generation, performance optimization, security review, or test case generation. The skill auto-routes by primary intent and coordinates multiple workflows when the request spans more than one.

## Routing Rules

Classify by primary intent, then run the matching workflow. If multiple intents are present, run each in dependency order.

| Intent keywords | Workflow |
| --- | --- |
| bug, lỗi, fix, sửa lỗi, error, crash, fail | `bug-fix` |
| review, code review, đánh giá code | `code-review` |
| document, docs, tài liệu, readme | `documentation` |
| performance, optimize, hiệu năng, tốc độ | `performance-optimization` |
| security, bảo mật, vulnerability, injection | `security-review` |
| test, tests, testcase, kiểm thử | `tests` |

## Execution Dependencies

When multiple workflows are requested together, follow this order:
1. `bug-fix` or `security-review` first — fix bugs and vulnerabilities before anything else.
2. `performance-optimization` next — optimize only after correctness is confirmed.
3. `tests` after changes — generate regression tests for the fix/optimization.
4. `code-review` after implementation — review the final diff.
5. `documentation` last — document stable, final behavior.

## Workflow

### Phase 1: Classify & Select Workflow(s)
**Objective**: Route the request to the correct workflow(s) by primary intent.

- Match the request against the Routing Rules table.
- If multiple intents are detected, order them per Execution Dependencies.
- If intent is ambiguous, ask the user to clarify before proceeding — do not guess silently.
- Announce the selected workflow(s) to the user before executing.

### Phase 2: Execute Selected Workflow(s)
**Objective**: Run each workflow's checklist against the actual codebase.

#### Bug Fix
- Perform root cause analysis: read the affected code, trace the error path, identify the root cause — not just the symptom.
- Provide a step-by-step fix approach with exact file paths and line numbers.
- Define a testing strategy: how to confirm the fix works and prevent regression.
- Suggest prevention measures for similar issues in the future.

#### Code Review
- **Code Quality**: readability, maintainability, adherence to project conventions and best practices.
- **Security**: potential vulnerabilities introduced or exposed by the changes.
- **Performance**: potential bottlenecks or inefficient patterns.
- **Testing**: areas that need test coverage or are now untested.
- **Documentation**: whether code is properly documented and comments are accurate.

#### Documentation
- Overview and purpose of the file/component.
- API reference with parameters and return values.
- Usage examples with code snippets.
- Configuration options if applicable.
- Error handling and troubleshooting.
- Dependencies and requirements.
- Format as clear, structured Markdown.

#### Performance Optimization
- Analyze algorithm complexity and efficiency.
- Examine memory usage patterns (allocations, leaks, retention).
- Check database queries and optimization opportunities (indexes, N+1, batching).
- Evaluate caching strategies (applicable? invalidation correct?).
- Assess network requests and bundling opportunities.
- For frontend code, check rendering performance (re-renders, layout thrashing, bundle size).
- Suggest specific optimizations with expected impact — not generic advice like "make it faster".

#### Security Review
- Input validation and sanitization completeness.
- Authentication and authorization checks on every entry point.
- Data exposure and privacy concerns (PII in logs, responses, error messages).
- Injection vulnerabilities (SQL, XSS, command injection, SSRF).
- Cryptographic implementations (algorithm choice, key management, constant-time comparison).
- Dependencies with known vulnerabilities (CVEs, outdated packages).
- Provide specific recommendations for any issues found, with severity ranking.

#### Tests
- Happy path scenarios.
- Edge cases and boundary conditions (empty, null, max, min, off-by-one).
- Error handling and exceptions (expected failures, unexpected input types).
- Integration points with other components (mocks, stubs, contract tests).
- Performance considerations (load, stress, timeout behavior).
- Security edge cases (injection in test input, privilege escalation).
- Use the project's existing testing framework conventions; include setup/teardown as needed.

### Phase 3: Summarize & Hand Off
**Objective**: Report what was done and suggest next steps.

- Summarize: what was done, which workflows ran, which files were touched.
- Suggest follow-up actions (e.g. run tests, update docs, review again after changes).
- If multiple workflows ran, confirm each completed its checklist.

## Output Format
- For single-workflow requests: deliver the workflow's output directly (analysis, review findings, generated docs, test cases, etc.).
- For multi-workflow requests: clearly label each workflow's output with a `## [Workflow Name]` header, in execution-dependency order.
- End with a `## Summary` section listing completed workflows, files touched, and follow-up suggestions.

## Don'ts
- Do not run any workflow without first reading the relevant files — never review or analyze blindly.
- Do not delegate to other skills — this skill executes the workflow content itself.
- Do not guess the workflow when intent is ambiguous — ask the user to clarify.
- Do not reverse Execution Dependencies order — fixing bugs before optimizing, testing before reviewing.
- Do not expand beyond the user's stated scope without asking first.
- Do not give generic optimization advice ("make it faster", "use caching") — every suggestion must include a specific mechanism and expected impact.
- Do not skip the security review checklist items — each entry point must be checked even if no issues are obvious.

## Quality Checklist
- [ ] Request classified to the correct workflow(s) using the Routing Rules table?
- [ ] Relevant files read before executing any workflow?
- [ ] Each selected workflow's full checklist completed?
- [ ] Multiple workflows executed in Execution Dependencies order?
- [ ] Bug fix includes root cause (not just symptom), fix approach, testing strategy, and prevention?
- [ ] Code review covers all 5 areas (quality, security, performance, testing, documentation)?
- [ ] Security review checks all 6 categories and ranks findings by severity?
- [ ] Test cases cover happy path, edge cases, errors, integration, performance, and security?
- [ ] Summary section lists completed workflows, files touched, and follow-up suggestions?
- [ ] No workflow executed on files that were not read first?
