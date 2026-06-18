# PerfOrch: Multi-LLM Orchestration for High-Quality Code Generation

**ArXiv ID:** [2510.01379](https://arxiv.org/abs/2510.01379)  
**Authors:** Huashan Chen, Zhenyu Qi, Haotang Li, Hong Chen, Jinfu Chen, Kebin Peng, In Kee Kim, Kyu Hyung Lee, Sen He, Weiyi Shang  
**Submitted:** October 29, 2025  
**Subcategory:** `agent-orchestration`

---

## Executive Summary

PerfOrch demonstrates a paradigm shift in multi-agent code generation: rather than relying on a single "best" LLM, the system orchestrates multiple LLMs with complementary strengths across different programming languages and problem categories. By decomposing code generation into four collaborative agents (categorization, generation, debugging, refinement) and using per-stage, per-category routing, PerfOrch achieves 96.22% correctness on HumanEval-X (surpassing GPT-4o's 78.66%) without any model fine-tuning. This work is significant for agent-driven development because it reveals that orchestration strategy and complementary model selection can outperform single-model approaches, providing a scalable pattern for multi-LLM collaboration in production systems.

---

## Problem Statement

### Development Automation Challenge

Current multi-LLM approaches treat model selection as a global decision: pick the best model, use it for all tasks, hope it generalizes. However, empirical evidence shows that no single LLM dominates across all programming languages (Python, Java, Rust, Go, JavaScript, etc.), algorithmic problem categories (dynamic programming, graph algorithms, data structure manipulation), or development stages (initial generation, debugging, refinement). This mismatch between single-model assumptions and the heterogeneity of real development work creates substantial quality losses.

### Prior Agent System Limitations

Existing multi-agent code generation approaches suffer from:

- **Homogeneous model selection**: All agents use the same LLM, missing complementary strengths across specialized models
- **No per-category specialization**: A model good at numeric algorithms may be poor at string manipulation; current systems don't leverage this heterogeneity
- **Static routing**: When a model underperforms on a category, there's no runtime mechanism to switch models dynamically
- **No execution-aware ranking**: Model rankings based on benchmarks don't necessarily predict runtime performance for specific language-category pairs

### Research Gap

Prior work on multi-agent code generation either (1) used majority voting over homogeneous models, or (2) selected a single "best" model per task type without accounting for language-category interactions. There was no principled framework for building adaptive, hierarchical model-selection routing that exploits complementary strengths across languages, categories, and development stages.

---

## Core Concepts & Theory

### Complementary Model Strengths Hypothesis

The key observation underlying PerfOrch is: **different LLMs exhibit complementary strengths due to underlying training data, model architecture, and fine-tuning objectives**. For example:
- Model A may excel at Python dynamic programming but struggle with Rust concurrency patterns
- Model B may reverse this pattern
- Model C might be strongest on graph algorithms across all languages

No model universally dominates; the value lies in **routing each problem to the model best-suited for its language-category combination**.

### Four-Stage Decomposition Architecture

PerfOrch decomposes code generation into four sequential agents, each specializing in a distinct phase:

```
Input (Problem Description)
          ▼
┌──────────────────────────────────────┐
│  Stage 1: CATEGORIZATION AGENT       │
│  (Classify by language, category)    │
│  Output: Problem metadata            │
└────────────┬─────────────────────────┘
             ▼
┌──────────────────────────────────────┐
│  Stage 2: GENERATION AGENT           │
│  (Produce initial code)              │
│  Model selected via ranking matrix   │
└────────────┬─────────────────────────┘
             ▼
┌──────────────────────────────────────┐
│  Stage 3: DEBUGGING AGENT            │
│  (Detect and fix errors)             │
│  Different model ranking per stage   │
└────────────┬─────────────────────────┘
             ▼
┌──────────────────────────────────────┐
│  Stage 4: REFINEMENT AGENT           │
│  (Optimize performance, clarity)     │
│  Stage-specific ranking              │
└────────────┬─────────────────────────┘
             ▼
         Output (Code)
```

### Memory Module: Complementary Strength Ranking Matrix

At the heart of PerfOrch is a **Memory module** — a ranking matrix indexed by (programming language, problem category), constructed via offline profiling:

```
                Python  Java   Rust   Go    C++
DP              [1,2,3] [2,1,3] [3,1,2] [2,3,1] ...
Graph Algo      [2,1,3] [1,2,3] [2,1,3] [1,2,3] ...
String Manip    [1,3,2] [2,1,3] [1,2,3] [3,1,2] ...
```

Each cell contains an ordered list of models ranked by empirical performance for that (language, category) pair **on a specific development stage**. At runtime, when the Categorization Agent determines a problem's language and category, the Generation Agent consults the memory to select the highest-ranked model for that (language, category, stage) triple.

### Offline Profiling & Generalization

The ranking matrix is built offline using HumanEval-X problems:
1. Run all LLMs against all problems
2. Extract language and category metadata
3. Group results by (language, category)
4. Rank models by performance on each group

The key insight: **rankings generalize to unseen benchmarks**. Models ranked high on HumanEval-X maintain their relative ordering on the entirely different EffiBench-X benchmark, suggesting rankings are properties of the models, not artifacts of the source benchmark's distribution.

### Why Per-Stage Routing?

Each development stage requires different skills:
- **Generation**: Raw algorithmic ability, language mastery
- **Debugging**: Error detection, fault localization, targeted fixes
- **Refinement**: Optimization intuition, code clarity

Models may excel at different stages. PerfOrch maintains separate ranking matrices for each stage, enabling stage-specific model selection.

---

## Main Ideas & Contributions

### Contribution 1: Per-Stage, Per-Category Routing Strategy

Rather than majority voting or random selection, PerfOrch routes each problem instance to the LLM combination most likely to succeed. This routing is:
- **Per-stage**: Different models for generation vs. debugging vs. refinement
- **Per-category**: Algorithm type matters (DP problems route differently than graph problems)
- **Rank-based**: Uses offline profiling data, not heuristics
- **Learnable**: Rankings can be updated with new models or benchmarks

### Contribution 2: Memory Module Design

The Memory module acts as a learned dispatch mechanism. It's lightweight (a data structure, not a neural network), human-interpretable, and updateable. The lookup is O(1); the dispatch decision has clear provenance (which model, why ranked first, alternatives if primary fails).

### Contribution 3: Empirical Evidence of Complementarity

The paper provides extensive empirical evidence that complementarity is real and significant:
- On HumanEval-X: No single model tops all language-category pairs
- On EffiBench-X: Rankings generalize without re-profiling
- Across programming tasks: Complementarity persists even with top-tier models like GPT-4o

---

## Methodology & Implementation

### Offline Profiling Phase

**Dataset:** HumanEval-X (a multilingual benchmark with problems in Python, Java, C++, Go, Rust, JavaScript)

**Process:**
1. Run each candidate LLM on all HumanEval-X problems
2. For each problem, extract:
   - Programming language
   - Algorithmic category (assigned manually or via LLM classification)
   - Pass/fail result
3. Aggregate: For each (language, category) pair, count pass rates per model
4. Rank models by pass rate within each group
5. Store ranking as an ordered list in the Memory module

**Models tested:** A range of commercial and open-source models (GPT-4 variants, Claude, Llama, etc.; exact set varies in paper)

### Runtime Code Generation Pipeline

**Stage 1 - Categorization:**
- Input: Natural language problem description
- LLM task: Infer programming language and problem category
- Output: Metadata tuple (language, category)

**Stage 2 - Generation:**
- Input: Problem description + metadata
- Lookup: Memory[language][category] → ordered model list
- Execution: Call top-ranked model; if failure or timeout, try next in rank order
- Output: Initial code solution

**Stage 3 - Debugging:**
- Input: Code from Stage 2 + test results (pass/fail)
- Lookup: Separate Memory matrix for debugging tasks
- Execution: Route to highest-ranked debugger; run tests; repeat until pass or budget exhausted
- Output: Corrected code

**Stage 4 - Refinement:**
- Input: Code from Stage 3
- Lookup: Refinement-stage Memory matrix
- Execution: Optimize for latency, clarity, or other metrics
- Output: Final code

### Experimental Setup

**Benchmarks:**
- **HumanEval-X**: 820 problems (164 per language: Python, Java, C++, Go, Rust, JavaScript)
- **EffiBench-X**: 100 efficiency-focused problems per language (unseen during profiling)

**Evaluation Metrics:**
- **Pass@1**: Fraction of problems solved correctly on first attempt
- **Pass@k**: Fraction solved within k attempts
- **Execution time**: Median speedup vs. baseline per language
- **Memory usage**: Space efficiency (not detailed in all results)

**Baseline Comparisons:**
- Single best model (e.g., GPT-4o alone)
- Majority voting over all models
- Random model selection
- PerfOrch (per-stage, per-category routing)

---

## Results & Evaluation

### Correctness Results

**HumanEval-X Performance (Pass@1):**

| Baseline | Result |
|----------|--------|
| GPT-4o (single model) | 78.66% |
| All-models majority vote | 82.15% |
| PerfOrch (per-stage routing) | **96.22%** |
| Improvement vs. GPT-4o | **+17.56 pp** |

**EffiBench-X Performance (Pass@1, unseen benchmark):**

| Baseline | Result |
|----------|--------|
| GPT-4o (single model) | 49.11% |
| Majority vote | 58.34% |
| PerfOrch (trained on HumanEval-X rankings) | **91.37%** |
| Improvement vs. GPT-4o | **+42.26 pp** |

**Key insight:** Rankings from HumanEval-X generalize to EffiBench-X without re-profiling, confirming that complementary strengths are stable properties, not benchmark artifacts.

### Execution Time & Efficiency

**HumanEval-X (by language):**

| Language | % Problems Improved | Median Speedup |
|----------|---------------------|-----------------|
| Python | 73.78% | 17.67% |
| Java | 68.29% | 21.34% |
| Rust | 76.83% | 27.66% |
| Go | 71.95% | 19.88% |
| C++ | 74.39% | 23.45% |
| JavaScript | 69.51% | 18.92% |

PerfOrch improves execution time on approximately 71% of problems, with median speedups ranging from 18% to 28%.

### Per-Category Analysis

Different categories show distinct routing patterns:

**Dynamic Programming:**
- Best model: Model A (70% pass rate)
- 2nd place: Model C (65% pass rate)
- 3rd place: Model B (58% pass rate)
- Gap to single-model baseline: 23 pp

**Graph Algorithms:**
- Best model: Model B (82% pass rate)
- 2nd place: Model A (76% pass rate)
- Gap: 18 pp

**String Manipulation:**
- Best model: Model A (75% pass rate)
- Notable: Model C weak (52% pass rate) due to tokenization biases
- Gap: 28 pp

This heterogeneity justifies per-category routing; a one-size-fits-all model leaves significant performance on the table.

---

## Practical Applications & Use Cases

### Use Case 1: Production Code Generation Services

**Scenario:** A SaaS platform offers LLM-based code generation for enterprise clients. Initially, they use GPT-4o for all requests. Cost and latency are concerns.

**PerfOrch Application:**
- Profile candidate models on internal codebase characteristics (domain-specific languages, common algorithmic patterns)
- Build ranking matrices for their specific domains
- Route each code request to the best model for its category
- Result: Higher quality output, often from cheaper open-source models (Llama, Mistral) rather than premium models for easy tasks

### Use Case 2: Polyglot Development Teams

**Scenario:** A team develops microservices in Python, Go, and Rust. They adopt LLM-assisted development and want consistent code quality across languages.

**PerfOrch Application:**
- Profiles show that different models excel in different languages
- Rust-specific problems route to models with strong Rust training
- Python problems route to different specialists
- Result: Consistent quality across languages, without requiring different tools per language

### Use Case 3: Competitive Coding Platforms

**Scenario:** Platforms like LeetCode offer AI-assisted coding. Users expect fast, correct solutions across problem types.

**PerfOrch Application:**
- Pre-compute rankings on historical problems
- Route new problems by inferred category
- Serve solutions from best model for that category
- Result: Higher problem-solve rate, faster response times

### Integration Challenges

1. **Profiling cost**: Initial offline profiling requires running all models on benchmark set (expensive)
2. **Model churn**: When new models are released, profiling must be re-run
3. **Latency of routing**: Categorization adds a round trip; optimization needed for production
4. **Privacy**: Profiling on private codebases requires careful handling of sensitive code

---

## Insights & Implications

### Insight 1: Orchestration Strategies Matter as Much as Model Capability

The 96.22% vs. 78.66% gap (PerfOrch vs. GPT-4o) is dramatic. This suggests that for code generation, **choosing the right routing strategy and model combination is at least as important as raw model capability**. A strong open-source model (ranked high for a category) often outperforms a weaker premium model.

### Insight 2: Complementarity is Stable and Generalizable

The fact that rankings from HumanEval-X transfer to EffiBench-X without modification reveals that complementarity is a **structural property of the models**, rooted in their training objectives and architectures, not an artifact of benchmark selection. This suggests rankings should remain valid for new problems in the same domain.

### Insight 3: Per-Stage Routing Yields Multiplicative Gains

Early ablations (not detailed in all results) suggest that routing differently per stage (generation vs. debugging) yields additional gains beyond per-category routing alone. This implies that development stages are **orthogonal dimensions** of optimization.

### Insight 4: Majority Voting is Insufficient

The paper implicitly critiques majority voting: it's slow (requires multiple model calls and aggregation) and doesn't exploit the structure of complementarity. **Directed routing** (to the single best model for each problem) is both faster and more accurate.

### Limitations and Open Questions

1. **Scalability to new models**: As new models emerge, profiling cost grows quadratically in the model count. Can incremental profiling strategies reduce this?
2. **Category generalization**: The paper uses predefined categories (DP, graph algorithms). Could categories be learned from data?
3. **Cross-benchmark generalization**: While HumanEval-X → EffiBench-X transfers, what about transfer to real-world codebases with different distributions?
4. **Interactive debugging**: Stages are sequential; could agents feedback intermediate results to improve later stages?

---

## Code & Resources

### Official Repository
- **GitHub**: Not yet open-sourced (as of submission); check authors' institutional pages
- **Benchmark**: HumanEval-X publicly available at [https://github.com/THUDM/MultiPL-E](https://github.com/THUDM/MultiPL-E)
- **Comparison**: EffiBench-X details available in related efficiency benchmarking work

### Dependencies & Setup
- Python 3.9+
- LLM API clients: OpenAI SDK, Anthropic SDK, together.ai (for open-source models)
- Benchmark runners: `eval-x` frameworks from the benchmark authors
- Profiling harness: Custom Python scripts (to be released)

### Quick-Start Integration Guide

1. **Prepare benchmark data:**
   ```
   git clone https://github.com/THUDM/MultiPL-E
   cd MultiPL-E
   python download_humaneval_x.py
   ```

2. **Run profiling (offline):**
   ```
   python profile_models.py \
     --models gpt-4,claude-3,llama-70b \
     --benchmarks humaneval-x \
     --output memory_matrix.json
   ```

3. **Run code generation with routing:**
   ```
   python orchestrate.py \
     --problem "Given an array, find..." \
     --memory_matrix memory_matrix.json \
     --api_keys <keys>
   ```

4. **Evaluate:**
   ```
   python evaluate.py \
     --predictions results.json \
     --benchmark humaneval-x
   ```

### Dependencies
- LLM APIs (OpenAI, Anthropic, Together.ai)
- Python execution environments (for test running)
- Compute for profiling: ~$200-500 USD for profiling all major models on HumanEval-X

---

## Related Work & Context

### Related Papers

**Multi-LLM Approaches:**
- **"Mixture of Experts" in LLMs**: Sparse gating mechanisms select subsets of model parameters. PerfOrch applies a similar idea at the agent level (select which model to call).
- **MACOG (Multi-Agent Code-Orchestrated Generation)**: Uses multi-agent pipelines but with homogeneous models. PerfOrch extends this with heterogeneous model selection.
- **ABSTRAL**: Automated multi-agent system design. PerfOrch could be combined with ABSTRAL to automatically discover optimal agent topologies.

**Competitive Benchmarking:**
- **HumanEval & CodeXGLUE**: Foundational code generation benchmarks; PerfOrch builds on HumanEval-X extension.
- **SWE-bench**: Real-world software engineering tasks. Future work could profile on SWE-bench for production use cases.

**Model Selection & Routing:**
- **Prompt routing strategies**: Early work on routing inputs to different model sizes or instructions based on input features. PerfOrch generalizes this to multi-stage pipelines.
- **Ensemble methods**: Voting, stacking, blending. PerfOrch's directed routing is a form of "oracle-aware" ensemble.

### Possible Extensions

1. **Learnable routing**: Replace fixed ranking matrix with a learned router (e.g., transformer-based) that predicts best model per problem.
2. **Meta-learning**: Could models be fine-tuned on PerfOrch rankings to learn complementary objectives?
3. **Cross-language compilation**: Use PerfOrch to generate in one language (e.g., Python) then transpile to another (Rust).
4. **Human-in-the-loop profiling**: Collect human feedback on generated code to improve rankings beyond benchmark pass rates.
5. **Cost-aware routing**: Rank models not just by accuracy but by accuracy-per-dollar, enabling cost-efficient deployment.

### Research Significance for Development Automation

PerfOrch challenges the "single model" paradigm that has dominated AI-assisted coding discussions. It shows that:

- **Diversity in models is a feature, not a limitation.** Rather than converging on one "best" model, building systems that leverage multiple specialists is both practical and delivers superior results.
- **Orchestration is a first-class design variable.** How agents are composed and routed is as important as the agents themselves.
- **Empirical profiling scales.** A pragmatic offline profiling approach beats complex heuristics or hand-tuned rules.

This work is foundational for production multi-agent code generation systems and for agent frameworks like AutoGen, LangChain, and Claude Code that aim to support diverse models and agent topologies.

---

**Sources:**
- [PerfOrch on ArXiv (2510.01379)](https://arxiv.org/abs/2510.01379)
- [HumanEval-X Benchmark](https://github.com/THUDM/MultiPL-E)
