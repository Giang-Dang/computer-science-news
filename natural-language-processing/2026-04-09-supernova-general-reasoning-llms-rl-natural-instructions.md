# SUPERNOVA: Eliciting General Reasoning in LLMs with Reinforcement Learning on Natural Instructions

**ArXiv ID:** [2604.08477](https://arxiv.org/abs/2604.08477)  
**Published:** April 9, 2026  
**Authors:** Ashima Suvarna, Kendrick Phan, Mehrab Beikzadeh, Hritik Bansal, Saadia Gabriel  
**Institution:** University of California, Los Angeles  
**Field:** Natural Language Processing / Machine Learning  

---

## Executive Summary

SUPERNOVA is a data curation framework for Reinforcement Learning with Verifiable Rewards (RLVR) that extends strong RL-based reasoning from specialized domains (math, code) to general reasoning tasks such as causal inference, temporal understanding, and logical deduction. By systematically mining large-scale instruction-tuning datasets for verifiable training signal, SUPERNOVA enables models trained on its curated data to outperform strong baselines by up to **52.8% relative improvement** on the challenging BBEH benchmark. This work directly addresses one of the most important open problems in LLM reasoning: why do current models reason well in math but poorly in general settings?

---

## Problem Statement

Reinforcement Learning with Verifiable Rewards (RLVR) has revolutionized LLM reasoning in formal domains. Systems like DeepSeek-R1, QwQ, and others have demonstrated dramatic improvements in mathematical and code reasoning by rewarding correct final answers and penalizing incorrect ones—without needing dense supervision on intermediate reasoning steps.

However, **general reasoning**—causal inference, commonsense reasoning, temporal understanding, spatial reasoning, analogical thinking—has not benefited from RLVR to the same degree. The root cause is a data bottleneck: RLVR requires (a) problems with clear, verifiable correct answers, and (b) sufficient diversity to cover all reasoning skills. Math competitions and coding challenges naturally satisfy (a), but general reasoning tasks do not have standardized answer verification pipelines.

The gap has serious practical consequences: LLMs that excel at math olympiad problems still struggle with tasks like "What would happen if X?" or "Which event happened before Y?" that require genuine reasoning about the world rather than symbolic manipulation.

---

## Core Concepts & Theory

### Reinforcement Learning with Verifiable Rewards (RLVR)

RLVR trains a policy `π_θ` (the LLM) to maximize expected reward `R` on a distribution of problems `P`:

```
max_θ E_{p~P, y~π_θ(·|p)}[R(y, p)]
```

Where:
- `p` = input problem
- `y` = model output (chain-of-thought + final answer)
- `R(y, p)` = binary reward: 1 if answer is correct, 0 otherwise

The reward function `R` must be **verifiable**—deterministically checking correctness. For math, this means exact-match or symbolic equivalence checking. For code, this means running test cases.

### Why General Reasoning Lacks RLVR Data

General reasoning tasks from benchmarks like BIG-Bench, MMLU, or commonsense QA have multiple-choice answers that could, in principle, serve as verification signals. However, they typically suffer from:

1. **Label noise**: Human-annotated answers may be inconsistent
2. **Ambiguity**: Multiple interpretations of a question may all be "correct"
3. **Small scale**: Not enough problems to drive RL training
4. **Skill imbalance**: Benchmarks oversample certain reasoning types

### The SUPERNOVA Insight: Mining Instruction-Tuning Datasets

The key insight is that **large-scale instruction-tuning datasets** (like FLAN, Natural Instructions, Super-Natural Instructions) contain millions of tasks with expert-annotated ground-truth answers. These datasets were originally created for supervised fine-tuning but contain rich, diverse reasoning problems with verifiable outputs.

SUPERNOVA repurposes these datasets for RLVR through:
1. **Task selection**: Filtering for tasks with unambiguous, verifiable answer formats
2. **Micro-mixing**: Carefully combining data from different reasoning categories to balance the training distribution

---

## Main Ideas & Key Contributions

### 1. SUPERNOVA Data Curation Framework

SUPERNOVA is a systematic pipeline that transforms instruction-tuning datasets into RLVR training data:

```
Instruction-Tuning Dataset
        ↓
   Task Filtering
   (verifiability, difficulty, answer format)
        ↓
   Task Selection
   (coverage across 8+ reasoning categories)
        ↓
   Micro-Mixing
   (balance by skill type)
        ↓
   RLVR Training Data
        ↓
   RLVR Training (GRPO / PPO)
        ↓
   General Reasoner LLM
```

### 2. Task Selection as a Critical Factor

Through ablation studies, the authors show that **which tasks are included** in training is more important than the raw quantity of data. Including tasks that require causal inference, temporal ordering, and analogical reasoning—even if individually small—dramatically improves generalization.

### 3. Micro-Mixing for Balanced Reasoning

"Micro-mixing" refers to carefully controlling the mixing ratio across reasoning categories at a fine granularity (e.g., 15% causal, 20% temporal, 25% logical, etc.) rather than training uniformly on all tasks. This prevents the model from over-specializing in the most common task types.

### 4. Reasoning Category Coverage

SUPERNOVA covers 8+ general reasoning categories:
- Causal reasoning ("If X happens, what follows?")
- Temporal reasoning ("What happened before/after?")
- Spatial reasoning ("What is to the left of?")
- Analogical reasoning ("A is to B as C is to ?")
- Commonsense reasoning (everyday world knowledge)
- Multi-step logical deduction
- Counterfactual reasoning ("What if X had not happened?")
- Numerical reasoning in context

---

## Methodology & Implementation

### Training Setup

- **Base models**: Qwen3.5 family and comparable LLMs
- **RL algorithm**: GRPO (Group Relative Policy Optimization) — a more stable variant of PPO that avoids value function training
- **Training data size**: Millions of instruction-tuning examples filtered to RLVR-compatible format
- **Compute**: Multi-GPU cluster training (details in paper)

### GRPO Overview

GRPO trains the policy by sampling a group of responses `{y_1, ..., y_G}` for each question, computing rewards `{R_1, ..., R_G}`, and optimizing with:

```
L_GRPO(θ) = -E[Σ_i (R_i - mean(R)) / std(R) · log π_θ(y_i | p)]
            + β · KL[π_θ || π_ref]
```

This normalizes rewards within each group, providing stable gradient signal without needing a separate value model.

### Evaluation Benchmarks

| Benchmark | Description | Type |
|-----------|-------------|------|
| **BBEH** | BIG-Bench Extra Hard | Hard general reasoning |
| **Zebralogic** | Constraint-satisfaction logic puzzles | Logical deduction |
| **MMLU-Pro** | Professional knowledge + reasoning | Mixed |
| **ARC-Challenge** | Science reasoning | Science |

### Key Results

- **BBEH**: Up to **52.8% relative improvement** over Qwen3.5 baseline
- **Zebralogic**: Strong improvements over chain-of-thought baselines
- **MMLU-Pro**: Consistent gains across model sizes
- **Pass@k**: SUPERNOVA-trained models show consistent improvement as k increases, confirming improved reasoning diversity

---

## Practical Applications & Real-World Use Cases

### 1. Scientific Discovery Assistants
A general reasoning LLM trained with SUPERNOVA could assist researchers by:
- Inferring causal relationships from experimental data
- Reasoning about temporal sequences in longitudinal studies
- Evaluating counterfactual hypotheses

### 2. Legal and Financial Analysis
Complex reasoning tasks like contract analysis, regulatory compliance checking, and financial risk assessment require multi-step causal and temporal reasoning—precisely the skills SUPERNOVA targets.

### 3. Healthcare Decision Support
Medical diagnosis requires temporal reasoning (symptom progression), causal inference (what caused this condition?), and counterfactual thinking (what if the patient had received treatment X instead?).

### 4. Education and Tutoring Systems
General reasoning is the foundation of critical thinking education. SUPERNOVA-trained models could serve as tutoring assistants that teach students to reason, not just compute.

---

## Insights & Implications

### What This Says About Reasoning in LLMs

SUPERNOVA's success provides empirical evidence that:
1. **RLVR generalizes beyond math/code** when appropriate training data exists
2. **Data curation matters more than scale** for reasoning—a carefully curated small dataset beats a massive but unbalanced one
3. **Task selection and mixing ratios are hyperparameters** that deserve as much attention as architecture and optimization

### The Domain-Dependence Problem

SUPERNOVA also implicitly highlights a fundamental limitation: current LLMs' "reasoning" is heavily shaped by the domains where RLVR data is abundant (math, code). General reasoning requires general RLVR data, which SUPERNOVA now provides a path toward.

### Limitations

- **Verification for open-ended tasks**: Some general reasoning tasks (e.g., open-ended causal explanations) are still difficult to verify automatically
- **Benchmark saturation**: As SUPERNOVA becomes adopted, benchmark contamination becomes a risk
- **Compositional reasoning**: Combining multiple reasoning types in a single problem remains challenging

---

## Code & Resources

- **Paper (arXiv)**: [https://arxiv.org/abs/2604.08477](https://arxiv.org/abs/2604.08477)
- **HuggingFace**: [https://huggingface.co/papers/2604.08477](https://huggingface.co/papers/2604.08477)

**Dependencies**:
- PyTorch, Transformers (HuggingFace)
- GRPO/trl library for RL training
- GPU cluster recommended (A100 or H100)

---

## Related Work & Context

### Prior Work
- **DeepSeek-R1**: Demonstrated RLVR for math reasoning at scale
- **QwQ-32B**: Strong RLVR-trained reasoning model
- **RLHF (InstructGPT)**: RLVR's predecessor using human preference rewards
- **Natural Instructions / Super-Natural Instructions**: The instruction-tuning datasets SUPERNOVA mines for RL data

### Related Concurrent Work
- **General365** (2604.11778): Benchmarks the same general reasoning gap
- **StepPO** (2604.18401): Addresses RLVR for agentic settings
- **When Can LLMs Learn to Reason with Weak Supervision?** (2604.18574): Theoretical analysis of conditions for RLVR success

### Future Directions
- Extending SUPERNOVA to video and multimodal reasoning tasks
- Automated reward model discovery for tasks that resist rule-based verification
- Combining SUPERNOVA-style data curation with process reward models
