# ReaComp: Compiling LLM Reasoning into Symbolic Solvers for Efficient Program Synthesis

**Authors:** (Research team — see full paper for complete authorship)  
**ArXiv ID:** 2605.05485  
**Submitted:** May 5, 2026  
**Research Focus:** Neuro-symbolic program synthesis, LLM reasoning compilation, efficient code generation

## Executive Summary

ReaComp introduces a paradigm shift in program synthesis by **compiling LLM reasoning traces into reusable symbolic solvers**. Rather than repeatedly querying expensive LLMs, the approach distills recurring strategies and failure patterns from LLM reasoning into standalone program synthesizers over constrained DSLs. This neuro-symbolic hybrid achieves state-of-the-art accuracy (91.3% on PBEBench-Lite, 84.7% on PBEBench-Hard) while reducing token consumption by 78%, delivering both superior performance and dramatic cost efficiency for automated code generation and software development automation.

## Problem Statement

Program synthesis with LLMs faces critical efficiency and cost challenges:

- **Inference Cost:** Every synthesis task requires multiple LLM queries with high token consumption, making production deployment expensive
- **Test-Time Scaling Plateau:** Increasing test-time compute (more LLM attempts) shows diminishing returns on hard benchmarks
- **Redundant Reasoning:** LLMs repeatedly solve similar sub-problems across different synthesis tasks, lacking accumulated knowledge
- **Combinatorial Explosion:** Hard synthesis tasks require exploring large solution spaces; LLMs struggle without external guidance
- **Generalization:** LLM performance degrades sharply on out-of-distribution or hard instances requiring deep search

The fundamental gap: **LLMs are expensive at test time but rich in reasoning-time knowledge**. Current approaches fail to leverage offline reasoning to build efficient test-time solvers.

## Core Concepts & Theory

### Neuro-Symbolic Synthesis Pipeline

ReaComp decomposes program synthesis into an offline phase (expensive) and a test-time phase (cheap):

```
┌────────────────────────────────────────────────────────────────┐
│                    OFFLINE PHASE (Training)                     │
├────────────────────────────────────────────────────────────────┤
│ 1. Run LLM on synthesis dataset, capture reasoning traces       │
│ 2. Extract strategies, failure modes, and solution patterns     │
│ 3. Distill into symbolic program synthesizers (DSL rules)       │
│ 4. Compile into efficient constraint-based solvers              │
│ 5. Create solver ensembles for diverse problem types            │
└────────────────────────────────────────────────────────────────┘
                             ↓
┌────────────────────────────────────────────────────────────────┐
│                   TEST-TIME PHASE (Inference)                   │
├────────────────────────────────────────────────────────────────┤
│ 1. Run symbolic solvers FIRST (no LLM cost)                     │
│ 2. If solvers succeed → return result (fast + cheap)            │
│ 3. If solvers fail → use LLM as fallback (only when needed)    │
│ 4. Ensemble voting from multiple solvers                        │
│ 5. Neuro-symbolic hybrid for hardest instances                  │
└────────────────────────────────────────────────────────────────┘
```

### Solver Induction: From Reasoning to Rules

The core innovation extracts **executable symbolic rules** from LLM reasoning traces:

```
LLM Reasoning Trace              Extracted Strategy
─────────────────────────────────────────────────────
"To implement sort, I need:     RULE: For sorting tasks,
 1. Compare operation           RequiredOps = [compare, swap]
 2. Swap operation              SkipRules = [recursive_sort]
 3. Avoid recursion             MaxDepth = 5
 4. Use at most 5 lines"        
                                Compiled Solver:
                                DSL: {op_type, param_bounds}
                                Constraint: ¬(recursive ∧ N>5)
```

### Constrained DSL Compilation

Program synthesis over a **Constrained Domain-Specific Language (DSL)** replaces expensive search with constraint satisfaction:

1. **DSL Definition:** Operators (function calls, control flow, data structures)
2. **Constraints:** Rules extracted from LLM reasoning (avoid patterns, enforce invariants)
3. **Solver:** Constraint satisfaction problem (CSP) or SMT solver finds programs satisfying constraints
4. **Efficiency:** Symbolic solvers explore solution space via pruning rather than enumeration

**Example DSL for array operations:**

```
Program ::= [Stmt]
Stmt ::= Assign | ControlFlow | FunctionCall
Assign ::= var "=" Expr
Expr ::= var | const | Expr Op Expr | FunctionCall
FunctionCall ::= builtin_op(args)

Constraints (extracted from reasoning):
  ∧ (builtin_ops ⊆ {sort, search, filter, map})
  ∧ (program_length ≤ 10)
  ∧ (recursion_depth ≤ 2)
  ∧ (¬(uses_external_library))
```

### Ensemble Strategies

ReaComp combines multiple specialized solvers:

```
┌─────────────────────────────────────────────────────┐
│         Solver Ensemble Architecture                │
├─────────────────────────────────────────────────────┤
│ Solver-1 (List Operations)                          │
│   ├─ Optimized for array/list programs              │
│   └─ Constraints from "list manipulation" traces    │
│                                                      │
│ Solver-2 (Arithmetic)                               │
│   ├─ Optimized for math operations                  │
│   └─ Constraints from "numerical" traces            │
│                                                      │
│ Solver-3 (String Processing)                        │
│   ├─ Optimized for text operations                  │
│   └─ Constraints from "string" traces               │
│                                                      │
│ Solver-4 (General Purpose)                          │
│   ├─ Fallback for mixed-type programs               │
│   └─ Broader constraints, less specific             │
│                                                      │
│ Voting/Consensus: If k/4 solvers agree → return    │
└─────────────────────────────────────────────────────┘
```

## Main Ideas & Contributions

### 1. Offline Reasoning → Online Efficiency

The paper's central insight: **Expensive offline LLM reasoning can be "compiled" into cheap test-time symbolic solvers**, decoupling:
- Development cost (high: train solvers offline)
- Inference cost (low: run solvers at test time)

This flips the efficiency curve compared to pure LLM approaches where every inference is expensive.

### 2. Zero-Cost LLM Fallback

By using symbolic solvers as the primary mechanism, the framework achieves:
- **Base Performance:** Solvers alone reach 91.3% on PBEBench-Lite, 84.7% on hard instances
- **Hybrid Boost:** Neuro-symbolic combo improves hard-instance accuracy to 85.8% by combining solver suggestions with LLM refinement
- **Cost Efficiency:** 78% reduction in token consumption while improving accuracy

### 3. Task-Specific Solver Specialization

Different classes of synthesis problems benefit from different solvers. ReaComp learns to:
- Identify task type (list operations, arithmetic, string processing, etc.)
- Route to appropriate specialized solver
- Ensemble votes across solvers for consensus

### 4. Practical Program Synthesis

The results demonstrate that **symbolic approaches remain highly competitive** despite the LLM era, especially when seeded with reasoning patterns from LLMs.

## Methodology & Implementation

### Offline Solver Induction Pipeline

**Phase 1: Trace Collection**
1. Execute LLM reasoning on a dataset of synthesis tasks
2. Record complete reasoning traces (CoT, failed attempts, heuristics)
3. Annotate successful programs with execution traces

**Phase 2: Strategy Extraction**
1. Parse reasoning traces to identify recurring patterns:
   - Common operator sequences
   - Constraints on program structure
   - Failure modes to avoid
2. Cluster similar reasoning patterns
3. Extract formal rules (constraints) from each cluster

**Phase 3: DSL Compilation**
1. Define base DSL with operators relevant to task domain
2. Add constraints extracted from reasoning analysis
3. Compile constraints into solver-compatible form (SMT, CSP)
4. Create specialized solvers for each problem class

**Phase 4: Ensemble Construction**
1. Train individual solvers on task subsets
2. Implement voting/consensus mechanism
3. Test ensemble on validation set

### Datasets & Benchmarks

**PBEBench (Programming by Example):**
- **Lite:** Easier instances, ~70% baseline LLM accuracy
- **Hard:** Challenging instances, ~68% baseline LLM accuracy
- Tests synthesis from input-output examples

**SLR-Bench (Synthesis via Linear Representation):**
- Hard-tier instances where pure neural approaches struggle
- ReaComp improves from 34.4% → 58.0% (+16.6pp)

**Evaluation Metrics:**
- **Accuracy:** Percentage of programs generating correct output for all test cases
- **Token Consumption:** Total LLM calls (measures cost)
- **Inference Latency:** Wall-clock time for solving
- **Generalization:** Performance on out-of-distribution instances

### Experimental Results

**Standalone Symbolic Solvers:**
- PBEBench-Lite: **91.3% accuracy** (vs. LLM baseline: ~80%)
- PBEBench-Hard: **84.7% accuracy** (vs. LLM baseline: ~68%)
- SLR-Bench Hard-Tier: Significant improvement baseline (exact figures unavailable — see full paper)

**Neuro-Symbolic Hybrid (Solver + LLM Fallback):**
- PBEBench-Hard: **85.8% accuracy** (improvement from 68.4%)
- Token Reduction: **78% fewer LLM calls** vs. pure LLM approach
- SLR-Bench Hard-Tier: **58.0% accuracy** (improved from 34.4%, +16.6pp)

**Inference Efficiency:**
- Symbolic solvers: Milliseconds per task (no LLM latency)
- LLM fallback: Only for ~10-15% of instances (on hard benchmarks)
- End-to-end hybrid: Dramatic speedup over pure LLM approaches

**Outperformance vs. LLM Test-Time Scaling:**
- Pure LLM with test-time scaling (multiple attempts): +10pp improvement, high token cost
- ReaComp hybrid: +17.4pp improvement, 78% lower token cost
- Demonstrates symbolic compilation beats brute-force LLM scaling

## Practical Applications & Use Cases

### Automated Code Generation in Development Tools

**Use Case:** Developer tool suggests completing a utility function.

**Workflow:**
1. User writes partial function signature and doc string
2. Tool routes to "General Purpose" solver (multi-domain)
3. Solver synthesizes program from specifications in milliseconds (zero LLM cost)
4. If solver fails, LLM generates code as fallback
5. Cached solver patterns improve future completions

**Benefit:** Sub-second latency, predictable costs, fewer server calls.

### Test Case Generation

**Use Case:** Automatically generate test cases for new code.

**Workflow:**
1. Extract input-output examples from existing tests
2. Route to "List Operations" solver (if handling array data)
3. Synthesize test case generator program
4. Deploy generator to create diverse test cases
5. LLM refines edge cases if generator fails

**Benefit:** Fast test generation, reduced manual test writing.

### Refactoring & Code Transformation

**Use Case:** Refactor code to use new library APIs.

**Workflow:**
1. Old code snippet + new API specification
2. Symbolic solver translates old API calls to new API
3. Validates transformation preserves semantics (test-based validation)
4. Fallback to LLM for complex multi-step refactorings

**Benefit:** Automated code upgrades at scale, cost-efficient.

### Program Repair

**Use Case:** Autonomous debugging to fix failing code.

**Workflow:**
1. Failing program + error trace
2. Constrain solver: "fix must be local to function F"
3. Enumerate candidate fixes using symbolic solver
4. Test each candidate, accept first correct fix
5. If no symbolic fix works, escalate to LLM-based repair

**Benefit:** Fast, targeted repairs without expensive search.

## Insights & Implications

### Symbolic Methods Remain Competitive

Despite the LLM revolution, **symbolic program synthesis** (CSP, SMT solvers) achieves impressive results when seeded with reasoning patterns from LLMs. This challenges the narrative that pure neural approaches are superior.

### Neuro-Symbolic Hybrids Are Practical

Combining symbolic solvers (fast, deterministic) with LLM fallback (flexible, powerful) yields:
- Better accuracy than either approach alone
- Better efficiency than pure LLM
- Interpretability of symbolic decisions

### Offline Compilation Paradigm

The ability to "compile" expensive LLM reasoning into cheap test-time solvers opens new efficiency frontiers:
- Shift compute from inference to training time
- Enable real-time synthesis for interactive tools
- Reduce API costs for large-scale deployments

### DSL Design is Critical

The quality of extracted constraints (DSL design) directly impacts solver accuracy. Future work should focus on:
- **Automatic DSL Discovery:** Learn DSLs from reasoning traces without manual design
- **Adaptive Constraints:** Constraints that vary by task difficulty
- **Transfer Learning:** Reuse solvers across different task distributions

### Cost-Efficiency for Developer Tools

For production developer tools (code completion, refactoring, generation):
- Pure LLM: High latency, unpredictable costs
- ReaComp: Predictable costs (mostly symbolic solver), 78% token reduction
- Hybrid serves latency-critical and cost-critical applications

## Code & Resources

**Official Repository:** To be confirmed (check arXiv for updates)

**Dependencies:**
- LLM framework (Claude, GPT-4, or open-source LLM)
- Constraint solver: Z3 SMT solver or OR-Tools CSP solver
- Program synthesis toolkit: Prose, Sketch, or similar DSL framework
- Dataset: PBEBench, SLR-Bench (public benchmarks)

**Integration Path:**
1. Collect LLM reasoning traces on your synthesis task dataset
2. Design domain-specific DSL (operators, constraints)
3. Extract constraints from reasoning patterns
4. Compile to SMT/CSP solver
5. Validate solver accuracy on held-out test set
6. Deploy hybrid (solver + LLM fallback)

**Quick-Start Implementation Outline:**

```python
# Pseudocode for ReaComp pipeline
from llm_framework import LLM
from smt_solver import SMTSolver
from synthesis_dataset import SynthesisBench

# Phase 1: Collect reasoning traces
llm = LLM("claude")
traces = []
for task in SynthesisBench.train:
    reasoning_trace = llm.reasoning_prompt(task.spec)
    traces.append((task, reasoning_trace))

# Phase 2: Extract constraints
from constraint_extractor import ConstraintExtractor
extractor = ConstraintExtractor()
constraints = extractor.extract_from_traces(traces)

# Phase 3: Compile to SMT solver
dsl = define_dsl_for_domain("program_synthesis")
solver = SMTSolver(dsl, constraints)

# Phase 4: Evaluate hybrid approach
correct = 0
for task in SynthesisBench.test:
    # Try symbolic solver first
    program = solver.synthesize(task.spec)
    if program is None or not program.passes_tests(task.tests):
        # Fallback to LLM
        program = llm.synthesize(task.spec)
    
    if program.passes_tests(task.tests):
        correct += 1

print(f"Hybrid Accuracy: {correct / len(SynthesisBench.test)}")
```

## Related Work & Context

### Program Synthesis Literature

- **Inductive Synthesis:** PROSE (Microsoft), FlashFill synthesize from examples
- **Constraint-Based:** Sketch, Rosette use SMT solvers for synthesis
- **Neural Synthesis:** DeepCoder, CodeSearchNet use neural networks
- **Hybrid Approaches:** Constraint solving guided by neural models

### LLM-Based Code Generation

- **Code Completion:** GitHub Copilot, CodeCompletion based on LLM pretraining
- **Program Synthesis:** LLMs with reasoning (CoT) for complex synthesis tasks
- **Neuro-Symbolic:** Prior work combining neural and symbolic approaches

### Cost Optimization in ML

- **Model Compression:** Distillation, quantization to reduce inference cost
- **Caching:** Reusing computation across similar inputs
- **Offline Processing:** Heavy lifting at training time, lightweight inference

### Future Research Directions

1. **Automatic DSL Discovery:** Learn DSLs from LLM reasoning without manual design
2. **Adaptive Reasoning Compilation:** Different compilation strategies for different task classes
3. **Transfer Across Domains:** Reuse compiled solvers for related synthesis problems
4. **Human-Guided Compilation:** Programmers specify high-level synthesis strategies, automatically compile
5. **Verified Synthesis:** Formally prove correctness of compiled solvers
6. **Scaling to Complex Programs:** Extend to larger, more complex program synthesis tasks

### Implications for Development Automation

ReaComp demonstrates that **intelligent code generation tools can be both accurate AND efficient** by combining:
- LLM reasoning quality (offline)
- Symbolic solver efficiency (online)
- Fallback flexibility (hybrid)

This pattern will likely define next-generation developer tools that achieve production-grade cost efficiency while maintaining LLM-level flexibility.
