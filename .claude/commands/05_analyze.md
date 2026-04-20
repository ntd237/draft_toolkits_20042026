---
description: "Task: Analyze and comprehensively understand AI system codebases through systematic code analysis, architecture discovery, data flow mapping, and performance optimization recommendations."
type: "auto"
---

# AI Code Analysis and Understanding

## Purpose

This command guides systematic and comprehensive analysis of AI system codebases to develop deep understanding of code structure, logic flows, architecture patterns, and optimization opportunities. It establishes a disciplined approach to analyzing existing systems, documenting architectural decisions, identifying performance bottlenecks, recognizing design patterns, and providing actionable recommendations for improvements. The analysis process encompasses codebase structure discovery, architecture reconstruction, data flow analysis, detailed component examination, performance and security assessment, and synthesized recommendations for enhancements. This command serves multiple purposes: onboarding new team members to understand existing systems, preparing for refactoring or major changes, conducting architectural code reviews, identifying optimization opportunities, and creating comprehensive technical documentation.

## Language Requirements

- All responses must be delivered in Vietnamese for user communication
- When receiving requests in languages other than Vietnamese, first restate understanding in English before proceeding
- Internal analysis and technical thinking conducted in English, then translated to Vietnamese for final delivery

---

# Code Analysis Workflow - Seven Phases

## Phase 1: Requirements Analysis and Scope Definition

**Objective**: Thoroughly understand analysis requirements, define scope, and establish analytical framework.

Execute the following analysis:
- Conduct requirement gathering: understand what aspects of codebase need analysis, identify specific concerns or problem areas, determine analysis objectives and focus areas
- Define analysis scope: establish which code components to analyze in detail, identify critical paths requiring deep examination, determine breadth and depth of analysis
- Identify stakeholder needs: understand who will use analysis results, determine appropriate level of technical detail, identify specific questions to address
- Establish context: understand project purpose and business context, review project history and maturity, gather information about technology stack and architectural constraints
- Document analysis constraints: identify any limitations on code access or sensitive areas, note time constraints or complexity limitations, document any known issues or areas of concern
- Determine analysis approach: select appropriate analysis techniques and tools, plan workflow phases based on project characteristics, establish quality standards for analysis

Deliverables must include clearly defined analysis objectives, scope documentation, stakeholder needs analysis, and planned analysis approach.

## Phase 2: Project Overview and Architecture Discovery

**Objective**: Systematically discover and document overall project structure, technology stack, and architectural organization.

Execute architecture discovery:
- Analyze repository structure: examine directory organization and module hierarchy, identify main components and subsystems, map file organization and relationships, document naming conventions and organizational patterns
- Identify technology stack: catalog programming languages and framework versions, list dependencies and third-party libraries with versions, document databases and supporting infrastructure, identify external service integrations
- Locate and trace entry points: identify application entry points and initialization flows, trace initial execution paths, understand configuration and environment setup, document bootstrapping process
- Create architecture diagrams: design diagrams showing major layers and component organization, visualize component relationships and data flows, illustrate external service integrations, create subgraphs grouping related components
- Document core modules: identify primary functional modules and their responsibilities, describe module relationships and dependencies, understand data flow between modules, assess module criticality
- Analyze architectural patterns: identify architectural style (monolithic, microservices, etc.), recognize design patterns at system level, assess architectural decisions and trade-offs

Deliverables must include architecture diagrams with clear component descriptions, technology stack inventory, documented entry points, module responsibility map, and architectural pattern analysis.

## Phase 3: Data Flow and Workflow Analysis

**Objective**: Understand how data flows through systems and how critical business workflows execute.

Execute data and workflow analysis:
- Select critical workflows: identify most important user workflows and business processes, rank workflows by criticality and frequency, select 3-5 workflows for detailed analysis, document workflow objectives and success criteria
- Create workflow diagrams: develop sequence diagrams for each critical workflow, show actor interactions and system component participation, document decision points and conditional flows, illustrate error handling paths, visualize data transformations through workflow
- Document data models: identify primary entities and their relationships, describe entity attributes and data types, document validation rules and constraints, create data relationship diagrams, explain key database queries and operations
- Identify integration points: locate all external system interactions, document API calls and their purposes, understand message queue producers and consumers, identify file I/O operations and data transfers
- Analyze request handling: trace how requests flow through system layers, understand request validation and processing, document response generation and formatting, identify potential failure points

Deliverables must include workflow diagrams for critical business processes, data model documentation with relationships, integration points inventory, request/response flow documentation, and identified error paths.

## Phase 4: Detailed Component Analysis and Code Examination

**Objective**: Conduct deep analysis of important modules and code components to understand implementation logic and design decisions.

Execute detailed analysis:
- Prioritize components for analysis: assess component complexity and code size, determine business criticality, identify areas with known issues or concerns, select 3-7 components for detailed examination
- Analyze component organization: understand module structure and internal organization, examine class hierarchies and relationships, document responsibilities and interfaces, understand dependencies and coupling
- Perform function-level analysis: examine important functions and methods, document function signatures and parameters, explain algorithm logic and implementation approach, identify edge cases and error conditions, assess performance characteristics, analyze complexity
- Identify design patterns: recognize design patterns applied throughout code, document pattern implementations and benefits, understand problem each pattern solves, assess appropriateness of pattern choices
- Review error handling strategies: examine exception handling approaches, understand error classification and handling logic, identify gaps in error handling coverage, assess error recovery mechanisms
- Analyze code quality indicators: identify code duplication and opportunities for consolidation, assess code readability and maintainability, understand test coverage and testing strategies, examine configuration management approaches

Deliverables must include detailed component analysis, design pattern inventory with locations and benefits, error handling strategy documentation, code quality assessment, and identified improvement opportunities.

## Phase 5: Performance and Security Analysis

**Objective**: Identify performance bottlenecks, security vulnerabilities, and optimization opportunities.

Execute performance and security analysis:
- Identify performance bottlenecks: locate inefficient algorithms and operations, find unoptimized queries and database access, identify blocking or synchronous operations, discover resource utilization issues, recognize caching opportunities
- Analyze concurrency characteristics: examine concurrent access patterns and shared resources, identify potential race conditions, understand synchronization mechanisms, assess thread-safety, review locking strategies
- Conduct security assessment: review authentication and authorization mechanisms, examine input validation approaches, identify potential vulnerabilities, assess sensitive data handling, review API security controls
- Analyze resource utilization: examine memory usage patterns, understand CPU utilization characteristics, identify I/O bottlenecks, assess scalability limitations, understand resource constraints
- Create findings tables: develop bottleneck identification tables with location, issue, impact, and severity, create security findings inventory, document performance characteristics and limitations
- Propose optimization strategies: identify multiple approaches for each bottleneck, estimate potential performance gains, assess implementation complexity, understand trade-offs and side effects

Deliverables must include bottleneck identification with impact analysis, security findings with severity assessment, performance characteristics documentation, and prioritized optimization strategies with estimated improvements.

## Phase 6: Synthesis and Comprehensive Assessment

**Objective**: Synthesize analysis findings into comprehensive strengths and improvement assessment.

Execute comprehensive synthesis:
- Identify system strengths: recognize well-implemented patterns and design, document effective architectural choices, understand business value delivered, identify areas of high code quality, recognize efficient algorithms and optimizations
- Document areas for improvement: identify architectural limitations, recognize maintainability concerns, find performance optimization opportunities, understand scalability constraints, identify missing features or capabilities
- Assess technical debt: inventory technical debt items and their impact, estimate effort to address each item, understand consequences of deferring resolution, prioritize debt items by impact
- Develop improvement recommendations: create specific, actionable recommendations, estimate implementation effort for each recommendation, document expected benefits and trade-offs, prioritize recommendations by impact and effort
- Create implementation roadmap: organize recommendations into phases, estimate timeline for implementation, sequence recommendations by dependencies, identify quick wins and major initiatives
- Plan knowledge transfer: identify documentation gaps, plan knowledge transfer activities, recommend refactoring opportunities, suggest architectural improvements

Deliverables must include strengths assessment, improvement recommendations with effort estimates and expected benefits, technical debt inventory, implementation roadmap with phasing, and knowledge transfer plan.

## Phase 7: Final Report and Actionable Recommendations

**Objective**: Deliver comprehensive analysis report with actionable recommendations and clear implementation guidance.

Execute report finalization:
- Compile executive summary: provide high-level overview of findings, summarize key strengths and opportunities, highlight critical recommendations, outline implementation approach
- Document detailed findings: organize findings by category (architecture, performance, security, quality), provide specific evidence and examples, link recommendations to findings
- Create comprehensive recommendations: develop 5-7 major recommendations with full justification, explain implementation approach for each, document expected outcomes and metrics, assess risks and mitigation strategies
- Design implementation roadmap: sequence recommendations logically, estimate timeline and effort, identify dependencies between recommendations, highlight quick wins for immediate impact
- Prepare knowledge transfer materials: develop documentation recommendations, plan onboarding materials, create architectural guidance, suggest training activities
- Establish metrics and monitoring: define success criteria for improvements, establish performance baselines, plan measurement approach, create monitoring and alerting strategy

Deliverables must include comprehensive analysis report with findings and recommendations, implementation roadmap with timelines and effort estimates, quick wins list for immediate execution, technical debt registry with prioritization, and knowledge transfer plan.

---

## Expected Results

After completing the code analysis workflow, the user receives:

1. **Architecture Documentation**: Complete understanding of system architecture, component organization, and design patterns
2. **Data Flow Documentation**: Clear mapping of data flows and critical business workflows through the system
3. **Code Quality Assessment**: Detailed examination of code organization, design patterns, error handling, and quality indicators
4. **Performance Analysis**: Identified bottlenecks with impact assessment and optimization strategies
5. **Security Assessment**: Identified vulnerabilities and security concerns with recommended mitigations
6. **Comprehensive Findings**: Clear synthesis of strengths, weaknesses, and improvement opportunities
7. **Actionable Recommendations**: Prioritized recommendations with implementation guidance, effort estimates, and expected benefits
8. **Implementation Roadmap**: Sequenced, phased approach to implementing improvements with timeline and resource estimates

---

## Important Rules

### Required Practices

- Always conduct thorough analysis across all phases before finalizing recommendations
- Always create diagrams and visualizations for architecture, data flows, and workflows
- Always provide specific code locations and examples supporting all findings
- Always explain design rationale and architectural decisions, not just what exists
- Always document findings with evidence and concrete examples
- Always prioritize recommendations based on impact and implementation effort
- Always assess security implications and performance impact of recommendations
- Always conduct comprehensive phase gates before proceeding to next phase
- Always validate findings and recommendations with stakeholder review
- Always document assumptions and limitations affecting analysis

### Prohibited Practices

- Do not make recommendations without understanding existing design rationale
- Do not skip phases or analysis steps to accelerate completion
- Do not provide generic recommendations without code-specific evidence
- Do not suggest changes without assessing performance and security implications
- Do not ignore edge cases or error handling in component analysis
- Do not create recommendations without effort estimates and impact assessment
- Do not proceed without validation that analysis scope is complete and accurate
- Do not skip security and performance assessment
- Do not omit knowledge transfer and documentation recommendations
- Do not write code implementations; analysis only, no implementation

---

## Best Practices Summary

**Comprehensive Understanding**: Conduct thorough analysis across all dimensions—architecture, data flows, components, performance, security—to develop complete understanding before making recommendations.
**Evidence-Based Analysis**: Ground all findings and recommendations in specific evidence from code analysis, providing code locations, examples, and data supporting conclusions.
**Clear Visualization**: Create diagrams and visualizations for architecture, workflows, and data flows to communicate complex concepts clearly and facilitate understanding.
**Prioritized Recommendations**: Rank recommendations by business impact and implementation effort, highlighting quick wins for immediate value and major initiatives for long-term improvement.
**Trade-off Analysis**: Explicitly document trade-offs inherent in recommendations, explaining what is gained and sacrificed with each improvement.
**Implementation Guidance**: Provide clear implementation roadmap with phasing, sequencing, dependencies, and effort estimates enabling practical execution.
**Knowledge Transfer**: Include recommendations for documentation, training, and knowledge transfer to enable team understanding and long-term maintainability.