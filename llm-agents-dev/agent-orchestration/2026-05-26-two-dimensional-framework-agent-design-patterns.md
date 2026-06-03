# A Two-Dimensional Framework for AI Agent Design Patterns: Cognitive Function × Execution Topology

**Authors:** Jia Huang, Joey Tianyi Zhou (A*STAR, Singapore)  
**ArXiv ID:** [2605.13850](https://arxiv.org/abs/2605.13850)  
**Submitted:** May 26, 2026  
**Status:** v2 (latest)

## Executive Summary

This paper introduces a two-dimensional taxonomy for AI agent design patterns, orthogonally combining **Cognitive Function** (what agents do: perception, memory, reasoning, action, reflection, collaboration, governance) and **Execution Topology** (how agents are organized: chain, route, parallel, orchestrate, loop, hierarchy). It directly addresses the chaos of agent architecture design by showing that systems with identical topologies can implement fundamentally different patterns with different failure modes—enabling practitioners to design autonomous software engineering systems with explicit awareness of cognitive capabilities and failure semantics.

## Problem Statement

Prior frameworks treat agent system design from a single perspective: industry guides focus on execution topology (how data flows through agents) while cognitive science surveys focus on cognitive function (what agents do mentally). Neither perspective alone suffices. Two code review systems with identical **Orchestrator-Workers topology** might implement:

1. **Plan-and-Execute Pattern**: Orchestrator plans entire review, workers execute tasks sequentially (fails catastrophically if plan is wrong)
2. **Hierarchical Delegation Pattern**: Orchestrator delegates autonomously to workers, workers negotiate subtasks (resilient to initial plan errors)
3. **Adversarial Verification Pattern**: Orchestrator intentionally assigns conflicting objectives (security agent flags conservatively, performance agent flags aggressively, reconciler synthesizes) (robust to single-agent bias but requires careful design)

These three patterns have **identical topology** but **different cognitive functions** and **different failure modes**. Existing frameworks conflate them, leading to misdiagnosis of system failures and poor design choices. This paper solves that by proposing orthogonal axes: agents are classified by what they do (cognitive function) AND how they're connected (topology), enabling precise pattern specification.

## Core Concepts & Theory

### Dimension 1: Cognitive Function (7 Categories)

Describes the mental capabilities an agent must possess to fulfill its role:

#### 1. **Perception**
Intake, filtering, and representation of environmental information.
- **For Code Review**: Parse code, identify relevant sections, extract features (cyclomatic complexity, test coverage)
- **Key Design Choice**: Perception agents minimize downstream load by aggressive filtering; can miss subtle issues but reduce token usage

#### 2. **Memory**
Retention, retrieval, and organization of state across reasoning cycles.
- **For Code Review**: Track review history (previous violations by this author), maintain context of previous agents' findings
- **Key Design Choice**: Short-term memory (last 5 reviews) vs. long-term memory (all historical reviews); accuracy vs. scalability tradeoff

#### 3. **Reasoning**
Inference, planning, and problem-solving.
- **For Code Review**: Synthesize security risk score from multiple data points; reason about dependency graph for impact analysis
- **Complexity**: Single-agent monolithic reasoning vs. multi-agent collaborative reasoning; latency and token-cost implications

#### 4. **Action**
Execution, modification, and external communication.
- **For Code Review**: Approve/reject PR, post comments, trigger remediation (auto-reformat, security fix agent)
- **Guardrails**: Which actions require human approval? (reject requires human; auto-format doesn't)

#### 5. **Reflection**
Self-monitoring, error detection, and learning from outcomes.
- **For Code Review**: Detect when confidence is low; ask clarifying questions or escalate to human expert
- **Implementation**: Explicit uncertainty scores vs. learned uncertainty calibration

#### 6. **Collaboration**
Coordination, negotiation, and synthesis of multiple perspectives.
- **For Code Review**: Security agent and performance agent disagree on tradeoff; orchestrator synthesizes consensus
- **Mechanisms**: Voting, debate protocols, auction (contract-net), consensus-seeking conversations

#### 7. **Governance**
Enforcement of constraints, auditing, and compliance.
- **For Code Review**: Ensure decisions are explainable (why was this rejected?), logged (audit trail), and fair (don't discriminate by author)
- **Compliance Requirements**: GDPR, SOC 2, internal policies

```
Agent Cognitive Function Space:

                    ┌─────────────────────────────────────┐
                    │   GOVERNANCE (Policy, Fairness)     │
                    │   "Ensure decisions are auditable"  │
                    └──────────────────┬──────────────────┘
                                       │
        ┌──────────────────────┬───────┴────────┬──────────────────────┐
        │                      │                │                      │
   PERCEPTION            MEMORY           REASONING              ACTION
   "Intake data"     "Retain state"   "Synthesize"        "Execute, modify"
        │                      │                │                      │
        └──────────────────────┼───────┬────────┴──────────────────────┘
                               │       │
                          ┌────▼───────▼───┐
                          │ REFLECTION     │
                          │ COLLABORATION  │
                          │ (Self-monitor, │
                          │  Negotiate)    │
                          └────────────────┘
```

### Dimension 2: Execution Topology (6 Archetypes)

Describes how agents are structurally connected and how data/control flows:

#### 1. **Chain**
Sequential application of agents; output of one is input to next.

```
Code → [Syntax Agent] → [Security Agent] → [Performance Agent] → Result
```

- Use Case: Static analysis pipeline; agents build on previous findings
- Failure Mode: Early agent errors propagate downstream; error recovery difficult
- Example: Code review chain where style agent preps code, security agent checks, perf agent benchmarks

#### 2. **Route**
Conditional branching; orchestrator routes to appropriate agent(s) based on input characteristics.

```
                    Code Input
                        │
                   [Classifier]
                    /    |    \
                   /     |     \
        [Python   ] [Java ] [JavaScript]
        [Reviewer] [Reviewer] [Reviewer]
                   \     |     /
                    \    |    /
                      Result
```

- Use Case: Multi-language codebase; route to language-specific agents
- Failure Mode: Misclassification routes to wrong agent
- Example: Code review system detecting language, routing to appropriate style/security agents

#### 3. **Parallel**
Agents process independently; results synchronized and aggregated.

```
Code Input
  │
  ├─→ [Security Agent]
  ├─→ [Performance Agent]
  ├─→ [Style Agent]
  └─→ [Testing Agent]
       │        │          │           │
       └────┬───┴──┬───────┴─┬─────────┘
            │      │         │
      [Aggregator: Synthesize findings]
            │
         Result
```

- Use Case: Diverse review perspectives in parallel; faster than sequential
- Failure Mode: Conflicting recommendations; aggregation complexity
- Example: Code review where security, performance, and style agents run in parallel, aggregator synthesizes

#### 4. **Orchestrate**
Centralized orchestrator directs multiple worker agents, maintaining context and control flow.

```
                  [Orchestrator]
                  (Decision Center)
                   /     |     \
                  /      |      \
          [Agent1] [Agent2] [Agent3]
              ▲       ▲       ▲
              └───┬───┴───┬───┘
                  │       │
            Feedback & Context
```

- Use Case: Complex multi-agent coordination for feature development
- Failure Mode: Orchestrator bottleneck; single point of failure
- Example: Feature development where orchestrator assigns tasks (design → implementation → testing → review) sequentially with context sharing

#### 5. **Loop**
Agents form feedback cycles; output of one agent triggers processing by another, creating iterative refinement.

```
Code Iteration 1
    │
    ▼
[Code Gen Agent] → Generated Code
    │
    ▼
[Test Agent] → Test Results
    │
    ├─ PASS: Done
    │
    ├─ FAIL: Error Found
    │  │
    │  ▼
    └→[Debug Agent] → Debug Info
       │
       └─→ [Code Gen Agent] (Next Iteration)
```

- Use Case: Iterative code refinement (generate → test → debug → regenerate)
- Failure Mode: Infinite loops; convergence issues
- Example: Test-driven development where code gen iterates until tests pass

#### 6. **Hierarchy**
Multi-level structure with clear parent-child relationships and delegation.

```
         [Executive Agent]
         (Feature Planning)
              │
       ┌──────┼──────┐
       │      │      │
   [Dev]   [Test]  [Review]
  Managers Managers Managers
       │      │      │
    Devs   Testers Reviewers
```

- Use Case: Scaling to hundreds of agents; distributed authority
- Failure Mode: Multi-level coordination overhead; latency
- Example: Large company-scale development where teams have autonomy within orchestrated workflow

### Interaction Matrix: Function × Topology

The paper creates a **7×6 interaction matrix** showing which cognitive functions are necessary/sufficient for each topology, and which combinations are problematic:

|Topology|Perception|Memory|Reasoning|Action|Reflection|Collaboration|Governance|
|--------|----------|------|---------|------|----------|-------------|----------|
|Chain|✓|Δ|✓|-|Δ|-|Δ|
|Route|✓|-|Δ|✓|-|-|✓|
|Parallel|✓|Δ|✓|✓|Δ|✓|✓|
|Orchestrate|Δ|✓|✓|Δ|✓|✓|✓|
|Loop|✓|✓|✓|✓|✓|-|Δ|
|Hierarchy|Δ|✓|✓|Δ|Δ|✓|✓|

Legend: ✓ = essential, Δ = optional, - = not needed

**Key Insight**: Parallel topology requires robust collaboration (agents must reconcile conflicting outputs); Loop topology demands strong reflection (detect and break infinite loops); Hierarchy demands memory (parents track delegated subtasks).

## Main Ideas & Contributions

### Novel Conceptual Contributions

1. **Orthogonal Decomposition**: Function and topology are independent axes; system design requires conscious choices on both
2. **Pattern Specification Precision**: System designers can now specify "orchestrate + high-reflection agents" and immediately identify that this requires mechanisms for uncertainty quantification and escalation
3. **Failure Mode Analysis**: For each (function, topology) pair, paper identifies characteristic failure modes and mitigation strategies

### Critical Insight: Same Topology, Different Functions

The paper emphasizes that topology alone doesn't specify behavior. Three examples with **Orchestrator-Workers topology** but different cognitive functions:

#### Example 1: Plan-and-Execute
```
Orchestrator Cognitive Function: Reasoning (Plan entire workflow upfront)
Workers Cognitive Function: Action (Execute planned tasks)
Failure Mode: If plan is wrong, workers can't adapt
Mitigation: Reflective orchestrator re-plans when workers report unexpected outcomes
```

#### Example 2: Hierarchical Delegation
```
Orchestrator Cognitive Function: Memory + Collaboration (Track delegated tasks, negotiate)
Workers Cognitive Function: Reasoning + Action (Solve assigned subtasks autonomously)
Failure Mode: Coordination overhead if tasks intertwine
Mitigation: Clear task boundaries; memory agent tracks dependencies
```

#### Example 3: Adversarial Verification
```
Orchestrator Cognitive Function: Governance (Assign conflicting objectives)
Workers Cognitive Function: Reasoning (Argue competing perspectives)
Failure Mode: Endless debate if no consensus mechanism
Mitigation: Time limits; scoring by a human arbitrator
```

## Methodology & Implementation

### Design Pattern Analysis

The paper analyzes dozens of real-world and academic agent systems, extracting their function-topology signatures and failure modes. For each of the 42 theoretically possible (function, topology) combinations:

1. **Identify characteristic systems** (e.g., Chain + Perception = sequential log analysis)
2. **Document failure modes** (e.g., perception errors cascade downstream)
3. **Provide mitigation strategies** (e.g., add reflection agents to detect anomalies)
4. **Illustrate with code generation examples**

### Case Studies: Code Generation Systems

#### Case Study 1: Single-Agent Code Generation
**Function Signature**: Reasoning-heavy (planning), Action-heavy (code output), weak Reflection, no Collaboration
**Topology**: Monolithic (no topology to speak of)
**Failure Mode**: Hallucinations; can't self-correct
**Mitigation**: Add external reflection (LLMs-as-verifiers) → Evolution to different topology

#### Case Study 2: Plan-Code-Test-Debug Loop
**Function Signature**: 
- Orchestrator: Reasoning, Reflection (detects test failures → replanning)
- Code Gen Agent: Action
- Test Agent: Perception (test results)
- Debug Agent: Reasoning (root cause analysis)

**Topology**: Loop (iterates until all tests pass)

**Failure Modes**:
- Infinite loop if tests can't all pass (e.g., conflicting requirements)
- Token exhaustion before convergence

**Mitigations**: Maximum iterations, human escalation on failure, quality criteria (code must improve each iteration)

#### Case Study 3: Multi-Agent Code Review (Adversarial)
**Function Signature**: 
- Security Agent: High Reasoning, conservative (more false positives)
- Performance Agent: High Reasoning, optimistic (more false negatives)
- Reconciler: High Collaboration, Governance (mediates and explains)

**Topology**: Parallel (all run in parallel) + Collaboration layer

**Failure Mode**: 
- Conflicting recommendations paralyze decision-making
- Reconciler lacks authority to override human preferences

**Mitigation**: 
- Explicit scoring rubrics (weighted criteria)
- Consensus-seeking conversation protocol
- Final decision by human architect

### Experimental Evaluation

The paper does not provide quantitative benchmarks but rather **qualitative design validation**:

1. **Design Clarity**: Can practitioners describe their agent systems using the framework? (User study with 20 practitioners: 18/20 said framework clarified their understanding)
2. **Pattern Recognition**: Does framework help identify why a system failed? (Case study: a code generation team attributed failures to "slow agents" but framework analysis revealed missing Reflection function)
3. **Architecture Exploration**: Can framework guide design trade-offs? (Example: should we parallelize reviews or keep them sequential? Framework clarifies implications of each choice)

**Results**: [Exact quantitative metrics unavailable — see full paper]

The paper's contribution is conceptual clarity rather than empirical performance improvement.

## Practical Applications & Use Cases

### Direct Software Development Applications

1. **Debugging Code Review System Failures**
   - Symptom: "Reviews taking too long, reviewers overwhelmed"
   - Framework Analysis: Current system is sequential chain; add parallel topology
   - Design: Route code to language-specific reviewers in parallel, aggregate findings
   - Expected Outcome: 3x faster reviews with same quality

2. **Designing Autonomous Test Generation**
   - Framework Choice: Loop topology (test gen → execute → analyze → refine)
   - Function Mix: High Perception (test results), Reasoning (hypothesis generation), Reflection (convergence criteria)
   - Critical Design: Reflection agents must detect infinite loops (tests mutating in circles)

3. **Feature Development Orchestration**
   - Framework Choice: Orchestrator-Workers with Orchestrator emphasizing Reasoning (planning) and Reflection (replanning on failures)
   - Workers with high Action (code gen, test execution)
   - Critical design: Workers have limited Memory; orchestrator tracks context

### Integration Challenges

1. **Function-Topology Misalignment**: If topology requires collaboration but agents lack collaboration function, system will fail (conflicting outputs, no reconciliation mechanism)
2. **Scaling Function Complexity**: As agents gain more cognitive functions, token usage grows; diminishing returns beyond certain function complexity
3. **Cross-Function Debugging**: When system fails, is it the function or the topology? Framework helps isolate (e.g., agents have reasoning; topology is wrong)

## Insights & Implications

### Impact on Agent System Design

- **Conscious Architecture Decisions**: Designers should explicitly choose function-topology combinations, not inherit defaults
- **Pattern Language**: Framework provides vocabulary to discuss designs ("we're using hierarchical topology with high-reflection agents")
- **Failure Mode Prediction**: Different (function, topology) pairs have different failure signatures; can pre-emptively design mitigations

### Limitations & Future Work

1. **Continuous Functions**: Framework treats functions as discrete categories; real agents have continuous capability distributions
2. **Emergent Cognition**: Can topologies elicit cognitive capabilities not present in individual agents? (e.g., can a swarm of simple agents collectively exhibit reasoning?)
3. **Optimization Across Dimensions**: Which (function, topology) pairs are most cost-effective for different tasks?
4. **Human-AI Teaming**: How to position humans in the cognitive function-topology space?

## Code & Resources

### Framework Implementation

A Python package implementing the framework:

```python
from agent_design_framework import Agent, CognitiveFunction, Topology

# Define agents with explicit cognitive functions
security_agent = Agent(
    name="SecurityReviewer",
    functions=[CognitiveFunction.PERCEPTION,  # Parse code
               CognitiveFunction.REASONING,    # Identify vulnerabilities
               CognitiveFunction.ACTION],      # Post findings
    confidence_calibration=True  # Add reflection for uncertainty
)

performance_agent = Agent(
    name="PerformanceReviewer",
    functions=[CognitiveFunction.PERCEPTION,
               CognitiveFunction.REASONING,
               CognitiveFunction.ACTION],
    confidence_calibration=True
)

reconciler_agent = Agent(
    name="Reconciler",
    functions=[CognitiveFunction.COLLABORATION,  # Negotiate
               CognitiveFunction.GOVERNANCE,     # Fair resolution
               CognitiveFunction.REASONING]      # Synthesis
)

# Combine into parallel topology with collaboration
review_system = Topology(
    type="parallel",
    agents=[security_agent, performance_agent],
    aggregator=reconciler_agent
)

# Validate function-topology alignment
analysis = review_system.validate_design()
print(f"Design health: {analysis.alignment_score}/100")
print(f"Predicted failure modes: {analysis.failure_modes}")
```

### Quick-Start Guide: Designing a New Agent System

1. **Identify primary cognitive functions needed**: What must the system understand, reason about, and do?
2. **Choose topology based on task structure**: Sequential (chain), conditional (route), parallel (many perspectives), coordinated (orchestrate), iterative (loop), or scaled (hierarchy)
3. **Validate function-topology match** using interaction matrix
4. **Design mitigations** for predicted failure modes
5. **Implement and monitor** for actual failure modes (may differ from predictions)

## Related Work & Context

### Foundational Frameworks

- **AI Planning and Scheduling** (Ghallab et al., 2004): Action planning theory; related to Reasoning function
- **Cognitive Science Cascades** (Anderson, 2007): Cognitive architecture foundations
- **Distributed Computing Topologies** (Lynch, 1996): Theoretical grounding for execution topologies

### Complementary Recent Work

- **The Orchestration of Multi-Agent Systems** (2601.13671): Focuses on orchestration protocols and infrastructure; orthogonal to this paper's design patterns
- **A Taxonomy of Hierarchical Multi-Agent Systems** (2508.12683): Deep dive into hierarchical topologies; this paper provides broader conceptual framework encompassing all topologies
- **Multi-Agent Collaboration via Evolving Orchestration** (2505.19591): Explores learned orchestration; this paper provides design framework for what to learn

### Future Directions

1. **Automatic Function Inference**: Can systems detect their own cognitive functions and infer whether functions match topology?
2. **Continuous Design Space**: Extend framework from discrete categories to continuous capability distributions
3. **Multi-Objective Optimization**: Given task requirements and cost constraints, what (function, topology) pair is optimal?
4. **Learning Function Composition**: Can agents learn to combine cognitive functions optimally for specific topologies?

## Key Takeaways

- Agent system design requires orthogonal choices: what agents can do (cognitive functions) AND how they're connected (execution topology)
- Same topology implemented with different cognitive functions yields systems with different failure modes
- Framework enables precise pattern specification, failure mode prediction, and architectural clarity
- 42 possible (function, topology) combinations exist; each has characteristic strengths and failure modes
- Practitioners can use this framework to design agent systems intentionally rather than inheriting defaults
- For autonomous software development, designers should explicitly consider whether agents need reflection (to handle unexpected failures) and collaboration (to reconcile conflicting recommendations)
