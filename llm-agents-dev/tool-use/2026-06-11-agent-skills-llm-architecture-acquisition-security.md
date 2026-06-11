# Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward

**ArXiv ID:** [2602.12430](https://arxiv.org/abs/2602.12430)  
**Authors:** Renjun Xu, Yang Yan  
**Submitted:** February 2026 (v3 and later revisions through June 2026)  
**Research Focus:** Comprehensive taxonomy and architecture of agent skills for LLM-based systems

## Executive Summary

This systemization of knowledge (SoK) paper provides the first comprehensive framework for understanding agent skills—reusable, composable packages of procedural knowledge that extend LLM capabilities beyond atomic tool calls. Agent skills represent a paradigm shift from monolithic models toward modular, extensible agents that dynamically load capabilities on demand. The paper formalizes skill architecture through the SKILL.md specification, maps the complete skill lifecycle from discovery through retirement, and introduces governance frameworks addressing security, trust, and scalability. By synthesizing research and industry practice, this work establishes conceptual foundations for the emerging agent skills ecosystem while identifying critical open challenges in skill acquisition, composition, and security.

## Problem Statement

The transition from monolithic large language models to modular, skill-equipped agents introduces fundamental challenges that prior research has not systematically addressed:

1. **Architectural Fragmentation**: Existing agent frameworks adopt incompatible skill representations and composition patterns, preventing skill reuse and portability across platforms. There is no standardized way to express, discover, and load procedural knowledge into agents.

2. **Skill Lifecycle Complexity**: Unlike static model weights, skills must be dynamically acquired, evaluated, composed, updated, and eventually retired. Current practice lacks formalized processes for managing these transitions, leading to unmaintained skills and trust issues.

3. **Context Window Pressure**: Agents must access rich, detailed procedural knowledge without exceeding context window limits. Naive skill loading wastes tokens on irrelevant details; selective loading requires sophisticated routing logic.

4. **Security and Trust Gaps**: As skills become commoditized (shared across teams and organizations), supply-chain attacks, privilege escalation, and malicious skill injection emerge as critical threats. Existing governance is ad-hoc.

5. **Acquisition Bottleneck**: Skills are currently authored manually or extracted from code repositories without systematic methodology. As skill ecosystems grow, scalable, safe acquisition mechanisms become essential.

This paper addresses these gaps through a comprehensive framework for skill architecture, acquisition, governance, and composition patterns.

## Core Concepts & Theory

### Agent Skills vs. Tools: Fundamental Distinction

Unlike tools—atomic primitives with fixed interfaces (e.g., API calls) and no internal decision-making—agent skills embody procedural knowledge with:

- **Internal Complexity**: Multi-step workflows with branching logic
- **Compositional Structure**: Skills invoke subtasks, call tools, and compose with other skills
- **Runtime Adaptation**: Execution policies that adapt to context and agent state
- **Explicit Applicability Conditions**: Formal specifications of when a skill is relevant

This distinction separates skills from tools, making them callable modules that operate across tasks rather than one-off utilities.

### Progressive Disclosure Architecture

The defining architectural innovation is three-level progressive disclosure, minimizing context consumption while preserving access to arbitrarily deep procedural knowledge:

```
┌────────────────────────────────────────────────────────────────┐
│                 Progressive Disclosure Hierarchy               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Level 1: Routing Manifest (Lightweight Index)                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ - Skill name, short description (1 sentence)            │ │
│  │ - Security level and human-in-the-loop flag             │ │
│  │ - Semantic tags and category                            │ │
│  │ - Applicability conditions (brief)                      │ │
│  │ Size: ~200 bytes per skill                              │ │
│  │ Usage: Agent initialization, semantic routing           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  Level 2: Executable Instructions (Skill Content)              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ - SKILL.md Markdown body with step-by-step guidance     │ │
│  │ - Input-output specifications                           │ │
│  │ - Execution policies and error handling                 │ │
│  │ - Illustrative examples                                 │ │
│  │ Size: ~1-5KB per skill                                  │ │
│  │ Usage: Agent execution when skill is selected           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  Level 3: Technical Appendices (Deep References)               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ - Full API documentation                                │ │
│  │ - Code examples and edge cases                          │ │
│  │ - Performance characteristics and limitations           │ │
│  │ - Integration with other skills                         │ │
│  │ Size: ~5-20KB per skill                                 │ │
│  │ Usage: On-demand, when agent encounters novel scenarios │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

This architecture achieves:
- **Efficiency**: Most skill invocations only require Level 1-2 (400 bytes to 5KB)
- **Completeness**: Agents can access detailed information (Level 3) when needed
- **Scalability**: Thousands of skills can be available without overwhelming agent context

### SKILL.md Specification

The community has converged on SKILL.md as the portable standard for skill definition:

```yaml
---
# YAML Frontmatter: Metadata for routing and composition
name: "Refactor Function to Pure FP Style"
description: "Transform an imperative function into functional programming style with immutability"
category: "code-refactoring"
tags: [functional-programming, refactoring, code-quality]
version: "1.2.0"
security_level: "low"
human_in_the_loop: false
applicability_conditions:
  - "Task involves imperative code transformation"
  - "Target language supports functional patterns"
dependencies:
  - "code-analysis"
  - "syntax-understanding"
authors: ["engineering-team"]
created_date: "2025-10-15"
last_updated: "2026-05-20"
---

# Markdown Body: Executable Instructions for Agent

## Overview
Transform imperative code into functional programming style...

## Step 1: Analyze Current Implementation
- Identify mutable variables and state changes
- Map imperative logic to functional equivalents
- Document preconditions and invariants

## Step 2: Design Functional Alternative
- Use immutable data structures
- Replace loops with map/reduce/filter operations
- Implement pure functions without side effects

## Step 3: Implement and Test
- Write new functional implementation
- Ensure equivalent behavior with comprehensive tests
- Document performance characteristics
```

Key components:
- **YAML Metadata**: Enables routing, composition, and governance
- **Markdown Instructions**: Natural language guidance for LLM agents
- **Portable Format**: Human-readable, version-controllable, framework-agnostic

### Skill Lifecycle Stages

Skills progress through seven distinct phases:

```
Discovery → Practice → Distillation → Storage → Composition → Evaluation → Retirement
   ↓          ↓           ↓            ↓          ↓            ↓            ↓
 Need        Learn      Refine      Index    Integrate    Monitor      Remove
 identified  Skill      Quality     & Sync   w/ Others    & Improve   Obsolete
```

**Discovery**: Identify needed capabilities through usage patterns  
**Practice**: Initial skill development and testing with limited scope  
**Distillation**: Refine skill based on usage feedback and edge cases  
**Storage**: Index skill in ecosystem with rich metadata  
**Composition**: Integrate with other skills; establish dependencies  
**Evaluation**: Monitor skill usage, performance, and user satisfaction  
**Retirement**: Deprecate outdated skills; document successor patterns  

### Four Design Patterns for Skill Packaging

1. **Metadata-Driven Progressive Disclosure** (described above): Skill metadata drives routing; content loads progressively

2. **Executable Code Skills**: Skills encapsulating actual code (Python, shell, etc.) that agents execute directly
   - Advantages: Precise semantics, reproducible execution
   - Tradeoffs: Language lock-in, security validation complexity

3. **Self-Evolving Skill Libraries**: Skills that improve through feedback and agent interactions
   - Agents iteratively refine prompts and parameters based on outcomes
   - Requires formal evaluation criteria and rollback mechanisms

4. **Marketplace Distribution**: Skills distributed via curated registries with governance
   - Enables third-party skill contribution (Atlassian, Figma, Stripe, Notion)
   - Requires trust mechanisms and supply-chain security

## Main Ideas & Contributions

### 1. Formalized Skill Architecture Framework

The paper establishes the first comprehensive skill architecture specification, distinguishing skills from tools and defining how procedural knowledge is packaged, versioned, and discovered. The SKILL.md standard provides portable skill definitions that transcend framework boundaries, enabling skill ecosystem growth.

### 2. Complete Skill Lifecycle Formalization

Rather than treating skills as static artifacts, the paper maps seven distinct lifecycle stages from discovery through retirement, providing governance checkpoints at each phase. This lifecycle thinking enables systematic skill curation, deprecation, and evolution.

### 3. Progressive Disclosure for Context Efficiency

The three-level disclosure pattern solves the context window problem: agents can perform semantic routing and basic execution with ~200 bytes, load full instructions with ~5KB, or access deep references on-demand. This architecture enables thousand-skill ecosystems within practical token budgets.

### 4. Security & Trust Governance Framework

The paper introduces Skill Trust and Lifecycle Governance with four sequential gates:
- **G1 (Static Analysis)**: Flag known vulnerability signatures
- **G2 (Semantic Classification)**: Detect intent mismatches between declared purpose and implementation
- **G3 (Functional Testing)**: Validate skill behavior against specifications
- **G4 (Integration Testing)**: Ensure safe composition with other skills

This defense-in-depth approach addresses supply-chain risks as skills become commoditized.

### 5. Four Skill Acquisition Pathways

The paper identifies complementary acquisition approaches:

- **Reinforcement Learning with Skill Libraries**: Train agents to select and adapt existing skills
- **Autonomous Skill Discovery**: Systems like SEAgent mine codebases to identify common patterns and synthesize skills
- **Compositional Synthesis**: Combine existing skills to create new capabilities
- **Human Authorship**: Domain experts write skills for specialized domains

Each pathway has different scalability, quality, and human-labor tradeoffs.

## Methodology & Implementation

### Skill Ecosystem Survey

The paper synthesizes findings from:
- **Industry Practice**: Anthropic Skills with partner implementations (Atlassian, Figma, Canva, Stripe, Notion)
- **Research Systems**: SEAgent, skill mining frameworks, autonomous skill discovery
- **Community Evolution**: SKILL.md adoption across frontier model providers

### Evaluation Framework

**Architectural Evaluation**:
- Context efficiency: bytes required for routing vs. full execution
- Latency impact: overhead of skill loading and selection
- Coverage: breadth of tasks addressable with given skill set

**Lifecycle Evaluation**:
- Time from need identification to skill deployment
- Maintenance burden (skill updates, deprecations)
- Obsolescence rate and skill longevity

**Security Evaluation**:
- Supply-chain attack surface
- Intent-implementation mismatches detected
- Safe composition guarantees

### Key Findings

**Architectural Efficiency**: Progressive disclosure architecture significantly reduces skill-loading overhead compared to full-content approaches, enabling skill discovery across large skill repositories. [Exact figures unavailable — see full paper for detailed latency measurements]

**Ecosystem Growth**: Within four months of Anthropic's October 2025 launch of Agent Skills, 62,000 GitHub stars accumulated, indicating rapid adoption signal. Partner-built skills from major platforms (Atlassian, Figma, etc.) entered curated registries.

**Governance Effectiveness**: The four-gate governance framework effectively identifies common failure modes across static analysis, semantic classification, and functional testing phases. [Specific metrics and effectiveness percentages unavailable — see full paper for detailed evaluation results]

**Skill Acquisition Tradeoffs**: 
- Autonomous discovery is fastest but requires seed skills and careful validation
- RL-based adaptation enables skill improvement but demands clear reward specifications
- Human authorship is slowest but highest quality for specialized domains

## Practical Applications & Use Cases

### Industry Adoption: Atlassian, Figma, Stripe

Leading platforms have integrated skills into their APIs:
- **Atlassian**: Jira and Confluence skills for automated issue triage and documentation
- **Figma**: Design automation skills for layout, color harmony, accessibility
- **Stripe**: Payment automation skills for recurring billing, tax compliance

These integrations demonstrate that modular skill packaging enables broader LLM integration into existing tools.

### Skill Composition for Complex Workflows

Rather than monolithic agents, teams combine skills:
- **Code Review Workflow**: Compose "code-style-check" + "security-vulnerability-scan" + "performance-profiling" + "test-coverage-analysis"
- **Documentation Generation**: "extract-code-structure" → "write-docstrings" → "generate-readme" → "validate-examples"
- **Refactoring Pipeline**: "identify-refactoring-opportunity" → "generate-refactored-code" → "test-equivalence" → "safe-merge"

### Self-Evolving Skills

Skills that learn from experience:
- Performance optimization skill that learns cost-reduction techniques from successful deployments
- Test generation skill that improves coverage by analyzing failed edge cases
- Documentation skill that adapts to project-specific conventions

## Insights & Implications

### Impact on Agent-Driven Development

1. **Shift from Monolithic to Modular**: Rather than building larger models, teams build skill ecosystems. This distributes development effort and enables specialization.

2. **Commodification of Procedural Knowledge**: Procedural expertise (how to do code review, how to write tests, how to refactor) becomes packageable, shareable, and evaluable—not locked in model weights.

3. **Framework Agnosticism**: SKILL.md portability means skills written for one framework (AutoGen, LangGraph, etc.) work elsewhere, reducing platform lock-in.

4. **Governance Becomes Critical**: As skills scale from dozens to thousands, formal governance (versioning, deprecation, security gates) becomes essential infrastructure, not nice-to-have.

### Limitations & Open Challenges

1. **Skill Composition Semantics**: How do agents efficiently compose thousands of skills while handling interdependencies, conflicts, and coordination requirements? Current approaches are manually-designed; automatic composition optimization remains unsolved.

2. **Quality Assurance at Scale**: How to maintain skill quality as ecosystems grow beyond expert curation? Automated testing and formal verification are promising but not yet scaled to production skill directories.

3. **Security Guarantees**: Rejection sampling in SEVerA-style approaches provides guarantees for specific skills, but composition guarantees (safety properties preserved under skill combination) remain open.

4. **Generalization & Transfer**: A skill refined on one codebase may perform poorly on another. Transfer learning for skills is an underexplored research area.

5. **Lifecycle Automation**: Most skill lifecycle stages (discovery, distillation, retirement) are still manual. Automating these stages would unlock faster skill ecosystem evolution.

## Code & Resources

### SKILL.md Standard

**Specification**: [SKILL.md Format](https://github.com/anthropics/skills) — Portable skill definition standard

### Skill Repositories & Registries

- **Anthropic Skills**: [anthropics/skills repository](https://github.com/anthropics/skills) — Curated collection
- **SkillRet Benchmark**: Large-scale skill retrieval dataset (17,810 public agent skills) for evaluating skill discovery and composition
- **Partner Integrations**: Skills from Atlassian, Figma, Canva, Stripe, Notion in curated directories

### Key Libraries & Frameworks

- **Model Context Protocol (MCP)**: Provides the "how to connect" infrastructure; skills provide the "what to do"
- **AutoGen**: Multi-agent framework with skill support (v0.4+)
- **LangGraph**: Stateful orchestration compatible with skill definitions

### Security & Governance Tools

- **Static Analysis Tools**: Flag vulnerability signatures in skill implementations
- **Semantic Validators**: Detect intent-implementation mismatches
- **Functional Test Harnesses**: Validate skill behavior before deployment
- **Integration Test Frameworks**: Ensure safe skill composition

## Related Work & Context

### Foundational Concepts

- **Prompt Engineering & Few-Shot Learning**: Precursors to skills; less structured than formal skill definitions
- **Program Synthesis & Code Generation**: Addresses how to automatically create skillful code
- **Tool Use in LLMs**: Tools are atomic; skills add compositionality and state
- **Multi-Agent Coordination**: Skills enable agents to specialize; coordination determines team performance

### Adjacent Research

- **SEAgent**: Autonomous skill discovery from codebases
- **SEVerA**: Formal verification of self-evolving agents (uses FGGM for skill safety)
- **AutoGen & MetaGPT**: Frameworks that can represent and compose skills

### Future Research Directions

1. **Automatic Skill Composition**: Can agents automatically discover and chain skills to solve novel problems without human choreography?

2. **Skill Transfer Learning**: How to adapt skills learned on one codebase to new domains, teams, or codebases?

3. **Compositional Verification**: Formal methods guaranteeing that composed skills maintain safety and correctness properties.

4. **Emergent Skill Evolution**: Can skill ecosystems exhibit emergent properties—e.g., self-improving through feedback without explicit human updates?

5. **Trustworthy Skill Marketplaces**: How to build skill registries where third-party skills are trustworthy and transparent?

---

**Citation**: Xu & Yan, "Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward," arXiv:2602.12430, 2026.

**Note**: This paper was authored by leading researchers and updated through June 2026 (v4), incorporating industry developments and recent advances in agent skill practice.
