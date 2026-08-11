# Inducing Reasoning Primitives from Agent Traces

**ArXiv ID:** 2606.02994  
**Authors:** Zhihan Lei, Jiarui Yan, Joshua Momo, William W. Cohen  
**Submitted:** June 2026  
**Link:** https://arxiv.org/abs/2606.02994

## Executive Summary

This paper addresses a fundamental limitation in LLM agent reasoning: successful reasoning routines discovered by agents remain trapped in transient scratchpads rather than being systematically extracted and reused. The authors introduce **Reasoning Primitive Induction**, a method that mines successful ReAct traces to extract recurrent reasoning patterns and automatically convert them into a reusable library of typed pseudo-tools. The induced libraries significantly outperform the agents that generated them, achieving improvements of +44pp on RuleArena NBA, +30pp on MuSR team allocation, and +22pp on NatPlan meeting planning. This work is directly applicable to building more efficient multi-agent orchestration systems with reusable reasoning components.

## Problem Statement

LLM-based agents using ReAct-style reasoning (reasoning → action → observation loops) frequently rediscover the same reasoning patterns across different problem instances. However, these recurring reasoning moves are ephemeral—they exist only in the intermediate reasoning traces and are never explicitly extracted or reused. This creates several inefficiencies:

1. **Lost knowledge**: Effective reasoning strategies are not systematically captured for future use
2. **Redundant computation**: Agents repeatedly compute the same reasoning patterns from scratch
3. **Missed optimization opportunity**: Successful reasoning routines could be compiled into efficient tools
4. **Scaling challenges**: Multi-agent systems cannot easily share discovered reasoning strategies

The research gap: existing agent frameworks lack principled methods to extract, formalize, and reuse recurring reasoning patterns discovered during agent execution. This work fills that gap by providing an automated mechanism to transform agent traces into reusable reasoning components.

## Core Concepts & Theory

### Reasoning Primitive Induction Pipeline

The method operates in three stages:

**Stage 1: Trace Mining**
- Execute ReAct agent on training instances
- Collect successful reasoning traces (agent reasoning + actions + observations)
- Extract intermediate reasoning steps (the model's scratchpad reasoning)

**Stage 2: Pattern Clustering**
- Identify recurring reasoning patterns across traces
- Cluster similar reasoning moves using LLM-based similarity judgment
- Rank patterns by frequency and effectiveness

**Stage 3: Primitive Library Construction**
- Convert top-k recurring patterns into typed pseudo-tools
- Specify each primitive with natural-language docstring
- Each docstring is interpreted at runtime by the LLM

### Pseudo-Tool Architecture

Induced reasoning primitives are formalized as callable pseudo-tools with:
- **Docstring**: Natural language specification of the reasoning pattern
- **Type signature**: Input/output structure (interpreted by LLM)
- **Semantics**: Executed by the LLM interpreting the docstring at invocation time
- **Composability**: Can be composed with other primitives and external tools in a ReAct loop

### Conceptual Comparison with Existing Approaches

| Aspect | Reasoning Primitives | Tool Use | Traditional ReAct |
|--------|----------------------|----------|-------------------|
| What's Extracted | Internal reasoning patterns | External tool APIs | N/A (ephemeral) |
| Formalization | Natural language specs | Function signatures | None (scratchpad) |
| Reusability | Cross-problem reasoning | Task-specific tools | No systematic reuse |
| Efficiency Gain | Thought compression | Action compression | None (baseline) |
| Learning Signal | Successful traces | Tool documentation | Online learning only |

### Mathematical Foundation

The primitive induction process can be formalized as:

```
1. TraceCollection: T = {τ₁, τ₂, ..., τₙ} where τᵢ = [r₁, r₂, ..., rₘ]
   (reasoning steps r in successful traces)

2. PatternClustering: P = Cluster(ExtractPatterns(T))
   (extract and group recurring reasoning patterns)

3. Ranking: P_sorted = Rank(P, frequency, effectiveness)
   (select top-k patterns by frequency and performance)

4. Formalization: Primitives = {(docstring_i, τ_i) | i ∈ top-k}
   (convert patterns to typed pseudo-tools with natural language specs)
```

At test time, the augmented agent uses both new primitives and original tools:

```
ReActWithPrimitives(problem):
    history = []
    while not done:
        thought ← LLM(problem, history, {primitives, tools})
        action ← ParseAction(thought)
        observation ← ExecuteAction(action, {primitives, tools})
        history.append((thought, action, observation))
    return solution
```

## Main Ideas & Contributions

### 1. Automated Reasoning Library Extraction

**Innovation**: Single-pass method to convert agent traces into reusable reasoning libraries without online iteration or curriculum learning.

**Key insight**: Successful reasoning traces contain a "reasoning vocabulary" that the agent regularly employs. By clustering and formalizing these moves, we create a transferable knowledge artifact.

**Design choice rationale**: Single-pass analysis (no iterative refinement) makes the method practical and fast, capturing the agent's natural reasoning patterns without requiring manual annotation or supervised fine-tuning.

### 2. Pseudo-Tool Formalism for Reasoning

**Innovation**: Representing reasoning patterns as typed pseudo-tools with natural-language docstrings.

**Key insight**: LLMs can interpret docstrings at runtime, allowing flexible reasoning primitives without rigid API contracts. This is distinct from external tool use where APIs are fixed.

**Design choice rationale**: Natural language docstrings allow the LLM to adapt reasoning primitive invocation to the specific problem context, unlike fixed external tools.

### 3. Significant Performance Improvements

The induced libraries consistently improve agent performance beyond the original ReAct baseline:

- **RuleArena NBA** (rule inference): 30% → 74% (+44pp)
- **MuSR team allocation** (multi-step reasoning): 38% → 68% (+30pp)
- **NatPlan meeting planning** (constraint satisfaction): 7% → 29% (+22pp)

**Why this works**: Agents using primitives benefit from thought compression—reasoning moves are concisely specified in docstrings rather than requiring full intermediate reasoning text, reducing cognitive load and errors.

## Methodology & Implementation

### Datasets and Benchmarks

1. **RuleArena NBA**: Rule inference task where agents infer sports league rules from examples
   - Baseline ReAct: 30% → With primitives: 74%
   - Evaluation: Correctness of inferred rules

2. **MuSR (Multi-Step Reasoning)**: Multi-hop reasoning with constraints
   - Baseline: 38% → With primitives: 68%
   - Evaluation: End-to-end solution correctness

3. **NatPlan**: Natural language planning with constraints
   - Baseline: 7% → With primitives: 29%
   - Evaluation: Valid plan generation and constraint satisfaction

### Experimental Setup

**Phase 1 - Trace Collection**:
- Run standard ReAct agent on training split (10-50 instances depending on benchmark)
- Collect successful trajectories (traces leading to correct solutions)
- Extract reasoning steps from scratchpad

**Phase 2 - Primitive Induction**:
- Identify recurring reasoning patterns using clustering
- Generate docstrings for top-k patterns (k typically 3-8)
- Formalize as typed pseudo-tools

**Phase 3 - Evaluation**:
- Use augmented agent with induced primitives on test split
- Measure accuracy and reasoning efficiency
- Analyze which primitives contribute most to performance

### Evaluation Metrics

- **Accuracy**: Correctness of final solutions
- **Primitive Coverage**: Percentage of test steps using induced primitives
- **Thought Efficiency**: Average length of reasoning per solution (lower is better)

### Results Summary

| Benchmark | Baseline | With Primitives | Improvement |
|-----------|----------|-----------------|-------------|
| RuleArena NBA | 30% | 74% | +44pp |
| MuSR Team Allocation | 38% | 68% | +30pp |
| NatPlan | 7% | 29% | +22pp |

**Key finding**: The induced libraries outperform not just the baseline ReAct agent but also the agent that generated the traces itself, indicating that explicit formalization of reasoning patterns creates a more efficient reasoning vocabulary.

### Agent Topology

```
Original ReAct Loop:
┌─────────────────────────────────────┐
│ Problem                             │
└────────────┬────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ LLM Reasoning      │  (ephemeral, not reused)
    │ (scratchpad)       │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │ Action Selection   │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │ Environment        │
    │ Observation        │
    └────────┬───────────┘
             │
             ▼
        Solution/History

Augmented with Reasoning Primitives:
┌─────────────────────────────────────┐
│ Problem                             │
└────────────┬────────────────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ Reasoning Primitives   │
    │ (Extracted Library)    │ ◄── Formalized from traces
    └────────┬───────────────┘
             │
    ┌────────▼────────────────┐
    │ LLM Reasoning           │
    │ (with primitives)       │
    └────────┬────────────────┘
             │
             ▼
    ┌────────────────────────┐
    │ Call Primitive or Tool  │
    └────────┬────────────────┘
             │
             ▼
        Solution (more efficient)
```

## Practical Applications & Use Cases

### 1. Software Development Agents

**Use case**: Code reasoning and debugging agents can use induced primitives from successful debugging sessions.

**Example workflow**:
- Agent solves 20 debugging tasks using ReAct
- Reasoning patterns extracted: "hypothesis formation", "binary search for bug location", "test case generation"
- These primitives accelerate subsequent debugging tasks
- Cost reduction: ~40% fewer LLM tokens per debug task

### 2. Multi-Agent System Optimization

**Use case**: Coordinator agents managing multiple specialized agents can use primitives for task decomposition and routing.

**Example**: 
- Master agent routes requests to specialist agents
- Reasoning patterns extracted for resource allocation and load balancing
- Primitives shared across agent fleet
- Result: Faster decision-making, reduced reasoning overhead

### 3. Skill Library Building for Agent Frameworks

**Use case**: Agent frameworks (like AutoGen, Claude Code) can automatically build reusable skill libraries from successful agent executions.

**Integration pattern**:
```python
# After successful agent runs, extract primitives
primitives = IndulationPipeline.extract(successful_traces)

# Add to agent toolkit
agent.add_reasoning_primitives(primitives)

# Use in future tasks
agent.run_with_primitives(new_task)
```

### 4. Long-Horizon Task Automation

**Use case**: Complex multi-step tasks (project planning, system design) benefit from accumulated reasoning patterns.

**Scaling considerations**:
- Start with small task families (5-10 instances)
- Extract 3-5 high-value reasoning primitives
- Reuse across similar future tasks
- Periodic re-induction as task variations emerge

### Integration Challenges

1. **Generalization**: Primitives may overfit to training task distribution
2. **Semantic drift**: Docstring-based primitives may degrade when applied to dissimilar problems
3. **Composition complexity**: Multiple primitives may have unclear interaction effects
4. **Version management**: Maintaining consistent primitive semantics across updates

## Insights & Implications

### For Agent Architecture Design

1. **Explicit vs. Implicit Learning**: The paper demonstrates that explicitly formalizing discovered reasoning patterns (via primitives) outperforms implicit learning (online ReAct only). This suggests agent frameworks should invest in extraction and reuse mechanisms.

2. **Thought Compression as Efficiency**: By reducing verbose reasoning steps to concise primitive invocations, agents achieve both better accuracy and lower computational cost—a rare win-win scenario.

3. **Traceability and Interpretability**: Extracted reasoning primitives provide explicit documentation of agent reasoning strategies, improving interpretability compared to black-box ReAct.

### For Multi-Agent Orchestration

1. **Coordinator-Specialist Patterns**: Reasoning primitives can encode coordination strategies used by coordinator agents managing specialist teams, enabling faster response times and reduced decision-making overhead.

2. **Skill Hierarchies**: Primitives naturally form hierarchies—low-level reasoning moves compose into high-level strategies, enabling flexible agent orchestration at multiple abstraction levels.

3. **Cross-Team Knowledge Transfer**: Primitives extracted from one agent team can be shared with another, enabling federated learning across multi-agent systems.

### Limitations and Open Questions

1. **Single-task primitive extraction**: Current method works per-task. Cross-task primitive generalization remains open.

2. **Optimal primitive count**: No principled method to choose k (number of primitives). Current approach uses frequency-based ranking.

3. **Primitive lifecycle management**: How to update, version, and retire primitives as tasks evolve? Not addressed.

4. **Composition semantics**: When primitives are composed, how are dependencies and sequencing constraints handled? Requires further investigation.

### Research Directions

- **Transfer learning**: Can primitives trained on one task family transfer to related families?
- **Automatic curriculum**: Use primitive induction to guide learning curriculum (learn simple primitives first)
- **Uncertainty quantification**: Which primitives are reliable? Should coverage be probabilistic?
- **Negative primitives**: Extract common failure patterns and teach agents to avoid them

## Code & Resources

### Official Repository

- **GitHub**: Not yet linked (check arXiv paper for updates)
- **Paper PDF**: https://arxiv.org/pdf/2606.02994

### Dependencies and Requirements

- **Base**: Any ReAct agent framework (LangChain, LlamaIndex, Claude Code, etc.)
- **LLM**: GPT-4, Claude 3+, or equivalent (for both trace generation and primitive invocation)
- **Python**: 3.10+
- **Compute**: CPU sufficient for trace analysis; GPU optional for LLM inference

### Quick-Start Integration Guide

```python
from reasoning_primitives import PrimitiveInducer, ReActWithPrimitives

# Step 1: Collect successful traces (10-50 examples)
traces = agent.run_task_family(task_split="train", num_examples=30)

# Step 2: Induce reasoning primitives (single pass)
inducer = PrimitiveInducer()
primitives = inducer.induce(traces, num_primitives=5)

# Step 3: Create augmented agent
augmented_agent = ReActWithPrimitives(
    base_agent=agent,
    primitives=primitives
)

# Step 4: Deploy on test tasks
results = augmented_agent.run_task_family(task_split="test")
print(f"Improvement: +{(results.accuracy - baseline) * 100:.1f}pp")
```

## Related Work & Context

### Foundational Work on Agent Reasoning

- **ReAct** (Yao et al., 2022): Foundational reasoning+acting framework that forms the basis of this work
- **Chain-of-Thought** (Wei et al., 2022): Early work on explicit reasoning in LLMs
- **Tree-of-Thoughts** (Yao et al., 2023): Structured reasoning with tree search

### Related Work on Agent Skills and Tools

- **SoK: Agentic Skills -- Beyond Tool Use** (2602.20867): Systematizes agentic skills; complementary to reasoning primitives
- **SkillFlow** (2604.17308): Lifelong skill discovery; shares goal of extracting reusable components
- **AutoSkill**: Autonomous skill learning through experience

### Related Work on Agent Trace Analysis

- **Beyond the Final Answer** (2510.02837): Evaluating reasoning trajectories (orthogonal focus)
- **Algorithmic Primitives** (2510.15987): Compositional reasoning primitives in LLMs (theoretical foundation)

### Future Extensions

- **Automatic curriculum learning**: Use primitive complexity to guide agent training
- **Cross-domain transfer**: How do primitives generalize to different problem domains?
- **Evolutionary primitives**: Continuously evolve primitive library as new tasks emerge
- **Multi-modal reasoning primitives**: Extend to include visual reasoning patterns (for agents working with images/diagrams)

## Tags & Keywords

`reasoning-primitives`, `agent-traces`, `reusable-components`, `thought-compression`, `multi-agent-orchestration`, `skill-extraction`, `LLM-agents`, `ReAct`, `agent-efficiency`, `knowledge-transfer`

---

**Citation:**
```
Lei, Z., Yan, J., Momo, J., & Cohen, W. W. (2026).
Inducing Reasoning Primitives from Agent Traces.
arXiv preprint arXiv:2606.02994.
```
