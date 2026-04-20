---
description: "Task: Create comprehensive documentation for AI projects including README files, API documentation, architecture guides, deployment procedures, user guides, and operational documentation tailored to diverse audience needs."
type: "auto"
---

# AI Project Documentation

## Purpose

This command guides the creation of comprehensive documentation for AI projects across multiple audiences and use cases. It establishes a systematic approach to documenting system architecture, APIs, deployment procedures, operational guidance, and user interfaces. Documentation encompasses technical specifications for engineers, architecture documentation for system designers, operational guides for DevOps teams, user guides for end users, and API documentation for integration partners. The documentation process ensures clear communication of system design, usage patterns, operational procedures, and troubleshooting guidance, enabling effective adoption and long-term maintenance.

## Language Requirements

- All responses must be delivered in Vietnamese for user communication
- When receiving requests in languages other than Vietnamese, first restate understanding in English before proceeding
- Internal analysis and technical thinking conducted in English, then translated to Vietnamese for final delivery

---

# Documentation Creation Workflow - Five Phases

## Phase 1: Documentation Requirements Analysis and Planning

**Objective**: Understand documentation requirements and plan comprehensive documentation strategy.

Execute the following analysis:
- Identify documentation audiences: determine who will use documentation (developers, DevOps engineers, end users, integrators), understand each audience's needs and technical background
- Analyze project characteristics: understand system complexity, scope, scale, architectural patterns, and unique aspects requiring documentation
- Review existing documentation: identify what documentation exists, assess completeness and quality, identify gaps to be filled
- Determine documentation scope: establish which components require documentation, identify critical paths requiring detailed documentation, prioritize based on impact
- Plan documentation structure: design logical organization of documentation, establish information architecture, plan cross-references and navigation
- Assess technology and tools: identify documentation tools needed, plan version control strategy, establish review and approval process
- Establish documentation standards: define documentation style guide, establish template formats, set quality standards for completeness and clarity

Deliverables must include documentation requirements analysis, identified documentation audiences with their needs, documentation scope definition, and planned documentation structure and standards.

## Phase 2: Core Documentation Creation - README and Overview

**Objective**: Create foundational documentation providing project overview, quick start, and essential information.

Execute README and overview creation:
- Create project overview: document project purpose and vision, explain problem being solved, describe key capabilities
- Write quick start guide: provide minimal steps to get system running, document prerequisites and dependencies, include basic usage examples
- Document project structure: explain directory organization and module roles, describe file organization and naming conventions, provide visual structure diagrams
- Provide essential background: explain key concepts and terminology, provide context for architectural decisions, describe major components
- Include usage examples: provide practical examples of common tasks, demonstrate typical workflows, show expected outputs
- Document configuration: explain configuration options and their effects, provide configuration examples, describe environment setup
- Add troubleshooting guide: document common issues and solutions, provide debugging strategies, link to detailed troubleshooting resources
- Include links to other documentation: provide navigation to detailed documentation, organize references for different audiences

Deliverables must include comprehensive README file with project overview, quick start, essential background, and navigation to additional documentation.

## Phase 3: Technical Documentation - Architecture, APIs, and Design

**Objective**: Create detailed technical documentation for engineers and architects.

Execute technical documentation:
- Create architecture documentation: explain system design and major components, document component interactions and data flow, provide architecture diagrams and descriptions
- Document data models: explain entity relationships and data structures, document schema and field meanings, provide examples of data representations
- Create API documentation: document all API endpoints with methods and parameters, explain request/response formats and data types, provide usage examples for each endpoint
- Document interfaces and contracts: explain component interfaces and their usage, document contracts and assumptions between components, provide integration guidelines
- Create design decision documentation: explain major design decisions and their rationale, document alternative approaches considered, explain trade-offs and implications
- Write integration guides: explain how to integrate with external systems, document required adapters and transformers, provide step-by-step integration procedures
- Document extension points: identify locations where system can be extended, explain extension mechanisms and patterns, provide extension examples
- Create code walkthrough documentation: provide guided tours through important code sections, explain key algorithms and implementations, document complex logic

Deliverables must include architecture documentation with diagrams, API reference with comprehensive endpoint documentation, data model documentation, and design decision documentation.

## Phase 4: Operational and Deployment Documentation

**Objective**: Create documentation for deployment, operations, monitoring, and maintenance.

Execute operational documentation:
- Create deployment guide: document deployment procedures and steps, explain environment requirements and setup, provide deployment scripts and automation
- Write operational procedures: document common operational tasks and workflows, create runbooks for typical operations, explain monitoring and alerting setup
- Create monitoring and alerting guides: document metrics to monitor and their meanings, explain alerting thresholds and conditions, provide monitoring dashboards and queries
- Write troubleshooting and debugging guides: document common operational issues, provide diagnostic procedures, explain log analysis and interpretation
- Create performance tuning guides: document performance optimization parameters, explain tuning strategies for different scenarios, provide tuning recommendations
- Write backup and recovery procedures: document backup strategies and procedures, explain recovery procedures, provide disaster recovery plans
- Create scaling guides: document scaling strategies and procedures, explain capacity planning, provide scaling recommendations
- Write security documentation: document security features and configurations, explain credential management, provide security best practices

Deliverables must include deployment guide with automation scripts, operational runbooks, monitoring and alerting documentation, troubleshooting guides, and performance tuning documentation.

## Phase 5: User and Audience-Specific Documentation

**Objective**: Create documentation tailored to specific audiences and use cases.

Execute audience-specific documentation:
- Create user guides for end users: explain system from user perspective, document features and how to use them, provide step-by-step usage guides
- Write administrator guides: explain system administration and configuration, document user management and access control, provide administrative procedures
- Create integration documentation for partners: explain integration requirements and options, provide integration examples, document authentication and security
- Write developer guides for extensions: explain how to extend and customize system, document APIs for customization, provide development examples
- Create training materials: document system concepts and terminology, provide training exercises, create reference materials for learning
- Write FAQ documentation: collect common questions and provide clear answers, organize by topic, link to detailed documentation for complex topics
- Create glossary and terminology guide: explain domain-specific terminology, document acronyms and abbreviations, provide references and context
- Review and validate documentation: verify technical accuracy and completeness, check consistency across documentation, validate examples actually work

Deliverables must include user guides, administrator guides, integration documentation, developer guides, training materials, and FAQ documentation.

---

## Expected Results

After completing the documentation creation workflow, the user receives:

1. **Comprehensive README**: Project overview, quick start guide, and essential information for new users
2. **Technical Architecture Documentation**: System design, component descriptions, and architectural diagrams
3. **Complete API Documentation**: Detailed endpoint reference with parameters, responses, and usage examples
4. **Deployment and Operations Guides**: Deployment procedures, operational runbooks, monitoring setup, and troubleshooting guides
5. **User and Administrator Guides**: End-user guides and system administration documentation
6. **Integration and Developer Documentation**: Integration guides and extension documentation for partners and developers
7. **Supporting Materials**: FAQs, glossaries, training materials, and additional reference documentation
8. **Documentation Quality Assurance**: Verified accuracy, completeness, and internal consistency across all documentation

---

## Important Rules

### Required Practices

- Always analyze audience needs before creating documentation
- Always create comprehensive README as foundational documentation
- Always provide quick start guides for new users
- Always document all APIs with parameters, responses, and examples
- Always explain system architecture with diagrams and descriptions
- Always include troubleshooting guides and common issue resolutions
- Always provide step-by-step procedures for operational tasks
- Always explain configuration options and their effects
- Always document deployment procedures and automation
- Always create monitoring and alerting documentation
- Always validate that documentation examples actually work
- Always organize documentation logically with clear navigation
- Always keep documentation consistent with actual system behavior

### Prohibited Practices

- Do not create documentation without understanding audience needs
- Do not write vague or ambiguous instructions
- Do not omit examples and usage patterns
- Do not fail to include troubleshooting guides
- Do not skip API documentation or reference information
- Do not create documentation that contradicts actual system behavior
- Do not organize documentation in confusing structures
- Do not fail to explain key concepts and terminology
- Do not omit deployment and operational procedures
- Do not skip validation that documentation is accurate and complete

---

## Best Practices Summary

**Audience-Focused Documentation**: Create documentation tailored to different audience needs, from quick starts for beginners to detailed technical references for architects and operators.
**Comprehensive Coverage**: Provide complete documentation spanning architecture, APIs, deployment, operations, and user guidance rather than fragmentary documentation with gaps.
**Practical Examples**: Include working examples demonstrating key concepts, common usage patterns, and integration procedures that users can follow and adapt.
**Clear Organization**: Structure documentation logically with consistent navigation, cross-references, and hierarchical organization enabling readers to find needed information efficiently.
**Troubleshooting Focus**: Emphasize practical troubleshooting and common issue resolution to enable operators and users to solve problems independently.
**Accuracy and Consistency**: Ensure documentation remains synchronized with actual system behavior, validate examples work correctly, and maintain consistency across all documentation.