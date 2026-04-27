# General365: Benchmarking General Reasoning in Large Language Models Across Diverse and Challenging Tasks

**ArXiv ID:** [2604.11778](https://arxiv.org/abs/2604.11778)  
**Published:** April 13, 2026  
**Authors:** Research team (details in paper)  
**Field:** Natural Language Processing / AI Evaluation  
**HuggingFace:** [https://huggingface.co/papers/2604.11778](https://huggingface.co/papers/2604.11778)

---

## Executive Summary

General365 is a new benchmark exposing a critical weakness in state-of-the-art LLMs: while current models achieve near-perfect scores on mathematical and scientific reasoning benchmarks, the **best model achieves only 62.8% accuracy** on General365's 365 seed problems and 1,095 variants spanning 8 general reasoning categories. By restricting required background knowledge to K-12 level, General365 isolates *reasoning ability* from *factual knowledge*, revealing that LLM reasoning is heavily domain-dependent and that genuine general reasoning—applicable across everyday situations—remains a significant open challenge.

---

## Problem Statement

The AI community has celebrated impressive benchmarks: GPT-4 and its successors approach human performance on the SAT, AMC math competitions, and programming contests. Models trained with RLVR (DeepSeek-R1, QwQ, Qwen3) post near-perfect scores on established math benchmarks like GSM8K and MATH.

However, these benchmarks share a common characteristic: they evaluate reasoning within **narrow, well-defined domains** where:
1. The problem structure is predictable (word problems, proofs, code)
2. The reasoning type is fixed (arithmetic, algebraic, algorithmic)
3. The answer format is standardized (numerical, true/false, code)

**General reasoning**—the kind humans use daily—is fundamentally different:
- Problems arise in diverse, unpredictable contexts
- Multiple reasoning types may be required in a single problem
- Background knowledge is limited to common sense and basic K-12 education
- Answer formats vary

By excelling at specialized mathematical reasoning but failing at general reasoning, LLMs demonstrate a form of **reasoning domain-dependence**: they have learned to reason within specific templates but have not developed generalizable reasoning capabilities.

### The K-12 Knowledge Constraint

A key methodological choice in General365 is **restricting required background knowledge to K-12 level**. This design decision:
- Ensures the benchmark measures *reasoning*, not *memorized facts*
- Makes the benchmark accessible to human evaluators for validation
- Prevents LLMs from "cheating" by recalling specialized domain knowledge

If a model fails General365, it cannot blame "insufficient knowledge"—the knowledge required is universally accessible. Failure must therefore reflect insufficient reasoning capability.

---

## Core Concepts & Theory

### The 8 General Reasoning Categories

General365 covers 8 categories of general reasoning:

| Category | Description | Example Task |
|----------|-------------|-------------|
| **Causal Reasoning** | Identify causes and effects, counterfactuals | "If this factory closes, what happens to the town's tax revenue?" |
| **Temporal Reasoning** | Order events, understand time relationships | "What could have happened between events A and B?" |
| **Spatial Reasoning** | Navigate 2D/3D space, mental rotation | "After following these directions, where are you relative to start?" |
| **Analogical Reasoning** | Find structural parallels between domains | "A is to B as C is to ?" in non-mathematical contexts |
| **Commonsense Reasoning** | Everyday physical and social world reasoning | "Why does this plan seem problematic?" |
| **Multi-step Logical Deduction** | Chain multiple inference steps | Complex syllogisms and constraint satisfaction |
| **Counterfactual Reasoning** | Reason about hypothetical alternatives | "If X had not happened, would Y still occur?" |
| **Pragmatic/Contextual Reasoning** | Infer meaning from context and implicit cues | "What does this action signal about the person's intentions?" |

### Benchmark Design Principles

**Seed problems + Variants**: Each of the 365 seed problems has 3 variants (surface rephrasing, distractors changed, context changed), yielding 1,095 total problems. This allows measuring:
- Whether models truly understand the reasoning or exploit surface patterns
- Consistency: does the model answer all variants of a seed problem correctly?

**Difficulty calibration**: Problems are calibrated to be challenging for current LLMs while remaining solvable by humans with K-12 knowledge. Problems where GPT-4 achieves >95% accuracy are excluded as "too easy"; problems where even expert humans achieve <60% are excluded as "ambiguous."

**Multi-choice format**: Problems are presented in multiple-choice format (4 options) to enable unambiguous automatic evaluation, with answer choices carefully designed to include common reasoning errors as distractors.

---

## Main Ideas & Key Contributions

### 1. Revealing the Reasoning Domain-Dependence Problem

The benchmark's most important contribution is empirical: demonstrating that top LLMs (including the best available at time of publication) achieve only 62.8% on General365, compared to near-100% on math benchmarks. This gap directly exposes reasoning domain-dependence.

### 2. Methodology for Decoupling Reasoning from Knowledge

The K-12 constraint and careful problem design methodology provides a template for future benchmarks that aim to isolate reasoning ability from factual recall.

### 3. Consistency Analysis

By testing seed problems and variants, General365 can distinguish models that reason reliably (consistent across variants) from models that reason superficially (high variance across variants). Current models show surprisingly high inconsistency.

### 4. Category-Level Diagnosis

The 8-category breakdown allows identifying which reasoning types are strongest and weakest for each model, enabling targeted improvement.

---

## Methodology & Implementation

### Problem Construction Process

1. **Expert problem writers**: Human domain experts write seed problems in each of the 8 categories
2. **K-12 knowledge audit**: Problems are reviewed to ensure no specialized knowledge is required
3. **Variant generation**: 3 variants per seed problem with surface rephrasing, distractor changes, and context changes
4. **Human validation**: All problems solved by human panels to confirm correctness and difficulty calibration
5. **Final curation**: 365 seed problems × 4 answer choices × 3 variants = 1,095 total problems

### Evaluation Protocol

- **Format**: Multiple-choice (4 options, 1 correct)
- **Prompting**: Chain-of-thought prompting (models encouraged to show reasoning steps)
- **Models evaluated**: 26 leading LLMs including GPT-4o, Claude Sonnet, Gemini Ultra, Qwen3-72B, and leading RL-trained reasoning models

### Key Results

| Model | Accuracy | Notes |
|-------|----------|-------|
| Top-performing model | **62.8%** | Best any model achieves |
| Human baseline | ~91% | K-12 problems are solvable for humans |
| Random baseline | 25% | 4-choice multiple choice |
| GPT-4o | ~58% | Below best model |
| RL-trained reasoning models | 55-62% | Math-specialized RL doesn't help much |

**Category breakdown** (estimated from paper context):
- Logical deduction: ~70% (strongest for LLMs)
- Commonsense: ~65%
- Causal reasoning: ~58%
- Counterfactual: ~55%
- Spatial reasoning: ~50% (weakest area)

---

## Practical Applications & Real-World Use Cases

### 1. LLM Development and Evaluation

General365 provides a critical new evaluation dimension for LLM developers. Teams building the next generation of models now have a reliable signal for whether improvements to math/code reasoning transfer to general reasoning.

### 2. Hiring and Aptitude Assessment AI

HR technology companies building AI assistants for job screening and aptitude testing need models with genuine general reasoning. General365 helps identify when models are ready for these applications.

### 3. Educational AI Systems

Intelligent tutoring systems that help students develop critical thinking skills require AI with genuine general reasoning. General365 exposes the gap between current AI and what's needed for these applications.

### 4. Safety-Critical Decision Support

AI systems that assist with decisions in uncertain, real-world situations (emergency management, crisis counseling, policy analysis) require general reasoning. General365 quantifies how far current AI is from the reasoning quality needed here.

---

## Insights & Implications

### The Illusion of General Reasoning

Perhaps the most important insight from General365 is that current LLMs give the *illusion* of general reasoning because math and code benchmarks are mistaken for general intelligence tests. General365 shows that mathematical problem-solving and general reasoning are partially separable skills, and LLMs have developed the former much more strongly.

### RLVR Does Not Generalize Automatically

Models trained with RLVR (like DeepSeek-R1, QwQ) that excel at math show only marginal improvements on General365. This suggests that RLVR training on math problems develops math-specific reasoning skills rather than general reasoning. (This motivates work like SUPERNOVA [2604.08477] that explicitly trains RLVR for general reasoning.)

### Consistency as a Probe for Reasoning Quality

The variant-based consistency analysis is a methodological insight: a model that reasons correctly about a problem should answer all variants correctly. High inconsistency rates suggest that models are pattern-matching rather than reasoning.

### Limitations

- **English-only**: General365 currently covers only English problems
- **Multiple-choice format**: Some reasoning tasks are naturally open-ended; forcing them into multiple choice may distort difficulty
- **Cultural specificity**: "Commonsense" reasoning may be culturally specific; the benchmark may inadvertently favor Western cultural contexts
- **Static benchmark**: Like all benchmarks, General365 will eventually saturate as models improve

---

## Code & Resources

- **Paper (arXiv)**: [https://arxiv.org/abs/2604.11778](https://arxiv.org/abs/2604.11778)
- **HuggingFace**: [https://huggingface.co/papers/2604.11778](https://huggingface.co/papers/2604.11778)

**Benchmark Usage**:
```python
# Via HuggingFace datasets (expected)
from datasets import load_dataset
dataset = load_dataset("general365")  # name may vary

# Evaluate a model
from transformers import pipeline
model = pipeline("text-generation", model="your-model")
for problem in dataset["test"]:
    response = model(problem["prompt"])
    # compare to problem["answer"]
```

---

## Related Work & Context

### Prior Reasoning Benchmarks
- **BIG-Bench / BBEH**: Large-scale LLM capability benchmarks
- **MMLU**: Massive multitask language understanding (knowledge-heavy)
- **ARC-Challenge**: Science reasoning for K-12 level
- **HellaSwag**: Commonsense inference

### Concurrent Work
- **SUPERNOVA** (2604.08477): Attempts to close the general reasoning gap via RLVR training
- **When Can LLMs Learn to Reason with Weak Supervision?** (2604.18574): Theoretical analysis
- **ICLR 2026 paper on LLM Reasoning Rethinking**: Conceptual analysis of reasoning types

### Future Directions
- Multilingual extension of General365
- Process-level evaluation: not just final answers but reasoning steps
- Dynamic difficulty: benchmark that adapts to model capability
- Connecting General365 performance to real-world task performance
