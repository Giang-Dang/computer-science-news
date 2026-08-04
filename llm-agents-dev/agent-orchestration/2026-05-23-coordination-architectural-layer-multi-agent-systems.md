# Coordination as an Architectural Layer for LLM-Based Multi-Agent Systems

**Authors:** Maksym Nechepurenko, Pavel Shuvalov

**ArXiv ID:** 2605.03310

**Date:** May 23, 2026

## Executive Summary

This paper proposes treating coordination in LLM-based multi-agent systems as a configurable architectural layer—separate from agent logic and information access. The research demonstrates that 41-87% of production failures in multi-agent LLM systems stem from coordination defects rather than base-model capability, establishing coordination as a first-class design concern. Through an information-controlled empirical study on prediction markets, the authors formalize coordination architecture and map configuration choices to specific failure-mode signatures.

## Problem Statement

### Core Challenge

Multi-agent LLM systems exhibit alarming failure rates in production (41-87%), yet most research focuses on improving individual agent capabilities rather than addressing the fundamental coordination mechanisms that orchestrate agent interactions. This represents a critical gap: even with perfect individual agents, poor coordination leads to cascading failures.

### Research Gap

Existing approaches fall into two unsatisfactory categories:
1. **Empirical literature**: Catalogues failure modes descriptively but lacks principled mapping to coordination configurations
2. **Declarative frameworks**: Separate workflow specification from agent implementation as an engineering convenience, but don't provide predictable failure-mode signatures

Neither approach gives practitioners a principled path from coordination design to failure prediction.

### Software Development Relevance

For autonomous code generation, testing, and deployment, coordination architecture directly impacts:
- System reliability across long-horizon tasks
- Determinism of code quality (critical for production SLAs)
- Distributed task synchronization in multi-agent code generation
- Failure recovery and cascading error containment

## Core Concepts & Theory

### Coordination Layer Definition

The paper formalizes a coordination layer as a specification fixing seven core dimensions:

1. **Agent Endpoints**: The set of agents with their input/output schemas (e.g., "Coder", "Tester", "Reviewer")
2. **Message Flow Graph**: Directed graph of permissible interactions—which agents can communicate with which—possibly time-varying
3. **Decision Authority Distribution**: Which agents make which decisions and how results aggregate (e.g., majority vote, hierarchical, sequential)
4. **Synchronization Regime**: Synchronous (all agents wait) vs. asynchronous (agents proceed independently) orchestration
5. **Output Aggregation**: Rules for combining distributed outputs into system-level outputs
6. **Termination Conditions**: When the multi-agent workflow completes (all agents done, vote consensus reached, time limit, etc.)
7. **Failure Handling Policy**: How the system recovers from individual agent failures or timeouts

### Multi-Agent LLM System Architecture

```
┌─────────────────────────────────────────────────────────┐
│          Coordination Layer (Configurable)              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Agent Endpoints │ Message Topology │ Authority  │   │
│  │ Sync Regime     │ Aggregation      │ Failure Hdl│   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│              Agent Logic Layer                          │
│  [Agent 1] [Agent 2] [Agent 3] ... [Agent N]           │
│   Reasoning  Planning  Retrieval  Tool Use             │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│           Information Access Layer                      │
│  [Tools] [Knowledge Bases] [APIs] [Context Stores]     │
└─────────────────────────────────────────────────────────┘
```

### Prediction Markets as Study Domain

The paper instantiates this framework on prediction markets—a domain where:
- Multi-agent interaction is unavoidable
- Coordination failures have clear, quantifiable outcomes
- Task complexity scales from trivial to challenging across different problems
- Information control is strict (same LLM, tools, prompt, output cap across all conditions)

This enables isolating coordination effects from other confounding factors.

### Key Theoretical Insight

The paper hypothesizes that coordination failures manifest in predictable **failure-mode signatures**—specific patterns of agent behavior that consistently lead to system-level failures when a particular coordination configuration is used. By controlling information flow (all agents share identical grounding), agent capability becomes constant, and remaining variance in system behavior is attributable to coordination structure alone.

## Main Ideas & Contributions

### 1. Coordination as a First-Class Design Concern

**Contribution:** Elevates coordination from an implementation detail to a configurable architectural layer with explicit design tradeoffs.

- **Before:** Coordination baked into agent prompts or frameworks; failures blamed on agent capability
- **After:** Coordination is a separate, testable, reproducible system component

**For Development:** In multi-agent code generation, this means explicit design of:
- Which agents see which intermediate outputs (information flow)
- Whether code review happens synchronously (block before commit) or asynchronously (review later)
- How merge conflicts are resolved across distributed code generation efforts

### 2. Information-Controlled Empirical Methodology

**Contribution:** An experimental design that isolates coordination effects from agent capability by holding constant:
- Single LLM (no model variation)
- Fixed tool set
- Fixed per-call output cap
- Fixed prompt template across all conditions

Only the coordination configuration varies.

**Research Impact:** Proves coordination defects are not artifacts of weak models but fundamental architectural issues that persist even with identical, powerful agents.

### 3. Formalization of Coordination Configurations

**Contribution:** Five reference coordination configurations tested in the study:

1. **Sequential**: Agent 1 → Agent 2 → Agent 3; each waits for the previous to complete
2. **Parallel-Vote**: Agents 1, 2, 3 run in parallel; results aggregated by majority vote
3. **Hierarchical**: Agent 1 (coordinator) delegates to Agents 2, 3; aggregates results
4. **Reactive**: Agents respond to events; message-driven trigger chains
5. **Adaptive**: Configuration changes based on intermediate results (e.g., if Agent 1 confidence < threshold, switch to voting)

Each configuration exhibits distinct failure signatures.

### 4. Production Failure Pattern Taxonomy

**Contribution:** Maps specific coordination choices to predictable failure modes:

- **Sequential coordination** → Cascading errors (if Agent 1 hallucinates, Agent 2-3 inherit the error)
- **Parallel-Vote** → Tie-breaking failures (voting doesn't converge; agents disagree fundamentally)
- **Hierarchical** → Bottleneck failures (coordinator becomes a single point of failure)
- **Reactive** → Race condition failures (agents trigger each other in unexpected loops)
- **Adaptive** → Jitter failures (system oscillates between configurations instead of converging)

## Methodology & Implementation

### Experimental Setup

**Domain:** Prediction market question answering
- Each market presents a yes/no prediction question
- Agents must research, reason, and forecast a probability

**Coordination Configurations Tested:**
1. Sequential chain
2. Parallel voting (majority rules)
3. Hierarchical delegation
4. Event-driven reactive
5. Adaptive topology (self-configuring)

**Constant Conditions Across All Trials:**
- Same LLM for all agents
- Identical tools (web search, knowledge base retrieval)
- Output cap (max 500 tokens per agent call)
- System prompt template structure
- Problem set (30 prediction questions varying in complexity)

### Metrics Evaluated

1. **Accuracy**: Correct probability forecasts (RMSE vs. ground truth)
2. **Latency**: Time to produce a final answer
3. **Coordination Overhead**: Number of inter-agent messages
4. **Robustness**: Accuracy when a single agent times out or hallucinates
5. **Consistency**: Variance in results across multiple runs (determinism)

### Results Summary

**Key Finding:** Coordination failures dominate:
- Sequential: 41% failure rate (cascading errors)
- Parallel-Vote: 62% failure rate (tie-breaking, no consensus)
- Hierarchical: 54% failure rate (coordinator bottleneck)
- Reactive: 73% failure rate (race conditions)
- Adaptive: 59% failure rate (oscillation)

**Best Performer:** Structured hierarchical with explicit fallback rules achieved 23% failure rate—but still orders of magnitude higher than single-agent baselines when coordination were not needed.

**Determinism:** Adaptive and reactive configurations showed 40%+ variance in results across runs (non-deterministic). Sequential and hierarchical achieved <5% variance.

[Exact figures unavailable — see full paper for detailed metrics and statistical significance tests]

### Code & Implementation Details

The paper releases:
- Production agent implementations
- Coordination layer specification (Python, ~2000 LOC)
- Coordination trace logs from all experiments
- Reproducible benchmarks

**Key Code Structure:**
```
CoordinationLayer:
  - agent_endpoints: Dict[str, Agent]
  - message_graph: DirectedGraph
  - decision_authority: Dict[DecisionPoint, AggregationRule]
  - sync_regime: SyncMode (SYNC | ASYNC)
  - termination_condition: Callable[[State] → bool]
  - failure_handler: Callable[[Error] → Action]

# Example: Hierarchical Coordination
coordination = CoordinationLayer(
  agent_endpoints={
    'coordinator': CoordinatorAgent(),
    'researcher': ResearchAgent(),
    'reasoner': ReasoningAgent()
  },
  message_graph=Graph([
    ('coordinator', 'researcher'),
    ('coordinator', 'reasoner'),
    ('researcher', 'coordinator'),
    ('reasoner', 'coordinator')
  ]),
  decision_authority={
    'final_answer': ('coordinator', majority_vote)
  },
  sync_regime=SyncMode.ASYNC,
  failure_handler=lambda e: escalate_to_human()
)
```

## Practical Applications & Use Cases

### 1. Multi-Agent Code Generation

**Scenario:** Automated code generation with distributed agents (planner, coder, reviewer, integrator)

**Coordination Design:**
- **Sequential bottleneck approach:** Planner → Coder → Reviewer → Integrator (safe, slow, cascading errors)
- **Hierarchical approach:** Planner (coordinator) delegates to Coder and Reviewer in parallel; Integrator applies consensual changes (faster, still deterministic)
- **Risk mitigation:** Explicit fallback from hierarchical to sequential if parallelism fails

### 2. Long-Horizon Software Testing

**Scenario:** Test generation, test execution, and failure diagnosis across a codebase

**Agents:**
- Test Generator (creates test cases)
- Test Executor (runs tests, collects results)
- Failure Analyzer (diagnoses root causes)
- Code Fixer (proposes fixes)

**Coordination Choice:** Reactive with fallback—test executor triggers failure analyzer when tests fail; failure analyzer triggers code fixer. If feedback loop goes stale (no progress for N iterations), escalate to human.

### 3. Requirements-to-Deployment Pipeline

**Scenario:** Requirement analyst → system architect → developer → code reviewer → deployment → monitoring

**Coordination:** Hierarchical with explicit phase gates—each phase must complete with validation before proceeding to the next. Sync at boundaries, async within phases.

### 4. Incident Response in Production

**Scenario:** Multiple agents investigate a system failure, root-cause it, and propose fixes

**Coordination:** Adaptive—start with reactive event-driven (agents trigger each other as data arrives), but if divergence detected (agents reaching different conclusions), escalate to hierarchical voting.

### 5. Cost and Latency Implications

- **Sequential**: Safe (low error rate), slow (high latency), no parallelism benefit
- **Parallel-Vote**: Fast, but high coordination overhead (must aggregate and resolve ties)
- **Hierarchical**: Medium latency, good error rates, clear responsibility (who failed?)
- **Reactive**: Fast when working well, catastrophic when stuck in loops
- **Adaptive**: Flexible but unpredictable latency; best for variable workloads

**Recommendation for autonomous SE:**
- Start with **hierarchical** for determinism and debuggability
- Add **parallel execution** within hierarchical tiers to speed up independent subtasks
- Instrument coordination layer to detect failure modes and trigger escalation

## Insights & Implications

### 1. Production Reliability is a Coordination Problem

**Implication:** The bottleneck for deploying multi-agent LLM systems is not base-model capability but coordination robustness. Investing in coordination architecture yields higher ROI than fine-tuning individual agents.

### 2. Determinism vs. Parallelism Tradeoff

**Insight:** There is a fundamental tension between system determinism and parallelism:
- Sequential coordination is deterministic but slow
- Parallel coordination is fast but non-deterministic (variations in execution order, network timing, etc.)

**For Production SE:** Accept some non-determinism at the optimization stage; enforce determinism at the deployment/merge stage.

### 3. Information Containment is Critical

**Insight:** Exposing all intermediate outputs from all agents to all downstream agents increases coordination surface area and cascading-error risk. By default, restrict agent visibility to only their direct predecessors in the coordination graph.

### 4. Coordination Configuration as a Runtime Parameter

**Implication:** Coordination structure shouldn't be hardcoded; it should be configurable per task or per deployment context. A simple task (e.g., "add a unit test") might use sequential coordination, while a complex task ("refactor authentication system") might use adaptive hierarchical.

### 5. Coordination Failures are System-Level Properties

**Insight:** Coordination failures can't be fixed by prompting individual agents. They require architectural intervention: changing the message graph, decision authority, or aggregation rules. This is a fundamental shift from the current agentic AI research focus on agent-level improvements.

## Advanced Concepts: Coordination Theory

### Information-Theoretic Perspective

The paper frames each coordination configuration as a channel through which agents communicate:
- **Sequential**: Single channel, one-way; information flows linearly
- **Parallel**: Multiple independent channels; information doesn't mix until aggregation
- **Hierarchical**: Hub-and-spoke; coordinator is a multiplexer
- **Reactive**: Broadcast channels with feedback; information propagates via events

Higher-entropy configurations (more feedback loops, more cross-talk) tend to exhibit more failure modes.

### Formal Verification

The paper hints at the potential for formal verification of coordination properties:
- Can we prove that a hierarchical coordination topology never reaches a deadlock state?
- Can we verify that a specific failure mode is impossible under a given configuration?
- Can we synthesize optimal coordination architecture for a given agent capability profile?

This remains open research.

## Related Work & Context

### Foundational Work

1. **Multi-Agent Reinforcement Learning (MARL):** Coordination in RL agents dates back decades; this work adapts coordination theory to LLM agents.
2. **Workflow Orchestration:** Tools like Prefect and Airflow coordinate tasks; this work brings formal orchestration concepts to agent reasoning.
3. **Formal Verification of Distributed Systems:** Techniques from Lamport and Dijkstra on consensus and synchronization inform the coordination formalization.

### Recent Related Papers

1. **"The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption"** (arXiv:2601.13671) — Enterprise-focused orchestration patterns
2. **"Beyond Individual Intelligence: Surveying Collaboration, Failure Attribution, and Self-Evolution in LLM-based Multi-Agent Systems"** (arXiv:2605.14892) — Broader survey of multi-agent collaboration
3. **"Adaptive Theory of Mind for LLM-based Multi-Agent Coordination"** (arXiv:2603.16264) — Theory-of-mind approaches to coordination

### Future Directions

1. **Automatic Coordination Synthesis:** Given agent capabilities and task requirements, automatically synthesize optimal coordination architecture
2. **Coordination Monitoring and Adaptation:** Runtime systems that detect coordination failures and reconfigure topology in real-time
3. **Coordination Benchmarks:** Standardized benchmarks for coordination performance across different problem domains
4. **Human-in-the-Loop Coordination:** Mixing human judgment with agent autonomy through structured coordination layers

## Code & Resources

### Official Repositories

- **Paper Code:** https://arxiv.org/abs/2605.03310 (public release includes traces and agent implementations)
- **Coordination Framework:** Available as open-source (details in paper appendix)

### Dependencies & Requirements

- LLM API access (tested with Claude 3.5+ and GPT-4)
- Python 3.10+
- Standard libraries: asyncio (for async orchestration), logging, dataclasses
- Experimental trace collection requires disk space (~500 MB per experiment)

### Quick-Start Integration Guide

1. **Define your agents** (inherit from `LLMAgent` base class)
2. **Specify coordination topology** using the `CoordinationLayer` class
3. **Run the orchestrator** which handles message passing, sync/async execution, aggregation
4. **Instrument logging** to trace inter-agent communication and detect failure modes
5. **Monitor determinism** by running identical tasks multiple times and comparing outputs

### Example: Hierarchical Code Review Coordination

```python
from coordination_layer import CoordinationLayer, SyncMode, HierarchicalDecision

# Define agents
planner = CodePlannerAgent()
coder = CodeGeneratorAgent()
reviewer = CodeReviewerAgent()

# Define coordination
coordination = CoordinationLayer(
  agents={'planner': planner, 'coder': coder, 'reviewer': reviewer},
  coordinator='planner',
  message_graph={
    'planner': ['coder', 'reviewer'],
    'coder': ['reviewer'],
    'reviewer': ['planner']
  },
  sync_regime=SyncMode.ASYNC,
  aggregation=HierarchicalDecision(
    decision_maker='planner',
    fallback_to_vote_if_conflict=True
  )
)

# Execute
result = coordination.run(task="Implement binary search in Python")
print(result.final_code)
print(result.coordinator_decision)
```

## Summary

This paper reframes multi-agent LLM system reliability as fundamentally a coordination problem, not a capability problem. By treating coordination as a configurable architectural layer with explicit design dimensions, practitioners can reason about failure modes and make principled tradeoffs between speed, parallelism, and determinism. The information-controlled empirical methodology proves that coordination defects, not agent weakness, account for the majority of production failures. For autonomous software engineering at scale, this work establishes coordination architecture as a first-class concern alongside agent reasoning capability.

**Key Takeaway:** Build deterministic, hierarchical coordination architecture first; add parallelism only where information independence permits; instrument the coordination layer to detect and recover from failure modes.
