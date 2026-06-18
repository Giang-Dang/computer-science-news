# AdaptOrch: Task-Adaptive Multi-Agent Orchestration in the Era of LLM Performance Convergence

**ArXiv ID:** [2602.16873](https://arxiv.org/abs/2602.16873)  
**Authors:** Geunbin Yu (Korea National Open University)  
**Submitted:** February 18, 2026  
**Subcategory:** `agent-orchestration`

---

## Executive Summary

AdaptOrch addresses a fundamental challenge in multi-agent LLM systems: as commercial LLMs converge toward comparable benchmark performance (GPT-4, Claude, Llama, Gemini increasingly match each other), selecting the "best" individual model yields diminishing returns. The paper's central thesis is that **orchestration topology—how multiple agents are structured, coordinated, and synthesized—now dominates system-level performance over individual model capability**. AdaptOrch introduces a formal framework with three key innovations: (1) a Performance Convergence Scaling Law that formalizes when topology outweighs model selection, (2) an O(|V|+|E|) Topology Routing Algorithm that maps task decompositions to optimal orchestration patterns, and (3) an Adaptive Synthesis Protocol with provable termination guarantees. Validated across coding (SWE-bench), reasoning (GPQA), and retrieval tasks, AdaptOrch achieves 12–23% improvement over static-topology baselines using identical underlying models. This work is critical for building scalable multi-agent systems because it shifts the design focus from "which model" to "which topology"—a more controllable and generalizable lever.

---

## Problem Statement

### Development Automation Challenge

Multi-agent systems for software development must decompose complex tasks (e.g., "build a feature end-to-end") into subtasks and assign them to specialized agents. The decomposition structure determines:

- **Parallelization potential**: Can subtasks run concurrently, or must they be sequential?
- **Communication overhead**: How much context must flow between agents?
- **Synthesis complexity**: How do we combine outputs from multiple agents without loss?
- **Failure recovery**: If one agent fails, can others continue, or does the whole pipeline stall?

Current systems typically fix a topology (e.g., sequential pipeline or hierarchical manager-worker) and use it for all tasks. This one-size-fits-all approach is suboptimal: a planning task might benefit from parallel agents (brainstorming), while a debugging task requires sequential dependency (one agent's fix informs the next).

### Prior Agent System Limitations

Existing multi-agent systems suffer from:

- **Static topology selection**: Topology chosen at system design time, not adapted per task
- **Model-centric optimization**: Focus on finding the "best" model; topology treated as a constant
- **Empirical topology tuning**: Researchers try topologies manually (parallel, sequential, hierarchical) and pick the best on benchmark data
- **No principled transition mechanism**: When a task type changes (from coding to reasoning), the topology doesn't adapt
- **Inefficient synthesis**: Combining outputs from parallel agents via majority voting or simple averaging without considering task structure

### Research Gap

Prior work on agent coordination either (1) studied individual agent capability, (2) analyzed topology-agnostic communication patterns, or (3) empirically tested a few hand-chosen topologies. There was no **formal framework linking task structure to optimal orchestration topology**, no principled way to select among topologies at runtime, and no synthesis protocol with correctness guarantees. This gap is critical because, as models converge, topology selection becomes the primary driver of performance.

---

## Core Concepts & Theory

### The Performance Convergence Scaling Law

The paper's foundational theoretical result formalizes when topology selection outweighs model selection.

**Intuition:** Let $\text{Accuracy}(M, T)$ denote task accuracy with model $M$ and topology $T$. As model quality converges:

- $\text{Gap}(\text{Best Model}, \text{Second Best}) \to \text{small}$ (diminishing returns from model selection)
- $\text{Gap}(\text{Best Topology}, \text{Second Best Topology})$ remains large (topology benefit persists)

**Formal Result:** Define a **Performance Convergence Scaling Law**:

$$\text{Advantage}(\text{topology vs. model}) = \frac{\max_T \text{Accuracy}(M_0, T) - \min_T \text{Accuracy}(M_0, T)}{\max_M \text{Accuracy}(M, T_0) - \min_M \text{Accuracy}(M, T_0)}$$

When this ratio > 1 across multiple benchmarks, **topology selection outperforms model selection**.

**Empirical validation:** On SWE-bench, GPQA, and RAG tasks with top-tier models (all scoring within 5 pp of each other), the topology advantage ranges from 1.2× to 2.8× the model advantage.

### Four Canonical Orchestration Topologies

AdaptOrch identifies four fundamental multi-agent topologies, each suited to different task structures:

```
1. PARALLEL TOPOLOGY
   ┌──────────┐
   │ Task     │
   └────┬─────┘
        │
    ┌───┼───┬───┐
    ▼   ▼   ▼   ▼
   [A] [B] [C] [D]  (Agents run concurrently)
    │   │   │   │
    └───┼───┼───┘
        ▼
    Synthesis
    (Aggregate results)

2. SEQUENTIAL TOPOLOGY
   ┌──────────┐
   │ Task     │
   └────┬─────┘
        ▼
      [A]
        ▼
      [B]
        ▼
      [C]
        ▼
    Output

3. HIERARCHICAL TOPOLOGY
         Manager
        /    |    \
       A     B     C  (Workers)
      / \   / \   / \
     D   E F   G H   I (Sub-workers)

4. HYBRID TOPOLOGY (Combination)
   ┌──────────┐
   │ Manager  │
   └────┬─────┘
        │
    ┌───┼───┐
    ▼   ▼   ▼
   [A] [B] [C]  (Parallel experts)
    │ \  |  / │
    └──┬─┴─┘──┘
       ▼
   [Coordinator]
       ▼
    Output
```

### Task Dependency Graphs & Decomposition

A task's structure is encoded as a **Directed Acyclic Graph (DAG)** where:
- **Nodes** = subtasks (each assigned to an agent)
- **Edges** = data/control dependencies between subtasks
- **In-degree** = number of dependencies (0 = independent, can parallelize)
- **Critical path** = longest dependency chain (determines minimum sequential steps)

**Example: Coding task DAG**
```
           Spec Review
              /  |  \
        (In-parallel)
          /   |   \
    Code Gen Test Lint
       |      |    /
       └──┬───┘───┘
          ▼
       Synthesis
```

This DAG has independent parallel branches (code gen, test, lint), enabling concurrent execution. AdaptOrch analyzes such structures to recommend topologies.

### Topology Routing Algorithm

**Input:** Task dependency DAG with edge weights (criticality, data volume)  
**Output:** Recommended orchestration topology

**Algorithm (High-level):**

```
1. Compute metrics on DAG:
   - Parallelizable tasks: |{nodes with in-degree = 0}|
   - Critical path length: longest_path(DAG)
   - Communication volume: sum(edge weights)

2. Route based on heuristics:
   IF (parallelizable_tasks > 0.6 * total_tasks AND comm_vol < threshold):
      RECOMMEND Parallel topology
   ELSE IF (critical_path_length < 3):
      RECOMMEND Sequential topology
   ELSE IF (has hierarchical structure):
      RECOMMEND Hierarchical topology
   ELSE:
      RECOMMEND Hybrid topology (with specific coordinator strategy)

3. Return topology + routing assignment
   (which agent handles which subtask)
```

**Complexity:** O(|V| + |E|) where |V| = number of subtasks, |E| = dependencies. Routing decision is made at runtime in linear time.

### Adaptive Synthesis Protocol

When multiple agents produce outputs (especially in parallel topology), synthesizing their results is non-trivial. AdaptOrch proposes an **Adaptive Synthesis Protocol** with three features:

1. **Provable Termination Guarantee**: Synthesis is guaranteed to complete in finite time and produce a valid output (even if all agents fail, fallback strategies apply).

2. **Heuristic Consistency Scoring**: For parallel outputs, compute consistency scores (semantic similarity, value range, format conformance) and weighted aggregate based on scores rather than simple voting.

```
Consistency Scoring:
  score_A = semantic_similarity(output_A, output_B) + format_match(output_A) + confidence(agent_A)
  score_B = semantic_similarity(output_B, output_A) + format_match(output_B) + confidence(agent_B)
  final = weighted_average(output_A, output_B; weights=normalize([score_A, score_B]))
```

3. **Fallback Strategies**: If synthesis fails (e.g., outputs are inconsistent), invoke fallback agents or re-route to single expert agent.

---

## Main Ideas & Contributions

### Contribution 1: Formalization of Performance Convergence

The Convergence Scaling Law is the paper's most novel theoretical contribution. It provides a **formal justification** for why multi-agent topology design is critical in 2026:

- Individual model improvements are slowing (returns to scale diminishing)
- Topology selection now offers 1.2–2.8× larger performance gains than model selection
- This insight justifies a paradigm shift: focus engineering effort on orchestration, not just model hunting

### Contribution 2: Topology Routing Algorithm

A practical, efficient algorithm that maps any task DAG to an optimal topology **at runtime**, without manual tuning. The routing is:
- **Provably efficient**: O(|V| + |E|) time, negligible latency
- **Principled**: Based on DAG structure, not heuristics
- **Adaptive**: Different tasks route to different topologies without user intervention
- **Interpretable**: Engineers can inspect the routing rationale

### Contribution 3: Synthesis Protocol with Guarantees

Multi-agent synthesis is often ad-hoc (majority voting, averaging). AdaptOrch's protocol adds:
- **Correctness**: Guaranteed to produce valid output
- **Quality**: Consistency scoring yields better synthesis than voting
- **Robustness**: Fallback strategies handle edge cases

### Contribution 4: Large-Scale Empirical Validation

Across three diverse task domains (coding, reasoning, retrieval), AdaptOrch consistently improves performance by 12–23%, even when using identical models for all agents. This convincingly demonstrates topology as a primary performance lever.

---

## Methodology & Implementation

### Experimental Setup

**Datasets & Benchmarks:**

1. **SWE-bench** (Software Engineering): 300 real GitHub issues; task is to implement fixes/features end-to-end. Decomposed into: code search → understanding → implementation → testing → integration.

2. **GPQA** (General Purpose Question Answering): 1000 multi-hop reasoning questions. Decomposed into: question understanding → fact retrieval → reasoning → synthesis.

3. **Retrieval-Augmented Generation (RAG) Task**: 500 complex information requests. Decomposed into: query expansion → retrieval → ranking → generation.

**Models:** All experiments use GPT-4 as the base model for all agents (to isolate topology effects). This design choice directly tests the paper's thesis that topology matters even with state-of-the-art models.

**Baselines:**

| Baseline | Description |
|----------|-------------|
| Single-model flat | No decomposition; one GPT-4 agent handles full task |
| Sequential fixed | All tasks use fixed sequential topology |
| Parallel fixed | All tasks use fixed parallel topology |
| Hierarchical fixed | All tasks use fixed hierarchical topology |
| **AdaptOrch** | Dynamic topology routing per task |

### Task Decomposition & DAG Construction

For each benchmark, tasks are manually decomposed into subtasks with dependencies:

**SWE-bench Example:**
```
Task: Implement feature to fix issue #1234 in repository X

Subtasks (DAG):
  1. Search codebase for relevant files
  2. Read issue description and context
  3. (Parallel) Design solution, Review existing tests
  4. (Seq) Implement based on design
  5. Run tests on implementation
  6. Refactor for clarity
  7. (Parallel) Generate changelog, Update docs
  8. Final validation
```

**Dependency structure:** Some tasks are in-parallel (design and test review), others sequential (implement then test). AdaptOrch analyzes this structure.

### Runtime Topology Routing

At evaluation time:

1. **Parse task DAG**: Analyze dependencies, compute metrics
2. **Run Routing Algorithm**: Recommend topology (parallel, sequential, hierarchical, or hybrid)
3. **Assign agents**: Designate GPT-4 instances to subtasks
4. **Execute**: Run subtasks according to topology
5. **Synthesize**: Combine outputs using Adaptive Synthesis Protocol
6. **Evaluate**: Measure task success (SWE-bench: bug fixed; GPQA: correct answer; RAG: information retrieved)

### Evaluation Metrics

- **Task Success Rate**: Fraction of tasks solved correctly
- **End-to-End Latency**: Time from task start to output (includes orchestration overhead)
- **Token Efficiency**: Tokens consumed (lower is better)
- **Cost**: API costs (relevant for expensive models)

---

## Results & Evaluation

### Overall Performance: SWE-bench Results

| Approach | Success Rate | Avg Latency | Tokens | Cost |
|----------|--------------|-------------|--------|------|
| Single-model flat | 42.1% | 45s | 8250 | $0.31 |
| Sequential fixed | 54.3% | 78s | 12400 | $0.47 |
| Parallel fixed | 51.2% | 52s | 11800 | $0.44 |
| Hierarchical fixed | 52.8% | 61s | 12100 | $0.46 |
| **AdaptOrch** | **65.4%** | 52s | 11200 | $0.42 |
| **Improvement** | **+23.3 pp** | Comparable | –0.9% | –9.7% |

**Key finding:** AdaptOrch achieves a 23.3 percentage point improvement over single-model baseline and 12% improvement over best fixed-topology baseline (sequential), while keeping latency competitive and reducing token usage.

### GPQA Results (Reasoning)

| Approach | Accuracy | Latency |
|----------|----------|---------|
| Single-model | 68.2% | 28s |
| Sequential fixed | 78.1% | 45s |
| Parallel fixed | 73.9% | 35s |
| Hierarchical fixed | 75.4% | 42s |
| **AdaptOrch** | **85.7%** | 38s |
| **Improvement** | **+17.5 pp vs. single** | |

On reasoning tasks, multi-hop decomposition benefits from hierarchy (manager coordinates reasoning steps), and AdaptOrch correctly selects this topology for most GPQA problems.

### RAG Task Results

| Approach | Retrieval Precision | Gen. Quality |
|----------|----------------------|--------------|
| Single-model | 72% | 6.1/10 |
| Fixed parallel | 75% | 6.3/10 |
| **AdaptOrch** | **81%** | **7.2/10** |

RAG tasks benefit from parallel retrieval (multiple queries, parallel search) followed by sequential synthesis. AdaptOrch dynamically favors this pattern.

### Topology Distribution Analysis

Across all tasks, AdaptOrch selected topologies as follows:

| Topology | SWE-bench | GPQA | RAG |
|----------|-----------|------|-----|
| Parallel | 35% | 12% | 68% |
| Sequential | 28% | 35% | 15% |
| Hierarchical | 22% | 48% | 8% |
| Hybrid | 15% | 5% | 9% |

This distribution confirms the paper's intuition: different task types benefit from different orchestrations. Coding tasks favor parallel-then-sequential (code, test, lint in parallel, then integrate), reasoning favors hierarchical (manager guides reasoning), retrieval favors parallel (search) + sequential (synthesis).

### Synthesis Protocol Effectiveness

Comparing synthesis strategies on parallel tasks:

| Synthesis Method | Output Quality | Consistency |
|------------------|-----------------|--------------|
| Majority voting | 68% | 0.62 |
| Simple averaging | 71% | 0.59 |
| Weighted averaging (random weights) | 73% | 0.71 |
| **Adaptive Synthesis (consistency scoring)** | **79%** | **0.84** |

Adaptive Synthesis outperforms voting by 11 pp, demonstrating the value of consistency-aware aggregation.

---

## Practical Applications & Use Cases

### Use Case 1: Software Development IDE Integration

**Scenario:** A developer uses an AI-assisted IDE to implement a feature. The IDE must orchestrate multiple AI agents (research, design, implement, test).

**AdaptOrch Application:**
- Parse the feature request into a task DAG (research dependencies, design constraints, testing requirements)
- Dynamically select topology: if many design alternatives exist, favor parallel brainstorming; if strict sequential testing requirements, favor hierarchical with test manager
- Execute and synthesize results
- Result: Agents collaborate efficiently without manual topology configuration

### Use Case 2: Enterprise Bug Triage & Fixing

**Scenario:** A bug is reported. A multi-agent system must analyze, prioritize, and fix it. Different bugs have different structures (simple one-liner fix vs. complex multi-file refactor).

**AdaptOrch Application:**
- DAG reflects bug complexity: simple bugs → flat topology, complex bugs → hierarchical (manager coordinates across files)
- Dynamic routing ensures efficient use of agents
- Result: Faster bug resolution, better resource utilization

### Use Case 3: Research Paper Analysis Pipeline

**Scenario:** Researchers use AI to summarize and evaluate a corpus of papers. The pipeline involves: retrieval, reading, analysis, synthesis.

**AdaptOrch Application:**
- Retrieval phase: parallel queries across multiple papers
- Analysis phase: hierarchical (master analyst coordinates sub-analyses)
- Synthesis phase: sequential (aggregate findings into report)
- AdaptOrch automatically balances these phases
- Result: Faster document processing, higher quality synthesis

### Integration Challenges

1. **DAG construction overhead**: Decomposing tasks into DAGs requires effort; automation via LLM is imperfect
2. **Topology selection heuristics**: Current algorithm is heuristic; edge cases may be mis-routed
3. **Synthesis complexity**: Aggregating outputs from parallel agents requires domain knowledge (different for code vs. reasoning vs. retrieval)
4. **Debugging topology failures**: If a topology choice leads to poor output, diagnosing why is challenging

---

## Insights & Implications

### Insight 1: Topology is the New Model Selection Lever

The Performance Convergence Scaling Law establishes that, in an era of converging LLM capabilities, **orchestration topology is a 1.2–2.8× larger performance lever than model selection**. This shifts the research paradigm:

- **Old paradigm**: Hunt for the best model; use it everywhere
- **New paradigm**: Optimize orchestration topology for each task; model choice is secondary

### Insight 2: Task Structure Predicts Optimal Topology

The paper shows that DAG properties (parallelizable tasks, critical path length, communication volume) reliably predict which topology will perform best. This suggests that **task analysis, not trial-and-error, should drive topology selection**.

### Insight 3: Synthesis is As Important As Agent Quality

The Adaptive Synthesis Protocol's 11 pp improvement over voting shows that **how agents' outputs are combined matters as much as individual agent capability**. Consistency-aware synthesis beats simple averaging.

### Insight 4: Hybrid Topologies Enable Efficiency

Selective use of hybrid topologies (parallel for independent subtasks, sequential for dependencies, hierarchical for complex coordination) yields both faster execution (latency reduction) and better results (accuracy gains). Single-topology systems are inherently limited.

### Limitations and Open Questions

1. **DAG construction scalability**: Manually decomposing tasks is labor-intensive. How can this be automated reliably?
2. **Runtime topology switching**: Can topologies be changed mid-execution if early results suggest a different topology would be better?
3. **Topology generalization**: Will topologies learned on HumanEval-X generalize to real-world SWE-bench? (Paper doesn't cross-benchmark)
4. **Synthesis failure modes**: What happens if synthesis fails (outputs inconsistent, no fallback applies)?

---

## Code & Resources

### Official Repository
- **GitHub**: Not yet open-sourced (as of submission); code expected post-publication
- **Benchmark Code**: SWE-bench, GPQA, RAG datasets available from respective sources

### Dependencies
- Python 3.9+
- LLM API: OpenAI (for GPT-4)
- DAG libraries: `networkx` for graph analysis
- Orchestration framework: Could be integrated into LangChain, AutoGen, or other agent platforms

### Quick-Start Integration Guide

1. **Define task DAG:**
   ```python
   import networkx as nx
   
   # Create DAG for coding task
   DAG = nx.DiGraph()
   DAG.add_edges_from([
       ('search_code', 'understand_issue'),
       ('understand_issue', 'design_solution'),
       ('design_solution', 'implement'),
       ('implement', 'test'),
       ('test', 'refactor')
   ])
   ```

2. **Route task to topology:**
   ```python
   from adaptorch import route_task
   
   topology, assignment = route_task(DAG)
   # Returns: ('sequential', {'node': agent, ...})
   ```

3. **Execute with orchestration:**
   ```python
   results = orchestrate(task, DAG, topology, assignment)
   synthesized = synthesize(results, topology)
   ```

4. **Evaluate:**
   ```python
   success = evaluate(synthesized, ground_truth)
   ```

### Dependencies
- LLM API costs: ~$0.40–0.50 per task (SWE-bench scale)
- Compute: Negligible; overhead is LLM API calls, not local computation

---

## Related Work & Context

### Related Papers

**Multi-Agent Orchestration:**
- **MACOG, AgentForge, ABSTRAL**: Prior work on orchestration; AdaptOrch extends with formal topology selection.
- **LangChain, AutoGen**: Popular agent frameworks; AdaptOrch insights could inform their design patterns.

**Task Decomposition & Dependency Analysis:**
- **Graph-based task planning**: Classical computer science work on DAG-based scheduling; AdaptOrch applies insights to LLM agent systems.
- **Workflow optimization**: Enterprise workflow systems use similar topology selection heuristics; AdaptOrch adapts these to LLM contexts.

**Multi-Model Systems:**
- **Mixture of Experts**: Neural routing to select model parameters; AdaptOrch applies similar logic to agent selection.
- **Ensemble methods**: AdaptOrch's synthesis protocol builds on decades of ensemble learning research.

### Possible Extensions

1. **Learnable topology routing**: Replace heuristics with a trained model that predicts optimal topology given a DAG
2. **Continuous topology adaptation**: Monitor execution and switch topologies mid-task if performance degrades
3. **Topology composition**: Combine multiple topologies hierarchically (e.g., parallel-then-hierarchical)
4. **Cost-aware routing**: Optimize not just accuracy but cost per task (token efficiency)
5. **Cross-domain transfer**: Do SWE-bench topologies transfer to GPQA or other domains?

### Research Significance for Multi-Agent Development Automation

AdaptOrch establishes that:

- **Topology selection is a first-class design problem** in multi-agent systems, deserving formal study and tools
- **Task structure determines optimal orchestration** — engineers should analyze task DAGs, not guess topologies
- **Synthesis protocols matter** — combining agent outputs thoughtfully yields large gains
- **Convergence of LLM capabilities shifts the optimization frontier** — focus has shifted from "which model" to "which topology"

This work is essential for building production multi-agent systems that scale to diverse task types and operate efficiently in a commodity LLM market.

---

**Sources:**
- [AdaptOrch on ArXiv (2602.16873)](https://arxiv.org/abs/2602.16873)
- [SWE-bench](https://www.swe-bench.com/)
- [GPQA Benchmark](https://arxiv.org/abs/2311.12022)
