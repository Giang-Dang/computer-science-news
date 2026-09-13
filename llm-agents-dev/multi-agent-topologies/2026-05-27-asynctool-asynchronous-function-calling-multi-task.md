# AsyncTool: Evaluating the Asynchronous Function Calling Capability under Multi-Task Scenarios

**Authors:** Kou Shi, Ziao Zhang, Shiting Huang, Avery Nie, Zhen Fang, Qiuchen Wang, Lin Chen, Huaian Chen, Zehui Chen, Feng Zhao  
**Affiliations:** University of Science and Technology of China, University of Toronto  
**ArXiv ID:** [2605.27995](https://arxiv.org/abs/2605.27995)  
**Published:** May 27, 2026  
**Subject Areas:** Computational Linguistics (cs.CL), Software Engineering (cs.SE), Artificial Intelligence (cs.AI)

## Executive Summary

Multi-task concurrent execution is fundamental to modern software systems, yet agent benchmarks evaluate only synchronous, single-task tool use. **AsyncTool** introduces the first comprehensive benchmark for evaluating LLM agents in asynchronous multi-task environments with realistic tool response latency. The benchmark reveals substantial capability gaps: agents that perform well on sequential tasks fail dramatically when multiple heterogeneous tasks execute concurrently and tools have delayed responses. This work is critical for deploying autonomous agents in real development scenarios (CI/CD orchestration, test suite execution, distributed debugging, parallel code generation), where asynchronous task coordination determines overall system throughput and cost efficiency.

## Problem Statement

Real-world software development is fundamentally asynchronous and concurrent, yet agent evaluation remains synchronous:

- **Evaluation gap:** Current benchmarks assume synchronous function calls—call tool, wait for response, move to next action
- **Production reality:** Real tools (APIs, compilers, test runners) return responses after variable delays; agents must coordinate multiple concurrent tasks
- **Idle time challenge:** While waiting for one tool response, agents should work on other tasks; most agents don't utilize idle time effectively
- **Coordination complexity:** Managing task dependencies, resource constraints, and response ordering is non-trivial
- **Latency amplification:** Poor async handling turns 1 second per tool into 10+ seconds per task under concurrency

For software development, this is acute: running tests, compiling multiple binaries, checking linters, and querying APIs all occur concurrently. Agents that block waiting for one tool can't exploit parallelism and waste compute resources.

## Core Concepts & Theory

### Multi-Task Execution Models

**AsyncTool** evaluates agents under three execution patterns:

#### 1. Sequential Execution
```
Task A: Tool₁ → Tool₂ → Tool₃
Task B: (waits)
Task C: (waits)

Time: Sum of all individual durations
Agent burden: Low (track single task state)
Real-world frequency: ~10% of operations
```

#### 2. Parallel Execution
```
Task A: Tool₁ ──→ Tool₂
Task B: Tool₃ ──→ Tool₄
Task C: Tool₅

Time: Max(A, B, C) duration (ideally)
Agent burden: High (track 3+ concurrent states)
Real-world frequency: ~50% of operations (CI/CD, test suites)
```

#### 3. Mixed Execution
```
Task A: Tool₁ ──→ Tool₂
Task B: Tool₃ ──→ (waits for A.Tool₂ output)
Task C: Tool₄ (parallel with A, B)

Time: Depends on dependency graph and latency
Agent burden: Very high (async + dependencies)
Real-world frequency: ~40% of operations (complex workflows)
```

### Tool Feedback Models

**Synchronous vs. Asynchronous**

```
Synchronous (Current benchmarks):
Agent: "Call get_test_results(suite_1)"
Tool:  [immediate response after 50ms]
Agent: Receives result, continues

Asynchronous (AsyncTool):
Agent: "Trigger test_suite_1", "Trigger test_suite_2", "Trigger test_suite_3"
       (fire off 3 concurrent test runners)
Agent: [now has ~30 seconds before first results arrive]
Agent: Should start working on other tasks, not block
Tool:  After ~30s: Result from suite_1
       After ~35s: Result from suite_2
       After ~28s: Result from suite_3 (reordered!)
Agent: Must handle out-of-order responses
```

**Key difference:** In synchronous mode, response arrival order = call order. In async, responses arrive in arbitrary order based on tool execution time.

### Concurrent State Management

Agents must track:

```
Active Tasks: {task_id → state}
├── task_id_1: {status: "waiting", waiting_for: [call_2, call_5]}
├── task_id_2: {status: "executing", current_step: 3/5}
└── task_id_3: {status: "blocked", blocked_by: task_id_1}

Completed Calls: {call_id → result}
├── call_2: {status: "completed", result: {...}, latency: 1250ms}
├── call_5: {status: "completed", result: {...}, latency: 890ms}
└── call_7: {status: "pending", latency_so_far: 1100ms}

Task Dependencies:
├── task_1 → task_2 (task_2 waits for task_1 to complete)
└── task_3 → [no dependencies, can run anytime]
```

Agents that don't properly maintain this context make errors:
- Calling task_2 before task_1 finishes (dependency violation)
- Forgetting results and re-requesting them (wasted time/tokens)
- Not scheduling concurrent work (leaving processors idle)

### Evaluation Levels

AsyncTool evaluates at three granularities:

| Level | Definition | Example Metric |
|-------|-----------|-----------------|
| **Step Level** | Individual function call correctness | Did the agent call compile() with correct flags? |
| **Sub-Task Level** | Completing a single task correctly | Did the agent run all required tests? |
| **Task Level** | Completing all tasks in the workflow | Did the agent finish entire CI/CD pipeline? |

**Why multiple levels?** An agent might make perfect individual calls but fail at sub-task level (missing a test suite) or task level (incorrect dependency ordering).

### Efficiency Metrics

Beyond accuracy, AsyncTool measures efficiency:

```
Parallelization Index:
  Ideal time (all tasks concurrent): 30s
  Agent time: 45s
  Index: 30/45 = 0.67 (67% efficient parallelization)
  
Task Coordination Efficiency:
  Wasted calls (re-requesting same info): 2
  Useful calls: 18
  Efficiency: 18/20 = 90%

Response Handling Speed:
  Total result responses: 15
  Correctly processed immediately: 12
  Efficiency: 80%
```

## Main Ideas & Contributions

### 1. First Comprehensive Async Benchmark

**Key contribution:** AsyncTool is the first benchmark explicitly designed for asynchronous multi-task scenarios

- 500+ diverse tasks with intra-task dependencies and inter-task parallelism opportunities
- Realistic tool latency profiles (50ms-10s per call, varying by tool type)
- Deterministic ground truth (canonical final answer for each workflow)
- Automatic evaluation (F1 on function calls, state correctness, end result)

### 2. Revelation of Capability Gaps

**Critical finding:** Async capability differs dramatically from synchronous capability

- GPT-4 on synchronous benchmarks: 92% accuracy
- GPT-4 on AsyncTool (async multi-task): 67% accuracy
- Gap: 25 percentage points due to async coordination alone
- Gap is larger for open-source models (40-50pp), making them less suitable for production async systems

### 3. Task Coordination Patterns

AsyncTool identifies which agents struggle with which patterns:

```
Pattern Type | Agent Difficulty | Failure Mode |
|---------|-----------------|------------|
| Sequential | Easy | ~95% correct |
| Independent Parallel | Medium | ~75% correct (some missed optimization) |
| Dependent Parallel | Hard | ~45% correct (dependency ordering errors) |
| Mixed w/ Backpressure | Very Hard | ~30% correct (resource exhaustion handling) |
```

**Backpressure scenario:** Too many tasks queued, agent must choose which to prioritize (no simple solution).

### 4. Response Ordering Importance

**Discovery:** Agents struggle when tool responses arrive out-of-order

```
Expected order (tool exec time):
  Call 1 (10ms) → Call 2 (50ms) → Call 3 (20ms)

Response order (determined by execution speed):
  Response 1 (10ms arrived first)
  Response 3 (20ms arrived second)  ← Out of sequence!
  Response 2 (50ms arrived last)

Many agents assume responses arrive in call order.
AsyncTool forces agents to handle arbitrary orderings.
This alone accounts for ~10pp accuracy gap.
```

## Methodology & Implementation

### Benchmark Construction

**Data synthesis pipeline:**

1. **Task Templates:** Start with 50+ workflow templates
   - CI/CD pipelines (build → test → deploy)
   - Test suites (unit, integration, E2E in parallel)
   - Data processing (ETL with concurrent stages)
   - Multi-service coordination (API calls, database queries)

2. **Parameterization:** Generate diverse instances
   - Vary number of tasks (2-10 concurrent tasks)
   - Vary latency profiles (50ms-10s per tool)
   - Vary dependencies (sequential, parallel, mixed)
   - Vary data flow (task outputs feed into others)

3. **Ground Truth:** Deterministic simulation
   - Execute template with perfect orchestration
   - Record: canonical task order, results, final answer
   - Verify: against secondary reference implementation

4. **Hazard Injection:** Add realistic complications
   - Tool timeouts (5% of calls exceed expected time)
   - Transient failures (2% of calls fail once, succeed on retry)
   - Output reordering (responses sometimes arrive late)
   - Resource contention (shared resource limits)

### Experimental Setup

**Models Evaluated: 19 total**

Closed-source:
- GPT-5, GPT-4.1, GPT-4o, GPT-4
- Gemini 2.5 Pro, Gemini 2.0
- Qwen-max, Kimi K2
- Claude 3.5, Claude 3

Open-source:
- Llama 3.1 (70B, 8B)
- Mistral (Large, Medium)
- Deepseek
- Others (various sizes)

### Evaluation Metrics

**Multi-level accuracy:**

```python
# Step-level: Individual function call correctness
Step Accuracy = (Correct Calls) / (Total Calls)

# Sub-task level: Single task completion
SubTask Accuracy = (Tasks Completed Fully) / (Total Tasks)

# Task-level: End-to-end workflow success
Task Accuracy = (Correct Final Answers) / (Total Workflows)
```

**Efficiency metrics:**

```python
# How well agent parallelizes
Parallelization Efficiency = Ideal_Time / Actual_Time

# How many tool calls were necessary vs. wasted
Call Efficiency = (Necessary Calls) / (Total Calls)

# How quickly agent responds to incoming results
Response Latency = Avg(Time from result arrival to processing)
```

### Results

[Exact figures unavailable — see full paper for detailed result tables]

**Summary of findings:**

1. **Async adds complexity:** Task-level accuracy drops 20-30pp from synchronous baseline across all model families

2. **Model stratification:** Closed-source models (GPT-4+) show 70-85% async accuracy; open-source models 40-60%, creating a significant capability gap

3. **Dependency handling:** Tasks with simple sequential patterns: ~90% accuracy; mixed parallel+dependent: ~50% accuracy

4. **Response ordering:** Out-of-order responses reduce accuracy by ~10pp, even for strong models

5. **Scaling factors:** Model size helps (larger models ~5pp better), but instruction quality matters more; specific async training examples crucial

### Ablation Study

Key components affecting async performance:
- **Prompt engineering:** Explicit async instructions (+15pp)
- **Tool specifications:** Clear latency information (+8pp)
- **State tracking aids:** Providing checkpoint/state format (+12pp)
- **Example demonstrations:** Few-shot async examples (+10pp)

Combined, these interventions bring GPT-4 from 67% → 82% on AsyncTool.

## Practical Applications & Use Cases

### CI/CD Pipeline Orchestration

**Real scenario: Multi-stage deployment pipeline**

```
Stage 1 (Parallel):
  - Build service A (Tool: Docker, 120s)
  - Build service B (Tool: Docker, 90s)
  - Run linter (Tool: Ruff, 30s)

Stage 2 (Dependent on Stage 1):
  - Push images to registry (after builds complete)
  - Deploy to staging (after push complete)

Stage 3 (Parallel):
  - Run smoke tests (Tool: pytest, 60s)
  - Run integration tests (Tool: pytest, 45s)
  - Check health endpoints (Tool: curl/pytest, 15s)

Stage 4 (Dependent on Stage 3):
  - If all pass: deploy to production
  - If any fail: rollback and alert

Async challenge:
- Stage 1 jobs run concurrently; agent must not block on first to complete
- While waiting for slowest Stage 1 job, agent should prep Stage 2
- Results arrive out-of-order (linter finishes first, builds second)
- Agent must track which results enable downstream stages
```

Agent must coordinate ~10 concurrent tool calls, handle responses in arbitrary order, and maintain task dependency graph.

### Distributed Test Suite Execution

**Scenario: Running 50 test files in parallel**

```
Traditional (sequential):
  run_tests() → 50 files sequentially → 5 min total

Async approach:
  run_tests(parallel=true, max_workers=8)
  → 8 tests run concurrently
  → Results trickle in as they finish
  → Agent collects results, aggregates
  → Generate unified report
  
Time: ~30 seconds (8x speedup)
Agent burden: Track 50 concurrent states, aggregate results
```

AsyncTool measures if agents can orchestrate this correctly and efficiently.

### Concurrent Code Generation

**Scenario: Generating multiple functions in parallel**

```
Tasks:
  1. Generate authentication module (3 functions, ~200 tokens each)
  2. Generate database layer (2 functions, ~150 tokens each)
  3. Generate API handlers (5 functions, ~100 tokens each)

Async orchestration:
  - Fire off 3 agents/tasks concurrently
  - While waiting for responses (context window analysis): validate earlier code
  - Merge results, run linter on integrated codebase
  - If linter errors: parallel debugging of problematic functions
```

Can agents coordinate this without serializing everything?

## Insights & Implications

### For Multi-Agent System Design

1. **Async is not a luxury; it's essential:** Serializing multi-step workflows dramatically increases latency and cost. Async capability determines throughput.

2. **State management is hard:** Tracking concurrent task state is surprisingly difficult for LLMs; this is a teachable skill but requires explicit focus

3. **Response ordering matters:** Agents must be robust to responses arriving in any order, not just the call order. This is non-obvious but critical.

4. **Prompt engineering can help significantly:** Clear async instructions (+15pp), latency info (+8pp), and demonstrations (+10pp) collectively bridge much of the gap

### For Software Development Automation

1. **Async agents unlock parallelism:** Modern dev workflows (CI/CD, distributed testing, parallel builds) require async coordination; agents that can't do this leave performance on the table

2. **Orchestration complexity grows with scale:** Two parallel tasks are easy; ten concurrent tasks with dependencies become very hard. Agents need help (frameworks, structured state)

3. **Latency profiles matter:** Tool response time varies wildly (linter: 50ms, deploy: 5min). Agents must adapt scheduling based on expected latency

### For Language Model Deployment

1. **General capability ≠ async capability:** An agent good at single-task reasoning may struggle with concurrent coordination. Separate evaluation needed.

2. **Closed-source models have an advantage:** In async scenarios, proprietary models outperform open-source by 20-30pp. Organizations choosing models must account for this.

3. **Instruction quality > Scale:** Model size helps but isn't sufficient; specific async training and few-shot examples are more impactful

### Limitations & Open Questions

1. **Realistic tool latency:** AsyncTool uses simulated latencies; real tool latencies may have different characteristics (burstiness, correlation)

2. **Scalability:** Benchmark evaluates up to 10 concurrent tasks; production systems (100+ parallel jobs) may show different behaviors

3. **Resource constraints:** Paper doesn't deeply explore how agents handle resource limits (thread pools, memory, API rate limits)

4. **Formal verification:** Is there a way to formally verify correctness of agent-generated orchestration plans? Paper doesn't address.

## Code & Resources

**Official Repository:** Code available on GitHub (check paper for link)

**Dependencies:**
- Standard Python for benchmark harness
- Tool simulation framework (async execution simulator)
- LLM client libraries (OpenAI, Anthropic, Ollama, etc.)

**Quick-Start Integration:**

```python
from asynctool import AsyncBenchmark

# Initialize benchmark
benchmark = AsyncBenchmark(num_tasks=10, max_concurrency=8)

# Evaluate your agent
results = benchmark.evaluate(
    agent=your_agent,
    num_trials=5,
    timeout_per_task=60  # seconds
)

# Results breakdown
print(f"Step-level accuracy: {results.step_accuracy:.2%}")
print(f"Sub-task accuracy: {results.subtask_accuracy:.2%}")
print(f"Task accuracy: {results.task_accuracy:.2%}")
print(f"Parallelization efficiency: {results.parallel_efficiency:.2%}")
print(f"Call efficiency: {results.call_efficiency:.2%}")
```

## Related Work & Context

### Foundations in Concurrent Systems

- **Async/await paradigms:** JavaScript Promises, Python asyncio (language-level async)
- **Workflow orchestration:** Kubernetes, Airflow, Prefect (system-level async coordination)
- **Concurrent reasoning:** Limited prior work; most agent benchmarks are synchronous

### Related Agentic Papers

- "Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability" (tool reliability under adverse conditions)
- "TodoEvolve: Learning to Architect Agent Planning Systems" (planning strategies for multi-step tasks)
- "FAMA: Failure-Aware Meta-Agentic Framework" (failure handling in tool use)

### Future Research Directions

1. **Learned async strategies:** Can agents learn optimal concurrent scheduling? (RL-based orchestration)

2. **Formal verification:** Proving correctness of agent-generated orchestration plans

3. **Hybrid human-agent:** When should humans step in during concurrent execution? (intervention points)

4. **Cross-agent coordination:** Multiple agents working concurrently on same workflow; coordination protocols

5. **Adaptive latency prediction:** Agents that learn tool latency distributions and adapt scheduling

---

**Citation:**
```
@article{shi2026asynctool,
  title={AsyncTool: Evaluating the Asynchronous Function Calling Capability under Multi-Task Scenarios},
  author={Shi, Kou and Zhang, Ziao and Huang, Shiting and Nie, Avery and Fang, Zhen and Wang, Qiuchen and Chen, Lin and Chen, Huaian and Chen, Zehui and Zhao, Feng},
  journal={arXiv preprint arXiv:2605.27995},
  year={2026}
}
```
