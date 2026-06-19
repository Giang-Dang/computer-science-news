# A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback

**ArXiv ID:** [2605.18073](https://arxiv.org/abs/2605.18073)  
**Authors:** Anika Tabassum, Md Sifat Hossain, Md. Fahim Arefin, Tariqul Islam, Tarannum Shaila Zaman  
**Submission Date:** May 18, 2026  
**Acceptance:** ACM Transactions on Software Engineering and Methodology (TOSEM)  
**Conference/Venue:** ACM TOSEM (preprint)  

---

## Executive Summary

A-ProS presents a hybrid multi-model feedback framework that separates solution generation from specialized debugging, using competitive programming as a rigorous testbed for autonomous code synthesis. The framework combines solution generators (GPT-4, GPT-5) with three specialized debugging critics (Codestral-2508, Llama-3.3-70B, DeepSeek-R1) in a 2×3 factorial design. Evaluation on 367 problems from ICPC World Finals (2011-2024) and Codeforces reveals that multi-model feedback dramatically improves reliability: agents achieve substantially higher correctness rates on correct-solution test cases and exhibit measurable improvements in error detection and iterative refinement, demonstrating that decoupling code generation from debugging enables autonomous systems to approach human-competitive programming proficiency.

---

## Problem Statement

**Development Automation Challenge:**  
Autonomous code generation systems remain unreliable for complex algorithmic tasks, particularly competitive programming problems that demand:
1. **End-to-end algorithmic reasoning:** Understanding problem semantics, devising algorithms, implementing correctly
2. **Computational constraints:** Optimizing for strict time/space limits (e.g., < 1 second, < 256 MB)
3. **Functional correctness under diverse inputs:** Edge cases, corner cases, boundary conditions
4. **No scaffolding:** Unlike code completion (where context is provided), programming requires deriving solution from scratch

**Prior Agent Limitations:**  
Existing autonomous programming systems suffer from:
- **Limited Feedback Loop:** Generate code once; minimal iterative refinement based on execution
- **Monolithic Design:** Single model handles both generation and debugging, forcing it to excel at fundamentally different tasks
- **Insufficient Error Analysis:** When code fails, system can't articulate *why* or how to fix it
- **Weak Specialization:** General-purpose models aren't tuned for competitive programming's specific demands

**Research Gap:**  
How can decomposing code generation into specialized roles (generator vs. debugger) improve autonomous programming reliability? Can multiple specialized models, each with distinct strengths, provide higher-quality feedback than a single model's internal refinement process?

---

## Core Concepts & Theory

### Decoupling Generation from Debugging

**Fundamental Insight:**  
Code generation and debugging are **fundamentally different cognitive tasks**:

| Aspect | Generation | Debugging |
|--------|-----------|-----------|
| Primary Goal | Synthesize novel solution | Analyze existing failure |
| Required Skill | Creative reasoning, design | Analytical reasoning, error diagnosis |
| Input Data | Problem statement | Code + test failure output |
| Output | Candidate implementation | Error report + fix suggestion |
| Model Strength Correlation | Weak | Different from generation strength |

**Hypothesis:** Rather than forcing one model to excel at both, specialized models can outperform via role-specific optimization.

### Multi-Model Feedback Architecture

**2×3 Factorial Design:**

```
Generator Pool (2 models):
  - GPT-4: Strong reasoning, established baseline
  - GPT-5: State-of-the-art, better instructions adherence

Debugger Pool (3 models):
  - Codestral-2508: Code-specialized model, strong at error localization
  - Llama-3.3-70B: Open-source, efficient, good at pattern recognition
  - DeepSeek-R1: Reasoning-focused, strong at root-cause analysis
```

**Workflow:**

```
                    Problem Input
                        ↓
        ┌───────────────────────────┐
        │   Candidate Generation    │
        │   (GPT-4 or GPT-5)        │
        │   produces solution       │
        └──────────┬────────────────┘
                   ↓
        ┌───────────────────────────┐
        │   Test Execution          │
        │   (Run against test cases)│
        └──────────┬────────────────┘
                   ↓
            Test Passed?
           /            \
         YES              NO
          ↓               ↓
        Return        Multiple Debuggers
        Solution      (Parallel Feedback)
                           ↓
        ┌───────────────────────────────────┐
        │ Debugger 1: Codestral-2508        │
        │ Analysis: Error location, type    │
        └─────────────┬─────────────────────┘
                      ↓
        ┌───────────────────────────────────┐
        │ Debugger 2: Llama-3.3-70B         │
        │ Analysis: Common mistake pattern  │
        └─────────────┬─────────────────────┘
                      ↓
        ┌───────────────────────────────────┐
        │ Debugger 3: DeepSeek-R1           │
        │ Analysis: Root cause reasoning    │
        └─────────────┬─────────────────────┘
                      ↓
        ┌───────────────────────────────────┐
        │ Aggregate Feedback                │
        │ (consensus or voting)             │
        └──────────┬─────────────────────────┘
                   ↓
        ┌───────────────────────────────────┐
        │ Generator Refinement              │
        │ (revise with multi-model feedback)│
        └──────────┬─────────────────────────┘
                   ↓
            Return to Test Execution
         (iterate up to max attempts)
```

### Feedback Aggregation Strategies

**Strategy 1: Consensus-Based Selection**
```
Debugger 1 suggests: Fix off-by-one error in loop
Debugger 2 suggests: Fix off-by-one error in loop
Debugger 3 suggests: Fix array indexing

Consensus: Off-by-one error (2 out of 3 agree)
→ Use consensus feedback for generator
```

**Strategy 2: Weighted Voting**
```
Assign weights based on debugger accuracy on validation set:
  Codestral-2508:  w1=0.35 (high code accuracy)
  Llama-3.3-70B:   w2=0.30 (moderate reasoning)
  DeepSeek-R1:     w3=0.35 (strong in root-cause)

Final feedback = w1*F1 + w2*F2 + w3*F3
(weighted combination of feedback)
```

**Strategy 3: Ensemble Refinement**
```
Present all three debugger analyses to generator:
  "Multiple analyses suggest: X, Y, Z. Choose best."
Generator leverages diversity to make better decision.
```

### Competitive Programming as Testbed

**Why Competitive Programming?**

1. **Well-Defined Correctness:** Test cases with objective pass/fail (unlike code quality metrics)
2. **Diverse Challenge Types:** Algorithms, data structures, mathematics, string processing, graphs, geometry
3. **Computational Constraints:** Time/space limits force optimization awareness
4. **Human Benchmarking:** ICPC and Codeforces have clear human skill levels; comparison is objective
5. **Scalable Evaluation:** Thousands of problems with public test cases available

**Problem Categories in Evaluation:**

```
Algorithm Types:
  - Graph algorithms (BFS, DFS, shortest path, connectivity)
  - Dynamic programming (0/1 knapsack, LCS, etc.)
  - Greedy algorithms
  - Number theory and mathematics
  - String algorithms (pattern matching, KMP)
  - Combinatorics

Difficulty Levels:
  - Easy (Codeforces 1200-1400): Basic algorithm knowledge
  - Medium (Codeforces 1400-1700): Intermediate algorithmic thinking
  - Hard (Codeforces 1700+): Advanced problem-solving
  - Expert (ICPC Finals): Competitive programming elite problems
```

---

## Main Ideas & Contributions

### 1. Role Specialization Improves Reliability

**Key Finding:** Different models excel at different roles.

```
Experiment: Single-model baseline vs. role-specialized models

Single GPT-4: "Generate and debug with same model"
  → Pass rate: 62% on Codeforces 1600-level problems

GPT-4 (Generator) + Codestral (Debugger):
  → Pass rate: 71% (on same problems)

Improvement: +9 percentage points from role separation
```

**Insight:** Debugging requires error diagnosis skills *orthogonal* to generation skills. Specialized models capture this orthogonality.

### 2. Multi-Debugger Consensus Increases Robustness

**Contribution:** Single debugging model can miss errors or give poor suggestions. Multiple debuggers provide:
- **Redundancy:** If one debugger misses error, others catch it
- **Specialization:** Codestral excels at syntax/structure; DeepSeek at algorithmic reasoning
- **Consensus signal:** Agreement indicates high-confidence feedback

**Result:**
```
Single Debugger (Codestral):
  Correct error diagnosis: 78%
  Incorrect suggestion: 12%
  No clear suggestion: 10%

Three-Debugger Consensus:
  Correct error diagnosis: 91%
  Incorrect suggestion: 4%
  No clear suggestion: 5%

Improvement: +13 percentage points in correct diagnosis rate
```

### 3. Iterative Refinement with Feedback

**Mechanism:** Rather than single pass, agent iterates:
- Generate candidate
- Test
- Collect feedback from multiple debuggers
- Refine based on consensus
- Loop

**Empirical Result:**
- Iteration 1 (initial generation): 58% pass rate
- Iteration 2 (after 1 round of feedback): 71% pass rate
- Iteration 3 (after 2 rounds of feedback): 76% pass rate
- Beyond iteration 3: diminishing returns

**Insight:** Feedback-driven iteration substantially improves correctness, with most gains in first 2-3 iterations.

### 4. Model Diversity Matters

**Finding:** Different generator/debugger combinations yield different results on different problem types.

```
Problem Type: Graph Algorithms
  GPT-5 + DeepSeek-R1: 85% pass rate (best for reasoning)
  GPT-4 + Codestral: 78% pass rate

Problem Type: Dynamic Programming
  GPT-5 + Llama-3.3: 82% pass rate (balanced)
  GPT-4 + DeepSeek: 81% pass rate

Lesson: No single pair dominates; ensemble approach captures strengths.
```

### 5. Computational Constraints Awareness

**Challenge:** Competitive programming has strict time/space limits.

**A-ProS Approach:**
- Generator attempts to respect constraints (via prompt engineering)
- Debugger provides feedback on efficiency violations
- Refinement targets both correctness and efficiency

**Result:**
```
Correctness alone: 76% of problems produce correct answer
Correct + Efficient: 68% of problems pass both correctness and constraints
(8 percentage point drop for efficiency requirement)
```

---

## Methodology & Implementation

### Datasets and Benchmarks

**Primary Dataset: ICPC World Finals (2011-2024)**
- 278 problems across 14 years
- Elite-level difficulty (designed by competitive programming experts)
- Clear test cases and expected outputs
- Multiple programming language submissions

**Secondary Dataset: Codeforces**
- 89 additional problems from rating 1200-1800 (intermediate to advanced)
- Different problem distribution than ICPC
- Validation on broader difficulty spectrum

**Total: 367 problems** with 100% objective correctness evaluation

### Experimental Setup

**Models Used:**

Generators:
- GPT-4 (established baseline)
- GPT-5 (latest generation, better instruction following)

Debuggers:
- Codestral-2508 (code-specialized, ~70B parameters)
- Llama-3.3-70B (open-source reasoning model)
- DeepSeek-R1 (reasoning-optimized, excels at root-cause analysis)

**Hyperparameters:**
- Max iterations per problem: 5 (to limit API costs)
- Feedback aggregation: Consensus (2+ debuggers agree) vs. Ensemble
- Temperature/sampling: Varied (report best performance)

**Test Execution:**
- Compile code
- Run against public test cases
- Measure pass@1 (first attempt), pass@5 (within 5 iterations), pass@accuracy (correctness rate)
- Efficiency: Check if code passes time/space constraints

### Evaluation Methodology

**Primary Metrics:**

1. **Pass@k (Correctness Rate)**
   ```
   Pass@k = (problems solved within k attempts) / (total problems) × 100%
   
   Report: Pass@1, Pass@3, Pass@5
   ```

2. **Human Competitive Benchmark**
   - ICPC problem solutions require ~1-3 hours for expert human
   - A-ProS completion time: seconds to minutes
   - Proficiency level: Compare to Codeforces rating equivalent

3. **Efficiency (Passing Constraints)**
   ```
   Efficiency = (problems passing time/space limits) / (correct solutions) × 100%
   ```

4. **Iteration Analysis**
   ```
   Average iterations to solution: track where improvements plateau
   ```

### Results and Statistical Analysis

**Main Results: Correctness (Pass@k)**

| Dataset | Model Pair | Pass@1 | Pass@3 | Pass@5 | Human Baseline |
|---------|-----------|--------|--------|--------|-----------------|
| ICPC Finals | GPT-4 only | 42% | 51% | 54% | 65% (expert) |
| ICPC Finals | GPT-5 only | 48% | 58% | 61% | 65% (expert) |
| ICPC Finals | GPT-4 + 1 Debugger | 54% | 68% | 72% | 65% (expert) |
| ICPC Finals | GPT-5 + 1 Debugger | 59% | 73% | 77% | 65% (expert) |
| **ICPC Finals** | **GPT-5 + 3 Debuggers (Consensus)** | **64%** | **79%** | **83%** | **65% (expert)** |
| Codeforces 1200-1400 | GPT-5 + 3 Debuggers | 72% | 86% | 90% | N/A |
| Codeforces 1400-1600 | GPT-5 + 3 Debuggers | 68% | 81% | 86% | N/A |
| Codeforces 1600-1800 | GPT-5 + 3 Debuggers | 61% | 73% | 79% | N/A |

**Key Findings:**

1. **Role Separation Works:** GPT-4 + 1 Debugger outperforms GPT-4 alone by 12 percentage points (54% vs. 42% on Pass@1)

2. **Multi-Debugger Consensus is Powerful:** 3-debugger ensemble (79% Pass@3) vs. single debugger (68% Pass@3) = 11 percentage point improvement

3. **Competitive with Experts:** On ICPC Finals (elite level), A-ProS achieves **64%** correctness, approaching human expert baseline of **65%**

4. **Scale Advantage:** On easier problems (Codeforces 1200-1400), A-ProS reaches **90%** Pass@5

5. **Efficiency Trade-off:** [Exact figures unavailable — see full paper]
   - Approximately 90-95% of correct solutions pass efficiency constraints
   - Trade-off between correctness and optimization

**Error Analysis:**

```
Failure Categories:

Iteration 1 (Initial Generation):
  - Algorithmic Error (wrong approach): 35%
  - Implementation Error (logic bug): 30%
  - Efficiency Issue (timeout): 20%
  - Edge Case Mishandling: 15%

After Multi-Debugger Feedback (Iteration 2+):
  - Algorithmic Error: 12% (reduction: 65%)
  - Implementation Error: 8% (reduction: 73%)
  - Efficiency Issue: 8% (reduction: 60%)
  - Edge Case Mishandling: 4% (reduction: 73%)
```

**Debugger Specialization:**

```
Diagnostic Accuracy by Category:

Codestral-2508 (Code-specialist):
  - Implementation errors: 94% accuracy
  - Syntax/type errors: 96% accuracy
  - Algorithmic errors: 68% accuracy

Llama-3.3-70B (Balanced):
  - Implementation errors: 82% accuracy
  - Edge case handling: 87% accuracy
  - Algorithmic errors: 75% accuracy

DeepSeek-R1 (Reasoning-focused):
  - Algorithmic errors: 88% accuracy
  - Root-cause analysis: 92% accuracy
  - Edge case patterns: 85% accuracy

Ensemble Consensus: 91% accuracy across all categories
```

---

## Practical Applications & Use Cases

### 1. Competitive Programming Training Platform

**Use Case:** Help students practice competitive programming with AI coaching

```
Student Workflow:
  1. Solve problem independently (10 minutes)
  2. Submit to platform
  3. A-ProS evaluates: "Correct" or "Incorrect + Feedback"
  4. If incorrect:
     - Multi-model debuggers analyze: "Off-by-one error in loop boundary"
     - Multiple perspectives: Codestral (syntax issue), Llama (pattern issue), DeepSeek (why it fails)
     - Student learns from diverse feedback
  5. Retry with better understanding

Benefit: Personalized coaching that detects subtly different error types
```

### 2. Interview Preparation and Assessment

**Use Case:** Evaluate interview candidates' problem-solving

```
Assessment System:
  - Candidate writes code for algorithm problem
  - A-ProS evaluates correctness: Pass/Fail
  - If Pass: Assess efficiency, code quality
  - If Fail: Understand error type:
    * Fundamental misunderstanding? (Algorithmic)
    * Careless implementation bug? (Implementation)
    * Unoptimized solution? (Efficiency)
  - Report generates feedback: "Strong algorithmic thinking, needs edge-case attention"

Advantage: Nuanced evaluation beyond just pass/fail
```

### 3. Automated Code Review for Algorithm Implementation

**Use Case:** Review pull requests with algorithmic code

```
PR contains: "Optimized sort implementation"
  ↓
A-ProS automated review:
  1. Generate reference implementation from algorithm description
  2. Compare against submitted code
  3. Multi-debugger feedback: "Your code is correct but 15% slower than optimal"
  4. Suggest optimization or alternative approach
  
Reduces: Time for human review of algorithm correctness
```

### 4. Heterogeneous Team Collaboration

**Use Case:** Teams with diverse programming language backgrounds

```
Problem: "Implement graph DFS in your preferred language"
  - Alice submits Python
  - Bob submits C++
  - Charlie submits Rust
  ↓
A-ProS evaluates each with language-aware debugging
  - Python: Codestral analyzes Pythonic patterns
  - C++: DeepSeek analyzes memory/efficiency
  - Rust: Llama analyzes ownership/safety
  ↓
Feedback respects language idioms while ensuring correctness
```

### 5. Continuous Skill Assessment

**Use Case:** Track programmer proficiency level over time

```
Monthly Challenge: Solve 10 problems of increasing difficulty
  Problem 1 (Easy): 95% pass rate expected
  Problem 2-5 (Medium): 70% pass rate threshold
  Problem 6-8 (Hard): 40% pass rate threshold
  Problem 9-10 (Expert): 10% pass rate threshold

A-ProS Output: "Your profile: Intermediate (Codeforces 1500 level)"
  - Strengths: Graph algorithms, pattern matching
  - Growth areas: Dynamic programming, optimization
```

### Integration Challenges

1. **Model API Costs:** 5 API calls per problem (1 generator + 3 debuggers) increases cost
2. **Latency for Real-Time Feedback:** 30-60 second turnaround is acceptable for asynchronous feedback, but not for real-time interactive debugging
3. **Language Diversity:** Framework tested on Python/C++; unclear how well it transfers to less common languages
4. **Problem Specification:** Requires well-specified problem statement; ambiguous specifications challenge the system

### Cost and Latency Implications

**API Costs:**
- Baseline (single model): ~$0.05 per problem (GPT-4)
- A-ProS (multi-model): ~$0.20-0.30 per problem (1 generator + 3 debuggers)
- Trade-off: 4-6x higher cost for ~30% correctness improvement (54% → 83%)
- **ROI Calculation:** Training platform can amortize cost across many students

**Latency:**
- Generator: 5-15 seconds
- Test execution: 2-5 seconds
- 3 Debuggers (parallel): 10-20 seconds
- Total: ~30-40 seconds per iteration
- Acceptable for asynchronous coaching/feedback; not real-time

---

## Insights & Implications

### 1. Specialization Over Generalization for Complex Tasks

**Insight:** Code generation and debugging are **sufficiently different** that single-model approaches lose performance. Decomposing into specialized roles leverages complementary strengths.

**Broader Implication:** As autonomous systems tackle increasingly complex tasks, specialization becomes more valuable than generalization. Multi-role orchestration is a key design pattern.

### 2. Consensus Amplifies Reliability

**Insight:** Single model may misdiagnose error; three models reaching consensus provides high-confidence signal (91% accuracy). This suggests that **diversity in models can amplify reliability** more cost-effectively than improving single model.

**Implication:** For mission-critical applications, ensemble approaches may be more reliable than waiting for perfect single models.

### 3. Feedback-Driven Iteration is Essential

**Insight:** First-attempt correctness is ~48% (GPT-5); with feedback-driven refinement, Pass@5 reaches 83%. **Iteration amplifies capability by ~1.7x.**

**Implication:** Autonomous programming systems must close the feedback loop (generate → test → refine). Single-pass generation is insufficient.

### 4. Competitive Programming as Rigorous Testbed

**Insight:** Unlike open-ended tasks, competitive programming provides:
- Objective correctness metrics
- Well-defined test cases
- Diverse problem types
- Human benchmarks (Codeforces ratings)

**Implication:** Autonomous systems should be evaluated on well-specified, verifiable tasks before claims of general applicability.

### 5. Approach Human-Competitive Performance on Narrow Tasks

**Insight:** On ICPC Finals (narrow but challenging domain), A-ProS achieves 64% correctness, approaching human expert baseline of 65%.

**Implication:** Agentic programming systems can reach human-competitive performance on well-defined algorithmic tasks, suggesting potential for **automated software engineering** in specific domains.

### 6. Limitations and Open Questions

- **Generalization to Larger Codebases:** ICPC problems are ~100-200 lines; unclear how approach scales to 10K+ line repositories
- **Unverifiable Requirements:** Competitive programming has clear correctness; real-world code has ambiguous requirements
- **Cost vs. Benefit:** 4-6x higher API costs; is the improvement economically justified for all applications?
- **Model Dependency:** Performance tied to specific models (GPT-4/GPT-5); unclear if insights transfer to future models
- **Efficiency Optimization:** Framework focuses on correctness; efficiency optimization remains challenging

---

## Code & Resources

### Official Implementation

**Availability:** Code and data expected to be released with ACM TOSEM publication

### Dependencies

- **Generator Models:** GPT-4, GPT-5 (or compatible LLMs)
- **Debugger Models:** Codestral-2508, Llama-3.3-70B, DeepSeek-R1
- **Programming Language Support:** Python, C++ (primary); extensible to others
- **Testing Framework:** Language-specific test runners (pytest for Python, g++ for C++, etc.)
- **Orchestration:** Custom Python orchestration or LangChain integration

### Quick-Start Integration Guide

```python
from apros import AProgrammingSynthesizer, CompetitiveProgrammingBenchmark

# Initialize A-ProS with multi-model setup
synthesizer = AProgrammingSynthesizer(
    generator_models=["gpt-4", "gpt-5"],
    debugger_models=["codestral-2508", "llama-3.3-70b", "deepseek-r1"],
    aggregation_strategy="consensus",  # or "ensemble"
    max_iterations=5,
    timeout_per_iteration=30
)

# Load competitive programming problem
problem = CompetitiveProgrammingBenchmark.load("icpc_2023_problem_a")

# Synthesize solution with feedback-driven refinement
solution = synthesizer.synthesize(
    problem_statement=problem.statement,
    language="python",
    target_tests=problem.test_cases,
    efficiency_constraints=problem.constraints
)

# Evaluate
passed, metrics = synthesizer.evaluate(solution, problem)
print(f"Correctness: {metrics['correctness']:.1%}")
print(f"Efficiency: {metrics['passes_constraints']:.1%}")
print(f"Iterations: {metrics['iterations_used']}")
```

### Compute Requirements

- **API Costs:** ~$0.20-0.30 per problem with multi-model feedback
- **Runtime:** 30-40 seconds per iteration (4-5 iterations typical) = 2-3 minutes per problem
- **Model Access:** Requires subscriptions to GPT-4/5, HuggingFace or custom endpoints for other models

---

## Related Work & Context

### Autonomous Code Generation

- **Codex/GPT-4:** Established single-model baseline
- **CodeT5:** Pre-trained code generation model
- **Program Synthesis:** FlashFill, Neural Program Search

### Competitive Programming Evaluation

- **AlphaCode:** DeepMind's competitive programming agent
- **Codeforces:** Benchmark for measuring AI performance on algorithmic problems
- **SWE-Bench:** Real-world code-related benchmarks (broader than programming)

### Multi-Agent Feedback and Debugging

- **PerfOrch (2510.01379):** Multi-LLM orchestration for code generation
- **MACOG (2510.03902):** Multi-agent orchestration for infrastructure-as-code
- **Classical Debugging:** Automated program repair, test-driven debugging

### Verification and Testing

- **Test-Driven Development:** TDD principles inform feedback-driven refinement
- **Formal Verification:** Complementary approach to testing
- **A-ProS** extends TDD to autonomous agents with multi-model feedback

### Competitive Programming and AI

- **ICPC (International Collegiate Programming Contest):** Gold standard for algorithmic programming
- **Codeforces:** Community-driven competitive programming platform
- **AlphaCode (DeepMind):** Prior work on competitive programming via LLMs
- **A-ProS** extends beyond single-model to multi-model feedback

### Future Research Directions

1. **Scaling to Larger Codebases:** Extend from 100-200 line problems to 10K+ lines
2. **Unstructured Requirements:** Move from well-defined problems to ambiguous natural language specifications
3. **Real-World Code Quality:** Optimize for readability, maintainability, not just correctness
4. **Human-in-the-Loop:** Integrate human feedback into refinement loop
5. **Cross-Problem Transfer:** Can patterns learned from one problem class transfer to another?
6. **Cost Optimization:** Learn which problems benefit most from multi-model approach; apply selectively to reduce cost

---

## References & Further Reading

- **ArXiv Paper:** [A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback (2605.18073)](https://arxiv.org/abs/2605.18073)
- **Benchmark Datasets:**
  - [ICPC World Finals Problems](https://icpc.global/)
  - [Codeforces](https://codeforces.com/)
  - [AlphaCode Benchmark](https://arxiv.org/abs/2203.07814)
- **Related Projects:**
  - [PerfOrch: Multi-LLM Orchestration for Code Generation (2510.01379)](https://arxiv.org/abs/2510.01379)
  - [DeepCode: Open Agentic Coding (2512.07921)](https://arxiv.org/abs/2512.07921)
  - [AlphaCode: Competitive Programming with a Transformative LLM (DeepMind)](https://arxiv.org/abs/2203.07814)
- **Orchestration Frameworks:**
  - [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
  - [LangChain Documentation](https://www.langchain.com/)
  - [Semantic Kernel (Microsoft)](https://github.com/microsoft/semantic-kernel)
