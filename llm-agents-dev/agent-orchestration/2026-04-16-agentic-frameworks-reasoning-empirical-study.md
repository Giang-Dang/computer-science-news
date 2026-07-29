# Agentic Frameworks for Reasoning Tasks: An Empirical Study

**Authors:** Zeeshan Rasheed, Abdul Malik Sami, Muhammad Waseem, Kai-Kristian Kemell, Mika Saari, Pekka Abrahamsson (Tampere University, Finland)

**ArXiv ID:** 2604.16646

**Submitted:** April 16, 2026

---

## Executive Summary

This paper presents a systematic empirical evaluation of 22 widely-used agentic frameworks across three reasoning benchmarks (BBH, GSM8K, ARC), addressing the critical gap in understanding which frameworks are suitable for real-world applications. Rather than benchmarking individual LLM capabilities, this study focuses on how different framework architectures affect agent reasoning performance, execution efficiency, and computational cost. The findings reveal that orchestration design—not underlying model capabilities—is often the limiting factor in agent system performance.

---

## Problem Statement

### Development Automation Challenge

As LLM-based agentic systems proliferate for software engineering tasks, practitioners face a critical decision: which agent framework best balances reasoning performance, efficiency, and maintainability? The problem is compounded by the rapid evolution of frameworks and the heterogeneous design choices made across them.

### Prior Limitations

Existing evaluations either:
- Focus on single-task or domain-specific benchmarks
- Test only a handful of frameworks
- Don't measure practical metrics like execution time and computational cost
- Fail to characterize how framework design affects reasoning capabilities

### Research Gap

No systematic comparison existed that evaluated multiple frameworks under unified experimental conditions, measuring reasoning accuracy alongside efficiency metrics essential for production deployment.

---

## Core Concepts & Theory

### Agentic Framework Architecture

An agentic framework is a software system that wraps an LLM with:
1. **Planning mechanisms** - decompose goals into subtasks
2. **Tool invocation** - call external APIs, code, or environments
3. **Iterative refinement** - evaluate results and adapt
4. **State management** - track agent progress and context

### Framework Classification Taxonomy

The study developed a taxonomy based on architectural design dimensions:

```
Frameworks
├── Planning Strategy
│   ├── Reactive (immediate tool calls)
│   ├── Sequential (linear planning)
│   ├── Hierarchical (goal decomposition)
│   └── Adaptive (dynamic re-planning)
├── Tool Integration
│   ├── Function calling
│   ├── Plugin system
│   ├── API-based
│   └── Native integration
├── Reasoning Loop
│   ├── Single-step
│   ├── Multi-step iteration
│   └── Reflexive loops
└── Orchestration
    ├── Monolithic LLM
    ├── Multi-agent coordination
    └── Role-based specialization
```

### Framework Comparison Dimensions

**Architectural Patterns:**
- **Agent-centric:** Single agent with multiple tools (e.g., ReAct pattern)
- **Hierarchy:** Meta-agent coordinating sub-agents (e.g., hierarchical planning)
- **Pipeline:** Sequential stages with specialized agents (e.g., planning → execution → verification)
- **Ensemble:** Multiple agents voting or collaborating in parallel

**Capability Binding:**
- Static tool definitions loaded at startup
- Dynamic tool discovery and composition
- Skill-based modular capabilities
- Runtime tool generation

---

## Main Ideas & Contributions

### Key Contribution 1: Systematic Framework Evaluation

**What was studied:**
- 22 frameworks selected from 1,200 GitHub repositories (Jan 2023 - July 2025)
- Standardized evaluation across three reasoning benchmarks
- Measurement of reasoning accuracy, execution time, and computational cost

**Framework Coverage:**
The 22 frameworks represent the diversity of approaches in the ecosystem, including:
- LangChain agents
- AutoGPT derivatives
- Claude Agent SDK approaches
- Custom orchestration systems
- Multi-agent specialized frameworks

### Key Contribution 2: Orchestration-First Insight

**Critical Finding:** Orchestration design is often the bottleneck, not individual LLM reasoning capability.

The study demonstrates that:
- Two frameworks using the same underlying LLM can have dramatically different accuracy (e.g., 82% vs 45%)
- Execution time varies by 3-5x across frameworks on identical tasks
- Cost per task ranges from 0.14¢ to 2.30¢ for the same reasoning work

**Implication:** Framework selection has as much impact on agent effectiveness as model selection.

### Key Contribution 3: Consistency as a Design Criterion

**Consistency metric:** Does a framework maintain comparable performance across different reasoning domains?

Findings:
- 12 of 22 frameworks showed consistent performance (±2% accuracy variance)
- 10 frameworks exhibited high variance, suggesting specialized but brittle designs
- Consistent frameworks average: 74.6–75.9% accuracy, 4–6 seconds, 0.14–0.18¢ per task

---

## Methodology & Implementation

### Experimental Setup

**Benchmarks Selected:**

1. **BigBench Hard (BBH)** - 23 challenging reasoning tasks
   - Arithmetic, word problems, logical reasoning
   - Requires multi-step decomposition
   
2. **GSM8K** - 8,500 grade school math word problems
   - Tests numerical reasoning and problem decomposition
   - Canonical benchmark for reasoning agents
   
3. **ARC (AI2 Reasoning Challenge)** - 7,787 multiple-choice science questions
   - Tests world knowledge and analogical reasoning
   - Mix of easy and challenge splits

**Unified Experimental Conditions:**
- Same hardware environment (A100 GPUs where applicable)
- Standardized prompts across frameworks
- Identical LLM configuration (temperature=0 for determinism)
- Timeout limits (300 seconds per task)

### Framework Execution Pipeline

```
Input Task
    ↓
Framework Initialization
    ├─ Load framework dependencies
    ├─ Configure planning module
    └─ Bind tool/skill definitions
    ↓
Agent Planning Loop
    ├─ Decompose goal into sub-goals
    ├─ Select tool/skill
    ├─ Execute with context
    ├─ Parse and evaluate result
    └─ Decide: continue or terminate?
    ↓
Result Extraction & Evaluation
    ├─ Extract final answer
    ├─ Compare with ground truth
    └─ Record metrics (accuracy, time, cost)
```

### Metrics & Measurement

**Primary Metrics:**
1. **Reasoning Accuracy** - percentage of tasks with correct final answer
2. **Execution Time** - wall-clock seconds from task start to completion
3. **Computational Cost** - API charges and compute resource utilization ($/task)
4. **Consistency** - accuracy variance across the three benchmarks

**Secondary Metrics:**
- Planning steps per task
- Tool invocation count
- Failure modes and error types
- Memory utilization

### Results and Statistical Analysis

**Overall Performance Summary:**

| Metric | Best | Worst | Mean | StdDev |
|--------|------|-------|------|--------|
| Accuracy (%) | 89.2 | 12.4 | 62.3 | 18.7 |
| Execution Time (s) | 2.1 | 47.3 | 12.8 | 11.2 |
| Cost per Task (¢) | 0.08 | 2.50 | 0.51 | 0.52 |

**Consistent Performers (n=12):**
- Accuracy: 74.6–75.9% (σ < 2%)
- Execution Time: 4–6 seconds
- Cost: 0.14–0.18¢ per task

**Problem Frameworks (n=10):**
- High variance across benchmarks
- Frequently exceed timeout
- Often fail at intermediate planning steps

**Framework Failure Analysis:**

Breakdown of failure modes:
- **Orchestration issues (42%):** Framework fails to properly sequence steps or handle tool outputs
- **Context management (28%):** Loss of relevant context in multi-step reasoning
- **Tool selection (18%):** Incorrect tool invocation or misuse
- **Timeout/resource (12%):** Execution exceeded time or memory limits

### Agent Topologies Observed

**Reactive Agent Pattern:**
```
Input → Tool Selection → Tool Execution → Output
  ↑─────────────────────────────────────────┘
           Direct single-step response
```

**Sequential Planning Pattern:**
```
Input → Plan Generation → Step 1 → Step 2 → Step 3 → Output
         ↑ Re-plan on failure feedback
```

**Hierarchical Pattern:**
```
Input → Meta-Agent Planning
         ├─ Subtask 1 → Specialist Agent → Result
         ├─ Subtask 2 → Specialist Agent → Result
         └─ Subtask 3 → Specialist Agent → Result
         ↓
      Result Synthesis → Output
```

---

## Practical Applications & Use Cases

### Direct Software Development Applications

1. **Code Generation & Debugging**
   - Framework choice affects code quality and iteration cycles
   - Consistent frameworks generate more reliable scaffolding for multi-file projects

2. **Test Generation**
   - Reasoning benchmarks correlate with test coverage and edge-case detection
   - Framework efficiency impacts test generation throughput

3. **Documentation Generation**
   - Multi-step reasoning needed to understand code structure
   - Execution time directly affects developer workflow

4. **Refactoring Recommendation**
   - Cost-efficiency critical when processing large codebases
   - Consistency ensures predictable behavior across different code domains

### Concrete Example: Bug Analysis Workflow

A framework orchestrating bug analysis:
```
Bug Report Input
├─ Code Retrieval Specialist: Fetch relevant files (max 3 attempts)
├─ Syntax Analysis Agent: Identify type errors and patterns
├─ Test Case Agent: Generate minimal reproducers
├─ Hypothesis Agent: Propose root cause (with reasoning)
└─ Fix Agent: Generate patches with justification

Framework Choice Implications:
- Consistent framework: 74.6% accuracy, 5.2s, 0.16¢
- Inconsistent framework: 45.3% accuracy, 18.7s, 0.68¢
- Impact: 65% more accurate bugs caught, 3.6x faster, 4.25x cheaper
```

### Integration Challenges

- **Framework coupling:** Switching frameworks requires re-tuning prompts and tool bindings
- **Version instability:** Framework APIs evolve rapidly; production systems need stability guarantees
- **Skill/tool portability:** Not all frameworks have equal support for tool composition
- **Cost predictability:** Variable execution paths make budgeting difficult

### Scalability Considerations

- Large-scale analysis of thousands of tasks benefits from frameworks with predictable execution time
- Streaming/online learning scenarios require frameworks supporting incremental planning
- Multi-tenant systems need frameworks with isolated context management

---

## Insights & Implications

### Advancement in Autonomous Development Systems

1. **Framework maturity matters more than model capability**
   - Architectural decisions outweigh LLM choice
   - Practitioners should invest in framework engineering

2. **Consistency is a competitive advantage**
   - Consistent frameworks enable reliable automation at scale
   - Enables accurate cost prediction and SLA guarantees

3. **Orchestration is the optimization frontier**
   - Tuning planning strategies shows higher ROI than model fine-tuning
   - Tool binding and sequencing are critical design points

### Limitations and Open Questions

1. **Limited to reasoning tasks**
   - Results may not generalize to embodied agents or continuous learning systems
   - Code generation specifically may require different orchestration patterns

2. **Snapshot evaluation**
   - Frameworks evolve rapidly; results become stale
   - Need continuous evaluation infrastructure

3. **Simplified tool environments**
   - Real software engineering involves complex API interactions
   - Error recovery and exception handling not fully tested

4. **Single-turn evaluation**
   - Multi-turn interactions (refinement, iteration) not benchmarked
   - Developer feedback loops not captured

### Relevance to Skill Frameworks and Agent Topologies

- Framework choice determines whether skills can be reused across tasks
- Consistent frameworks enable reliable skill discovery and composition
- Modular topologies (multi-agent) show better skill reusability than monolithic agents

---

## Code & Resources

### GitHub Repositories Evaluated

The study analyzed 22 frameworks from public repositories, though specific framework links vary by version. Key frameworks included:

- **LangChain:** Extensive agent implementations across multiple domains
- **AutoGPT:** Pioneering multi-step planning approach
- **CrewAI:** Role-based multi-agent orchestration
- **Claude Agent SDK:** Specialized integration for Claude models
- **Custom implementations:** Research-specific frameworks

### Dependencies and Requirements

**Core Dependencies:**
- Python 3.9+
- LLM API access (OpenAI, Anthropic, others depending on framework)
- Standard libraries: requests, json, logging

**Compute Requirements:**
- GPU optional but recommended for embedding-heavy frameworks
- Typical task: 2-6GB RAM, <10s execution
- API costs: 0.14–0.18¢ per task for consistent frameworks

### Quick-Start Integration Guide

To evaluate a framework against reasoning benchmarks:

```python
from framework import Agent, tools

# Initialize agent with framework
agent = Agent(
    tools=[code_search, execute, reasoning],
    planning_strategy="hierarchical",
    max_iterations=10
)

# Run reasoning task
result = agent.solve(
    task="Solve this problem step by step",
    benchmark="GSM8K",
    timeout_seconds=300
)

# Metrics collection
metrics = {
    "accuracy": result.correct,
    "execution_time": result.elapsed_seconds,
    "cost": result.api_cost,
    "consistency_score": result.variance_across_domains
}
```

---

## Related Work & Context

### Foundational Work

- **ReAct (Reasoning + Acting):** Seminal work showing interactive reasoning improves LLM performance
- **Chain-of-Thought Prompting:** Foundation for multi-step reasoning
- **Tool Use in LLMs:** Early exploration of LLM tool invocation capabilities

### Related Framework Papers

1. **From Static Templates to Dynamic Runtime Graphs** (arXiv:2603.22386)
   - Workflow optimization for LLM agents
   - Complements this study with dynamic topology selection

2. **ABSTRAL: Automated Multi-Agent System Design** (arXiv:2603.24885)
   - Automatic agent topology design
   - Builds on framework evaluation to guide architecture selection

3. **Agentic Design Patterns: A System-Theoretic Framework** (arXiv:2601.27087)
   - Theoretical foundations for agent orchestration
   - Provides conceptual vocabulary for framework comparison

### Future Research Directions

1. **Continuous Evaluation Infrastructure**
   - Automated benchmarking as frameworks evolve
   - Real-time framework recommendation system

2. **Framework Co-Design**
   - Optimize framework-specific prompting strategies
   - Develop domain-specific orchestration patterns

3. **Hybrid Approaches**
   - Combine strengths of multiple frameworks
   - Adaptive framework selection based on task characteristics

4. **Multi-Modal Reasoning**
   - Extend evaluation to code, vision, and multi-step planning
   - Measure framework support for heterogeneous tool types

---

## Summary

This empirical study provides practitioners with critical guidance for framework selection in agentic development systems. By demonstrating that orchestration design is often the limiting factor—not LLM capability—the paper elevates the importance of framework engineering. The consistency metric introduced here offers a practical way to assess framework reliability for production systems. The finding that 12 of 22 frameworks achieve 74.6–75.9% accuracy with predictable costs provides a baseline for what robust agent orchestration can achieve and opens the door to further optimization within this consistent subset.

