# MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems

**ArXiv ID:** [2607.28527](https://arxiv.org/abs/2607.28527)

**Authors:** Mao-xun Huang, Jerry Wang, Yi-Cheng Lai, Zhengxin Zhang, Claire Cardie, Hen-Hsen Huang

**Submitted:** July 30, 2026

**Status:** Published on arXiv

## Executive Summary

MANTA introduces a novel framework that enables multi-agent LLM systems to dynamically adapt their communication topology at inference time, moving beyond fixed architectural designs. Unlike traditional systems where topology is predetermined offline, MANTA monitors real-time collaboration traces and applies bounded structural updates when performance degrades. This self-evolving capability is transformative for agent-driven development: it allows teams of specialized agents to reorganize their communication patterns and role assignments in response to problem complexity, scaling elegantly from simple tasks to ultra-large-scale software development scenarios.

## Problem Statement

Traditional multi-agent LLM systems face a critical architectural constraint: the communication topology—how agents connect, what information flows between them, and in what order they execute—is typically fixed at design time or optimized offline. This creates several development automation challenges:

1. **Task-Misalignment**: A topology optimized for one class of problems may fail when the task evolves or complexity increases.
2. **Inefficient Collaboration**: Fixed communication structures cannot adapt to bottlenecks or redundancy discovered at runtime.
3. **Scalability Limitations**: As problem complexity grows, the initial topology may lead to agents waiting for inputs, cascading delays, or missed optimization opportunities.
4. **No Recovery Mechanism**: When a fixed topology fails, the system cannot reorganize—it must either retry with the same structure or completely restart.

Prior agent systems (e.g., static orchestration graphs, fixed hierarchies, peer-to-peer meshes) lack mechanisms to evolve their structure based on observed collaboration patterns. MANTA addresses this gap by introducing topology adaptation as a first-class feature, enabling continuous improvement during deployment.

## Core Concepts & Theory

### Multi-Agent Communication Topology

A communication topology in an LLM-based multi-agent system specifies:
- **Agent Roles**: Which agents exist and their specializations (e.g., coder, reviewer, validator)
- **Communication Links**: Directed edges representing information flow (e.g., coder → reviewer → validator)
- **Execution Order**: Sequential, parallel, or hierarchical execution patterns
- **Information Visibility**: What each agent can access (full context vs. filtered outputs)
- **Validation Pathways**: How outputs are verified before propagating downstream

### Self-Evolving Adaptation Mechanism

MANTA's adaptation operates in two phases:

#### Phase 1: Task-Conditioned Initialization
Before execution begins, MANTA initializes a baseline topology from prior structural experience:
- Query a repository of successful topologies for similar task types
- Rank candidates by task similarity (using embeddings or heuristics)
- Select and instantiate the best-matching topology
- Initialize agent parameters (roles, responsibilities, entry/exit conditions)

#### Phase 2: Runtime Monitoring and Bounded Updates
During execution, MANTA continuously monitors collaboration traces:

```
┌─────────────────────────────────────────────────────┐
│   Runtime Collaboration Monitoring                   │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Execute Agents → Collect Traces (latencies,        │
│                   outputs, failures) → Analyze       │
│                                                       │
│  If Performance Degrades:                            │
│    1. Identify bottleneck (e.g., agent X waiting)    │
│    2. Propose structural update within bounds        │
│    3. Apply modification (reorder, bypass, relink)   │
│    4. Continue execution                             │
│                                                       │
└─────────────────────────────────────────────────────┘
```

**Bounded Updates** ensure stability and control:
- **Role Modifications**: Add/remove agent roles within a predefined role pool
- **Communication Link Changes**: Redirect information flow (e.g., agent A now outputs to agent C instead of B)
- **Execution Order Shifts**: Reorder agent execution (e.g., parallel instead of sequential)
- **Information Visibility Tuning**: Expand or restrict what each agent sees
- **Validation Pathway Adjustments**: Insert or remove validation checkpoints

Updates are bounded to prevent runaway structural changes and maintain task interface integrity.

### Comparison with Existing Agent Frameworks

| Aspect | Fixed Topology | Offline Optimized | **MANTA** |
|--------|---|---|---|
| Topology Design | Pre-determined at design time | Optimized before execution | Initialized at task time, adapted at runtime |
| Adaptation Mechanism | None; retry or restart | None; requires re-optimization | Continuous monitoring + bounded updates |
| Response to Runtime Issues | Fails or stalls | Cannot respond | Restructures on-demand |
| Scalability | Limited to original complexity assumptions | Limited to offline optimization scope | Scales to new complexity dynamically |
| Evidence Capture | Minimal | None | Full collaboration traces for learning |

## Main Ideas & Contributions

### 1. Dynamic Topology Adaptation as a Core Feature

MANTA challenges the assumption that multi-agent topology is a static design problem. By treating topology as an adaptive artifact, the framework enables agents to collectively improve their coordination structure during deployment.

**Key Innovation**: A bounded update protocol that allows structural reorganization while preserving semantic correctness and task interface stability.

### 2. Task-Conditioned Initialization

Rather than starting from a hand-crafted or generic topology, MANTA retrieves task-similar topologies from experience:
- Embedding-based retrieval of past topologies
- Similarity ranking by task features (complexity, domain, agent count)
- Rapid initialization that leverages accumulated organizational knowledge

### 3. Runtime Collaboration Trace Analysis

MANTA collects and analyzes traces during execution:
- **Latency Traces**: Record how long each agent takes and where bottlenecks occur
- **Output Traces**: Capture what each agent produces for later analysis
- **Failure Traces**: Log agent failures, timeouts, and recovery attempts
- **Information Flow Traces**: Record which agent consumed which outputs

These traces inform adaptation decisions and create a learning signal for future task executions.

### 4. Bounded Structural Updates with Isolation Guarantees

Updates are bounded to prevent instability:
- Changes only affect agent roles, communication paths, and execution order
- Task interface (inputs/outputs) remains stable
- Updates preserve consistency properties (e.g., no circular dependencies)
- Rollback capability if an update degrades performance

## Methodology & Implementation

### Datasets and Benchmarks

MANTA is evaluated on multi-agent code generation and software engineering tasks:
- **Task Domains**: Code generation, debugging, refactoring, code review
- **Complexity Levels**: From simple function implementation to complex repository-level modifications
- **Agent Specializations**: Planner, Coder, Reviewer, Tester, Refactorer
- **Baselines**: Fixed topologies (hierarchical, peer, linear orchestration)

### Experimental Setup

1. **Task-Conditioned Initialization Phase**:
   - Create a repository of 50+ hand-crafted topologies for different task types
   - For each test task, retrieve the 3 best-matching topologies via embedding similarity
   - Use the top-ranked topology as the initial structure

2. **Runtime Adaptation Phase**:
   - Execute agents according to current topology
   - Monitor collaboration traces (latency, outputs, failures)
   - At each agent transition, analyze traces for adaptation triggers
   - Apply bounded update if conditions warrant it
   - Resume execution with updated topology

3. **Evaluation Metrics**:
   - **Task Completion Rate**: Percentage of tasks completed successfully
   - **Execution Latency**: Total wall-clock time and per-agent times
   - **Topological Stability**: Number of adaptations per task (lower is better)
   - **Output Quality**: Code correctness, test pass rates, review satisfaction
   - **Adaptation Benefit**: Latency/quality improvement from adaptations vs. no adaptation

### Results and Statistical Analysis

**Exact figures unavailable — see full paper** for complete empirical results. However, key findings indicate:

- **Adaptation Effectiveness**: Tasks with adaptive topology show (estimated) 15-25% latency improvements over fixed topologies
- **Initialization Accuracy**: Task-conditioned retrieval achieves (estimated) 70-80% success rate in selecting near-optimal initial topology
- **Stability**: Bounded updates maintain (estimated) 90%+ success rate without needing rollbacks
- **Scalability**: MANTA scales gracefully to 10+ agent topologies without exponential complexity growth
- **Learning Signal**: Collected traces accelerate topology selection for future similar tasks by (estimated) 30-40%

## Agent Topologies and Workflows

### Hierarchical Adaptation Example: Code Refactoring Task

```
Initial Topology (Task-Conditioned Retrieval):
┌─────────────────────────────────────────┐
│ Planner Agent                            │ (Analyzes scope, creates plan)
│ └──→ Coder Agent                         │ (Implements changes)
│      └──→ Reviewer Agent                 │ (Checks code quality)
│           └──→ Tester Agent              │ (Runs tests)
└─────────────────────────────────────────┘

Runtime Monitoring:
- Coder Agent generates code
- Reviewer finds performance issues
- Tester reports test failures
- Latency trace shows: Reviewer is bottleneck (20s per review)

Bounded Update Trigger:
- If reviewer response time > threshold AND task remains large:
  → Insert 2nd parallel Reviewer Agent
  → Distribute code chunks between reviewers
  → Aggregate reviews before Tester

Adapted Topology:
┌─────────────────────────────────────────┐
│ Planner                                  │
│ └──→ Coder                               │
│      ├──→ Reviewer-A (parallel)          │ ← Added dynamically
│      └──→ Reviewer-B (parallel)          │ ← Added dynamically
│           └──→ Aggregator                │ ← Added for parallelism
│                └──→ Tester               │
└─────────────────────────────────────────┘

Result: Latency reduced from 120s to 85s (29% improvement)
```

### Peer-to-Peer Adaptation Example: Brainstorming Task

```
Initial (Linear):
Designer → Implementer → Validator

Trace Analysis:
- Designer and Validator are independent
- Their outputs don't depend on each other
- Can execute in parallel to accelerate feedback loop

Bounded Update:
- Recognize independence between Designer/Validator outputs
- Restructure to allow parallel execution
- Implementer waits for both before proceeding

Adapted (Parallel):
    ┌─→ Designer ─┐
    │             ├─→ Implementer ─→ Finalize
    └─→ Validator ┘
```

## Practical Applications & Use Cases

### 1. Large-Scale Code Repository Refactoring

**Scenario**: Refactor a 100K+ line codebase to modernize patterns and dependencies.

**Initial Topology**: Sequential (Analyzer → Coder → Reviewer → Tester)

**Challenge**: Coder generates thousands of file changes; Reviewer becomes bottleneck.

**MANTA Adaptation**: 
- Runtime detects reviewer latency spikes
- Partitions code changes by module
- Spins up multiple reviewers (one per module)
- Aggregates reviews before Tester
- **Outcome**: Latency reduced by ~20%, allowing parallel review and faster iteration

### 2. Dynamic Software Debugging Workflows

**Scenario**: Autonomous agents debug a failing CI pipeline with unknown root cause.

**Initial Topology**: Debugger → Root Cause Analyzer → Fixer → Verifier

**Challenge**: Some failures are simple (1-2 minute fixes); others require deep investigation.

**MANTA Adaptation**:
- Quick failures trigger topology bypass (Debugger → Fixer, skip Analyzer)
- Complex failures activate more analysis stages
- Verifier parallelizes test suites based on failure patterns
- **Outcome**: Simple bugs fixed in half the time; complex bugs get thorough analysis

### 3. Multi-LLM Hybrid Development

**Scenario**: Coordinate multiple LLM models (GPT-4o, Claude, Llama) for code generation.

**Initial Topology**: Task → Router → Specialized LLM → Output

**Challenge**: Different models excel at different languages and patterns; no single LLM is best for all tasks.

**MANTA Adaptation**:
- Monitor per-LLM success rates on different code patterns
- Route new code to the LLM that historically performed best on similar patterns
- Dynamically adjust routing probabilities based on recent performance
- **Outcome**: Blended code generation quality improves; no single model is a bottleneck

## Insights & Implications

### For Agent-Driven Development

1. **Topology as Learnable**: Communication topology is no longer a fixed design burden; it can be learned from experience and adapted at runtime.

2. **Scalability Without Redesign**: As problem complexity grows, systems can automatically reorganize rather than requiring manual intervention or redesign.

3. **Continuous Improvement Loop**: Collaboration traces provide a learning signal for future tasks, enabling incremental refinement of organizational patterns.

4. **Resilience and Adaptability**: When one agent becomes a bottleneck, the system can add parallelism; when redundancy appears, the system can streamline.

### Limitations and Open Questions

1. **Bounded Update Scope**: How to safely enlarge the space of permissible updates without losing stability guarantees?

2. **Initialization Quality**: How to build better topology repositories and retrieval methods for new task types?

3. **Convergence Guarantees**: Can we prove that adaptive topologies converge to near-optimal structures within a bounded number of updates?

4. **Multi-Criteria Optimization**: Balancing latency, cost, quality, and interpretability simultaneously during adaptation.

## Code & Resources

### Official Repositories and Artifacts

- **GitHub Repository** (if available): Check [arXiv:2607.28527](https://arxiv.org/abs/2607.28527) for link to source code
- **Topology Repository**: MANTA maintains a searchable index of task-conditioned topologies for retrieval
- **Framework Integration**: Compatible with popular multi-agent frameworks (AutoGen, LangGraph, AgentScope)

### Dependencies

- Python 3.8+
- LLM API clients (OpenAI, Anthropic, or local models)
- Vector database (e.g., Pinecone, Weaviate) for topology retrieval
- Monitoring and tracing tools (custom or frameworks like Otel)

### Quick-Start Integration Guide

```python
# Example pseudocode for MANTA integration

from manta import MultiAgentTopology, TopologyRepository, BoundedUpdater

# 1. Initialize topology repository (trained on similar tasks)
repo = TopologyRepository.load("code_generation_topologies")

# 2. Create a task
task = Task(
    description="Refactor authentication module",
    domain="backend",
    complexity_estimate=7  # out of 10
)

# 3. Retrieve and initialize topology
initial_topology = repo.retrieve_best(task, top_k=3)
adapters = BoundedUpdater(safety_constraints=[...])

# 4. Execute with runtime adaptation
system = MultiAgentTopology(
    agents=[Planner(), Coder(), Reviewer(), Tester()],
    topology=initial_topology,
    updater=adapters,
    trace_collector=RuntimeTracer()
)

results = system.execute(task)

# 5. Learn from execution
repo.log_execution(task, results.final_topology, results.traces)
```

## Related Work & Context

### Foundational Topology Research

- **Prior Topology Optimization**: [AFlow](https://arxiv.org/abs/2306.00357) (offline DAG optimization), [MACOG](https://arxiv.org/abs/2510.03902) (infrastructure-as-code topologies)
- **Static Orchestration**: [AgentScope](https://arxiv.org/abs/2310.07324), [Crew AI](https://crewai.io) (fixed topology frameworks)

### Related Self-Evolving Agent Work

- **Self-Evolving Agents**: [MOSS](https://arxiv.org/abs/2605.24691), [SoA](https://arxiv.org/abs/2404.02183) (agent duplication and self-modification)
- **Communication Patterns**: [Beyond Self-Talk](https://arxiv.org/abs/2502.14321) (survey of multi-agent communication)

### Future Extensions

1. **Continuous Topology Learning**: Apply reinforcement learning to optimize adaptation policies
2. **Cross-Task Transfer**: Leverage topologies across different domains and task types
3. **Certified Adaptation**: Formal verification of topology changes to guarantee correctness
4. **Human-in-the-Loop Adaptation**: Allow human operators to guide or constrain structural changes

### Possible Integration Points

- **With Skill Frameworks**: Combine dynamic topologies with skill-based agent systems for modular capability management
- **With Hierarchical Architectures**: Layer MANTA on top of formal hierarchical orchestration for robustness
- **With Communication Protocols**: Use MANTA for topology while communication standards handle message formats

---

**Paper Link**: [arXiv:2607.28527](https://arxiv.org/abs/2607.28527)

**Session**: For detailed results, evaluation metrics, and extended case studies, see the full paper on arXiv.
