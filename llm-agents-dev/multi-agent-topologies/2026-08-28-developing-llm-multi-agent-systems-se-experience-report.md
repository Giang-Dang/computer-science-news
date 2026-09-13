# Developing LLM-based Multi-Agent Systems in Software Engineering: A Mixed-Method Experience Report

**ArXiv ID:** 2608.11965  
**Submitted:** August 2026  
**Authors:** Mariama Celi Serafim De Oliveira, Motunrayo Osatohanmen Ibiyo, Marco Gianrusso, Claudio Di Sipio, Davide Di Ruscio, Phuong T. Nguyen  
**Venue:** Empirical Software Engineering (accepted)

## Executive Summary

This paper presents a mixed-method experience report on developing LLM-based multi-agent systems for software engineering tasks. As organizations increasingly adopt agentic AI for development workflows, this empirical study bridges the gap between single-agent systems and orchestrated multi-agent architectures. The work is significant for practitioners implementing production-grade multi-agent systems, offering empirical validation of design patterns and coordination mechanisms that go beyond theoretical frameworks.

## Problem Statement

Early applications of AI in software engineering focused on single, independent LLM agents performing isolated tasks (bug fixing, code review, etc.). However, real-world software development involves complex, interdependent workflows where:

- Multiple engineers work on different components simultaneously
- Task dependencies create ordering constraints
- Integration and coordination failures require recovery mechanisms
- Quality assurance requires distributed testing and validation

While recent advances have shifted toward multi-agent systems (MAS) that orchestrate multiple LLM-based agents, practical guidance on designing, implementing, and managing these systems in real organizational contexts remains limited. This paper addresses the gap between theoretical multi-agent architectures and deployed systems.

## Core Concepts & Theory

### Multi-Agent System Orchestration Layers

The paper identifies three critical layers in production multi-agent software engineering systems:

1. **Agent Design Layer**: Individual LLM agent specializations (architect, developer, reviewer, tester)
2. **Coordination Layer**: Mechanisms for task delegation, dependency management, and state synchronization
3. **Orchestration Layer**: High-level workflow management, quality gates, and persistent state tracking

### Agent Roles in Software Development

Building on frameworks like ChatDev and MetaGPT, the paper examines specialized agent roles:

- **CEO Agent**: Strategic planning and high-level task decomposition
- **Architect Agent**: Design decisions and architectural reasoning
- **Developer Agent**: Implementation and code generation
- **Reviewer Agent**: Code quality and design review
- **Tester Agent**: Test creation and quality assurance

### Multi-Agent Architecture Pattern

```
┌─────────────────────────────────────────────────┐
│         Orchestration Layer (Workflow)           │
│  - Phase Management (design → code → test)      │
│  - Quality Gates & Verification                 │
│  - State Persistence & Recovery                 │
└─────────────────────────────────────────────────┘
                        ▲
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Agent A │    │ Agent B │    │ Agent C │
   │ (Role)  │    │ (Role)  │    │ (Role)  │
   └─────────┘    └─────────┘    └─────────┘
        │               │               │
        └───────────────┼───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │   Coordination Layer           │
        │  - Task Scheduling            │
        │  - Dependency Resolution       │
        │  - Result Integration          │
        └───────────────────────────────┘
```

### Key Design Patterns Identified

1. **Waterfall vs. Iterative**: Sequential phase progression vs. iterative refinement
2. **Centralized vs. Decentralized**: Central orchestrator vs. peer-to-peer coordination
3. **Synchronous vs. Asynchronous**: Blocking task execution vs. concurrent independent work
4. **Single-Model vs. Multi-Model**: Uniform LLM across agents vs. role-specific models

## Main Ideas & Contributions

### 1. Empirical Validation of Multi-Agent Effectiveness

The paper provides empirical evidence that multi-agent orchestration improves outcomes on complex software engineering tasks compared to single-agent approaches. Key improvements identified:

- **Task Decomposition Quality**: Multi-agent systems produce better architectural plans through specialized reasoning
- **Code Quality**: Distributed review and testing catch more defects than single-pass generation
- **Workflow Efficiency**: Parallel independent work on non-dependent components reduces total execution time

### 2. Integration Challenges and Solutions

The paper documents real-world challenges in deploying multi-agent systems:

**Challenge**: Conflicting modifications by concurrent agents  
**Solution**: Isolated workspaces with merge conflict detection and resolution strategies

**Challenge**: Dependency tracking and ordering  
**Solution**: Explicit dependency graphs with topological sorting and conditional task gates

**Challenge**: Quality verification at system boundaries  
**Solution**: Executable test-based verification and multi-stage quality gates

### 3. State Management and Recovery

Production systems require:
- Persistent tracking of intermediate states across agent invocations
- Recovery mechanisms when individual agents fail
- Rollback capabilities for failed phases
- Audit trails for compliance and debugging

### 4. Communication Protocols and Interfaces

Effective multi-agent coordination requires well-defined interfaces:
- Structured message formats (JSON specifications for task definitions)
- Clear contract definitions for agent responsibilities
- Explicit input/output specifications to enable parallel work

## Methodology & Implementation

### Research Approach

**Mixed-Method Design**: Combines qualitative and quantitative research methods to capture both the breadth and depth of multi-agent system development experiences.

**Qualitative Components**:
- Case studies of deployed multi-agent systems in production
- Semi-structured interviews with engineers implementing multi-agent systems
- Observation of system behavior in operational contexts

**Quantitative Components**:
- Metrics on task completion rates, quality measures, and execution efficiency
- Comparative analysis of different architectural patterns
- Performance benchmarking across role configurations

### Study Subjects

The paper examines real-world deployments, likely including:
- Internal organizational multi-agent systems
- Open-source projects using frameworks like AutoGen and MetaGPT
- Commercial products employing orchestrated LLM agents

### Key Metrics Evaluated

- **Effectiveness Metrics**: Task completion rate, quality of generated artifacts, convergence to acceptable solutions
- **Efficiency Metrics**: End-to-end execution time, token consumption, parallel efficiency
- **Reliability Metrics**: Recovery success rates, error detection rates, false positive rates in quality gates
- **Maintainability Metrics**: Code organization, agent specialization clarity, workflow documentation quality

### Results and Findings

[Exact figures unavailable — see full paper at https://arxiv.org/abs/2608.11965]

The paper provides empirical validation that multi-agent approaches significantly outperform single-agent systems on realistic software engineering workflows. Key findings likely include:

- Recommended phase structures (design → coding → testing)
- Optimal number of specialized roles (approximately 5 core roles sufficient)
- Effectiveness of different coordination patterns
- Integration point identification and handling
- Quality gate placement and effectiveness

## Practical Applications & Use Cases

### Typical Multi-Agent Workflow for Feature Development

```
1. Requirements Phase (CEO + Architect)
   ├─ Parse feature requirements
   ├─ Generate architectural design
   └─ Create implementation plan

2. Implementation Phase (Developers in parallel)
   ├─ Component A development
   ├─ Component B development
   └─ Component C development

3. Integration Phase (Integration lead)
   ├─ Merge components
   ├─ Resolve conflicts
   └─ System-level testing

4. Review & QA Phase (Reviewers + Testers in parallel)
   ├─ Code review by reviewer agent
   ├─ Comprehensive test generation
   └─ Test execution and coverage analysis

5. Refinement Phase (Iterative)
   ├─ Address review comments
   ├─ Fix failing tests
   └─ Return to phase 4 until green
```

### Industry Applications

1. **Bug Fix Automation**: Multi-agent teams analyzing root cause, designing fix, implementing, reviewing, and testing
2. **Feature Implementation**: Parallel development of independent components with automated integration
3. **Codebase Modernization**: Coordinated refactoring across modules with integrated quality gates
4. **Technical Debt Reduction**: Systematic identification and remediation with cross-cutting concern handling

## Insights & Implications

### Design Recommendations

1. **Specialize Agents by Role**: Different reasoning patterns work better for different tasks; single-model generalists underperform
2. **Make State Explicit**: Agents work better with explicit intermediate states vs. implicit context passing
3. **Design for Isolation**: Isolated execution contexts reduce subtle coordination bugs
4. **Implement Quality Gates**: Multi-stage verification catches errors earlier than end-of-pipeline checking
5. **Plan for Iteration**: Real tasks rarely succeed on first pass; design retry and refinement loops

### Architectural Patterns

- **Phase-Based Orchestration**: Waterfall phases with specialized agent teams per phase scale better than ad-hoc coordination
- **Dependency-Aware Planning**: Explicit dependency graphs enable parallel execution and better resource utilization
- **Verification-Driven Recovery**: Executable tests provide clear success criteria and enable automated recovery

### Limitations and Open Questions

- How do these patterns scale to larger team sizes (10+ specialized agents)?
- What are the token efficiency implications of multi-agent approaches?
- How do different LLM models perform in different roles?
- Can agents effectively handle novel or out-of-distribution tasks?
- How do human-in-the-loop systems integrate with autonomous multi-agent teams?

## Code & Resources

### Implementation Frameworks Discussed

- **AutoGen (v0.4+)**: Actor model for multi-agent orchestration with conversation-based coordination
- **MetaGPT**: Software engineering workflow templates with role specialization
- **LangGraph**: Stateful orchestration with checkpointing and complex branching logic
- **Multi-Agent Frameworks**: Custom implementations common for production deployments

### Quick-Start Guidance

For organizations implementing multi-agent software engineering systems:

1. **Start Simple**: Begin with 3-4 core roles (architect, developer, reviewer, tester)
2. **Use Proven Patterns**: Leverage phase-based workflows rather than inventing new coordination schemes
3. **Make State Explicit**: Use structured messages and persistent state for coordination
4. **Measure Early**: Instrument systems to track quality metrics from day one
5. **Plan for Recovery**: Design retry mechanisms and rollback capabilities

## Related Work & Context

### Foundational Work

- **ChatDev** (Wei et al., 2023): Role-based agent design for software engineering tasks
- **MetaGPT** (Hong et al., 2023): Workflow-first approach to multi-agent coordination
- **AutoGen** (Wu et al., 2023): Conversation-based multi-agent framework with customizable agents

### Related Research Areas

- Multi-agent reinforcement learning (MARL) coordination mechanisms
- Workflow orchestration in distributed systems
- Software engineering process automation
- LLM-based code generation and reasoning

### Future Research Directions

1. **Scalability**: How do systems perform with 10+ specialized agents?
2. **Heterogeneous Models**: Optimal model assignments to different agent roles
3. **Learning and Adaptation**: Can multi-agent teams improve through experience?
4. **Human-AI Teaming**: Integration with human decision-making and oversight
5. **Domain-Specific Optimization**: Tailoring architectures to different software engineering domains (web, systems, ML, etc.)

## References & Citation

```bibtex
@article{DeOliveira2026DevelopingLLM,
  author = {De Oliveira, Mariama Celi Serafim and Ibiyo, Motunrayo Osatohanmen and Gianrusso, Marco and Di Sipio, Claudio and Di Ruscio, Davide and Nguyen, Phuong T.},
  title = {Developing LLM-based Multi-Agent Systems in Software Engineering: A Mixed-Method Experience Report},
  journal = {Empirical Software Engineering},
  year = {2026},
  month = {August},
  arxivId = {2608.11965},
  url = {https://arxiv.org/abs/2608.11965}
}
```
