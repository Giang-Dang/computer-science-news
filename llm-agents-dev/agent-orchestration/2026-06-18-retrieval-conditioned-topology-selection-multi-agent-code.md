# Retrieval-Conditioned Topology Selection with Provable Budget Conservation for Multi-Agent Code Generation

**ArXiv ID:** [2605.05657](https://arxiv.org/abs/2605.05657)  
**Authors:** Abhijit Talluri, Pujith Anne, Bhagavan Choudary Pendiyala, Raghavendra Chilukuri  
**Submitted:** May 7, 2026  
**Category:** CS.CL - Computation and Language

## Executive Summary

Retrieval-Guided Adaptive Orchestration (RGAO) addresses a critical bottleneck in multi-agent code generation: the optimal orchestration topology depends on the structural complexity of the code being modified, yet existing systems select topologies statically or heuristically. RGAO closes this loop by extracting structural complexity vectors from hierarchical code indices before selecting the orchestration topology, ensuring both correctness and bounded token consumption through provable budget conservation.

## Problem Statement

**Development Automation Challenge:**
Multi-agent systems for code generation deploy topologies like pipeline (waterfall), hierarchical (manager-worker), or collaborative (peer) architectures. However, the optimal topology depends on task complexity:
- Simple fixes (single-file) might need only a linear pipeline
- Complex refactoring (cross-file dependencies) might need hierarchical coordination
- Parallel exploration (multiple implementation strategies) might need a collaborative peer topology

**Prior Limitations:**
- Static topology selection: systems choose one topology and apply it to all tasks (inefficient)
- Heuristic-based selection: rule-of-thumb criteria (file count, function count) often fail on complex code with low surface metrics
- No budget awareness: orchestration decisions don't account for token cost, leading to runaway expenses on complex tasks
- No code understanding: topology selection ignores semantic code structure (dependencies, layers, abstractions)

**Research Gap:** No system existed to:
1. Understand code structural complexity from the codebase
2. Dynamically select the orchestration topology best suited to that complexity
3. Enforce token budgets across the selected topology with mathematical guarantees

## Core Concepts & Theory

### Multi-Agent Orchestration Topologies

The paper formalizes three canonical topologies and their characteristics:

```
┌──────────────────────────────────────────────────────────────────┐
│  Topology 1: Linear Pipeline (Task Waterfall)                    │
├──────────────────────────────────────────────────────────────────┤
│  Agent1 → Agent2 → Agent3 → Aggregator                           │
│  ├─ Best for: Sequential task decomposition                      │
│  ├─ Cost: 3N tokens (N = base cost per agent)                    │
│  ├─ Latency: High (sequential execution)                         │
│  └─ Suitability: Low-complexity, single-file changes             │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Topology 2: Hierarchical (Manager-Worker)                       │
├──────────────────────────────────────────────────────────────────┤
│                        Manager                                    │
│                      ↙    ↓    ↖                                  │
│                  Worker1  Worker2  Worker3                        │
│  ├─ Best for: Parallel sub-problem solving                       │
│  ├─ Cost: N + 3N_sub tokens (manager + workers)                  │
│  ├─ Latency: Lower (parallel execution)                          │
│  ├─ Coordination: Central manager tracks all workers              │
│  └─ Suitability: Medium-complexity, multi-file changes           │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Topology 3: Collaborative (Peer-to-Peer)                        │
├──────────────────────────────────────────────────────────────────┤
│        Agent1 ←→ Agent2                                           │
│         ↓         ↑                                               │
│        Agent3 ←→ Agent4                                           │
│  ├─ Best for: Exploratory multi-path synthesis                   │
│  ├─ Cost: 4N + inter-agent comm. overhead                        │
│  ├─ Latency: Variable (negotiation-dependent)                    │
│  ├─ Coordination: Peer consensus, message passing                │
│  └─ Suitability: High-complexity, novel design patterns          │
└──────────────────────────────────────────────────────────────────┘
```

**Cost Models:**
- Linear: Cost scales linearly with depth (sequential stages)
- Hierarchical: Cost is N_manager + sum(N_workers); manager overhead is amortized across workers
- Collaborative: Cost is per-agent base + communication overhead; negotiation can amplify cost

### Structural Complexity Vector Extraction

RGAO extracts a multi-dimensional code complexity profile:

**Structural Complexity Vector (SCV):**
```
SCV = (file_count, dependency_depth, avg_function_size, abstraction_layers, circular_deps, cross_module_refs)

Where:
  file_count: Number of files being modified
  dependency_depth: Maximum import chain depth (A imports B imports C)
  avg_function_size: Average function/method size in lines
  abstraction_layers: Number of distinct abstraction levels (interface → impl → util)
  circular_deps: Count of circular import/dependency chains
  cross_module_refs: Count of cross-module references requiring coordination
```

**Extraction via Hierarchical Code Index:**

The system builds a hierarchical code index (abstract syntax tree + import graph) in three layers:

1. **Syntax Layer**: Parse all files; build AST for each module
   - Extract function signatures, class hierarchies, imports
   - Compute complexity metrics per function (cyclomatic, fan-in/fan-out)

2. **Dependency Layer**: Build a directed graph of inter-file dependencies
   - Nodes: files
   - Edges: import statements with metadata (type: type-import, value-import, re-export)
   - Compute transitive closure to find dependency chains

3. **Abstraction Layer**: Identify abstraction levels in the codebase
   - API layer (interfaces, public exports)
   - Implementation layer (private classes, internal functions)
   - Utility layer (helpers, shared code)
   - Identify which files belong to which layer

**Example Extraction:**

```
Codebase: Multi-module web server
Files:
  - server/main.py        (orchestrates server startup)
  - server/routes.py      (defines HTTP routes)
  - server/middleware.py  (middleware chain)
  - utils/cache.py        (caching utilities)
  - utils/logger.py       (logging)
  - db/connection.py      (database connection pooling)
  - db/models.py          (ORM models)

Extracted SCV:
  file_count = 7
  dependency_depth = 3 (main.py → routes.py → db/models.py)
  avg_function_size = 45 (average lines per function)
  abstraction_layers = 3 (api: routes.py; impl: middleware, connection; util: cache, logger)
  circular_deps = 0 (well-structured)
  cross_module_refs = 12 (routes→db, middleware→cache, etc.)

Topology Selection: Hierarchical
  Rationale: 7 files, low circular deps, clear layering suggest modular design
            Manager can decompose: API changes → implementation changes → DB schema changes
```

### Topology Selection Algorithm

The paper formalizes topology selection as a classification problem:

```
Given: SCV = (f_count, dep_depth, func_size, layers, circ_deps, cross_refs)
Goal: Select topology T ∈ {Linear, Hierarchical, Collaborative}

Decision Rule (heuristic + learned)
├─ If f_count ≤ 2 and dep_depth ≤ 2 → Linear (simple, sequential)
├─ Else if circ_deps ≥ 1 or layers ≥ 3 → Hierarchical (structured decomposition)
└─ Else if cross_refs > 10 or (dep_depth > 4 and func_size > 100) → Collaborative (exploratory)

Refined via ML Classifier:
└─ Logistic regression trained on (SCV, optimal_topology_empirically_determined) pairs
   to predict topology class probabilities
```

The heuristic rules are augmented with a learned classifier trained on historical data to handle edge cases.

### Provable Budget Conservation

**Token Budget Model:**

For any task with estimated token budget B, RGAO guarantees that the selected topology T will incur cost ≤ B with high probability:

```
Cost(T, task) = Base_Cost(T) + Overhead(T, code_complexity)

Linear:
  Base_Cost = N_stages × N_per_agent
  Overhead = O(dep_depth) -- increases with dependency depth

Hierarchical:
  Base_Cost = N_manager + N_workers × N_per_agent
  Overhead = O(N_workers) -- increases with worker count

Collaborative:
  Base_Cost = N_agents + Communication_rounds × Overhead_per_round
  Overhead = O(N_agents²) worst-case -- negotiation can be expensive
```

**Conservation Guarantee:**

Using formal analysis, the paper derives:

```
Theorem: For a task with SCV-derived complexity score C and allocated budget B,
if topology T is selected via RGAO with budget_factor = 1.2 (20% safety margin),
then P(Cost(T, task) ≤ B) ≥ 0.95 (95th percentile confidence)
```

Proof sketch:
1. Measure historical cost variance per topology and complexity class
2. Fit cost distribution (normal approximation justified by CLT)
3. Set budget_factor to account for 2-sigma tail (95% confidence)
4. Empirically validate on held-out test set

**Budget-Aware Orchestration:**

Once topology is selected, RGAO enforces budget conservation during execution:
- Track cumulative token usage across agents
- If usage exceeds 90% of budget, trigger early stopping (truncate long generations)
- If usage reaches budget limit, halt and return best partial solution found

## Main Ideas & Contributions

### 1. Code-Aware Topology Selection

**Core Innovation:** Instead of selecting topologies based on task description alone, RGAO reads and analyzes the target codebase to understand its structure, then selects the optimal topology.

**Why It Matters:**
- Code structure reveals hidden complexity that task descriptions miss
- A task like "add logging" is trivial in a single-file module but complex in a 50-file service with layered architecture
- Topology selection based on code structure is more robust than heuristics based on task keywords

**Example:**

```
Task: "Add authentication check to API routes"

Codebase Analysis:
├─ Single-module: routes.py (~200 lines, one file)
└─ Selected Topology: Linear (implement → test → deploy)
   Cost: ~2,000 tokens

vs.

Codebase Analysis:
├─ Multi-layer: routes.py → middleware.py → auth_service/ → database/
├─ Multiple files (15+)
├─ Dependency depth: 4
└─ Selected Topology: Hierarchical (manager coordinates auth service, middleware, routes changes)
   Cost: ~5,000 tokens (but parallelizable, reduces latency)
```

### 2. Contract-Based Budget Conservation

**Innovation:** RGAO formalizes a "code-agent contract" system with six-dimensional budget vectors per sub-agent:

```
Contract = {
  max_tokens: 2000,           -- Token budget for this agent
  max_rounds: 5,              -- Max reasoning rounds
  max_api_calls: 10,          -- External API call limit
  max_computation_time: 30s,  -- Wall-clock time limit
  fallback_strategy: "truncate_and_return_best",  -- On budget exhaustion
  quality_threshold: 0.8      -- Minimum output quality required
}
```

Each agent operates under its contract; manager enforces conservation across the team.

**Budget Allocation Algorithm:**

Given total budget B and selected topology T with N agents:
1. Allocate base budget B_base = B / (N + overhead_factor)
2. Reserve contingency: B_contingency = 0.1 × B
3. Allocate remaining to workers: B_worker = (B - B_contingency) / N
4. Each worker assigned contract with max_tokens = B_worker

**Example Allocation:**

```
Total Budget: 10,000 tokens
Topology: Hierarchical with manager + 3 workers

Allocation:
  Manager: 10,000 × 0.2 = 2,000 tokens
  Worker1: (10,000 - 1,000) / 3 ≈ 3,000 tokens
  Worker2: (10,000 - 1,000) / 3 ≈ 3,000 tokens
  Worker3: (10,000 - 1,000) / 3 ≈ 3,000 tokens
  Contingency: 1,000 tokens (held in reserve)
```

### 3. Empirical Validation on Code Benchmarks

The paper validates RGAO on CodeExecution, HumanEval, and internal datasets:

**Metrics:**
- Correctness: Pass@k (does the generated code pass test cases?)
- Efficiency: Tokens-per-correct-solution (lower is better)
- Robustness: Fraction of runs that stay within budget

**Key Results:**
- RGAO improves efficiency by 25–40% vs. static topology selection
- Budget conservation is achievable: 95%+ of runs stay within budget
- Correctness is maintained: no significant regression in pass@k

## Methodology & Implementation

### Dataset & Benchmarks

**Benchmarks Used:**
1. **HumanEval+**: 164 Python programming problems with extended test cases
2. **CodeExecution**: 1,000 code generation tasks with execution-based correctness
3. **LeetCode-Hard**: 300 challenging algorithmic problems (high complexity)
4. **Real Codebases**: 10 open-source projects (varying structural complexity)

**Code Analysis Pipeline:**
For each benchmark task, RGAO:
1. Parses the target code or codebase
2. Builds hierarchical index (syntax + dependencies + abstractions)
3. Extracts SCV
4. Predicts optimal topology
5. Selects topology and allocates budgets
6. Executes with orchestrated agents under budget constraints

### Experimental Setup

**Models Tested:**
- GPT-4, Claude 3.5 Sonnet, Mistral 7B, Llama 70B
- Tested with default and instruction-tuned prompts

**Baselines:**
1. Static Linear: all tasks use linear pipeline
2. Static Hierarchical: all tasks use hierarchical topology
3. Static Collaborative: all tasks use collaborative topology
4. Rule-Based Heuristic: topology chosen by hand-crafted rules (file count, dependency depth)
5. Oracle: topology selected with access to ground truth (upper bound)

**Metrics:**
- **Correctness**: Pass@1, Pass@3, Pass@10
- **Efficiency**: avg tokens per correct solution
- **Budget Compliance**: % runs within allocated budget
- **Latency**: wall-clock time (for hierarchical/collaborative, compared to linear)

### Results and Analysis

**Overall Performance Table:**

| Benchmark | Topology | Correctness (Pass@1) | Tokens/Solution | Budget Compliance | vs. Linear Baseline |
|-----------|----------|-----|---------|-----|---------|
| HumanEval+ | Linear | 78.2% | 1,850 | 99.1% | — |
| HumanEval+ | Hierarchical | 79.5% | 1,210 | 97.8% | -34.6% tokens |
| HumanEval+ | RGAO (adaptive) | 79.1% | 1,095 | 98.6% | -40.8% tokens |
| CodeExecution | Linear | 72.5% | 2,340 | 94.8% | — |
| CodeExecution | Hierarchical | 73.2% | 1,650 | 93.2% | -29.5% tokens |
| CodeExecution | RGAO (adaptive) | 73.8% | 1,320 | 96.1% | -43.6% tokens |
| LeetCode-Hard | Linear | 58.3% | 3,500 | 88.5% | — |
| LeetCode-Hard | Hierarchical | 59.7% | 2,100 | 86.2% | -40.0% tokens |
| LeetCode-Hard | RGAO (adaptive) | 61.2% | 1,680 | 94.3% | -52.0% tokens |

**Key Findings:**

1. **RGAO Outperforms Static Topologies**: Adaptive topology selection achieves 25–52% token savings vs. linear, while maintaining or improving correctness.

2. **Complexity Correlation**: Token savings are largest on LeetCode-Hard (high structural complexity), suggesting RGAO captures real code structure.

3. **Budget Conservation Works**: RGAO keeps 94–98% of runs within budget, significantly better than static topology selection (86–99%).

4. **Correctness Improved**: RGAO achieves 1–3% higher correctness on complex tasks, suggesting better decomposition aligns with problem structure.

### Topology Selection Breakdown

**Frequency of Topology Selection Across HumanEval+:**

```
Linear:       45% (simple, single-module tasks)
Hierarchical: 42% (multi-module, structured)
Collaborative: 13% (exploratory, high-complexity)
```

**Example SCV → Topology Mappings:**

```
Task: "Implement Fibonacci with caching"
  SCV: (1, 1, 30, 1, 0, 0)  -- single file, simple, no dependencies
  Selected: Linear
  Rationale: Low complexity; sequential implementation → caching → testing

Task: "Multi-threaded web server with logging"
  SCV: (5, 3, 200, 2, 0, 8)  -- 5 files, moderate depth, cross-refs
  Selected: Hierarchical
  Rationale: Clear separation (main → handlers → utils); manager coordinates across layers

Task: "Design API gateway with multiple backend routing strategies"
  SCV: (12, 4, 150, 3, 2, 15)  -- many files, circular deps, complex abstractions
  Selected: Collaborative
  Rationale: Multiple design strategies needed; peer agents explore alternatives, negotiate best
```

### Failure Modes & Robustness

**Budget Overrun Analysis:**

On 4–6% of runs where budget was exceeded:
- Cause 1: Circular dependencies not detected (2%)
  - SCV missed subtle import cycles → underestimated complexity → Linear topology chose → overran
  - Fix: Strengthen circular dependency detection

- Cause 2: Dynamic code generation in target (1%)
  - Code generates functions at runtime → static analysis misses them → underestimated complexity
  - Fix: Add runtime profiling feedback loop

- Cause 3: Unexpected agent verbosity (1–2%)
  - Certain models produce longer explanations than expected → variance in token usage
  - Fix: Incorporate model-specific calibration in budget allocation

**Latency Analysis:**

Wall-clock time comparison (HumanEval, single task, 30-second timeout):

```
Linear:       ~8 seconds (sequential, slowest)
Hierarchical: ~5 seconds (parallel workers, ~40% faster)
Collaborative: ~7 seconds (negotiation overhead partially offsets parallelism)
```

Hierarchical topology offers best latency for moderate complexity; collaborative adds negotiation overhead that can negate parallelism gains on simpler tasks.

## Practical Applications & Use Cases

### 1. Adaptive Code Generation in CI/CD

**Scenario:** A pull request modifies code in a large monorepo. The CI system needs to generate explanations, tests, and documentation updates.

**RGAO Application:**
1. Analyze PR diff: extract changed files, dependency graph
2. Compute SCV for changed code
3. Select topology (likely Hierarchical for multi-file changes)
4. Allocate budgets per agent (code generator, test writer, doc generator)
5. Execute in parallel, bounded by contracts
6. Enforce cost limits: if budget exhausted, return best partial results

**Benefit:** 30–50% cost savings while maintaining quality; budget predictability for CI cost management.

### 2. Multi-Repository Refactoring

**Scenario:** Refactor a shared library used by 5+ consumer repositories.

**RGAO Application:**
1. Identify shared library code structure
2. Identify consumer repository structures
3. Detect impact scope: which consumers are affected?
4. Select topology: Hierarchical (manager: refactoring executor; workers: impact assessment per consumer)
5. Budget allocation: proportional to consumer codebase size
6. Execute: parallel impact assessment, aggregated results

**Benefit:** Parallelized analysis with budget guarantees; prevents runaway costs on large refactorings.

### 3. Rapid Prototyping with Budget Constraints

**Scenario:** Product manager asks agent to generate 3 different architectural designs for a new feature.

**RGAO Application:**
1. Analyze existing codebase structure
2. Detect complexity level
3. Select topology: Collaborative (multiple agents propose designs in parallel, negotiate trade-offs)
4. Allocate budget: split evenly among design agents
5. Execute: agents work in parallel, communicate design tradeoffs
6. Aggregate: manager synthesizes top-2 designs with cost accounting

**Benefit:** Exploratory capability with cost predictability; agents stay synchronized via budget contracts.

### Integration Challenges

**Real-World Considerations:**
- **Incomplete Codebases**: Not all code statically analyzable (dynamic imports, code generation); SCV extraction must handle partial information
- **Evolving Budgets**: Initial budget estimates may be wrong; system needs graceful degradation under budget pressure
- **Multi-Model Orchestration**: Different models have different token efficiency; budget allocation must be model-aware
- **Latency vs. Cost Tradeoff**: Hierarchical topology reduces tokens but increases latency (parallel execution); users may prefer latency; need configurable tradeoff

## Insights & Implications

### 1. Code Structure Predicts Orchestration Requirements

**Finding:** SCV metrics (file count, dependency depth, abstraction layers) are predictive of optimal orchestration topology. This suggests that **software engineering principles (modularity, layering, low coupling)** naturally align with multi-agent orchestration requirements.

**Implication:** Well-designed code (modular, layered) is easier for multi-agent systems to handle; poorly-designed code (tightly coupled, circular dependencies) requires more sophisticated orchestration and higher token costs.

### 2. Budget Conservation is Achievable and Valuable

**Finding:** With contract-based budget allocation and topology-aware cost modeling, systems can achieve 95%+ budget compliance while maintaining correctness and improving efficiency 25–50%.

**Implication:** Cost predictability is feasible in multi-agent code generation; organizations can confidently allocate AI budgets to code automation without fear of runaway expenses.

### 3. Topology Selection is Learnable

**Finding:** ML classifiers trained on (SCV, optimal_topology) pairs outperform hand-crafted heuristic rules, suggesting topology selection is a learnable supervised problem.

**Implication:** As more multi-agent systems run, organizations can accumulate historical data and continuously improve topology selection with task-specific fine-tuned models.

### 4. Trade-offs Between Efficiency, Latency, and Complexity

The paper reveals three fundamental tradeoffs:

- **Tokens vs. Latency**: Sequential (Linear) minimizes tokens but maximizes latency; Parallel (Hierarchical) trades tokens for speed
- **Correctness vs. Cost**: Collaborative topology explores multiple designs (higher correctness on hard problems) but at significantly higher cost
- **Robustness vs. Efficiency**: Conservative budget allocation (higher safety margin) ensures compliance but wastes tokens; aggressive allocation saves tokens but risks overruns

**Guidance:** User preferences should drive tradeoff selection; RGAO provides the mechanism, not the policy.

### 5. Real-World Impact: Cost and Scalability

In production multi-agent systems:
- Linear topology: 1–3 agents, ~10k tokens per task (small projects)
- Hierarchical topology: 3–10 agents, ~5k tokens per task (medium projects)
- Collaborative topology: 5+ agents, ~15k tokens per task (large/exploratory tasks)

RGAO's 25–50% efficiency gains translate directly to cost reductions: a system handling 1,000 code generation tasks/month could save $100–500/month in API costs alone.

## Limitations & Open Questions

1. **Circular Dependency Detection**: Current SCV extraction uses transitive closure, which misses some subtle circular patterns. Advanced algorithms (SCC decomposition) might improve detection.

2. **Dynamic Code**: Code that generates functions at runtime (decorators, metaclasses, DSLs) is not well-captured by static analysis. Hybrid static+runtime profiling could help.

3. **Model-Specific Costs**: Token efficiency varies significantly by model (GPT-4 vs. Mistral). Budget allocation is model-dependent; portability across models is challenging.

4. **No Learning from Failure**: System allocates budgets statically; if an agent overruns, it fails. Adaptive budget reallocation during execution (stealing budget from idle agents) is unexplored.

5. **Scalability to Very Large Projects**: Tested on projects with 5–100 files; behavior on 1,000+ file projects unknown.

## Code & Resources

**Official Resources:**
- [Paper on arXiv (Abstract)](https://arxiv.org/abs/2605.05657)
- [Paper PDF](https://arxiv.org/pdf/2605.05657)
- [Paper HTML](https://arxiv.org/html/2605.05657)

**Related Frameworks:**
- **Code-Agent**: Multi-agent framework with formal contracts (described in paper)
- **AutoGen** (Microsoft): Agent orchestration framework
- **LangGraph** (LangChain): State-based orchestration

**Key Dependencies:**
- Code parser: AST library (language-specific), graph analysis library
- LLM API: GPT-4, Claude, or open-source LLM
- Budget tracking: cost estimation model per LLM

**Integration Guide:**
To apply RGAO:
1. Build SCV extractor for your codebase
2. Train topology classifier on historical (SCV, optimal_topology) pairs
3. Implement contract-based agent execution
4. Set budget allocation formula and enforce limits during execution
5. Monitor cost vs. correctness; refine budget formula over time

## Related Work & Context

**Prior Work on Cost-Aware Orchestration:**
- [The Orchestration of Multi-Agent Systems](https://arxiv.org/abs/2601.13671) - Formal architectures
- [Understanding Multi-Agent LLM Frameworks](https://arxiv.org/abs/2602.03128) - Framework comparison and cost analysis
- [ClawArena-Team](https://arxiv.org/abs/2606.31174) - Benchmarking multi-agent coordination (complementary)

**Related Topology Selection Work:**
- [A Two-Dimensional Framework for AI Agent Design Patterns](https://arxiv.org/abs/2605.13850) - Taxonomy of agent patterns
- [From Static Templates to Dynamic Runtime Graphs](https://arxiv.org/abs/2603.23102) - Workflow optimization

**Code Generation & Program Synthesis:**
- [LLM-Based Multi-Agent Systems for Code Generation: A Literature Review](https://arxiv.org/abs/2604.16321) - Comprehensive survey
- [CodeXGLUE](https://arxiv.org/abs/2102.04664) - Code understanding and generation benchmarks

**Future Research Directions:**
1. **Adaptive Reallocation**: Dynamically reallocate budgets during execution based on agent progress
2. **Human-in-the-Loop Topology Feedback**: Let humans suggest topologies; learn from their choices
3. **Cross-Language SCV**: SCV extraction for polyglot codebases (Java + Python + TypeScript)
4. **Topology Evolution**: Iteratively refine topology selection based on task success/failure history
5. **Cascade Topologies**: Multi-level orchestration (manager-of-managers) for very large teams

## References

- Talluri, A., Anne, P., Pendiyala, B. C., & Chilukuri, R. (2026). Retrieval-conditioned topology selection with provable budget conservation for multi-agent code generation. *arXiv preprint arXiv:2605.05657*.

- [Paper on arXiv (Abstract)](https://arxiv.org/abs/2605.05657)
- [Paper PDF](https://arxiv.org/pdf/2605.05657)
- [Paper HTML](https://arxiv.org/html/2605.05657)
