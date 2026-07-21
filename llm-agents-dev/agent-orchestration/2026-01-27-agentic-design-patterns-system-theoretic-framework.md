# Agentic Design Patterns: A System-Theoretic Framework

**Authors:** Minh-Dung Dao, Quy Minh Le, Hoang Thanh Lam, Duc-Trong Le, Quoc-Viet Pham, Barry O'Sullivan, Hoang D. Nguyen

**ArXiv ID:** 2601.19752

**Publication Date:** January 27, 2026

**Venue:** University College Cork & Contributors

---

## Executive Summary

This paper presents a rigorous system-theoretic framework for designing robust AI agents built with foundation models. Rather than ad-hoc system design, the authors propose a principled taxonomy of 12 agentic design patterns grounded in five core functional subsystems. This work addresses critical challenges in agent reliability—including hallucination and poor reasoning—by providing architects with a structured methodology for building predictable, composable multi-agent systems for software development and complex reasoning tasks.

---

## Problem Statement

### Current Challenges in Agentic System Design

Foundation model-based AI agents suffer from:
1. **Hallucination and reasoning failures** that propagate unpredictably through system layers
2. **Ad-hoc system design** lacking principled, systematic foundations
3. **Brittleness in composition** when combining multiple agents or capabilities
4. **Unclear failure attribution** across poorly structured agent interactions

### Research Gap

While design patterns have proven invaluable in software engineering and distributed systems, agentic AI systems lack equivalent formal foundations. Existing agent frameworks are built reactively around specific use cases rather than derived from first principles about agent cognition, perception, and execution.

---

## Core Concepts & Theory

### System-Theoretic Foundation

The framework decomposes agentic AI systems into **five interacting functional subsystems**:

```
┌─────────────────────────────────────────────────────────────┐
│          Agentic AI System Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 1. Reasoning & World Model Subsystem               │     │
│  │    - Problem decomposition                         │     │
│  │    - Planning & sequencing                         │     │
│  │    - Outcome prediction                            │     │
│  └────────────────────────────────────────────────────┘     │
│                         ↕                                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 2. Perception & Grounding Subsystem                │     │
│  │    - Environment observation                       │     │
│  │    - Information extraction                        │     │
│  │    - Semantic grounding to reality                 │     │
│  └────────────────────────────────────────────────────┘     │
│                         ↕                                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 3. Action Execution Subsystem                      │     │
│  │    - Tool invocation                               │     │
│  │    - Environment manipulation                      │     │
│  │    - Effect verification                           │     │
│  └────────────────────────────────────────────────────┘     │
│                         ↕                                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 4. Learning & Adaptation Subsystem                 │     │
│  │    - Experience capture                            │     │
│  │    - Strategy refinement                           │     │
│  │    - Knowledge consolidation                       │     │
│  └────────────────────────────────────────────────────┘     │
│                         ↕                                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 5. Inter-Agent Communication Subsystem             │     │
│  │    - Message protocols                             │     │
│  │    - Coordination mechanisms                       │     │
│  │    - Agreement procedures                          │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Design Pattern Taxonomy (12 Patterns)

The framework derives 12 reusable agentic design patterns organized into four categories:

#### 1. **Foundational Patterns** (System Architecture)
- **Hierarchical Agent Architecture**: Coordinator + specialist agents with task decomposition
- **Reactive Agent Pattern**: Event-driven response without explicit planning
- **Reflective Agent Pattern**: Self-monitoring and metacognitive adjustment

#### 2. **Cognitive & Decisional Patterns** (Reasoning & Planning)
- **Multi-Perspective Reasoning**: Parallel evaluation of decisions from multiple angles
- **Evidence-Based Decision Making**: Structured accumulation of evidence before commitment
- **Contingency Planning Pattern**: Preparation of fallback strategies before execution

#### 3. **Execution & Interaction Patterns** (Action & Communication)
- **Safe Execution Pattern**: Verification gates and rollback capabilities before applying changes
- **Tool Orchestration Pattern**: Sequencing and composition of multiple tools
- **Collaborative Consensus Pattern**: Multi-agent agreement protocols for critical decisions

#### 4. **Adaptive & Learning Patterns** (Self-Improvement)
- **Experience Replay Pattern**: Iterative refinement through recorded traces
- **Knowledge Consolidation Pattern**: Distillation of learnings into reusable skills
- **Dynamic Capability Extension**: Runtime addition of new competencies based on task demands

### Mathematical Formulation

Each pattern can be formally represented as a tuple:
```
Pattern_i = (Subsystem_involvement, Interaction_topology, Failure_modes, Remediation_strategies)
```

This allows composition verification and automated detection of missing safeguards.

---

## Main Ideas & Contributions

### 1. Principled Agent Design Methodology

**Key Insight:** Agent robustness emerges from explicit design of interactions between the five functional subsystems, not from isolated improvements to individual components.

**Contribution:** Provides architects with a decision framework: "Given a target task and constraints, which patterns should I compose, and in what order?"

### 2. Pattern Composition Rules

The framework identifies safe composition rules:
- Hierarchical patterns can wrap reactive patterns
- Evidence-based decisions must precede safe execution
- Contingency planning requires multi-perspective reasoning
- Learning patterns feed back into reasoning and perception

### 3. Failure Mode Mapping

Each pattern has associated failure modes:
- **Hallucination propagation**: When reasoning subsystem confidence exceeds actual model reliability
- **Perception-action mismatch**: When grounding fails to map observations to executable concepts
- **Coordination deadlock**: When multi-agent communication patterns create cycles
- **Catastrophic forgetting**: When learning doesn't preserve critical prior capabilities

### 4. Foundation Model Compatibility

The framework explicitly addresses foundation model characteristics:
- Token budget constraints affecting reasoning depth
- Context window limitations for state maintenance
- Temperature/sampling effects on reasoning consistency
- Attention mechanisms and their implications for multi-step planning

---

## Methodology & Implementation

### Derivation Process

1. **Subsystem Identification**: Analyzed 200+ successful multi-agent systems to extract common functional components
2. **Pattern Extraction**: Identified recurring compositional structures across domains (software development, scientific discovery, business process automation)
3. **Verification**: Validated patterns against failure taxonomies from production deployments
4. **Formalization**: Expressed patterns in system-theoretic notation enabling mechanical composition checking

### Practical Application Steps

**Step 1: Characterize Task Requirements**
- Identify constraint: accuracy, latency, cost, safety criticality
- Map to required subsystem capabilities
- Determine acceptable failure modes

**Step 2: Select Core Pattern**
- Hierarchical for complex decomposable tasks
- Reactive for time-sensitive, low-latency requirements
- Reflective for open-ended exploration

**Step 3: Layer Patterns**
- Add evidence patterns for high-stakes decisions
- Add contingency for tasks with reversibility concerns
- Add learning patterns for repeated task classes

**Step 4: Verify Composition**
- Check for pattern anti-patterns
- Validate message flow consistency
- Simulate failure scenarios

### Software Development Specific Applications

For code generation and debugging tasks:
```
1. Hierarchical Coordinator
   ├─ Multi-perspective Reasoning (explore multiple code approaches)
   ├─ Evidence-Based Decision (commit to specific implementation)
   ├─ Safe Execution (test before applying)
   └─ Experience Replay (improve on next similar task)
```

For repository-level refactoring:
```
1. Reactive Agent (initial file analysis)
2. Collaborative Consensus (for architecture changes affecting multiple files)
3. Contingency Planning (prepare rollback if new approach fails tests)
4. Knowledge Consolidation (extract refactoring patterns for reuse)
```

---

## Practical Applications & Use Cases

### 1. Software Development Automation

**Code Generation Agents**: Hierarchical pattern + multi-perspective reasoning enables agents to evaluate multiple implementation strategies before committing code.

**Test Generation**: Evidence-based patterns ensure test suites cover identified edge cases before coverage claims are made.

**Refactoring Agents**: Safe execution patterns with comprehensive test verification prevent breaking changes.

### 2. Multi-Agent Development Teams

**Specialist Orchestration**: Different agents (planning, coding, testing, review) coordinate through explicit communication patterns preventing deadlock and missed handoffs.

**Conflict Resolution**: Collaborative consensus patterns enable agents to resolve disagreements about implementation direction.

**Knowledge Sharing**: Knowledge consolidation patterns allow teams to capture architectural decisions and coding patterns for reuse.

### 3. Autonomous Debugging and Repair

**Root Cause Analysis**: Reflective agent pattern enables agents to recognize when initial hypothesis about bug cause is inconsistent with evidence.

**Safe Program Repair**: Safe execution pattern ensures patches are tested across multiple scenarios before commitment.

### 4. Enterprise Process Automation

**Complex Workflows**: Hierarchical patterns handle multi-step business processes with rollback on partial failures.

**Exception Handling**: Contingency planning enables agents to handle edge cases gracefully.

### Integration Challenges

**Foundation Model Behavior**: Patterns must account for non-determinism in model reasoning; evidence accumulation helps mitigate this.

**Cost vs. Accuracy**: Framework enables explicit trade-offs between multi-agent collaboration (more robust) and single-agent efficiency (lower cost).

**Latency Requirements**: Reactive and streamlined hierarchical patterns for time-sensitive applications.

---

## Insights & Implications

### For Agent-Driven Development Systems

1. **Robustness Through Composition**: Agent reliability isn't achieved through larger models or more training data alone, but through proper architectural composition of subsystems.

2. **Patterns Enable Scaling**: The 12-pattern vocabulary provides reusable building blocks for constructing ever-more-complex agents without reinventing failure handling.

3. **Testability Framework**: Each pattern has identifiable test requirements, enabling systematic verification of agent behavior before deployment.

### Advancement in Autonomous Coding

- **From Black-Box to Transparent**: Agents designed through these patterns have explicable behavior tied to specific subsystem choices
- **From Trial-and-Error to Systematic**: Development teams can reason about which patterns to add rather than randomly trying agent variations
- **From Brittle to Resilient**: Contingency and learning patterns provide graceful degradation rather than failure cascades

### Limitations and Open Questions

1. **Computational Overhead**: Some patterns (multi-perspective reasoning, evidence accumulation) require multiple inference passes, increasing cost.

2. **Pattern Interaction Complexity**: Composing >3 patterns requires careful validation to avoid unintended interference.

3. **Foundation Model Dependency**: Framework derived assuming access to capable reasoning models; applicability to smaller models unclear.

4. **Observability**: Requires detailed instrumentation to understand pattern effectiveness in production.

### Research Implications

- **Pattern Mining**: Can frameworks automatically discover optimal pattern compositions for new task domains?
- **Self-Diagnosing Agents**: Can agents automatically detect which pattern composition is failing and recommend fixes?
- **Cross-Domain Transfer**: Do patterns discovered in software engineering apply to other domains (scientific discovery, business automation)?

---

## Code & Resources

### GitHub Repositories

**Framework Implementation:** [Paper repository with pattern composition tools]
- Pattern validation toolkit
- Composition rule checker
- Failure mode analyzer
- Pattern selection guide

### Dependencies

- Python 3.9+
- Foundation Model SDK (OpenAI, Anthropic, open-source LLM libraries)
- Standard libraries: asyncio, logging, dataclasses

### Quick-Start Integration Guide

```python
from agentic_patterns import (
    HierarchicalArchitecture,
    MultiPerspectiveReasoning,
    SafeExecutionPattern,
    VerificationComposer
)

# Define agent architecture
architecture = HierarchicalArchitecture(
    coordinator="planning-agent",
    specialists=[
        "coding-specialist",
        "testing-specialist",
        "review-specialist"
    ]
)

# Compose patterns
patterns = VerificationComposer.validate_composition([
    MultiPerspectiveReasoning(perspectives=3),
    SafeExecutionPattern(
        verification_gates=["type-checking", "unit-tests"],
        rollback_enabled=True
    )
])

# Deploy
agent_system = patterns.compose_into_system(architecture)
```

### Required Infrastructure

- Vector database for state persistence (optional but recommended)
- Logging system for observability
- Test infrastructure for pattern verification gates

---

## Related Work & Context

### Foundational Work

- **Software Engineering Design Patterns** (Gang of Four, 1994): Inspired pattern taxonomy approach
- **Distributed Systems Patterns** (Storey et al.): Coordination and consensus patterns adapted for multi-agent systems
- **Cognitive Science Literature**: Five subsystems derived from cognitive agent models

### Related Papers on Agent Architectures

- **BDI Agents** (Bratman, Israel, Pollack, 1988): Belief-Desire-Intention models precursor to reasoning subsystem
- **SOAR Cognitive Architecture**: Integrated subsystem perspective influences framework structure
- **ReAct Framework** (Yao et al., 2022): Reasoning+acting instantiates the reasoning-action subsystem interaction

### Related Patterns for Software Development

- **Agent Orchestration**: This framework provides deeper principled foundation for orchestration topologies
- **Skill-Based Agents**: Patterns here enable modular skill composition and verification
- **Tool Use & Function Calling**: Safe execution patterns ensure tools are invoked correctly

### Possible Extensions

1. **Self-Diagnosing Agents**: Can agents detect which pattern is failing and recommend fixes?

2. **Pattern Optimization**: Given task characteristics and constraints, which pattern composition maximizes performance per unit cost?

3. **Cross-Domain Validation**: Do these patterns discovered in software engineering apply to scientific discovery, business automation, or robotics?

4. **Formal Verification**: Can pattern compositions be verified using formal methods before deployment?

5. **Emergent Patterns**: Are there novel patterns emerging in large-scale multi-agent systems not captured by this taxonomy?

---

## References & Links

- **Paper HTML Version**: https://arxiv.org/html/2601.19752v1
- **Paper PDF**: https://arxiv.org/pdf/2601.19752.pdf
- **ArXiv Abstract**: https://arxiv.org/abs/2601.19752

### Related Benchmarks and Datasets

- **SWE-bench**: Code generation task evaluation
- **RACE-bench**: Repository-level code reasoning
- **CodeARC**: Program synthesis reasoning evaluation

---

**Keywords:** Agent Design Patterns, Multi-Agent Orchestration, Agent Architecture, System Theory, Foundation Models, Software Development Agents, Agentic AI

**Citation:**
```
Dao, M., Le, Q. M., Lam, H. T., Le, D., Pham, Q., O'Sullivan, B., & Nguyen, H. D. (2026).
Agentic Design Patterns: A System-Theoretic Framework. arXiv preprint arXiv:2601.19752.
```
