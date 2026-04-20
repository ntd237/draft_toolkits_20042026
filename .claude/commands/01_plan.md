---
description: "Task: Analyze requirements and create comprehensive project specifications and implementation plans for AI development tasks including new projects, refactoring, bug fixes, feature additions, and optimization."
type: "auto"
---

# AI Project Planning and Specification

## Purpose

This command guides the creation of detailed project specifications and implementation plans tailored to diverse AI development requirements. It addresses multiple scenarios: designing new AI systems from scratch, refactoring existing codebases, diagnosing and fixing bugs, adding new features to production systems, and optimizing performance bottlenecks. The planning phase establishes clear technical objectives, success metrics, architectural decisions, and phased implementation strategies before any code execution begins.

## Language Requirements

- All responses must be delivered in Vietnamese for user communication
- When receiving requests in languages other than Vietnamese, first restate understanding in English before proceeding
- Internal analysis and technical thinking conducted in English, then translated to Vietnamese for final delivery

---

# AI Planning Workflow - Four Phases

## Phase 1: Requirements Analysis and Classification

**Objective**: Thoroughly understand user requirements and determine the planning approach based on task type.

Execute the following analysis steps:
- Conduct comprehensive requirement gathering using clarifying questions to capture functional requirements, non-functional requirements, constraints, and success criteria
- Classify the task type: New Project (building from scratch), Refactoring (code restructuring), Bug Fix (identifying and resolving issues), Feature Addition (extending functionality), or Optimization (improving performance/efficiency)
- Document the current state: existing codebase analysis, technology stack, data characteristics, performance metrics if available
- Identify stakeholders, timeline expectations, and business context
- Assess technical constraints: computational resources, framework preferences, library ecosystem, production environment requirements

Deliverables must include clear task classification, comprehensive requirements documentation, constraint list, and identified assumptions that guide planning decisions.

## Phase 2: Architecture and Technical Specification Design

**Objective**: Create detailed technical specifications and architectural decisions aligned with identified requirements.

Execute the following specification design:
- Define the problem statement with mathematical formulation if applicable, including objective functions, success metrics, and evaluation criteria
- Design system architecture appropriate to task type: for new projects, propose overall system design; for refactoring, map existing components and propose improvements; for bug fixes, identify root causes and fix strategies; for features, design integration points; for optimization, identify bottlenecks
- Create data flow diagrams showing input/output specifications, data transformations, and processing stages
- Specify technical choices: model selection with justification, framework selection, library dependencies, design patterns
- Define interfaces: API specifications, configuration schemas, input/output formats, error handling strategies
- Establish quality criteria: code quality standards, testing strategies, performance targets, scalability requirements

Deliverables must include formal problem statement, architectural diagram description, interface specifications, technical choice justification matrix, and quality criteria documentation.

## Phase 3: Implementation Plan and Phased Strategy

**Objective**: Break down the implementation into clear, sequentially executable phases with measurable milestones.

Create the implementation roadmap:
- Design phase breakdown: identify logical stages from foundation to completion
- For each phase, define specific objectives, deliverables, resource requirements, estimated effort
- Establish dependencies: identify which phases depend on others, critical path analysis
- Create risk assessment: identify potential technical risks, mitigation strategies, contingency approaches
- Design integration points: how phases connect, validation between phases, rollback strategies if needed
- Plan validation checkpoints: success criteria for phase completion, acceptance criteria, testing strategy per phase

Deliverables must include detailed phase breakdown with clear objectives and deliverables, dependency graph, risk register with mitigation strategies, and checkpoint definitions.

## Phase 4: Documentation and Specification Finalization

**Objective**: Consolidate all planning work into a comprehensive, actionable specification document.

Execute finalization:
- Create executive summary capturing task overview, approach, timeline, and key decisions
- Document full technical specification including problem statement, architecture design, interface definitions, technology choices
- Produce detailed implementation plan with phases, milestones, effort estimates, and dependencies
- Record assumptions and constraints that informed planning decisions
- Prepare success metrics and acceptance criteria for each phase
- Generate handoff document for development team with all necessary context

Deliverables must include comprehensive specification document, implementation plan with phase details, risk register, and acceptance criteria documentation.

---

## Expected Results

After completing the planning workflow, the user receives:

1. **Clear Task Classification**: Explicit identification of planning type (new project, refactoring, bug fix, feature addition, optimization)
2. **Detailed Specification**: Complete technical specifications including problem formulation, architectural design, and interface definitions
3. **Implementation Roadmap**: Phased breakdown with clear objectives, deliverables, timeline estimates, and success criteria
4. **Risk Assessment**: Identified risks with mitigation strategies and contingency plans
5. **Architecture Artifacts**: Diagrams and descriptions of system design, data flow, and component interactions
6. **Decision Rationale**: Documented justification for technical choices and architectural decisions
7. **Acceptance Criteria**: Clear metrics for evaluating success of each phase and overall project

---

## Important Rules

### Required Practices

- Always conduct thorough requirements analysis before proceeding to specification design
- Always classify the task type to determine appropriate planning approach
- Always create formal problem statements with clear objectives and success metrics
- Always document architectural decisions with explicit justification and trade-off analysis
- Always break implementation into phases with measurable deliverables and clear success criteria
- Always identify and assess risks with mitigation strategies
- Always establish validation checkpoints between phases
- Always document assumptions that inform planning decisions
- Always create comprehensive handoff documentation for implementation teams

### Prohibited Practices

- Do not skip requirements analysis or assume understanding of requirements
- Do not create vague or ambiguous specifications
- Do not design phases without clear dependencies and milestone definitions
- Do not ignore non-functional requirements such as performance, scalability, and maintainability
- Do not omit risk assessment and mitigation planning
- Do not create plans without documented success criteria and acceptance conditions
- Do not mix planning concerns with implementation details

---

## Best Practices Summary

**Specification Excellence**: Create unambiguous technical specifications with formal problem statements, clear interfaces, and documented design rationale that eliminate guesswork during implementation.
**Phased Strategy**: Break work into logically coherent phases with clear dependencies, measurable deliverables, and validation checkpoints that enable progressive verification and risk mitigation.
**Comprehensive Risk Management**: Identify technical and project risks early with explicit mitigation strategies and contingency approaches rather than discovering problems during implementation.
**Clear Success Criteria**: Define explicit, measurable acceptance criteria and success metrics for each phase and the overall project to guide implementation decisions and quality assessment.
**Detailed Handoff**: Provide implementation teams with comprehensive documentation including architecture diagrams, interface specifications, risk registers, and assumption documentation to minimize ambiguity and rework.