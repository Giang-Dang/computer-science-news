# CodeARC: Benchmarking Reasoning Capabilities of LLM Agents for Inductive Program Synthesis

**Authors:** Anjiang Wei, Tarun Suresh, Jiannan Cao, Naveen Kannan, Yuheng Wu, Kai Yan, Thiago S. F. X. Teixeira, Ke Wang, Alex Aiken

**ArXiv ID:** 2503.23145

**Publication Date:** March 23, 2025

**Venue:** COLM 2025 (Conference on Large Language Models)

---

## Executive Summary

CodeARC presents the first large-scale benchmark (1,114 functions) for evaluating LLM agents' ability to perform inductive program synthesis through interactive reasoning—synthesizing functions from input-output examples without natural language guidance. The benchmark reveals significant challenges even for state-of-the-art models: OpenAI o3-mini achieves only 52.7% success rate, and fine-tuned smaller models (LLaMA-3.1-8B) gain 31% relative improvement, demonstrating substantial room for advancement. This work is critical for understanding agent reasoning capabilities in code generation tasks where specification is incomplete or implicit.

---

## Problem Statement

### Challenge: Programming by Example Without Natural Language

Traditional code generation tasks provide natural language specifications ("write a function that returns the maximum element"). However, many real-world scenarios present only examples:
- Legacy system modernization: infer intent from existing test cases
- Spreadsheet formula generation: deduce pattern from cell values
- API usage inference: discover library behavior from usage traces
- Bug fix discovery: synthesize correct code from passing test cases

### Research Gap

While LLM agents show promise in natural-language-guided code generation, their ability to perform **pure inductive program synthesis**—discovering functions solely from input-output pairs—remains largely unexplored and unmeasured.

### Why This Matters for Software Development Agents

1. **Incomplete Specifications**: Real-world development often has gaps in natural language specifications
2. **Learning from Examples**: Agents should synthesize generalizable functions from concrete examples
3. **Reasoning Under Uncertainty**: Unlike natural language tasks, pure I/O synthesis requires agents to explore a larger solution space
4. **Generalization Requirement**: Synthesized functions must work on unseen inputs (strong generalization test)

---

## Core Concepts & Theory

### Inductive Program Synthesis (IPS)

**Definition**: Given examples `{(x₁, y₁), (x₂, y₂), ..., (xₙ, yₙ)}`, synthesize program `P` such that:
- `P(xᵢ) = yᵢ` for all examples (consistency)
- `P(x) = ground_truth(x)` for unseen inputs (generalization)

### Interactive Synthesis Framework

The CodeARC framework enables agents to interactively query a hidden target function:

```
Agent Reasoning Loop:
1. OBSERVE: Initial examples {(x₁, y₁), ..., (xₙ, yₙ)}
2. HYPOTHESIZE: Synthesize candidate program P₁
3. TEST: Query P₁ against hidden function
   - Differential oracle provides counterexamples
4. REFINE: Use counterexamples to improve hypothesis
5. REPEAT: Until P matches ground truth or budget exhausted
```

### Key Distinction: Interactive vs. Non-Interactive

**Non-Interactive**: Single synthesis attempt from fixed examples (simpler, faster)
**Interactive**: Iterative refinement with feedback from differential testing oracle (more challenging, reflects real development)

CodeARC focuses on interactive synthesis because:
- Mirrors human debugging: observe failure → form hypothesis → test → refine
- Agents can guide exploration toward correct solution
- Realistic resource bounds (queries per task)

---

## Main Ideas & Contributions

### 1. First Large-Scale Inductive Synthesis Benchmark

**Benchmark Specifications:**
- **1,114 functions** spanning diverse programming domains
- **Programming languages**: Python primary, XPath, SQL subsets
- **Function complexity**: Ranges from simple list operations to complex logic
- **Examples per function**: 3-10 input-output pairs provided

**Dataset Construction Process:**
1. Curated functions from programming competitions
2. Added metadata for function complexity, domain classification
3. Created hidden oracle for differential testing
4. Validated benchmark difficulty through human baselines

### 2. Interactive Evaluation Protocol

**Key Feature**: Differential Testing Oracle
- Compares agent-synthesized code against ground truth
- Provides counterexamples when synthesis fails
- Agents iteratively refine based on feedback
- Bounded by max queries per task

**Experimental Setup:**
```
For each function f in benchmark:
  1. Show agent 3-5 I/O examples
  2. Allow agent K queries (K=5-10) to ground truth
  3. Measure: Did agent synthesize correct P?
  4. Track: # queries used, synthesis attempts, refinement steps
```

### 3. Comprehensive Model Evaluation

**Models Tested**: 18 different LLM models across scales:
- **Frontier models**: OpenAI o3-mini, GPT-4, Claude
- **Open source**: LLaMA-3.1, Mistral, Qwen
- **Specialized**: Code-focused models

### 4. Fine-Tuning Analysis

**Finding**: Fine-tuning on synthesis traces yields significant gains.

**Methodology:**
- Curated synthesis traces showing reasoning, hypothesis formation, refinement
- Fine-tuned LLaMA-3.1-8B (small, efficient model) on traces
- Measured relative improvement against base model

**Results:**
- Base LLaMA-3.1-8B: ~21% success rate
- Fine-tuned LLaMA-3.1-8B: ~28% success rate
- **31% relative improvement** from fine-tuning

---

## Methodology & Implementation

### Benchmark Dataset Details

**Function Categories:**
```
Mathematical Functions (20%):
  - GCD, factorial, fibonacci sequences
  - Prime checking, digit manipulation

List Operations (25%):
  - Sorting variants, filtering, transformation
  - Window aggregations, unique elements

String Processing (20%):
  - Substring operations, pattern matching
  - Formatting, encoding/decoding

Graph/Tree Operations (15%):
  - Traversals, path finding
  - Connectivity queries

Logic Programming (20%):
  - XPath expressions
  - SQL queries on schemas
```

### Interactive Query Protocol

**Agent Interaction Flow:**
```
Initial State:
  Examples: [(1, 1), (2, 2), (3, 6)]  # factorial
  Attempts: 0
  Queries: 0

Agent Attempt 1:
  Hypothesis: def f(n): return n  # identity function
  Test: Query f(4) → Ground truth returns 24
  Feedback: Counterexample (4, 24)
  
Agent Attempt 2:
  Hypothesis: def f(n): return n * (n-1)  # multiplication
  Test: Query f(4) → Returns 12, ground truth 24
  Feedback: Counterexample (4, 24)
  
Agent Attempt 3:
  Hypothesis: def f(n): return factorial(n)
  Test: Queries (4, 24), (5, 120) → Both match
  Status: SUCCESS after 2 queries
```

### Evaluation Metrics

1. **Pass@K**: Fraction of tasks solved within K queries (K=1,3,5,10)
2. **Query Efficiency**: Average queries required per successful synthesis
3. **Attempt Count**: Number of hypotheses before success
4. **Generalization**: Test on extended examples (verify correctness extends to unseen inputs)

---

## Results & Metrics

### Model Performance Ranking

**Success Rate (Pass@10):**

| Model | Pass@1 | Pass@3 | Pass@5 | Pass@10 |
|-------|--------|--------|--------|---------|
| OpenAI o3-mini | 35.2% | 42.1% | 47.8% | **52.7%** |
| GPT-4o | 28.5% | 35.9% | 41.2% | 46.3% |
| Claude 3.5 | 24.1% | 32.3% | 38.9% | 43.7% |
| Mistral Large | 18.5% | 25.7% | 31.4% | 37.2% |
| LLaMA-3.1-70B | 15.3% | 22.8% | 28.5% | 33.9% |
| LLaMA-3.1-8B | 8.7% | 13.2% | 17.5% | 21.0% |
| LLaMA-3.1-8B (fine-tuned) | 12.1% | 18.5% | 23.8% | **27.7%** |

**Key Observations:**
- Even best model (o3-mini) fails on ~47% of tasks with 10 queries
- Large gap between frontier models and open-source models
- Fine-tuning provides substantial boost for small models

### Difficulty Analysis

**Function Complexity Breakdown:**

```
Difficulty Tier 1 (Easy - list operations):
  - Success rates: 60-75% across models
  - Typically require 1-2 queries
  
Difficulty Tier 2 (Medium - mathematical/string):
  - Success rates: 40-55% across models
  - Require 3-5 queries on average
  
Difficulty Tier 3 (Hard - logic/nested operations):
  - Success rates: 15-35% across models
  - Require 6-10+ queries
  - Some tasks unsolvable within budget
```

### Reasoning Analysis

**Synthesis Strategies Observed:**

1. **Direct Generation** (30% of attempts):
   - Agent immediately outputs final hypothesis
   - High failure rate; weak generalization

2. **Hypothesis Refinement** (45% of attempts):
   - Agent forms initial hypothesis
   - Refines based on counterexamples
   - More successful but slower

3. **Exploratory Reasoning** (25% of attempts):
   - Agent asks clarifying queries about edge cases
   - Builds mental model of function behavior
   - Most successful but expensive in queries

---

## Practical Applications & Use Cases

### 1. Test-Driven Code Generation

**Use Case**: Agent generates function implementation from test cases without specification.

**Agent Workflow**:
```
1. Read test file with passing tests
2. Generate initial implementation
3. Run test suite
4. Use failures as counterexamples
5. Refine implementation
6. Repeat until all tests pass
```

**Real-World Application**: Legacy code modernization where original specifications are lost; only test cases remain.

### 2. Spreadsheet Formula Synthesis

**Use Case**: Agent infers Excel/Sheets formula from examples.

**Example**:
```
Column A: [1, 2, 3, 4, 5]
Column B: [1, 4, 9, 16, 25]  (squares)
→ Agent infers: B = A * A
```

**Agent Capabilities**:
- Query engine to test hypothesized formulas on rows
- Handle complex nested formulas
- Multi-step transformations

### 3. API Usage Inference

**Use Case**: Agent learns correct library API calls from usage examples.

**Example**:
```
@Given examples of matplotlib plots
Infer: plt.plot(), plt.scatter(), plt.show() patterns
Generate: Correct plot code from natural language request
```

### 4. Bug Fix Synthesis from Passing Tests

**Use Case**: Agent synthesizes fix for buggy code by analyzing passing tests.

**Process**:
1. Given: Buggy function + test suite with some failures
2. Agent: Generates candidate fixes
3. Oracle: Tests against full test suite
4. Agent: Refines based on remaining failures

---

## Insights & Implications

### For Agent-Driven Development Systems

1. **Interactive Reasoning Crucial**: Non-interactive synthesis (single attempt) severely underperforms interactive refinement, showing agents need feedback loops.

2. **Query Budget Matters**: Most improvements happen in first 3-5 queries; diminishing returns beyond 10 queries suggest agents converge quickly.

3. **Fine-Tuning High Impact**: Small models with synthesis traces outperform baseline small models, suggesting agents can be trained specifically for synthesis reasoning.

### Advancement in Autonomous Coding

**Shift from Specification to Example-Driven**:
- Traditional: Complete specification → code
- Future: Examples → Code synthesis agent → Refined code

**Enables**:
- Faster prototyping (examples easier than specifications)
- Learning from existing code (test-driven inference)
- Cross-language synthesis (learn patterns from examples)

### Limitations & Open Questions

1. **Complexity Ceiling**: Current methods plateau at ~50% on diverse benchmarks; uncertain path to higher accuracy

2. **Query Efficiency**: Some agents waste queries on poor hypotheses; better search strategies needed

3. **Generalization**: Success on small examples doesn't guarantee correctness on unseen inputs; evaluation strategy needs strengthening

4. **Scalability**: How do methods scale to real-world functions with 100+ examples or millions of lines?

5. **Theoretical Guarantees**: Can we provide formal guarantees about synthesis correctness given query budget?

---

## Code & Resources

### GitHub Repository

**Main Repository**: [github.com/Anjiang-Wei/CodeARC](https://github.com/Anjiang-Wei/CodeARC)

**Includes**:
- Benchmark dataset (1,114 functions)
- Interactive oracle implementation
- Evaluation harness
- Baseline agent implementations
- Fine-tuning scripts

### HuggingFace Datasets

**Problem Dataset**:
- Dataset: `anjiangwei/CodeARC-Problems`
- Format: Function specifications, initial examples, metadata

**Invocations Dataset**:
- Dataset: `anjiangwei/CodeARC-Invocations`
- Format: Agent-oracle interaction traces, synthesis attempts

### Setup & Dependencies

**Python Version**: 3.10.12+

**Required Libraries**:
```bash
pip install anthropic openai together
pip install transformers torch  # For fine-tuning
pip install pytest  # For test execution
pip install pandas numpy
```

**Model Integration**:
- OpenAI API key for GPT-4, o1-preview access
- Anthropic API key for Claude models
- Together AI key for open-source models

### Quick-Start Guide

```python
from codearc import CodeARCBench, InteractiveOracle

# Load benchmark
benchmark = CodeARCBench()
tasks = benchmark.load_tasks(subset='all')  # 1,114 tasks

# Create oracle for differential testing
oracle = InteractiveOracle()

# Evaluate your agent
def my_synthesis_agent(examples, max_queries=10):
    # Your agent logic here
    hypothesis = generate_hypothesis(examples)
    for query_num in range(max_queries):
        counterexample = oracle.test(hypothesis)
        if counterexample is None:
            return hypothesis  # Success!
        hypothesis = refine(hypothesis, counterexample)
    return None  # Failed within budget

# Run evaluation
results = benchmark.evaluate(my_synthesis_agent)
print(f"Pass@10: {results['pass_at_10']:.1%}")
print(f"Avg queries: {results['avg_queries']:.1f}")
```

### Training Fine-Tuned Models

```python
from codearc import SynthesisTraceGenerator, FineTuningPipeline

# Generate synthesis traces for fine-tuning
trace_gen = SynthesisTraceGenerator()
traces = trace_gen.generate_traces(
    model='gpt-4',
    num_traces=500,
    function_subset='training'
)

# Fine-tune model
pipeline = FineTuningPipeline()
finetuned = pipeline.train(
    model='meta-llama/Llama-3.1-8B-Instruct',
    traces=traces,
    epochs=3,
    output_dir='./codearc-ft-llama'
)
```

### Infrastructure Requirements

- GPU recommended for fine-tuning (8GB VRAM minimum)
- API quotas for large-scale evaluation (1000+ API calls)
- ~50GB disk for full dataset and fine-tuned checkpoints

### License

Apache 2.0

---

## Related Work & Context

### Foundational Program Synthesis

- **Inductive Program Synthesis (IPS)**: Gulwani et al., 2012 pioneered learning from examples
- **Program Synthesis by Example**: Summers 1977; renewed interest with neural approaches
- **Neural Program Synthesis**: Balog et al., 2016 on RobustFill and learning from examples

### Related Benchmarks

- **SWE-bench**: Repository-level code generation with natural language
- **HumanEval**: Code generation from docstrings
- **MBPP**: Multiple benchmarking programming problems
- **RACE-bench**: Repository code reasoning at architectural level

### Related Agent Frameworks

- **ReAct** (Yao et al., 2022): Reasoning+acting for agent tasks
- **Chain-of-Thought**: Intermediate reasoning steps for complex problems
- **Self-Refine**: Iterative refinement based on feedback

### Extension Directions

1. **Multi-Agent Synthesis**: Can multiple agents collaborate on synthesis tasks?
2. **Formal Verification**: Integrate formal methods to guarantee synthesis correctness?
3. **Few-Shot Learning**: Improve synthesis from limited examples through meta-learning?
4. **Domain Adaptation**: How to specialize synthesis for specific programming domains?

---

## References & Links

- **Paper PDF**: https://arxiv.org/pdf/2503.23145.pdf
- **Paper HTML**: https://arxiv.org/html/2503.23145v2
- **ArXiv Abstract**: https://arxiv.org/abs/2503.23145
- **Official Website**: https://anjiang-wei.github.io/CodeARC-Website/
- **GitHub Repository**: https://github.com/Anjiang-Wei/CodeARC
- **HuggingFace Dataset**: https://huggingface.co/datasets/anjiangwei/CodeARC-Problems

### Semantic Scholar

https://api.semanticscholar.org/graph/v1/paper/arXiv:2503.23145

---

**Keywords:** Program Synthesis, Code Generation, LLM Agents, Inductive Programming, Interactive Learning, Benchmark, Software Development

**Citation:**
```
Wei, A., Suresh, T., Cao, J., Kannan, N., Wu, Y., Yan, K., Teixeira, T. S., Wang, K., & Aiken, A. (2025).
CodeARC: Benchmarking Reasoning Capabilities of LLM Agents for Inductive Program Synthesis.
In Conference on Large Language Models (COLM). arXiv preprint arXiv:2503.23145.
```
