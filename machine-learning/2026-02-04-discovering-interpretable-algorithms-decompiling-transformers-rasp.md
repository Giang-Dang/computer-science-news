# Discovering Interpretable Algorithms by Decompiling Transformers to RASP

**Authors:** Xinting Huang, Aleksandra Bakalova, Satwik Bhattamishra, William Merrill, Michael Hahn

**ArXiv ID:** 2602.08857

**Conference:** ICML 2026 (May 2026)

## Executive Summary

This paper presents a novel method for extracting interpretable algorithms from trained transformer models by decompiling them into RASP (Restricted Access Sequential Processing) programs. The work demonstrates that length-generalizing transformers can internally implement simple, interpretable algorithms that can be automatically extracted as symbolic programs. This breakthrough in transformer interpretability provides direct evidence that transformers achieving length generalization do so by learning genuine algorithms rather than pattern matching.

## Problem Statement

Understanding how transformers achieve length generalization—the ability to generalize to sequences longer than those seen during training—remains a fundamental open question in deep learning. While prior work showed that transformer computations can be simulated in RASP, there was no systematic method to extract such programs from trained models. This gap between theoretical understanding and practical extraction hindered progress in transformer interpretability and our ability to understand what transformers actually learn.

## Core Concepts & Theory

### RASP Programming Language

RASP is a functional programming language with restricted capabilities designed to capture the computational patterns of transformers:
- **Operations:** Sequence aggregation, element-wise operations, and comparison-based selection
- **Expressivity:** Can simulate any transformer computation through faithful re-parameterization
- **Interpretability:** Programs written in RASP are human-readable and can be analyzed

### Methodology

The extraction process follows three key steps:

1. **Faithful Re-parameterization:** Re-parameterize the trained transformer to have the mathematical form of a RASP program, ensuring the transformer's behavior remains unchanged
2. **Causal Intervention:** Apply targeted causal interventions to identify which components are necessary for the transformer's behavior
3. **Program Extraction:** Synthesize a minimal sufficient sub-program that implements the same computation

### Key Insight

Length generalization in transformers correlates strongly with the existence of clean RASP decompositions. Transformers that can be decomposed into simple RASP programs generalize to longer sequences, while those without clean decompositions fail on longer sequences, suggesting that length generalization genuinely requires learning algorithms.

## Main Ideas & Contributions

### Novel Contributions

1. **General Extraction Method:** First systematic approach to extract interpretable algorithms from trained transformers
2. **Causal Intervention Framework:** Technique to identify minimal sufficient sub-programs through targeted interventions
3. **Length Generalization Connection:** Empirical evidence linking algorithm learnability to generalization behavior
4. **Automatic Symbolic Program Recovery:** Demonstrates automatic extraction of interpretable algorithms from transformer weights

### Technical Innovations

- **Re-parameterization Scheme:** Mathematically faithful transformation of transformer architecture to RASP form
- **Intervention Design:** Causal methodology to prune unnecessary components while preserving functionality
- **Program Simplification:** Techniques to derive minimal, interpretable sub-programs

## Methodology & Implementation

### Experimental Setup

- **Tasks:** Algorithmic tasks (sorting, addition, parity) and formal language tasks (balanced parentheses, Dyck languages)
- **Model Scale:** Small transformers (2-4 layers, 64-128 dimensions) trained to high accuracy on synthetic data
- **Comparison Baselines:** Raw transformer weights vs. extracted RASP programs

### Evaluation Metrics

- **Extraction Success Rate:** Percentage of models from which interpretable programs could be extracted
- **Program Complexity:** Number of operations in extracted programs
- **Length Generalization:** Accuracy on sequences up to 2-3x training length
- **Semantic Equivalence:** Verification that extracted programs match transformer behavior on test data

### Results

[Exact figures unavailable — see full paper]

- Successfully extracted simple, interpretable RASP programs from transformers trained on algorithmic and formal language tasks
- Extracted programs often have fewer than 10 operations despite transformer complexity
- Models with extractable clean programs achieved significantly better length generalization
- Qualitative examples show programs recovering classic algorithms (e.g., bubble sort, addition with carry)

## Practical Applications & Use Cases

### Research Applications

1. **Mechanistic Interpretability:** Understanding transformer internals through symbolic program analysis
2. **Model Auditing:** Verifying that transformers learn expected algorithms, not shortcuts
3. **Transfer Learning:** Using extracted algorithms to initialize models or transfer to new domains
4. **Safety and Alignment:** Ensuring critical models implement interpretable algorithms

### Domain-Specific Applications

1. **Formal Language Processing:** Ensuring models learn correct parsing algorithms
2. **Symbolic Reasoning:** Verifying transformers implement correct mathematical operations
3. **Algorithm Learning:** Training models on algorithmic tasks with verifiable solutions
4. **Controllable Generation:** Inserting specific algorithms into transformer programs

### Implementation Challenges

- Scalability to larger models (extraction becomes computationally expensive)
- Handling continuous vs. discrete program semantics
- Extracting programs from models trained on non-algorithmic tasks
- Balancing program interpretability with task performance

## Insights & Implications

### Broader Field Impact

1. **Mechanistic Understanding:** Provides concrete evidence that transformers can implement interpretable algorithms, advancing mechanistic interpretability research
2. **Length Generalization Theory:** Links algorithm structure to generalization, providing theoretical foundation for understanding when models generalize
3. **Symbolic AI Connection:** Bridges neural and symbolic AI, showing transformers can recover classical algorithms
4. **Interpretability as Default:** Suggests interpretable algorithms may be preferable to opaque patterns for robust learning

### State-of-the-Art Advancement

- First practical method for extracting interpretable symbolic programs from transformers
- Advances RASP-based mechanistic interpretability from theory to practice
- Provides new evaluation paradigm: algorithm learning rather than just task accuracy
- Opens new directions for interpretable model design and training

### Limitations and Open Questions

1. **Scalability:** Current method works on small models; scaling to large transformers remains open
2. **Domain Generalization:** Extraction shown primarily on algorithmic/formal tasks; effectiveness on natural language unclear
3. **Program Minimality:** Questions about whether extracted programs are truly minimal
4. **Continuous Tasks:** Handling non-discrete algorithmic tasks requires further research
5. **Partial Interpretability:** Some components may remain uninterpretable even after extraction

## Code & Resources

### Official Resources

- **ArXiv Paper:** https://arxiv.org/abs/2602.08857
- **PDF:** https://arxiv.org/pdf/2602.08857
- **ResearchGate:** https://www.researchgate.net/publication/400622257_Discovering_Interpretable_Algorithms_by_Decompiling_Transformers_to_RASP

### Related Work

- **RASP Language:** https://github.com/vicgalle/RASP-PyTorch
- **Mechanistic Interpretability:** Follow-up work on circuit analysis and attention head interpretation

### Computing Requirements

- **GPU:** Moderate requirements for small model experiments (RTX 3090 or equivalent)
- **Training Time:** Hours to days for algorithmic task training
- **Extraction Time:** Minutes to hours depending on model size and program complexity
- **Software:** PyTorch, custom RASP compiler/interpreter

## Related Work & Context

### Foundational Work

1. **RASP Language Definition:** Prior work showing transformers can simulate RASP programs
2. **Mechanistic Interpretability:** Circuit analysis (Anthropic), attention head interpretation
3. **Formal Language Learning:** Symbolic approaches to learning grammars and algorithms
4. **Program Synthesis:** Neural program synthesis literature

### Related Recent Papers

1. **Algorithmic Reasoning in Transformers:** Work on how transformers solve algorithmic tasks
2. **Attention Interpretation:** Studies showing how attention implements algorithms
3. **Formal Language Acquisition:** Neural models learning context-free grammars
4. **Program Extraction:** General techniques for extracting interpretable models from neural networks

### Future Research Directions

1. **Scaling to Large Models:** Methods for extracting programs from billion-parameter transformers
2. **Multi-Task Programs:** Programs capturing multiple tasks simultaneously
3. **Natural Language Algorithms:** Extracting interpretable procedures from language models
4. **Hybrid Interpretability:** Combining symbolic extraction with other interpretability methods
5. **Training-Time Interpretability:** Guiding training toward interpretable algorithms
6. **Continuous Program Semantics:** Extension to real-valued algorithms and continuous reasoning
