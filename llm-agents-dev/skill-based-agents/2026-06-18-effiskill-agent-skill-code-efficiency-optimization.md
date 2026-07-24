# EffiSkill: Agent Skill Based Automated Code Efficiency Optimization

**ArXiv ID:** [2603.27850](https://arxiv.org/abs/2603.27850)  
**Author:** Zimu Wang  
**Submitted:** March 27, 2026  
**Category:** CS.CL - Computation and Language

## Executive Summary

EffiSkill introduces a novel skill-based framework for automated code efficiency optimization, where reusable optimization skills encapsulate both concrete transformation mechanisms and higher-level procedural strategies. By mining slow-to-fast code pairs from large corpora, the system builds a portable library of Operator Skills (low-level transformations) and Meta Skills (high-level optimization strategies), enabling efficient code optimization without runtime execution or feedback. EffiSkill achieves 12.52 percentage point improvements over baselines and demonstrates skill portability across programming languages.

## Problem Statement

**Development Challenge:**
Code optimization is critical for production systems but remains largely manual:
- Developers must identify performance bottlenecks (profiling, flame graphs)
- Designers must understand optimization strategies (algorithm selection, data structure choices, system architecture patterns)
- Implementation requires careful code transformation while preserving correctness

**Prior Limitations:**
- Manual optimization: time-consuming, requires deep domain expertise
- LLM-based approaches: typically require runtime execution for feedback (slow), or lack structured optimization knowledge (generate code blindly)
- Fixed optimization libraries: don't adapt to new code patterns or emerging optimization techniques
- Lack of portability: learned strategies specific to one language or domain don't transfer

**Research Gap:** No system existed to:
1. Extract generalizable optimization knowledge from code corpora (slow → fast transformations)
2. Encapsulate this knowledge as reusable, composable skills
3. Apply skills without runtime execution or feedback
4. Transfer skills across languages and domains

## Core Concepts & Theory

### Skill-Based Optimization Architecture

EffiSkill's architecture combines two complementary skill layers:

```
┌──────────────────────────────────────────────────────────────────┐
│                    Optimization Task                             │
│  "Optimize this inefficient code for performance"                │
└────────────────────┬─────────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────────┐      ┌──────▼──────┐
    │ Diagnosis   │      │ Planning    │
    │ (detect     │      │ (compose    │
    │  bottleneck)│      │  skills)    │
    └────┬────────┘      └──────┬──────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌──────────▼────────────┐
         │  Skill Selection      │
         │  & Composition        │
         ├──────────────────────┤
         │ Meta Skills:          │
         │  - Loop Parallelization │
         │  - Caching Strategy   │
         │  - Data Structure     │
         │    Optimization       │
         └──────────┬────────────┘
                    │
         ┌──────────▼────────────┐
         │  Operator Skills      │
         │  Execution            │
         ├──────────────────────┤
         │ Operator Skills:      │
         │  - Loop Unrolling    │
         │  - Vectorization     │
         │  - Inlining          │
         │  - Memory Layout Fix │
         └──────────┬────────────┘
                    │
         ┌──────────▼────────────┐
         │  Candidate Gen.       │
         │  (optimized code)     │
         └───────────────────────┘
```

### Operator Skills: Low-Level Transformations

Operator Skills encode concrete code transformations that improve efficiency:

**Skill Definition Structure:**

```
OperatorSkill = {
  name: "Loop Unrolling",
  category: "loop_optimization",
  description: "Reduce loop iteration overhead by duplicating loop body",
  applicability_conditions: [
    "loop is fixed-iteration count",
    "loop body has no data dependencies across iterations",
    "loop body is small (< 50 lines)"
  ],
  transformation_pattern: [
    "detect loop: for i in range(n)"
    "unroll by factor k: for i in range(0, n, k): [execute k iterations]"
  ],
  execution_policy: "greedy",  -- Apply immediately when conditions met
  expected_speedup: "1.5-2.0x for small loops",
  correctness_guarantee: "semantic-preserving",
  example: {
    before: "for i in range(100): sum += arr[i]",
    after: "for i in range(0, 100, 4): sum += arr[i] + arr[i+1] + arr[i+2] + arr[i+3]"
  }
}
```

**Categories of Operator Skills:**

1. **Loop Optimizations**
   - Loop unrolling (reduce iteration overhead)
   - Loop fusion (combine nested loops)
   - Loop tiling (improve cache locality)
   - Vectorization (SIMD instruction usage)

2. **Data Structure Optimizations**
   - Array flattening (improve cache behavior)
   - Structure reordering (align hot fields)
   - Lazy initialization (defer allocations)

3. **Memory Optimizations**
   - Buffer allocation pooling (reduce allocation overhead)
   - Cache-aware data layout (improve cache hit rate)
   - Copy elimination (reduce memory bandwidth)

4. **Function-Level Optimizations**
   - Function inlining (reduce call overhead)
   - Constant propagation (pre-compute at compile time)
   - Dead code elimination (remove unused code)

### Meta Skills: High-Level Strategies

Meta Skills provide procedural guidance for selecting and composing Operator Skills:

**Skill Definition Structure:**

```
MetaSkill = {
  name: "CPU-Bound Loop Optimization Strategy",
  category: "high_level_strategy",
  description: "Detect CPU-bound inner loops and apply optimization sequence",
  applicability_conditions: [
    "function contains nested loops",
    "function call frequency is high (>10^6 calls)",
    "loop body is compute-intensive (> 50 operations)"
  ],
  procedure: [
    step1: "Detect innermost loop with high iteration count",
    step2: "Check for data dependencies (if none, loop-parallel)",
    step3: "Apply vectorization if SIMD applicable",
    step4: "Apply loop unrolling with factor k=4",
    step5: "Check correctness: run fast path tests",
    step6: "Measure speedup; accept if >= 1.3x"
  ],
  termination_criteria: "achieved 1.3x speedup or exhausted applicable skills",
  fallback_strategy: "revert to original if transformation increases code size > 50%",
  correctness_guarantee: "preserves semantics via test execution",
  expected_speedup: "1.5-3.0x for typical compute-bound loops"
}
```

**Meta Skill Examples:**

1. **CPU-Bound Optimization Strategy**
   - Detect compute-intensive code
   - Apply loop unrolling, vectorization, inlining
   - Measure and validate

2. **Memory-Bound Optimization Strategy**
   - Detect memory access patterns
   - Apply cache-aware data layout, tiling
   - Measure memory bandwidth improvement

3. **I/O-Bound Optimization Strategy**
   - Detect I/O bottlenecks
   - Apply async I/O, batching, prefetching
   - Measure I/O throughput improvement

### Skill Mining Pipeline

The system extracts skills from large-scale code corpora by mining slow-to-fast transformation pairs:

```
┌─────────────────────────────────────────────────┐
│  Input: Slow Code + Fast Code (same logic)      │
├─────────────────────────────────────────────────┤
│  Example:                                        │
│  Slow: sum = 0                                  │
│        for i in range(n):                       │
│          sum += arr[i]                          │
│                                                 │
│  Fast: sum = 0                                  │
│        for i in range(0, n, 4):                 │
│          sum += arr[i]+arr[i+1]+arr[i+2]+arr[i+3] │
└─────────────────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
    ┌────▼────────┐        ┌──────▼──────┐
    │ AST Diff    │        │ Pattern Matching │
    │ (analyze    │        │ (identify    │
    │  changes)   │        │  transformation) │
    └────┬────────┘        └──────┬──────┘
         │                         │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │ Extract Transformation  │
         │ Pattern & Conditions    │
         ├────────────────────────┤
         │ Pattern: loop unrolling │
         │ Conditions: fixed-iter, │
         │   no deps, small body   │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │ Generalize Pattern      │
         │ (extract parameterized  │
         │  transformation)        │
         └────────────┬────────────┘
                      │
         ┌────────────▼────────────┐
         │ Skill Definition        │
         │ (with templates &       │
         │  applicability rules)   │
         └────────────────────────┘
```

**Mining Algorithm:**

1. **Collection**: Gather pairs of slow and fast versions of the same code from:
   - GitHub commits (before/after performance improvements)
   - Code review comments mentioning performance
   - Benchmark improvements (e.g., LeetCode problem optimizations)

2. **Alignment**: Match slow code to fast code via semantic equivalence checking
   - Control flow graph matching
   - Data dependency verification

3. **Diffing**: Compare ASTs to identify transformations

4. **Pattern Extraction**: Abstract specific instances into parameterized patterns

5. **Generalization**: Extract applicability conditions and transformation templates

### Execution-Free Optimization Workflow

EffiSkill applies skills without runtime execution:

```
┌────────────────────────────────────────┐
│ Input: Inefficient Code                │
├────────────────────────────────────────┤
│ def find_max(arr):                     │
│   max = arr[0]                         │
│   for i in range(len(arr)):            │
│     if arr[i] > max:                   │
│       max = arr[i]                     │
│   return max                           │
└────────┬─────────────────────────────────┘
         │
┌────────▼─────────────────────────────────┐
│ Step 1: Diagnosis                        │
│ ├─ Identify loop                         │
│ ├─ Compute operation count               │
│ ├─ Profile data dependencies             │
│ └─ Classify: CPU-bound (simple compares) │
└────────┬─────────────────────────────────┘
         │
┌────────▼─────────────────────────────────┐
│ Step 2: Plan Composition                 │
│ ├─ Query Meta Skills:                    │
│ │   "Optimize CPU-bound comparison"      │
│ │ → retrieves CPU-Bound-Compare-Strategy │
│ ├─ Strategy specifies:                   │
│ │   1. Vectorization (if SIMD available) │
│ │   2. Loop unrolling (factor=4)         │
│ │   3. Early termination (optional)      │
│ └─ Generate execution plan               │
└────────┬─────────────────────────────────┘
         │
┌────────▼─────────────────────────────────┐
│ Step 3: Skill Retrieval & Composition    │
│ ├─ Retrieve Operator Skills:             │
│ │   - Loop Unrolling (1.5-2.0x speedup) │
│ │   - SIMD Vectorization (4.0x+ speedup)│
│ ├─ Compose in sequence                   │
│ └─ Resolve conflicts (if multiple skills │
│    apply, select non-conflicting subset) │
└────────┬─────────────────────────────────┘
         │
┌────────▼─────────────────────────────────┐
│ Step 4: Candidate Generation             │
│ ├─ Apply Loop Unrolling (factor=4)       │
│ │   def find_max_unrolled(arr):          │
│ │     max = arr[0]                       │
│ │     for i in range(0, len(arr), 4):    │
│ │       # 4 comparisons per iteration    │
│ │       m1 = arr[i] > max                │
│ │       m2 = arr[i+1] > max              │
│ │       # ... merge results              │
│ │     return max                         │
│ │                                         │
│ ├─ Apply SIMD Hint (code comment):       │
│ │   @simd                                │
│ │   for i in range(0, len(arr), 8):      │
│ └─ Return optimized code                 │
└────────────────────────────────────────┘
```

## Main Ideas & Contributions

### 1. Skill-Based Framework for Code Optimization

**Core Innovation:** Encapsulate optimization knowledge as reusable, composable skills rather than hand-coded rules or monolithic optimization engines.

**Why It Matters:**
- Portability: skills mined from Python apply to Java (with syntax adaptation)
- Composability: multiple skills can be combined (e.g., loop unrolling + vectorization)
- Explainability: each skill has clear applicability conditions and expected speedup
- Extensibility: new skills can be added incrementally without retraining

**Advantages Over Alternatives:**

| Approach | Portability | Composability | Explainability | Extensibility |
|----------|-------------|---------------|-----------------|---------------|
| Hand-coded rules | Low (rules per-domain) | Low | High | Low |
| LLM black-box | Medium | Low | Low | High |
| EffiSkill | High | High | High | High |

### 2. Operator + Meta Skill Separation

**Innovation:** Separate low-level transformation knowledge (Operator Skills) from high-level strategy knowledge (Meta Skills).

**Benefit:** Different expertise levels needed:
- Operator Skill mining: requires code transformation experts
- Meta Skill creation: requires algorithm/performance experts (fewer, can be manual)
- Composition: automatic (no experts needed)

This separation allows domain experts to contribute Meta Skills while system automatically mines Operator Skills.

### 3. Execution-Free Optimization

**Innovation:** Apply optimizations without runtime execution or feedback.

**Advantage:** Fast (no profiling overhead), safe (no risk of crash during optimization), scalable (optimize millions of code snippets in parallel).

**Mechanism:**
- Rely on proven transformation patterns (Operator Skills)
- Rely on expert-written strategies (Meta Skills)
- Apply heuristic correctness checks (control flow verification, data dependency checking)
- No runtime execution needed

**Trade-off:** Less precise than execution-based methods (can't measure actual speedup), but much faster and more scalable.

## Methodology & Implementation

### Skill Mining from Corpora

**Data Sources:**
- GitHub commits: extract before/after code pairs from performance-related commits (keywords: "optimize", "perf", "speedup", "bottleneck")
- Performance benchmarks: LeetCode solutions with multiple implementations at different optimization levels
- Code review comments: GitHub comments mentioning performance improvements
- Research papers: code snippets comparing baseline vs. optimized versions

**Mining Pipeline Steps:**

1. **Collection**: Gather 50K+ code pair triplets (language, slow code, fast code)
   - Filter: pairs must be semantically equivalent (same output for same input)
   - Verify: run both versions on test cases to confirm equivalence

2. **AST Diffing**: Extract syntactic differences between slow and fast versions
   - Build AST for each version
   - Compute AST diff (what nodes changed, added, deleted)
   - Filter: keep only pairs with localized changes (transformations affect < 5 AST nodes)

3. **Pattern Extraction**: Generalize specific transformations into parameterized patterns
   - Template slot variables: `loop_var`, `loop_body`, `unroll_factor`
   - Applicability conditions: extract constraints that make transformation valid
   - Example: Loop Unrolling pattern applies only if loop_body has no data dependencies across iterations

4. **Skill Assembly**: Convert patterns into skill definitions with metadata

5. **Validation**: Test mined skills on held-out code snippets
   - Apply skill to new code
   - Verify correctness (semantic equivalence checker)
   - Measure precision (% of applications that improve performance)

**Results:**
- Mined 2,847 Operator Skills
- Created 156 Meta Skills (combination of mined patterns + expert-written)
- Coverage: skills apply to 45% of optimization opportunities in EffiBench test set

### Experimental Setup

**Benchmarks:**
- **HumanEval-Optimization**: 100 Python problems with slow implementations; task is to generate optimized versions
- **EffiBench-X**: 500 diverse code snippets with known optimizations (custom benchmark)
- **LeetCode-Hard**: 300 challenging algorithmic problems (test on subset with performance-critical solutions)

**Models Tested:**
- GPT-4, Claude 3.5 Sonnet, Mistral 7B, Llama 70B
- Tested with vanilla prompting, chain-of-thought, and EffiSkill-augmented prompting

**Baselines:**
1. **Vanilla LLM**: Direct code generation without skills
2. **LLM + Code Comments**: Hints about optimization opportunities
3. **LLM + Optimization Rules**: Hand-coded optimization heuristics
4. **EffiSkill-Light**: Only Operator Skills, no Meta Skills
5. **EffiSkill-Full**: Both Operator and Meta Skills

**Metrics:**
- **Correctness**: Does generated code produce correct output?
- **Efficiency**: Does generated code improve performance? (compared to baseline)
- **Success Rate**: % of attempts that yield valid, optimized code

### Results and Metrics

**Main Results Table (HumanEval-Optimization, Pass@1):**

| Model | Vanilla | + Comments | + Rules | EffiSkill-Light | EffiSkill-Full | Improvement |
|-------|---------|-----------|---------|----------------|----------------|------------|
| GPT-4 | 71.5% | 73.2% | 74.8% | 81.3% | 84.0% | **+12.5%** |
| Claude 3.5 | 68.3% | 69.5% | 71.2% | 79.6% | 82.1% | **+13.8%** |
| Mistral 7B | 52.4% | 53.1% | 54.5% | 63.8% | 66.2% | **+13.8%** |
| Llama 70B | 58.7% | 59.8% | 61.2% | 70.4% | 72.9% | **+14.2%** |

**Analysis:**
- EffiSkill-Full achieves 12.5–14.2% improvement over vanilla prompting
- Improvement is consistent across model sizes (better for smaller models)
- Meta Skills contribute ~2–3% additional improvement over just Operator Skills

**Efficiency Gains (EffiBench-X):**

```
Average speedup of generated code:

Vanilla LLM:         1.2x (13% speedup)
+ Comments:          1.3x (30% speedup)
+ Rules:             1.5x (50% speedup)
EffiSkill-Light:     2.1x (110% speedup)
EffiSkill-Full:      2.4x (140% speedup)
```

EffiSkill achieves 2–2.4x speedups on average, with some optimizations reaching 5–10x on compute-bound code.

**Success Rate by Optimization Type:**

| Optimization Type | Vanilla | EffiSkill | Improvement |
|------|---------|-----------|------------|
| Loop Unrolling | 45% | 82% | +37pp |
| Vectorization | 38% | 71% | +33pp |
| Data Structure | 52% | 78% | +26pp |
| Caching/Memoization | 49% | 76% | +27pp |
| Function Inlining | 41% | 69% | +28pp |

**Cross-Language Transfer (trained on Python, applied to Java):**

| Optimization | Python Success | Java Success | Transfer Rate |
|------|--------|-----|----------|
| Loop Unrolling | 82% | 79% | 96% |
| Vectorization | 71% | 63% | 89% |
| Data Structure | 78% | 72% | 92% |
| Overall | 77% | 71% | 92% |

92% transfer rate demonstrates skill portability across languages.

**Skill Composition Analysis:**

```
Single Skill Application:        77% success, 1.8x speedup
Two Skills Composed:             84% success, 2.3x speedup
Three Skills Composed:           79% success, 2.1x speedup (conflicts reduce success)
Four+ Skills:                    62% success, 1.5x speedup (too many conflicts)

Optimal Composition Depth:       2–3 skills
```

Composing 2–3 skills achieves best results; more skills introduce conflicts and reduce success rate.

### Failure Modes & Analysis

**Types of Failures:**

1. **Inapplicable Skill Application** (18% of failures)
   - Skill applied when applicability conditions not met
   - Example: Loop unrolling applied to variable-iteration loop
   - Fix: Stricter condition checking needed

2. **Skill Conflicts** (12% of failures)
   - Two skills conflict (e.g., loop fusion contradicts loop unrolling)
   - Example: fusion wants to combine loops; unrolling wants to expand loop body
   - Fix: Build dependency graph to avoid conflicting skill combinations

3. **Incomplete Transformation** (8% of failures)
   - Skill partially applied, leading to incorrect code
   - Example: Loop unrolling updates loop condition but forgets to handle remainder iterations
   - Fix: Template-based generation with verification

4. **No Applicable Skills** (10% of failures)
   - Code pattern not covered by mined skills
   - Example: Custom data structure optimization not in skill library
   - Fix: Continuous skill mining to increase coverage

## Practical Applications & Use Cases

### 1. Automated Code Review for Performance

**Scenario:** Pull request submitted; CI system reviews for performance issues.

**Workflow:**
1. Parse changed functions
2. Apply Diagnosis: identify performance-critical functions
3. Retrieve applicable Meta Skills
4. Compose optimal Operator Skills
5. Generate optimized version
6. Compare performance (e.g., via profiling hint annotations)
7. If 1.3x+ speedup possible, comment on PR with suggestions

**Benefit:** Automated performance review reduces human effort; suggests concrete optimizations.

### 2. One-Shot Code Optimization for Deployments

**Scenario:** Production service has performance issue; developers want quick fix.

**Workflow:**
1. Extract problematic function from profiling data
2. Apply EffiSkill to generate optimized version
3. Run tests to verify correctness
4. Deploy if speedup achieves target (e.g., 1.2x+)

**Benefit:** Faster optimization cycle; reduces dependency on performance experts.

### 3. LLM-Assisted Programming with Performance Awareness

**Scenario:** Developer asks LLM to "generate efficient implementation".

**Workflow:**
1. LLM generates baseline code
2. Apply EffiSkill to optimize
3. Return optimized version to developer

**Benefit:** LLMs get performance-aware behavior without explicit instruction.

### 4. Skill Library for Custom Domains

**Scenario:** Organization has domain-specific optimization patterns (e.g., financial computation, scientific simulations).

**Workflow:**
1. Mine organization's code history for patterns
2. Extract domain-specific Operator Skills
3. Create domain-specific Meta Skills (expert-written)
4. Deploy skill library internally
5. Use for automated optimization across codebase

**Benefit:** Encodes organization's domain expertise; reusable across projects.

### Integration Challenges

**Real-World Considerations:**
- **Semantic Equivalence Verification**: Proving optimized code is correct is hard; EffiSkill uses heuristics (dependency checking, type analysis) but not full formal verification
- **Performance Variability**: Speedup depends on input size, hardware (CPU caches, SIMD capabilities); EffiSkill gives rough estimates
- **Skill Library Maintenance**: Skills need updating as programming languages and platforms evolve
- **Explainability**: Why did optimization apply? EffiSkill can trace skill composition but may need better explanations for users

## Insights & Implications

### 1. Optimization Knowledge is Encodable and Transferable

**Finding:** 2,847 Operator Skills mined from public corpora; 92% transfer rate across languages.

**Implication:** Optimization expertise is not language-specific; can be captured in language-agnostic skill definitions and adapted to new languages.

### 2. Execution-Free Optimization is Viable

**Finding:** EffiSkill achieves 2.4x average speedup without runtime execution; comparable to execution-based methods that require profiling.

**Implication:** Fast, scalable optimization is possible with static analysis + skill-based transformation; suitable for real-time code generation scenarios.

### 3. Skill Composition is Limited but Effective

**Finding:** 2–3 skill composition optimal; deeper composition introduces conflicts.

**Implication:** Optimization interactions are complex; automatic composition needs conflict detection. Manual expert guidance for deeper composition might be needed.

### 4. Meta Skills Enable Focused Optimization

**Finding:** Meta Skills (high-level strategies) contribute 2–3% improvement beyond Operator Skills.

**Implication:** Expert guidance on when/how to apply skills matters. Automatic skill application alone (Operator Skills) is good but incomplete; human experts can further guide strategy.

### 5. Practical Impact: Skill-Driven Developer Tools

EffiSkill demonstrates a new class of developer tools:
- **Skill-aware code generation**: LLMs + skills = efficient code without explicit instruction
- **Automated optimization**: No need to manually search optimization libraries
- **Domain-specific tuning**: Organizations can create custom skill libraries

## Limitations & Open Questions

1. **Correctness Verification**: Relies on heuristics (dependency checking); formal verification could strengthen guarantees.

2. **Skill Generalization**: Skills mined from specific contexts may not generalize. More work on skill abstraction and parameterization needed.

3. **Performance Prediction**: EffiSkill gives rough speedup estimates; more accurate prediction of actual performance improvement is needed.

4. **Deep Optimizations**: Complex optimizations requiring algorithm changes (e.g., switching from O(n²) to O(n log n)) are not addressed.

5. **Hardware-Specific Optimizations**: Skills for specific hardware (GPU, TPU, custom accelerators) not explored; SIMD hints provided but limited.

## Code & Resources

**Official Resources:**
- [Paper on arXiv (Abstract)](https://arxiv.org/abs/2603.27850)
- [Paper PDF](https://arxiv.org/pdf/2603.27850)
- [Paper HTML](https://arxiv.org/html/2603.27850v1)

**Related Frameworks:**
- **SoK: Agentic Skills** (2602.20867): Systematization of agentic skills beyond tool use
- **Agent Skills for Large Language Models** (2602.12430): Architecture and acquisition of agent skills
- **SkillFlow** (2605.13850): Flow-driven skill evolution for agentic systems

**Key Dependencies:**
- Code parser: AST library (language-specific)
- Semantic equivalence checker: can use simple pattern matching or formal methods
- LLM API: for code generation and composition planning

**Integration Guide:**
To apply EffiSkill:
1. Mine or curate Operator Skills for your domain
2. Write Meta Skills to encode high-level strategies
3. Integrate with LLM code generation pipeline
4. Use for optimization during generation or as post-processing step
5. Validate correctness and measure speedup empirically

## Related Work & Context

**Prior Work on Code Optimization:**
- Traditional compilers: hand-coded optimization passes; domain-specific but brittle
- Machine Learning for Optimization: learn from execution traces; slow, requires profiling
- AutoTuning Systems: search for optimal parameters; explores space exhaustively

**Skill-Based Frameworks:**
- [SoK: Agentic Skills -- Beyond Tool Use in LLM Agents](https://arxiv.org/abs/2602.20867) - Comprehensive taxonomy of agentic skills
- [Agent Skills for Large Language Models](https://arxiv.org/abs/2602.12430) - Architecture and lifecycle of agent skills
- [SkillFlow: Flow-Driven Recursive Skill Evolution](https://arxiv.org/abs/2605.13850) - Skill composition and evolution

**Code Generation & Optimization:**
- [LLM-Based Multi-Agent Systems for Code Generation](https://arxiv.org/abs/2604.16321) - Survey of multi-agent code generation
- [Large Language Model Guided Self-Debugging](https://arxiv.org/abs/2502.02928) - Self-correction in code generation

**Future Research Directions:**
1. **Formal Verification of Optimized Code**: Use SMT solvers to prove correctness of optimizations
2. **Learning Skill Composition Policies**: Train RL agents to learn optimal skill composition strategies
3. **Hardware-Aware Optimization Skills**: Skills specific to GPUs, TPUs, custom accelerators
4. **Skill Evolution**: Automatically improve skills based on feedback from real-world execution
5. **Cross-Domain Skill Transfer**: Mine skills from one domain (graphics) and transfer to another (simulation)

## References

- Wang, Z. (2026). EffiSkill: Agent skill based automated code efficiency optimization. *arXiv preprint arXiv:2603.27850*.

- [Paper on arXiv (Abstract)](https://arxiv.org/abs/2603.27850)
- [Paper PDF](https://arxiv.org/pdf/2603.27850)
- [Paper HTML](https://arxiv.org/html/2603.27850v1)
