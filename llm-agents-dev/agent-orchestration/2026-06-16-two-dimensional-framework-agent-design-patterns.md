# A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function × Execution Topology

**Authors:** Jia Huang, Joey Tianyi Zhou  
**Affiliation:** Agency for Science, Technology and Research (A*STAR), Singapore; Centre for Frontier AI Research (CFAR)  
**ArXiv ID:** 2605.13850  
**Submitted:** March 2026 | Revised: May 2026  
**Status:** Recent (2 weeks old)

## Executive Summary

This paper introduces a comprehensive two-dimensional framework for classifying AI agent design patterns by combining cognitive function dimensions (what the agent does) with execution topology dimensions (how data flows). The framework addresses a critical gap in existing agent architecture literature where industry guides focus solely on execution topology while cognitive science surveys emphasize cognitive function. By revealing that the same topology can implement fundamentally different patterns with distinct failure modes and design trade-offs, this work provides essential guidance for practitioners designing robust, production-grade agent systems.

## Problem Statement

### The Gap in Agent Architecture Understanding

Current frameworks for LLM-based agent architectures suffer from a critical limitation: they describe systems from only a single perspective:

- **Industry guides** (Anthropic, Google, LangChain) focus on **execution topology** — how data flows between components and what computational patterns are used
- **Cognitive science surveys** focus on **cognitive function** — the high-level capabilities and processes the agent employs (reasoning, memory, reflection, etc.)

### The Ambiguity Problem

Neither dimension alone disambiguates architecturally distinct systems. A concrete example: the same **Orchestrator-Workers topology** can implement three fundamentally different patterns:
1. **Plan-and-Execute:** Agent plans comprehensively, then delegates execution
2. **Hierarchical Delegation:** Agent delegates planning and execution hierarchically
3. **Adversarial Verification:** Agent generates solutions and employs critical reviewers

These three patterns have **fundamentally different failure modes** and **design trade-offs**, yet appear identical when described by execution topology alone.

### Research Gap

Practitioners lack a unified, systematic framework to understand and reason about agent design patterns. This leads to:
- Misaligned expectations about agent capabilities and failure modes
- Suboptimal architecture choices for specific use cases
- Difficulty comparing agent designs across different frameworks and implementations

## Core Concepts & Theory

### Two-Dimensional Classification Framework

The framework combines two orthogonal dimensions:

#### 1. Cognitive Function Axis (7 Categories)

Describes **what cognitive capabilities** the agent exhibits:

- **Perception:** Agent's ability to observe and interpret external inputs
- **Memory:** Mechanisms for storing, retrieving, and managing information
- **Reasoning:** Capability to think through problems, plan, and make decisions
- **Action:** Ability to execute tasks and interact with the environment
- **Reflection:** Capacity to evaluate outcomes and adapt behavior
- **Collaboration:** Ability to coordinate with other agents or humans
- **Governance:** Mechanisms for control, policy enforcement, and oversight

#### 2. Execution Topology Axis (6 Structural Categories)

Describes **how components are organized and communicate:**

Examples include:
- **Monolithic Agent:** Single agent handles all cognitive functions
- **Orchestrator-Workers:** Central orchestrator coordinates specialized worker agents
- **Peer-to-Peer:** Agents coordinate horizontally without central control
- **Hierarchical:** Multi-level delegation and coordination structure
- **Pipeline:** Sequential flow of data through specialized components
- **Reactive:** Event-driven, minimal planning or memory

### Key Design Insight

The same execution topology can implement different cognitive patterns. For example, an **Orchestrator-Workers topology** can emphasize different cognitive functions:

```
Topology: Orchestrator-Workers
           (Same Physical Architecture)
                    |
         ___________+___________
         |           |         |
    Plan-Execute  Hierarchical Adversarial
    (upfront       Delegation  Verification
     planning)     (distributed (multi-stage
                   planning)    checking)
         
    Different failure modes:
    - Plan-Execute: brittle to plan errors
    - Hierarchical: communication overhead
    - Adversarial: high cost, slower
```

### Design Space Navigation

The two-dimensional framework enables practitioners to:
1. **Identify trade-offs** explicitly before implementation
2. **Classify existing systems** systematically
3. **Design architectures** by consciously choosing cognitive function and topology combinations
4. **Anticipate failure modes** specific to their chosen pattern
5. **Compare alternatives** across dimensions

## Main Ideas & Contributions

### 1. Unified Classification System

The paper's primary contribution is a comprehensive, two-dimensional taxonomy that unifies previously fragmented approaches to agent architecture. This enables:
- Systematic comparison of design choices
- Clear articulation of what each pattern optimizes for
- Explicit discussion of trade-offs and failure modes

### 2. Disambiguation of Equivalent-Appearing Architectures

By revealing that the same topology can support different cognitive patterns, the framework prevents practitioners from assuming architectural equivalence. This is critical for:
- Selecting appropriate failure mitigation strategies
- Understanding where different agent systems will likely fail
- Debugging unexpected behaviors

### 3. Comprehensive Design Pattern Catalog

The paper documents 28 distinct design patterns across the two-dimensional space, providing a comprehensive reference for:
- Practitioners choosing agent architectures
- Researchers comparing agent systems
- Educators teaching agent design

### 4. Cognitive Function Formalization

The explicit enumeration of seven cognitive function categories provides a mental model for designing agents with specific capabilities. This is useful for:
- Systematically assessing what capabilities an agent needs
- Identifying missing functions in existing architectures
- Planning incremental capability additions

## Methodology & Implementation

### Framework Development

The authors developed the framework through:
1. **Literature review** of cognitive science, AI architecture literature, and industry practices
2. **Analysis of existing frameworks** from LangChain, Anthropic guides, academic papers
3. **Pattern extraction** and systematic categorization
4. **Validation** against diverse existing agent implementations

### Application to Real Systems

The framework is validated through analysis of production and research agent systems, demonstrating its utility for:
- Classifying complex systems (e.g., multi-team, multi-stage agent systems)
- Identifying which aspects of a system match each dimension
- Revealing architectural inconsistencies or suboptimal choices

### Results

The analysis produced:
- **7 cognitive function categories** with clear definitions and examples
- **6 execution topology categories** with distinctive characteristics
- **28 distinct design patterns** in the combined space
- **Clear failure mode mappings** for each pattern class

[Exact figures and additional metrics unavailable — see full paper]

### Agent Topologies and Workflows: ASCII Diagrams

#### Pattern 1: Plan-and-Execute (Orchestrator-Workers)

```
┌─────────────────────────────────────────────┐
│           PLANNING PHASE                    │
│  ┌─────────────────────────────────────┐   │
│  │  Orchestrator Agent                 │   │
│  │  - Analyze requirements             │   │
│  │  - Decompose into sub-tasks         │   │
│  │  - Create comprehensive plan        │   │
│  └──────────────┬──────────────────────┘   │
│                 │ (Structured plan)         │
└─────────────────┼─────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│           EXECUTION PHASE                   │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │
│  │Task 1│  │Task 2│  │Task 3│  │Task N│   │
│  │Worker│  │Worker│  │Worker│  │Worker│   │
│  └──────┘  └──────┘  └──────┘  └──────┘   │
│     │         │         │         │        │
│     └─────────┴─────────┴─────────┘        │
│                  │                         │
│            Aggregate results               │
└────────────────────────────────────────────┘

Failure Mode: Brittle to planning errors
             Information loss in plan decomposition
```

#### Pattern 2: Hierarchical Delegation

```
┌────────────────────────────────────────┐
│      Top-Level Orchestrator            │
│   (High-level goal understanding)      │
│          │         │         │         │
└──────────┼─────────┼─────────┼─────────┘
           │         │         │
    ┌──────▼──┐ ┌────▼────┐ ┌─▼────────┐
    │Sub-Team │ │Sub-Team │ │Sub-Team  │
    │Manager 1│ │Manager 2│ │Manager N │
    │   │ │   │ │   │    │ │   │ │    │
    └───┼─┼───┘ └───┼────┘ └───┼─┼────┘
        │ │         │          │ │
    ┌───▼─▼──┬───────▼──┬──────▼─▼──┐
    │ Worker │ Worker   │ Worker    │
    │ 1a-1c  │ 2a-2c    │ 3a-3c    │
    └────────┴──────────┴──────────┘

Failure Mode: Communication overhead across levels
             Coordination complexity
             Potential information loss at each level
```

#### Pattern 3: Adversarial Verification

```
Solution Generation Phase:
┌──────────────────────────┐
│   Generator Agent        │
│   - Proposes solutions   │
│   - Generates candidates │
└──────────┬───────────────┘
           │
           ▼
        Multiple
       Candidate
       Solutions
           │
           ▼
┌──────────────────────────────────────────┐
│    Reviewer/Critic Agents (Parallel)     │
│  ┌──────────────────────────────────┐   │
│  │ Reviewer 1: Logic Check          │   │
│  │ Reviewer 2: Edge Cases           │   │
│  │ Reviewer 3: Performance          │   │
│  │ Reviewer N: Security             │   │
│  └──────────────────────────────────┘   │
│  Aggregate criticism & feedback          │
└──────────────┬───────────────────────────┘
               │
               ▼
        Selection/Refinement
        of Best Solution

Failure Mode: High computational cost
             Slower iteration cycles
             Risk of groupthink among reviewers
```

## Practical Applications & Use Cases

### 1. Agent Architecture Selection

When designing a new agent system, practitioners can:
- Map their requirements to the cognitive function dimensions needed
- Choose execution topologies that match their constraints (latency, cost, reliability)
- Identify the specific pattern they're implementing and its known failure modes

**Example:** For a customer service agent needing high reliability:
- **Cognitive functions required:** Perception, Memory, Reasoning, Action, Reflection, Governance
- **Topology choice:** Orchestrator-Workers with Adversarial Verification pattern
- **Trade-off awareness:** Higher cost/latency but lower error rates

### 2. Debugging and Optimization

When an agent system exhibits unexpected behaviors:
- Map the implementation to the framework
- Identify which pattern it actually implements
- Cross-reference known failure modes for that pattern
- Design targeted improvements

**Example:** Agent frequently misinterprets user requirements:
- Current pattern: Plan-and-Execute
- Known failure: Brittle to planning errors
- Solution: Add Reflection/Revision cycle or switch to Hierarchical Delegation

### 3. Framework Comparison and Evaluation

Researchers comparing agent frameworks (LangChain, AutoGen, Semantic Kernel, etc.) can:
- Classify each framework's typical patterns
- Compare supported cognitive functions
- Identify topology flexibility and constraints
- Assess suitability for different use cases

### 4. Capability Roadmapping

Teams building agent systems can:
- Identify current cognitive functions and topology
- Plan capability additions systematically
- Understand how new functions might require topology changes
- Design evolution paths with clear justification

## Insights & Implications

### 1. Impact on Agent Development Practices

This framework fundamentally changes how practitioners think about agent design:
- **Before:** Architects choose topologies (orchestrator, peer-to-peer, etc.) and hope they work
- **After:** Architects explicitly map cognitive requirements to topologies and anticipate failure modes

This shift enables more deliberate, principled agent design.

### 2. Convergence and Standardization

The framework validates what industry practice has been discovering empirically: certain patterns (Orchestrator-Workers, Hierarchical Delegation) are universally adopted because they balance cognitive capability with implementation complexity.

### 3. Limitations and Open Questions

- **Formal semantics:** The framework is descriptive but not formally specified; how to formalize pattern semantics?
- **Hybrid patterns:** Many real systems combine multiple patterns; how to systematically compose them?
- **Emergent properties:** Do certain cognitive function + topology combinations exhibit unexpected properties?
- **Human-in-the-loop:** How does human oversight and control map to the governance dimension?

### 4. Future Research Directions

- **Pattern libraries:** Develop detailed libraries of patterns with complete trade-off analyses and optimization strategies
- **Formal verification:** Can formal methods verify pattern properties (correctness, safety, efficiency)?
- **Automated design:** Can tools automatically recommend optimal patterns given constraints?
- **Hybrid architectures:** How to systematically design agents that transition between patterns dynamically?

## Code & Resources

### Official Implementation & Code

- **GitHub:** Not yet available (paper recently published)
- **Project Status:** Primarily conceptual framework paper; no monolithic implementation

### Integration Strategy

The framework is designed for use as a **design methodology**, not a specific library:
1. Reference the framework when designing agent systems
2. Use it to classify and compare existing systems
3. Apply it to architectural decisions in projects using LangChain, Semantic Kernel, AutoGen, etc.

### Dependencies and Compute Requirements

- **No specific dependencies:** Framework is conceptual
- **Applicable to:** Any LLM-based agent system
- **Integration level:** Architect-level (design-time tool, not runtime)

### Related Tools and Frameworks

- **LangChain:** Can implement any pattern; use framework to clarify which one
- **Semantic Kernel:** Orchestrator-based, good for Plan-and-Execute and Hierarchical Delegation
- **Anthropic's Agent Framework:** Emphasizes Orchestrator-Workers topology
- **AutoGen:** Supports peer-to-peer and hierarchical topologies

## Related Work & Context

### Foundational Work

1. **BDI (Belief-Desire-Intention) Architecture** - Classical AI agent framework that maps to Reasoning and Action in the cognitive dimension

2. **Reactive Agent Architecture** - Minimal cognitive functions, fast execution; trade-off point in the framework

3. **STRIPS Planning** - Planning algorithms relevant to Reasoning dimension

### Prior Work on Agent Architectures

- **LangChain Framework Design:** Industry-standard orchestration approach
- **Anthropic's Agent Architecture:** Reference architecture for orchestrator-based agents
- **Multi-Agent Systems Literature:** Coordination and communication patterns

### Related Recent Papers

- "Agentic Design Patterns: A System-Theoretic Framework" (arXiv:2601.19752) - System-theoretic approach to design patterns
- "Making Sense of AI Agents Hype: Adoption, Architectures, and Takeaways from Practitioners" (arXiv:2604.00189) - Empirical study of real-world agent architectures
- "From Prompt-Response to Goal-Directed Systems" (arXiv:2602.10479) - Reference architecture and topology taxonomy
- "Agent Design Pattern Catalogue" (arXiv:2405.10467) - Comprehensive pattern catalog

### Future Research Directions

1. **Formal semantics:** Develop mathematical foundations for the framework
2. **Pattern composition:** How to systematically combine multiple patterns?
3. **Automated synthesis:** Can tools automatically design optimal agents given constraints?
4. **Hybrid dynamics:** How to design agents that adapt topology/cognitive functions dynamically?
5. **Governance and safety:** How do governance mechanisms interact with other cognitive functions?

## Key Takeaways

1. **Single-dimension thinking is insufficient:** Topology alone or cognitive function alone cannot fully characterize agent designs

2. **The same topology, different patterns:** The same execution topology can implement fundamentally different patterns with different failure modes

3. **Systematic pattern selection:** The framework enables explicit, principled choice of agent patterns rather than ad-hoc architecture selection

4. **Trade-off awareness:** Each pattern embodies specific trade-offs; understanding them is crucial for production systems

5. **Practical guidance:** The 28 design patterns provide concrete reference points for practitioners

6. **Convergence validation:** The framework validates what industry practice has empirically discovered about effective agent patterns

This framework represents a significant step toward more systematic, principled agent architecture design and should influence how practitioners design agent systems in coming years.

---

**Research Significance:** ⭐⭐⭐⭐⭐ (Fundamental framework for agent architecture design)

**Applicability to Development Automation:** ⭐⭐⭐⭐⭐ (Directly addresses systematic agent design)

**Implementation Complexity:** ⭐⭐☆☆☆ (Framework/methodology, not a specific system)
