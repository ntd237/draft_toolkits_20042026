---
description: "Task: Diagnose and resolve bugs in AI systems through systematic analysis, root cause identification, targeted fixes, and verification of resolutions while maintaining code quality and system integrity."
type: "auto"
---

# AI Bug Diagnosis and Fix

## Purpose

This command guides systematic bug diagnosis, root cause analysis, and targeted resolution in AI systems. It establishes a disciplined approach to identifying failures, understanding their sources, implementing fixes, and verifying resolutions. The debugging process addresses syntax errors, logic errors, runtime failures, performance degradation, data processing anomalies, and system integration issues. The approach emphasizes understanding root causes rather than surface-level symptom fixes, ensuring permanent resolution while maintaining code quality and system integrity.

## Language Requirements

- All responses must be delivered in Vietnamese for user communication
- When receiving requests in languages other than Vietnamese, first restate understanding in English before proceeding
- Internal analysis and technical thinking conducted in English, then translated to Vietnamese for final delivery

---

# Debugging and Fix Workflow - Four Phases

## Phase 1: Problem Analysis and Information Gathering

**Objective**: Thoroughly understand the problem, gather evidence, and establish baseline understanding for diagnosis.

Execute the following analysis:
- Conduct issue reproduction: understand how to consistently reproduce the problem, document reproduction steps, identify environmental conditions needed
- Collect diagnostic evidence: gather error messages, stack traces, log outputs, system states, relevant code sections, and input data that triggered the issue
- Analyze symptom characteristics: classify the error type (syntax, logic, runtime, performance, data corruption), determine when symptoms appear, assess severity and impact
- Identify affected components: trace which system modules are involved, understand data flow through affected components, identify integration points
- Establish baseline comparison: understand expected behavior, identify actual behavior, document differences between normal and error states
- Gather contextual information: review recent code changes, check version history, verify environment consistency, understand system configuration

Deliverables must include detailed problem description with reproduction steps, complete diagnostic evidence collection, affected component identification, and baseline comparison analysis.

## Phase 2: Root Cause Analysis and Diagnosis

**Objective**: Systematically investigate and identify the underlying root causes of the observed problem.

Execute diagnostic process:
- Trace execution flow: follow program execution through affected components, identify execution path deviations, understand state changes
- Analyze code logic: review relevant code sections for logical errors, check boundary conditions, validate algorithm correctness
- Examine state and data: verify data integrity throughout processing, check for unexpected state changes, validate data transformations
- Review dependencies and interactions: analyze component interactions, check interface contracts, verify correct dependency usage
- Inspect configuration and environment: validate configuration correctness, verify environment setup, check for environment-specific issues
- Analyze error messages and logs: interpret error messages for clues, search logs for error patterns, correlate logs across components
- Identify failure point: pinpoint exact code location where failure occurs, understand condition that triggers failure, determine why normal safeguards failed
- Formulate root cause hypothesis: document suspected root cause with evidence, consider alternative explanations, validate hypothesis against all evidence

Deliverables must include detailed root cause analysis with evidence documentation, execution flow analysis, alternative hypotheses considered and ruled out, and validated root cause statement.

## Phase 3: Fix Design and Implementation

**Objective**: Design and implement targeted fix that resolves root cause while maintaining system integrity.

Execute fix development:
- Design fix approach: develop strategy to resolve identified root cause, consider multiple fix options with trade-offs, select approach minimizing side effects
- Implement targeted fix: apply fix to root cause location, avoid over-broad changes, maintain existing code quality standards
- Implement safeguards: add checks to prevent recurrence, implement input validation if needed, add error handling for edge cases
- Update related code: identify other locations affected by root cause, apply consistent fixes, prevent similar issues elsewhere
- Add regression tests: create test cases that specifically catch this bug, verify tests fail without fix and pass with fix, add to regression test suite
- Validate fix completeness: verify fix resolves symptom, check that root cause is actually eliminated, validate no new issues introduced
- Document fix rationale: explain root cause, describe fix approach, document why this approach was chosen, note any limitations

Deliverables must include fixed code with inline explanatory comments, regression test cases, fix documentation explaining root cause and solution rationale.

## Phase 4: Verification and Quality Assurance

**Objective**: Verify fix resolution, ensure no regressions, and validate overall system health after fix implementation.

Execute verification:
- Conduct reproduction verification: reproduce original problem with fixed code, confirm symptom is resolved, verify expected behavior is restored
- Execute regression testing: run all existing tests to ensure no new failures, execute new regression tests specifically for this bug, verify test suite passes
- Perform related testing: test components that interact with fixed code, verify integration still works correctly, test boundary conditions
- Conduct code quality review: verify fix maintains code quality standards, check readability and maintainability, validate against project conventions
- Execute end-to-end testing: verify overall system functions correctly, test workflows affected by fix, validate data integrity throughout system
- Monitor for recurrence: observe system behavior after fix deployment, monitor logs for any related anomalies, be alert for similar issues
- Document lessons learned: record insights from this debugging session, identify improvements to prevent similar issues, update coding guidelines if needed

Deliverables must include verification report confirming fix resolution, regression test results, code quality review, and lessons learned documentation.

---

## Expected Results

After completing the debugging and fix workflow, the user receives:

1. **Root Cause Identification**: Clear, evidence-based identification of the underlying cause of the problem
2. **Targeted Fix**: Minimal, focused code changes that resolve the root cause without unnecessary modifications
3. **Regression Prevention**: Test cases that specifically catch this bug and prevent regression
4. **System Integrity**: Verification that fix resolves problem without introducing new issues
5. **Complete Documentation**: Detailed explanation of problem, root cause analysis, fix rationale, and lessons learned
6. **Quality Assurance**: Full test verification and code quality validation confirming fix viability
7. **Knowledge Capture**: Documented insights for preventing similar issues in the future

---

## Important Rules

### Required Practices

- Always gather complete diagnostic evidence before attempting diagnosis
- Always reproduce the problem to understand it fully
- Always analyze root cause rather than addressing surface symptoms
- Always trace execution flow to understand what actually happens
- Always consider alternative explanations before concluding on root cause
- Always validate root cause hypothesis against all available evidence
- Always implement targeted fixes addressing root cause
- Always add regression tests that specifically catch this bug
- Always verify fix resolves problem without introducing new issues
- Always conduct comprehensive testing before declaring fix complete
- Always document root cause analysis and fix rationale for future reference

### Prohibited Practices

- Do not attempt fixes before understanding root cause
- Do not implement broad changes hoping they fix the problem
- Do not skip regression testing after implementing fix
- Do not ignore error messages and log information
- Do not implement fixes without understanding why problem occurred
- Do not deploy fixes without comprehensive verification
- Do not create fixes that obscure root cause rather than resolving it
- Do not fail to add regression tests that prevent recurrence
- Do not ignore code quality during fix implementation
- Do not skip documentation of fix rationale and lessons learned

---

## Best Practices Summary

**Root Cause Focus**: Investigate and resolve underlying root causes rather than surface symptoms, ensuring permanent resolution and preventing similar issues.
**Systematic Diagnosis**: Follow disciplined debugging approach including reproduction, evidence gathering, hypothesis formation, and validation before implementing fixes.
**Minimal Impact**: Design fixes targeting specific root cause with minimal code changes to reduce risk of unintended consequences and maintain system coherence.
**Regression Prevention**: Create test cases specifically designed to catch this bug and add to regression suite to prevent problem recurrence in future versions.
**Comprehensive Verification**: Verify fix resolution through multiple approaches including reproduction verification, regression testing, related component testing, and end-to-end validation.
**Knowledge Capture**: Document root cause analysis, fix rationale, and lessons learned to build organizational knowledge and prevent similar issues in future development.