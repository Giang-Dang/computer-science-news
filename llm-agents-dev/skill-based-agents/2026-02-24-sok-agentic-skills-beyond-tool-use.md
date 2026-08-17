# SoK: Agentic Skills -- Beyond Tool Use in LLM Agents

**ArXiv ID**: [2602.20867](https://arxiv.org/abs/2602.20867)

**Authors**: Yanna Jiang, Delong Li, Haiyu Deng, Baihe Ma, Xu Wang, Qin Wang, Guangsheng Yu

**Submitted**: February 24, 2026

**Affiliations**: University of Technology Sydney, CSIRO Data61

---

## Executive Summary

This systematization of knowledge (SoK) paper establishes agentic skills as a fundamental primitive beyond simple tool use in LLM-based agent systems. Rather than treating agents as one-shot tool callers, agentic skills are reusable procedural capabilities that encapsulate knowledge, execution policies, and termination criteria—enabling reliable long-horizon workflows. The paper provides a comprehensive taxonomy of the skill lifecycle and seven design patterns for implementing skills in practice, directly advancing the field's understanding of how to architect scalable, composable multi-agent systems for complex development tasks.

---

## Problem Statement

### Development Automation Challenges

Large language model agents have shown promise in automating software development tasks, but current approaches face critical limitations:

1. **One-shot Tool Invocation**: Most existing systems treat tool use as atomic operations without feedback loops or adaptive correction
2. **Task Complexity**: Long-horizon development tasks (e.g., full system design, multi-stage testing, cross-component refactoring) require coordination beyond single function calls
3. **Knowledge Encapsulation**: Best practices, error handling procedures, and domain-specific workflows are scattered across codebases and documentation, not accessible to agents
4. **Composability Gap**: Existing frameworks lack abstractions for composing reusable agent behaviors across different contexts and teams

### Research Gap

Prior work has focused on:
- Tool frameworks (single-tool or limited tool ensembles)
- Plan-and-execute architectures (flat, non-adaptive workflows)
- LLM prompting tricks and in-context learning

But there was no principled, systematic characterization of how procedural knowledge should be packaged, discovered, executed, evaluated, and evolved within agentic systems—the gap this SoK paper fills.

---

## Core Concepts & Theory

### What Are Agentic Skills?

An **agentic skill** is a reusable procedural capability consisting of:

```
Skill = {
  procedure: executable instructions (prompts, code, workflows),
  metadata: discovery tags, applicability conditions,
  execution_policy: when/how to invoke, retry logic,
  termination_criteria: stopping conditions, convergence checks,
  interface: input/output contracts, error handling,
  constraints: resource limits, compliance boundaries
}
```

**Key Distinction from Tools**: Tools are stateless callables (e.g., "grep for this pattern"). Skills are stateful, adaptive procedures with built-in policies and long-horizon behavior (e.g., "systematically refactor this module and verify correctness").

### The Skill Lifecycle: Seven Phases

The paper maps skills across a complete lifecycle:

```
┌─────────────────────────────────────────────────────────────┐
│ SKILL LIFECYCLE PHASES                                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. DISCOVERY                                               │
│     └─ Identify patterns, failures, bottlenecks that        │
│        justify encapsulating behavior as a reusable skill   │
│                                                               │
│  2. PRACTICE / REFINEMENT                                   │
│     └─ Iteratively improve candidate skills through trial,  │
│        reflection, and external feedback                    │
│                                                               │
│  3. DISTILLATION                                            │
│     └─ Extract stable, generalizable procedure from         │
│        trajectories; package with metadata and constraints  │
│                                                               │
│  4. STORAGE                                                 │
│     └─ Persist skills in versioned repositories or          │
│        marketplace registries with clear governance         │
│                                                               │
│  5. COMPOSITION                                             │
│     └─ Combine skills into larger workflows; handle         │
│        dependencies and sequencing                          │
│                                                               │
│  6. EXECUTION                                               │
│     └─ Invoke skills in agent workflows with runtime        │
│        binding and context injection                        │
│                                                               │
│  7. EVALUATION & UPDATE                                     │
│     └─ Monitor performance, detect drift/failures, revise   │
│        or retire skills as requirements evolve              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Seven Design Patterns for Skill Implementation

The paper identifies empirically grounded patterns across real agent systems:

1. **Metadata-Driven Progressive Disclosure**
   - Skills expose capabilities through structured metadata (applicability conditions, requirements)
   - Agents query metadata to discover relevant skills before invocation
   - Enables efficient skill selection in large marketplaces

2. **Executable Code Skills**
   - Skill logic implemented as compiled or interpreted code (Python, JavaScript)
   - Direct execution without LLM interpretation; highest performance and determinism
   - Trade-off: requires stronger assumptions about execution environment

3. **Prompt-Based Procedural Skills**
   - Skill logic expressed as prompting instructions and reasoning chains
   - Flexible across different LLM backends; supports in-context learning
   - Trade-off: higher latency, potential inconsistency

4. **Hierarchical Skill Decomposition**
   - Complex skills broken into sub-skills with clear composition boundaries
   - Enables reuse at multiple levels of abstraction
   - Supports gradual skill refinement and testing

5. **Self-Evolving Skill Libraries**
   - Skills automatically capture execution traces and adapt based on failure patterns
   - Online learning: successful trajectories reinforce policies; failures trigger revision
   - Applicable when agents operate in relatively stable task distributions

6. **Skill Marketplace and Governance**
   - Centralized registry for publishing, discovering, versioning skills
   - Governance policies (permissions, resource quotas, audit trails) for enterprise adoption
   - Enables community-driven skill sharing and reuse across organizations

7. **Hybrid Skill Orchestration**
   - Skills combine prompting, code execution, and external tool invocation
   - Agents select execution modality based on task requirements
   - Balances flexibility with performance

### Multi-Agent Topologies with Skills

Common skill-enabled coordination patterns:

```
HIERARCHICAL SKILL COMPOSITION

    ┌──────────────────────────────────┐
    │  Orchestrator Agent              │
    │  - Routes tasks to specialists   │
    │  - Composes sub-skill outputs    │
    └────────────┬───────────┬─────────┘
                 │           │
        ┌────────▼─┐  ┌─────▼────────┐
        │ Specialist A│  │ Specialist B │
        │ Code Review │  │ Code Gen    │
        │ Skills      │  │ Skills      │
        └────────────┘  └─────────────┘

SUB-SKILL DEPENDENCIES

    Refactor Module
    ├─ Analyze Code Structure (skill)
    ├─ Generate Refactored Code (skill)
    ├─ Run Tests (skill)
    └─ Merge & Commit (skill)
```

---

## Main Ideas & Contributions

### 1. Skill-Centric Agent Architecture

**Novel Contribution**: Positioning skills as first-class abstractions, parallel to agents and tools, rather than treating them as lightweight wrappers around function calls.

**Key Insight**: Development automation requires capabilities that are:
- **Stateful**: maintain context across multiple invocations
- **Adaptive**: learn from execution outcomes and adjust behavior
- **Composable**: combine with other skills to solve complex tasks
- **Governable**: subject to permissions, audit, and resource constraints

### 2. Seven-Phase Lifecycle Framework

Rather than static skill definitions, skills evolve through a complete lifecycle. This enables:
- **Continuous Improvement**: skills improve over time through practice and reflection
- **Drift Detection**: monitoring systems identify when skills degrade as environments change
- **Knowledge Transfer**: successful skills can be distilled and shared across teams
- **Community Evolution**: marketplace mechanisms enable collective skill refinement

### 3. Design Patterns as Implementation Guidance

The seven patterns provide architects with concrete options for skill implementation:
- **Practitioners** choose patterns based on their development constraints (latency, determinism, flexibility)
- **Researchers** can innovate by inventing new patterns or hybrid combinations
- **Standardization**: patterns make skill systems more interoperable

### 4. Beyond Tool Use: Procedural Knowledge

**Fundamental Distinction**:
- **Tool Use**: "Call endpoint X with parameters Y" (atomic, stateless)
- **Skills**: "Systematically refactor this module, run tests after each change, and verify no regressions" (procedural, adaptive, multi-step)

Skills capture procedural knowledge that would otherwise require LLMs to reason about step-by-step, reducing latency and improving reliability.

---

## Methodology & Implementation

### Literature Review & Empirical Study

The paper is a **systematization of knowledge (SoK)**, not an empirical validation of a single system. The authors:

1. Surveyed 50+ recent agent systems and frameworks (AutoGen, LangGraph, CrewAI, etc.)
2. Analyzed open-source agent codebases to extract actual skill patterns
3. Interviewed practitioners building multi-agent systems in industry

### Case Studies

The paper includes case studies from real deployed systems:
- **Code Review Workflows**: Skills for PR analysis, test coverage verification, compliance checking
- **DevOps Automation**: Skills for deployment verification, rollback procedures, incident response
- **Data Pipeline Engineering**: Skills for ETL validation, quality checks, error recovery

### Implementation Frameworks Referenced

- **AutoGen** (Microsoft): Multi-agent conversation framework with skill composability in v0.4+
- **LangGraph** (LangChain): Stateful skill execution with checkpointing and branching
- **CrewAI**: Role-based agent framework with skill assignment and routing
- **Ray AIR**: Distributed agent training and skill evolution

### Results: Landscape Characterization

The SoK does not report quantitative metrics but rather provides:

1. **Taxonomy Completeness**: Covers 7 design patterns with examples from 20+ deployed systems
2. **Lifecycle Coverage**: Each phase (discovery through update) documented with at least 3 different implementation approaches
3. **Open Problems**: Identifies 12 research challenges (skill composability verification, marketplace governance, skill versioning)

---

## Practical Applications & Use Cases

### 1. Code Quality Automation

**Multi-Skill Workflow for Continuous Integration**:

```
GitHub Webhook (PR opened)
│
└─→ Code Analysis Skill
    ├─ Parse AST, identify hotspots
    ├─ Store findings
    │
    └─→ Code Review Skill
        ├─ Check against coding standards
        ├─ Identify potential bugs
        │
        └─→ Test Generation Skill
            ├─ Create test cases for risky code
            ├─ Run tests, capture coverage
            │
            └─→ Report Aggregation Skill
                └─ Synthesize findings into PR comment
```

**Benefit**: Skills are versioned independently; teams can update review rules without affecting generation logic.

### 2. Incident Response & Debugging

**Skill Composition for Autonomous Debugging**:

- **Diagnosis Skill**: Parse logs, identify error patterns, narrow root cause
- **Hypothesis Testing Skill**: Generate hypotheses, run diagnostic queries
- **Knowledge Lookup Skill**: Retrieve runbooks, previous incidents, architectural docs
- **Remediation Skill**: Apply fixes, monitor recovery, rollback if needed

**Advantage**: Reusable across different incident types; skills learn from success/failure patterns.

### 3. DevOps & Infrastructure Automation

**Skills for Deployment Verification**:
- Pre-deployment checks (security scanning, dependency verification)
- Canary deployment monitoring (gradual rollout with health checks)
- Rollback orchestration (coordinated service retirement, data migration)
- Post-deployment validation (smoke tests, integration tests, user acceptance tests)

Each skill can be developed, tested, and versioned independently while being composed into complex deployment workflows.

### 4. Data Engineering & ML Pipelines

**Skill-Based ETL Orchestration**:
- Data Quality Skill: validation rules, schema checking, anomaly detection
- Transformation Skill: data cleaning, feature engineering, aggregation
- Integration Skill: joins with external data sources, enrichment
- Publishing Skill: format output, update downstream systems, notify consumers

**Scalability**: Skills can be distributed across workers; each skill execution is independently monitored and logged.

---

## Insights & Implications

### Advancement in Autonomous Development Systems

1. **Modularity at New Level**: Moving from function-call modularity to procedural-knowledge modularity enables larger composable systems
2. **Reliability Through Specification**: Explicit execution policies and termination criteria (vs. implicit LLM reasoning) improves predictability
3. **Governance Enablement**: Marketplace and versioning patterns make agent systems suitable for enterprise environments with compliance requirements

### Impact on Agent-Driven Development

- **Faster Onboarding**: Teams can assemble solutions from existing skills without understanding every implementation detail
- **Continuous Improvement**: Skills improve through practice; teams don't need to redesign workflows from scratch
- **Cross-Organization Reuse**: Skill marketplaces enable knowledge sharing across companies (analogous to open-source packages)

### Limitations & Open Research Questions

1. **Skill Composability Verification**: How do we verify that composed skills produce correct results? Current approaches rely on execution testing.
2. **Marketplace Governance**: How should permissions, resource quotas, and trust be managed in shared skill registries?
3. **Skill Versioning & Compatibility**: How do breaking changes in skills propagate to dependent workflows?
4. **Skill Discovery at Scale**: How do agents efficiently find the right skills among thousands of candidates?
5. **Skill Evolution Safety**: How do we ensure self-evolving skills don't introduce security vulnerabilities or performance regressions?
6. **Cost Optimization**: Which skills should be executed where (LLM vs. code vs. external tools) to minimize cost?

### Relevance to Agent-Driven Development

This paper provides the conceptual foundation for treating agent systems as architectures, not just prompt templates. Organizations building internal AI coding assistants should:
- Map their development workflows to skill abstractions
- Invest in governance (versioning, permissions, audit)
- Build skill discovery mechanisms as systems scale
- Create feedback loops to continuously improve skills

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [SoK: Agentic Skills -- Beyond Tool Use in LLM Agents](https://arxiv.org/abs/2602.20867)
- **Paper PDF**: [https://arxiv.org/pdf/2602.20867](https://arxiv.org/pdf/2602.20867)
- **HTML Version**: [https://arxiv.org/html/2602.20867v1](https://arxiv.org/html/2602.20867v1)

### Related Frameworks & Implementations

- **[AutoGen](https://microsoft.github.io/autogen/)** (Microsoft) - Multi-agent orchestration with skill-like composability
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** (LangChain) - Stateful skill execution with persistence
- **[CrewAI](https://crewai.com/)** - Role-based agent framework with skill assignment
- **[Ray AIR](https://docs.ray.io/en/latest/air/air.html)** (Ray) - Distributed agent training and evaluation

### Skill Implementation Examples

From deployed systems:
- **GitHub-based**: AutoGen examples in the [MS research repository](https://github.com/microsoft/autogen)
- **LangChain**: Skill composition examples in [LangChain documentation](https://python.langchain.com/)
- **Industry**: Anthropic Claude uses skill-like abstractions internally for reliable tool use

---

## Related Work & Context

### Foundational Work

1. **Tool Use in LLMs** ([Schick et al., 2024](https://arxiv.org/abs/2302.04761))
   - Early work on function calling and tool selection
   - This SoK extends tool use to stateful, adaptive procedures

2. **Agent Frameworks** (AutoGen [Du et al., 2023](https://arxiv.org/abs/2308.08155), [2024](https://arxiv.org/abs/2404.00025))
   - Pioneered multi-agent conversation and orchestration
   - This paper systematizes the skill abstractions within such frameworks

3. **Program Synthesis** ([Ellis et al., 2018](https://arxiv.org/abs/1805.03677))
   - Skills as learned program fragments; this work extends to LLM-based procedural knowledge

### Related Recent Work

- **[SoK: Agentic Skills – Beyond Tool Use](https://arxiv.org/html/2602.20867v1)** (concurrent work)
- **[Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills](https://arxiv.org/abs/2607.09065)** - Marketplace implementation strategies
- **[SkillWiki: A Living Knowledge Infrastructure for Agent Skills](https://arxiv.org/abs/2606.16523)** - Skill documentation and discovery
- **[SkillRet: A Large-Scale Benchmark for Skill Retrieval in LLM Agents](https://arxiv.org/abs/2605.05726)** - Evaluating skill discovery

### Future Research Directions

1. **Formal Verification of Skill Composition**: Can we prove properties of composed skills?
2. **Automated Skill Generation**: Automatically extract skills from codebases or from agent trajectories
3. **Skill Marketplace Economics**: How should skills be priced and traded?
4. **Multi-Organization Skill Networks**: Federated skill discovery and composition across organizations
5. **Skill-based Agent Testing**: New testing frameworks specifically for skill-composed systems

---

## Summary

**SoK: Agentic Skills** provides the theoretical foundation and practical taxonomy for moving beyond simple tool use toward sophisticated, reusable procedural capabilities in LLM-based agent systems. By systematizing a complete lifecycle (discovery through evolution) and identifying seven concrete design patterns, this work enables practitioners to architect scalable, composable, and governable multi-agent systems for complex software development tasks.

The paper's key insight—that long-horizon development automation requires stateful, adaptive procedural knowledge, not just stateless function calls—elevates agent system design from ad hoc prompting to principled architecture. Organizations adopting agent-driven development should use this SoK as a guide for structuring their agent systems around reusable skills, implementing marketplace governance, and building continuous improvement pipelines.
