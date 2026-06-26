# From Agent Loops to Structured Graphs: A Scheduler-Theoretic Framework for LLM Agent Execution

**Authors:** Hu Wei, et al.  
**ArXiv ID:** 2604.11378  
**Publication Date:** April 13, 2026 (revised)  
**Research Focus:** Agent orchestration, execution DAGs, control flow abstractions

## Executive Summary

This paper presents a fundamental shift in how LLM agents are orchestrated, moving from implicit loop-based control flow to explicit directed acyclic graph (DAG) structures. The Structured Graph Harness (SGH) framework transforms agent loops—where dependencies, state mutations, and recovery paths are implicit in context—into statically analyzable DAG execution models. Demonstrates significant improvements in reproducibility, debuggability, and scalability of multi-agent systems, with implications for production deployment of autonomous software engineering agents.

## Problem Statement

### Fundamental Limitations of Agent Loops

Current agent frameworks rely on **implicit loop semantics:**

```python
# Typical agent loop (implicit control flow)
def run_agent(task):
    context = initialize_context(task)
    while not task_complete(context):
        thought = llm.think(context)
        action = llm.decide_action(thought)
        observation = execute_action(action)
        context.append(thought, action, observation)
    return extract_result(context)
```

**Problems with implicit loops:**

1. **Invisible Dependencies:** Which observations does decision T depend on? Hidden in context embeddings
2. **Unbounded Iteration:** No formal bound on loop execution; agents can get stuck in cycles
3. **Implicit State:** State mutations scattered throughout context, making recovery extremely difficult
4. **Unmutable History:** Once added to context, decisions and observations cannot be corrected
5. **Poor Composability:** Hard to compose multiple agent loops; context merging is error-prone
6. **Debugging Nightmare:** When agents fail, impossible to identify exactly which step caused breakdown

**Consequence:** Production deployment requires manual intervention on 15-30% of agent runs (empirical data from the paper).

### Agent Loop Weaknesses at Scale

| Challenge | Manifestation | Impact |
|-----------|--------------|--------|
| **Cycle Detection** | Agent repeats same action indefinitely | 22% of timeout failures in SWE-bench |
| **Context Overflow** | Token limit exceeded before task completion | 8% fail due to context exhaustion |
| **State Inconsistency** | Observations contradict previous state | 12% of failure cases involve state contradictions |
| **Error Propagation** | Single mistake cascades through subsequent steps | 34% of failures trace to upstream errors |
| **Recovery Ambiguity** | Unclear what state to restore after error | Manual debugging required for 67% of failures |

## Core Concepts & Theory

### Directed Acyclic Graph Execution Model

**Definition:** Replace the implicit loop with an explicit DAG where:
- **Nodes** represent atomic computational units (LLM calls, tool invocations)
- **Edges** represent data dependencies between nodes
- **Annotations** mark control flow: sequential, parallel, conditional, loop (bounded)

```
Agent Loop Execution Graph:

Traditional Loop:
┌─────────────────────────────────┐
│     Implicit Context Loop       │
│  ┌─────────────────────────────┐│
│  │ Step 1: Think               ││
│  │ Step 2: Decide              ││
│  │ Step 3: Execute             ││
│  │ Step 4: Observe (implicit)  ││
│  │ Step 5: Update Context      ││
│  │ [Repeat if not done]         ││
│  └─────────────────────────────┘│
│  [Implicit dependencies]        │
└─────────────────────────────────┘

Structured DAG:
            ┌──────────────────┐
            │  Parse Task      │
            │  (T0)            │
            └────────┬─────────┘
                     ↓
            ┌──────────────────┐
            │  Initial Plan    │
            │  (T1)            │
            └────────┬─────────┘
                     ↓
      ┌──────────────┴───────────────┐
      ↓                              ↓
 ┌─────────────┐             ┌──────────────┐
 │ Research 1  │             │ Research 2   │
 │ (parallel)  │             │ (parallel)   │
 └──────┬──────┘             └──────┬───────┘
        └──────────┬─────────────────┘
                   ↓
          ┌────────────────────┐
          │ Synthesize Results │
          │ (barrier)          │
          └────────┬───────────┘
                   ↓
          ┌────────────────────┐
          │ Generate Solution  │
          └────────┬───────────┘
                   ↓
          ┌────────────────────┐
          │ Validate & Test    │
          └────────┬───────────┘
                   ↓
          ┌────────────────────┐
          │ Format & Return    │
          └────────────────────┘
```

### Scheduler-Theoretic Framework

The framework models multi-agent execution using concepts from systems scheduling:

**Key Insight:** Multi-agent orchestration is isomorphic to task scheduling problems:
- Agents as processors
- Tasks as dependent jobs
- Constraints as resource/time limits

**Scheduling Primitives:**

1. **Ready Set:** Tasks whose dependencies are satisfied, ready for execution
2. **Critical Path:** Longest dependency chain determining minimum execution time
3. **Escape Hatch:** Explicit error recovery path triggering when task fails
4. **Escalation Protocol:** Rules for promoting failures up the hierarchy

**Formal Definition:**

$$G = (V, E, \text{constraints})$$

where:
- $V = \{v_0, v_1, ..., v_n\}$ are computational nodes
- $E \subseteq V \times V$ are directed edges (dependencies)
- $\text{constraints}$ include: timeout, token budget, max retries, conditional branching

**Execution Invariants:**

1. **Acyclicity:** Graph must be DAG (no infinite loops)
2. **Bounded Depth:** Max path length ≤ $k$ (typically $k=20$ for cognitive planning chains)
3. **Resource Constraints:** Total tokens across all nodes ≤ budget
4. **Deterministic Recovery:** Every node has defined escape path

### Separation of Concerns: Planning vs. Recovery

**Traditional Loop:** Planning and recovery intertwined in context

**SGH Framework:** Explicit separation:

```
Architecture Layers:

┌─────────────────────────────────┐
│  APPLICATION LAYER              │
│  (User task specification)      │
└────────────────┬────────────────┘
                 ↓
┌─────────────────────────────────┐
│  PLANNING LAYER                 │
│  • Decompose task into DAG      │
│  • Assign nodes to agents       │
│  • Set dependencies             │
│  • Estimate resource needs      │
└────────────────┬────────────────┘
                 ↓
┌─────────────────────────────────┐
│  EXECUTION LAYER                │
│  • Ready set queue              │
│  • Parallel execution           │
│  • State management             │
│  • Data flow between nodes      │
└────────────────┬────────────────┘
                 ↓
┌─────────────────────────────────┐
│  RECOVERY LAYER                 │
│  • Error classification         │
│  • Retry policies               │
│  • Escalation rules             │
│  • State rollback               │
└────────────────┬────────────────┘
                 ↓
┌─────────────────────────────────┐
│  VERIFICATION LAYER             │
│  • Postcondition checking       │
│  • Output validation            │
│  • Consistency verification     │
└─────────────────────────────────┘
```

**Recovery Protocols:**

```
Failure Detection → Classification → Resolution

Node Fails (e.g., LLM call fails)
    ↓
1. Classify Error
   ├─ Transient (network timeout) → immediate retry
   ├─ Resource exhaustion → reduce task scope
   ├─ Malformed input → fix and retry
   └─ Fundamental failure → escalate
    ↓
2. Apply Recovery Strategy
   ├─ Same node → retry with modified input
   ├─ Upstream → re-plan from earlier state
   ├─ Sibling → try alternative approach
   └─ Escalate → human intervention flag
    ↓
3. Verify Recovery
   ├─ Re-check invariants
   ├─ Validate state consistency
   └─ Resume execution
```

## Main Ideas & Contributions

### 1. Static DAG Representation for Agent Execution

**Innovation:** Transform implicit loops into explicit, static DAGs before execution begins.

**Advantages:**
- **Analyzable:** Can verify properties (no cycles, bounded depth, resource feasibility)
- **Optimizable:** Can apply graph algorithms (critical path analysis, parallelization)
- **Debuggable:** Each node's inputs/outputs explicitly defined
- **Reproducible:** Same input → exact same execution path (vs. context-dependent loops)

**Example: Code Review Task**

```
Task: "Review this Python code for bugs and performance issues"

Explicit DAG Planning:

┌──────────────────────────────────┐
│ 0: Parse Code                    │
│ Input: source code               │
│ Output: AST, metrics             │
└───────────────┬──────────────────┘
                ↓
    ┌───────────┴──────────┐
    ↓                      ↓
┌─────────────┐      ┌──────────────┐
│1: Identify  │      │2: Analyze    │
│   Bugs      │      │   Performance│
│ (parallel)  │      │ (parallel)   │
└──────┬──────┘      └──────┬───────┘
       │                    │
       └────────┬───────────┘
                ↓
        ┌──────────────────┐
        │3: Merge Findings │
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │4: Generate Review│
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │5: Format Output  │
        └──────────────────┘
```

### 2. Multi-Agent Orchestration with Explicit Dependencies

**Innovation:** Formalize multi-agent interaction through dependency annotations on DAG edges.

**Dependency Types:**

```
Edge Annotations:

1. Data Dependency
   Node A's output → Node B's input
   Example: Parse code result → bug detection analysis

2. Precedence Constraint
   Node A must complete before B starts
   Example: Plan must precede execution

3. Conditional Branch
   Edge active only if condition C true
   Example: If bugs found → generate fixes; else → skip

4. Aggregation/Barrier
   Multiple incoming edges; B waits for all
   Example: Multiple analyses → synthesis requires all results

5. Escalation Edge
   Triggered only on error in predecessor
   Example: Failed implementation → escalate to human review
```

**Graph Properties Verification:**

```python
def verify_dag_properties(graph):
    """Verify DAG satisfies execution invariants."""
    
    # 1. Acyclicity check
    if has_cycle(graph):
        raise ExecutionError("Graph contains cycle")
    
    # 2. Bounded depth (max planning chain length)
    max_depth = longest_path(graph)
    if max_depth > MAX_PLANNING_DEPTH:
        raise ResourceError(f"Plan too deep: {max_depth}")
    
    # 3. Resource feasibility
    total_tokens = sum(node.estimated_tokens for node in graph)
    if total_tokens > TOKEN_BUDGET:
        raise ResourceError(f"Insufficient tokens: {total_tokens}")
    
    # 4. Completeness check
    if not all_nodes_covered_by_recovery(graph):
        raise DesignError("Some nodes lack recovery paths")
    
    return True
```

### 3. Bounded Recovery with Escalation Protocol

**Innovation:** Define explicit recovery paths for each failure mode, with escalation to higher authority.

**Recovery Hierarchy:**

```
Level 0: Transient Failures (auto-retry)
├─ Network timeout → retry same node
├─ Rate limit → wait and retry
└─ Temporary LLM outage → exponential backoff

Level 1: Input/Output Failures (modify and retry)
├─ Malformed LLM response → parse and correct
├─ Tool execution error → adjust tool parameters
└─ Type mismatch → transform data format

Level 2: Logical Failures (alternative strategies)
├─ Plan infeasible → generate alternative plan
├─ Tool unavailable → find alternative tool
└─ Resource exhaustion → reduce task scope

Level 3: Fundamental Failures (escalation)
├─ Core logic error → alert human supervisor
├─ Impossible constraint → flag as unsolvable
└─ Repeated failure despite recovery → escalate
```

**Escape Hatch Mechanism:**

```
Node execution wrapper:

for attempt in range(MAX_RETRIES):
    try:
        result = execute_node(node)
        verify_postconditions(node, result)
        return result
    
    except TransientError as e:
        continue  # Retry same node
    
    except RecoverableError as e:
        # Try alternative approach
        if has_alternative_path(node):
            result = execute_alternative(node)
            return result
        else:
            raise
    
    except UnrecoverableError as e:
        # Escape hatch: trigger error recovery path
        trigger_escape_hatch(node, e)
        return escalation_result

raise FinalError("All recovery attempts exhausted")
```

### 4. Parallel Execution with Barrier Synchronization

**Innovation:** Explicit parallelization of independent tasks with synchronization barriers.

**Pattern: Fan-out and Fan-in**

```
Example: Comprehensive Code Analysis

┌─────────────────────┐
│ Parse Code (T0)     │
└──────────┬──────────┘
           ↓
      Fan-out to 4 parallel analyses:
      
      ┌──────────┬──────────┬──────────┬──────────┐
      ↓          ↓          ↓          ↓
   ┌────┐    ┌────┐    ┌────┐    ┌────┐
   │T1: │    │T2: │    │T3: │    │T4: │
   │Bug │    │Perf│    │Type│    │Sec │
   │Anal│    │Anal│    │Anal│    │Anal│
   └────┘    └────┘    └────┘    └────┘
      ↓          ↓          ↓          ↓
      └──────────┬──────────┬──────────┘
                 ↓
          Barrier (wait for all)
                 ↓
           ┌──────────────┐
           │T5: Synthesize│
           └──────────────┘
```

**Performance Advantage:**

```
Sequential execution:
- Parse (300ms)
- Bugs analysis (1200ms)
- Perf analysis (1100ms)
- Type analysis (800ms)
- Security analysis (950ms)
- Synthesis (600ms)
Total: 4,950ms

Parallel execution (4 concurrent):
- Parse (300ms)
- [All 4 analyses in parallel] (max 1,200ms)
- Synthesis (600ms)
Total: 2,100ms

Speedup: 2.36x (2,850ms saved)
```

## Methodology & Implementation

### Datasets and Evaluation

**Benchmarks Used:**

1. **SWE-Bench** (500 real GitHub issues)
   - Code generation and bug fixing
   - Multi-step reasoning required
   - Success measured by test execution

2. **Multi-Agent Scenarios** (custom)
   - Hierarchical task decomposition
   - Parallel independent subtasks
   - Requires explicit coordination

3. **Long-Horizon Planning** (100 tasks)
   - 10-30 step chains
   - Risk of cycle formation
   - Resource constraint satisfaction

### Experimental Setup

**Configurations Compared:**

| Configuration | Characteristics |
|---------------|-----------------|
| **Agent Loop** | Traditional implicit loop, no explicit DAG |
| **Flat DAG** | Simple linear task chain, no parallelization |
| **Structured DAG** | Full SGH with parallelization & recovery |
| **Manual Expert** | Hand-crafted DAG orchestration (upper bound) |

**Metrics:**

- **Success Rate:** Percentage of tasks solved without human intervention
- **Time to Solution:** Wall-clock time including retries
- **Recovery Effectiveness:** % of failures recovered vs. escalated
- **Resource Efficiency:** Token usage per successful task
- **Reproducibility:** % of runs with identical execution paths

### Results

**Primary Finding: Success Rate Improvement**

```
                Agent Loop    Flat DAG    SGH       Manual
SWE-Bench       68.2%         71.4%      78.9%     85.3%
LongHorizon     41.3%         52.1%      67.8%     72.5%
─────────────────────────────────────────────────────────
Average         54.75%        61.75%     73.35%    78.9%
```

**Improvement:** +18.6pp over agent loops (34% relative improvement)  
[Figures confirmed from paper Abstract & Results]

**Failure Mode Analysis:**

```
Failure Category          Agent Loop   SGH       Improvement
─────────────────────────────────────────────────────────
Infinite loop/cycle       22.1%        2.3%      ↓ 19.8pp
Context overflow          8.4%         0.6%      ↓ 7.8pp
State inconsistency       12.3%        1.1%      ↓ 11.2pp
Unrecoverable error       15.2%        8.4%      ↓ 6.8pp
Unknown/other             42.0%        87.6%     (solved)
─────────────────────────────────────────────────────────
Total failure rate        100%         12.4%     88% reduction
```

**Recovery Effectiveness:**

```
Failure Type              Recovery Success Rate
────────────────────────────────────────────
Transient failures        98.2% (immediate retry)
Input/output errors       91.4% (alternative strategy)
Logical failures          74.3% (re-planning)
Cascading failures        61.8% (escalation required)
```

**Parallel Execution Speedup:**

```
Task Type                    Sequential   Parallel   Speedup
─────────────────────────────────────────────────────────
Multi-step linear chain      5.2s        5.1s       1.02x
Code analysis (4 parallel)   4.9s        2.1s       2.33x
Research synthesis (8 prll)  12.3s       2.8s       4.39x
─────────────────────────────────────────────────────────
Average speedup (40 tasks)               2.6x
```

**Computational Cost:**

```
Overhead of SGH Planning:
- DAG creation: 200-500ms per task
- Property verification: 100-300ms
- Execution scheduling: 50-150ms
Total overhead: 0.35-0.95s per task

Offset by benefits:
- 34% fewer failed tasks (fewer retries)
- 2.6x faster due to parallelization
- 78% fewer escalations (less human intervention)

Net: 15-25% reduction in total execution time
     despite planning overhead
```

## Practical Applications & Use Cases

### 1. Autonomous Code Generation at Enterprise Scale

**Scenario:** Implement 500 features across 50 microservices

**Agent Loop Approach:**
- Single agent iterates on each feature
- Context window grows with each step
- Frequently hits token limits or cycles
- Success rate: 58%

**SGH Approach:**
```
Explicit DAG:
┌─────────────────┐
│ Parse Spec      │
└────────┬────────┘
         ↓
    Parallel:
    ├─ Design architecture
    ├─ Plan database schema
    ├─ Plan API routes
    └─ Plan test strategy
         ↓
    Barrier → Merge plans
         ↓
    Parallel:
    ├─ Implement services
    ├─ Generate DB migrations
    ├─ Create API handlers
    └─ Write test suite
         ↓
    Integration testing
         ↓
    Deploy
```

**Metrics:**
- Success rate: 78% (vs. 58% for agent loops)
- Time per feature: 2.1m (vs. 3.8m)
- Human intervention: 22% (vs. 42%)

### 2. Multi-Agent Debugging & Repair

**Scenario:** Agent trio debugging complex bugs in production code

```
Explicit Multi-Agent DAG:

┌──────────────────────────┐
│ Coordinator Agent        │
│ (orchestrates team)      │
└──────────────┬───────────┘
               ↓
   Parallel sub-agents:
   
   ├─ Analyzer Agent       ├─ Reproducer Agent    ├─ Fixer Agent
   │ ├─ AST analysis      │ ├─ Create test case  │ ├─ Fix code
   │ ├─ Error trace       │ ├─ Run reproducer    │ ├─ Verify fix
   │ └─ Identify root     │ └─ Collect stack     │ └─ Test suite
   │    cause             │    traces            │
   
   ↓        ↓        ↓
   └────────┬────────┘
            ↓
   Synthesize findings
            ↓
   Implement solution
            ↓
   Validate fix
```

**Benefits:**
- Parallel analysis reduces debugging time by 3.2x
- Explicit dependencies clarify information flow
- Recovery paths handle individual agent failures without cascade

### 3. Hierarchical Planning for Complex Tasks

**Scenario:** End-to-end ML pipeline development

```
Top-Level DAG:
┌─────────────────────────┐
│ Understand Requirements │
└────────────┬────────────┘
             ↓
      Sub-DAGs (nested):
      
┌──────────────────────────────────────┐
│ Data Pipeline Sub-DAG                │
├──────────────────────────────────────┤
│ ├─ Explore data                      │
│ ├─ Clean data                        │
│ ├─ Engineer features                 │
│ └─ Create train/test splits          │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Model Development Sub-DAG            │
├──────────────────────────────────────┤
│ ├─ Choose architecture               │
│ ├─ Implement model                   │
│ ├─ Train model                       │
│ └─ Evaluate metrics                  │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Deployment Sub-DAG                   │
├──────────────────────────────────────┤
│ ├─ Package model                     │
│ ├─ Create inference service          │
│ ├─ Deploy to staging                 │
│ └─ Run smoke tests                   │
└──────────────────────────────────────┘
```

**Advantages:**
- Explicit task structure visible to multiple agents
- Parallelizable components identified automatically
- Failures in one sub-DAG don't affect others
- Clear hand-off points between specialized sub-agents

## Integration and Deployment Considerations

### Framework Compatibility

**Integration with existing agent systems:**

```python
from sgf import StructuredGraphFramework

# Wrap existing agent loop in SGH
sgf = StructuredGraphFramework()

# Define DAG explicitly
dag = sgf.create_dag(
    nodes=[
        Node("parse", llm_parse_task),
        Node("plan", llm_create_plan),
        Node("research", parallel_web_search),
        Node("implement", llm_write_code),
        Node("test", run_tests),
    ],
    edges=[
        Edge("parse", "plan"),
        Edge("plan", ["research", "implement"]),  # parallel
        Edge(["research", "implement"], "test"),   # barrier
    ],
    recovery={
        "parse": "retry",
        "plan": "replan",
        "implement": "try_alternative",
        "test": "escalate",
    }
)

# Execute with explicit DAG
result = sgf.execute_dag(dag, task_input)
```

### Scalability Considerations

**DAG Size Limits:**
- Typical planning depth: 10-20 nodes (verified safe)
- Maximum nodes before analysis overhead exceeds benefit: ~100
- Parallel breadth: up to 10-15 concurrent agents
- Token budget: Must account for all nodes + safety margin

**Optimization Techniques:**
- Cache frequently used sub-DAGs
- Reuse DAG structures across similar tasks
- Pre-compute critical paths for resource estimation

## Insights & Implications

### For Multi-Agent Development

1. **Explicit is Better Than Implicit:** Making dependencies and control flow explicit enables dramatically better error handling, optimization, and debugging.

2. **Scheduler Theory as Foundation:** Agent orchestration isn't unique—applying task scheduling theory reveals well-understood solutions (critical path, barriers, escalation).

3. **Parallelism is Underutilized:** Current agent loops execute sequentially; explicit DAGs unlock 2-4x speedups through safe parallelization.

4. **Escape Hatch Philosophy:** Robust systems need explicit failure paths; implicit recovery in context is insufficient.

### Research Frontiers

**Open Questions:**

1. **Optimal DAG Structure Discovery:** Can agents automatically design optimal DAG structures for their own tasks?

2. **Dynamic Re-Planning:** Should DAGs be fixed before execution or adapt as new information emerges?

3. **Fault Tolerance:** How to handle mid-execution changes in agent availability or capabilities?

4. **Cost Modeling:** How to accurately estimate token costs before execution to set budgets intelligently?

### Limitations

- **Planning Overhead:** 0.35-0.95s per task for DAG creation and verification
- **Flexibility vs. Structure:** Over-specified DAGs limit agent adaptability
- **Fallback to Loops:** When DAG structure is unclear, benefits diminish
- **Human Interpretability:** Complex nested DAGs remain hard for humans to understand

## Code & Resources

### Official Framework

**Project:** Structured Graph Framework (SGF)  
**Language:** Python 3.10+  
**GitHub:** https://github.com/research/structured-graph-framework  
**License:** Apache 2.0

**Core Dependencies:**
```
networkx>=3.0              # DAG operations
pydantic>=2.0              # Schema validation
anthropic>=0.28.0          # Claude API
asyncio                    # Parallel execution
```

### Quick-Start Integration

```python
from sgf import DAGBuilder, SGFExecutor

# Build DAG
builder = DAGBuilder()
builder.add_node("parse", llm_call=parse_task)
builder.add_node("plan", llm_call=create_plan, depends_on=["parse"])
builder.add_node("research", llm_call=web_search, depends_on=["plan"])
builder.add_node("implement", llm_call=write_code, depends_on=["plan"])
builder.add_node("test", llm_call=validate, depends_on=["implement"])

# Add recovery paths
builder.set_recovery("parse", strategy="retry")
builder.set_recovery("plan", strategy="alternative")
builder.set_recovery("implement", strategy="escalate")

# Create barrier for parallelism
builder.add_barrier(["research", "implement"], "test")

dag = builder.build()

# Execute
executor = SGFExecutor(model="claude-opus-4")
result = executor.run(dag, task_input)

print(f"Success: {result.success}")
print(f"Execution time: {result.time_ms}ms")
print(f"Tokens used: {result.tokens}")
```

## Related Work & Context

### Control Flow in Multi-Agent Systems

**Prior Work:**
- **Hierarchical Task Networks (HTN):** Established hierarchical planning in AI (Erol et al., 1994)
- **STRIPS/PDDL:** Formal planning languages with explicit preconditions/effects
- **Workflow Systems:** Business process management with DAG-based execution (Airflow, Kubernetes)

**CODESKILL Advancement:** First large-scale system applying scheduler theory to LLM agent orchestration, demonstrating 34% performance improvement in practice.

### Recovery and Fault Tolerance

**Related Systems:**
- **Debugging the Debuggers** (2605.08717): Structured failure diagnosis
- **PROSE** (Program Synthesis by Example): Robust error handling in code synthesis
- **Chaos Engineering:** Systematic failure injection and recovery testing

**Synergy:** SGH provides explicit structure for testing and implementing recovery protocols.

### Parallel and Distributed Agents

**Related Frameworks:**
- **From Prompt-Response to Goal-Directed Systems** (2026-06-16): Evolution toward structured agent architectures
- **Self-Organized Agents** (2026-04-02): Multi-agent code generation with emergent coordination
- **ABSTRAL** (2026-03-24): Automated multi-agent system design

**Unique Contribution:** SGH formalizes the dependency and coordination structure using DAG theory, enabling both better human understanding and computational optimization.

### Future Integration Directions

1. **With RL for DAG Optimization:** Learn optimal DAG structures and parallelization strategies through reinforcement learning
2. **With Formal Verification:** Prove invariants about DAG execution (termination, resource bounds, correctness)
3. **With CODESKILL:** Skill composition as sub-DAGs with explicit data flow
4. **With Multi-Agent Communication:** DAG nodes as MCP endpoints for agent-to-agent interaction

---

**Citation:**

```bibtex
@article{wei2026agent_loops_graphs,
  title={From Agent Loops to Structured Graphs: A Scheduler-Theoretic Framework for LLM Agent Execution},
  author={Wei, Hu and others},
  journal={arXiv preprint arXiv:2604.11378},
  year={2026}
}
```

**Last Updated:** June 26, 2026
