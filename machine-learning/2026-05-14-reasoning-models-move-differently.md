# Reasoning Models Don't Just Think Longer, They Move Differently

**Authors:** [Paper 2605.15454]  
**ArXiv ID:** 2605.15454  
**Submitted:** May 14, 2026  
**Field:** Machine Learning, Mechanistic Interpretability  

---

## Executive Summary

This paper investigates whether reasoning-trained language models that allocate more tokens to harder problems are simply computing for longer steps or following fundamentally different internal trajectories. Through analysis of hidden-state trajectories in chain-of-thought reasoning, the authors demonstrate that trajectory geometry is strongly shaped by generation length, but after correcting for length effects, difficulty remains systematically coupled to corrected trajectory geometry. This work provides crucial insights into how reasoning models process information differently, advancing our understanding of mechanistic interpretability in large language models.

---

## Problem Statement

### Background
Modern reasoning-trained language models (such as o1, Deepseek-R1) spend more computation on harder problems during chain-of-thought reasoning. However, a fundamental question remains: are these models simply repeating similar computational steps for longer, or are they fundamentally altering their internal processing patterns?

### Prior Limitations
Previous work on chain-of-thought reasoning has primarily focused on:
- Output token count as a proxy for reasoning difficulty
- Observable behavioral patterns in generated text
- Empirical performance metrics on benchmarks

Few studies have examined the **internal geometric properties** of how hidden states evolve during reasoning, making it unclear whether difficulty-dependent computation represents deeper qualitative changes in model behavior.

### Research Gap
Understanding the internal mechanisms of reasoning models requires analyzing:
- How hidden-state trajectories evolve during different difficulty levels
- Whether trajectory geometry is merely a function of sequence length
- What role "corrected" geometric properties play in capturing true reasoning differences

---

## Core Concepts & Theory

### Hidden-State Trajectory Analysis

The core methodology involves analyzing the **geometry of hidden-state sequences** as models generate reasoning tokens:

```
Hidden State Trajectory = [h_1, h_2, ..., h_n]
  where h_i = hidden state at token i
  
Trajectory Geometry Properties:
  - Path length (cumulative distance between consecutive states)
  - Local curvature (deviation from straight lines)
  - Direction changes (angle between successive steps)
```

### Length Normalization & Correction

A critical insight is that longer sequences mechanically alter path statistics. The authors propose **length-corrected trajectory metrics**:

```
Corrected Metric = Original Metric / f(sequence_length)
  where f accounts for the expected growth of statistics with length
```

This normalization is essential because:
- Raw trajectory distance scales with sequence length
- Simple comparisons between short and long sequences are confounded
- True difficulty effects only emerge after accounting for length

### Domains Studied

The paper analyzes reasoning across three diverse domains:

1. **Competitive Programming** (code generation, algorithmic thinking)
2. **Mathematical Reasoning** (step-by-step proof construction)
3. **Boolean Satisfiability (SAT)** (constraint satisfaction problems)

Each domain tests whether reasoning differences generalize or are domain-specific.

### Comparison with Instruction-Tuned Models

The paper compares reasoning-trained models against instruction-tuned baselines trained on similar data but without explicit reasoning optimization, providing a controlled comparison for isolating reasoning-specific effects.

---

## Main Ideas & Contributions

### 1. Trajectory Geometry Reflects Reasoning Type
After correcting for length effects, **corrected trajectory geometry systematically differs** between easy and hard problems across all tested domains. This demonstrates that harder problems don't just require longer computation—they involve fundamentally different internal processing.

### 2. Domain-Specific Patterns Emerge
The most striking reasoning-specific differences appear in the **code domain**, where:
- Harder problems show **more direct corrected trajectories** (less wandering)
- Less heterogeneous local curvature (more consistent trajectory shape)
- These patterns are distinctly stronger in reasoning-trained than instruction-tuned models

This suggests that reasoning training shapes models to adopt qualitatively different computational strategies for complex code problems.

### 3. Trajectory Properties as Interpretability Tool
Hidden-state trajectory analysis provides a new lens for understanding:
- How models internally represent problem difficulty
- Whether models develop specialized "reasoning modes" distinct from standard generation
- How reasoning scales with problem complexity

---

## Methodology & Implementation

### Experimental Setup

**Model Selection:**
- Reasoning-trained models (spending variable tokens per problem)
- Instruction-tuned baseline models (same training data, no reasoning optimization)
- Multiple model sizes to test scalability

**Data & Benchmarks:**
- Competitive programming problems (LeetCode, Codeforces)
- Mathematical reasoning (MATH dataset, Olympiad problems)
- Boolean satisfiability (SAT competition instances)

**Hidden State Extraction:**
- Collect hidden states from all transformer layers
- Store trajectories for successful and failed reasoning attempts
- Normalize by sequence length and domain

### Evaluation Metrics

1. **Path Length:** Cumulative L2 distance between consecutive hidden states
   ```
   Path_Length = Σ ||h_{i+1} - h_i||_2
   ```

2. **Local Curvature:** Deviation from straight-line paths
   ```
   Curvature = angle(h_{i-1}-h_i, h_i-h_{i+1})
   ```

3. **Trajectory Heterogeneity:** Variance in local geometric properties

### Results Summary

| Metric | Easy Problems | Hard Problems | Significance |
|--------|---------------|---------------|-------------|
| Raw Path Length | Variable by domain | Longer | Confounded with length |
| **Corrected Path Length** | Baseline | More direct | Reasoning-specific |
| Local Curvature | Higher heterogeneity | Lower heterogeneity | **Code domain strongest** |

**Key Finding:** After length correction, code domain shows the clearest separation, with harder problems exhibiting more direct, consistent trajectories in reasoning-trained models compared to baselines.

---

## Practical Applications & Use Cases

### 1. Reasoning Model Diagnostics
Trajectory analysis can diagnose whether a model is:
- Genuinely engaging in difficult reasoning
- Simply generating longer text without deeper processing
- Failing due to trajectory collapse (internal state collapse)

### 2. Model Interpretability & Safety
Understanding reasoning trajectories helps detect:
- Whether models are following intended reasoning patterns
- Potential shortcuts or spurious correlations in reasoning
- Training inefficiencies (models that don't optimize trajectories)

### 3. Reasoning Model Development
Insights into trajectory geometry could inform:
- Better training objectives that shape internal reasoning trajectories
- Architectures that support richer trajectory space
- Early stopping criteria based on trajectory health

### 4. Domain-Specific Model Specialization
The finding that code domains show stronger patterns suggests:
- Different tasks benefit from different reasoning architectures
- Task-specific trajectory priors could improve model design

---

## Insights & Implications

### Broader Field Impact

1. **Mechanistic Understanding of Reasoning:** This work demonstrates that reasoning-trained models develop genuinely different internal computation patterns, not just longer repetitions. This is crucial for understanding how models solve hard problems.

2. **Trajectory Geometry as a First-Class Concept:** The paper elevates hidden-state trajectory analysis from observation to a rigorous analytical tool, opening new directions in mechanistic interpretability.

3. **Domain-Dependent Effects:** The stronger patterns in code suggest that reasoning capabilities may be domain-specific, with implications for generalization and transfer learning.

### Limitations & Open Questions

1. **Causal Understanding:** While the paper shows correlations between trajectory geometry and problem difficulty, it doesn't establish causal mechanisms. What specific computations drive these trajectory differences?

2. **Generalization Across Models:** Do these patterns hold for other reasoning-trained models and architectures?

3. **Trajectory-to-Performance Mapping:** How do trajectory properties relate to actual problem-solving accuracy? Can we predict success from trajectory shape alone?

4. **Scaling Laws:** How do trajectory properties evolve with model scale, training data, and reasoning training intensity?

---

## Code & Resources

### Official Repositories
- **ArXiv Paper:** https://arxiv.org/abs/2605.15454
- **HTML Version:** https://arxiv.org/html/2605.15454

### Dependencies & Compute Requirements
- **Requirements:** PyTorch, transformers library, numpy, scikit-learn
- **Compute:** GPU access recommended for hidden state extraction from large models
- **Data:** Competitive programming datasets (LeetCode, Codeforces), MATH dataset

### Quick Start Guide

```bash
# 1. Install dependencies
pip install torch transformers numpy scikit-learn matplotlib

# 2. Load a reasoning-trained model
from transformers import AutoTokenizer, AutoModelForCausalLM
model_name = "openai/o1-base"  # or similar reasoning model
model = AutoModelForCausalLM.from_pretrained(model_name, output_hidden_states=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 3. Extract hidden states during generation
input_text = "Solve: 2x + 3 = 7"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, output_hidden_states=True, return_dict_in_generate=True)
hidden_states = outputs.hidden_states  # List of layer outputs for each token

# 4. Compute trajectory metrics
import numpy as np
trajectory = np.array([h[-1].mean(dim=0).detach().cpu() for h in hidden_states])
path_length = np.sum(np.linalg.norm(np.diff(trajectory, axis=0), axis=1))
```

---

## Related Work & Context

### Prior Work on Chain-of-Thought Reasoning
- Wei et al. (2022): "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Nye et al. (2021): Studying emergent reasoning capabilities in scaling
- Openai o1 and Deepseek-R1 papers: Industrial reasoning model design

### Mechanistic Interpretability Foundation
- Anthropic's Mechanistic Interpretability research program
- Nanda et al.: Introduction to mechanistic interpretability concepts
- Sap et al.: Social reasoning in neural networks

### Related Recent Work
- **Stop When Reasoning Converges** (2605.17672): Complementary work on early stopping for reasoning models
- **Does Your Reasoning Model Implicitly Know When to Stop Thinking?** (2602.08354): Similar question about when reasoning should terminate
- **Don't Overthink it** (2505.17813): Investigation of optimal thinking chain lengths

### Future Research Directions

1. **Causal Intervention Studies:** Use ablation/intervention techniques to causally identify which trajectory properties drive reasoning success.

2. **Cross-Model Generalization:** Extend analysis to larger, more diverse set of reasoning-trained models to identify universal patterns.

3. **Architecture Implications:** Use trajectory insights to design architectures optimized for specific reasoning tasks.

4. **Real-Time Monitoring:** Develop methods to monitor trajectory health during inference as a proxy for reasoning quality.

5. **Trajectory-Guided Training:** Incorporate trajectory geometry directly into training objectives to shape reasoning behavior.

---

## Key Takeaways

- Reasoning-trained models don't just compute longer—they follow fundamentally different internal trajectories
- After correcting for length effects, trajectory geometry systematically varies with problem difficulty
- The code domain shows the strongest reasoning-specific trajectory patterns
- Trajectory analysis provides a promising new tool for mechanistic interpretability research
- These insights could inform better reasoning model design and interpretability tools
