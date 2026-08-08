# Why Large Language Models Fail at Tabular Prediction

**Authors:** Marta Garnelo, Wojciech M. Czarnecki  
**ArXiv ID:** 2608.02412  
**Submitted:** August 3, 2026  
**Category:** Machine Learning (cs.LG)

## Executive Summary

This paper investigates a critical paradox in modern AI: despite their remarkable success across diverse tasks, large language models (LLMs) conspicuously fail at predictive analytics over tabular data. Rather than accepting this empirically observed failure, the authors conduct a systematic investigation to identify the root cause. Through controlled experiments testing five competing hypotheses, they demonstrate that **dimensionality is the fundamental limiting factor**—LLMs are the only method among nine tested whose accuracy decreases as input dimensionality increases. This finding has profound implications for the field of tabular machine learning and validates the emerging focus on specialized tabular foundation models rather than generic LLM adaptation.

## Problem Statement

Large language models have revolutionized AI by achieving state-of-the-art performance across a remarkable range of tasks: natural language understanding, code generation, reasoning, and more. Yet they have notably failed at a seemingly simple task: predictive analytics over tabular data. This gap is puzzling because:

1. Tabular data is ubiquitous in real-world applications (finance, healthcare, e-commerce)
2. Classical machine learning methods handle tabular data well
3. LLMs can encode information in various modalities, yet struggle with structured numerical data

The field has responded by developing tabular foundation models specifically designed for this task, but the fundamental question remains unanswered: **Why do LLMs fail?** Understanding this failure mode is critical for knowing whether LLM adaptation efforts are addressing the root cause or merely papering over a deeper architectural incompatibility.

## Core Concepts & Theory

### Pure Inference Regime

The authors establish a controlled experimental framework that isolates LLM core capabilities:
- **Single generation pass:** No iterative refinement or multi-turn interaction
- **Full in-context data:** Training and test data included in the prompt
- **No external tools:** No scaffolding, Python execution, or agent frameworks
- **No fine-tuning:** Pure pre-trained model inference

This regime is more controlled than typical LLM applications but reflects the capabilities mentioned in model documentation.

### Five Competing Hypotheses

The paper systematically tests five alternative explanations for LLM failure:

1. **Hypothesis (a) - Data Complexity:** LLMs cannot handle noisy or non-linearly-separable data
2. **Hypothesis (b) - Format Obscuration:** CSV linearization obscures column structure
3. **Hypothesis (c) - Tokenization:** Numeric value tokenization causes information loss
4. **Hypothesis (d) - Query Size:** Number of test points per query limits processing
5. **Hypothesis (e) - Dimensionality:** Higher input dimensionality fundamentally challenges LLMs

### Mathematical Framework

**Dimensionality Analysis:**
- Generate random linear projections of 31 benchmark datasets
- Systematically vary dimensionality while preserving task structure
- Compare LLM accuracy against classical baselines across dimensionality ranges
- Measure behavioral similarity between LLM and distance-based methods

**Behavioral Mapping:**
- Compare LLM predictions to 252 configured classical models
- Measure grid agreement rates in 2D space
- Quantify deviation patterns as dimensionality increases

## Main Ideas & Contributions

### Key Discovery: Dimensionality is Decisive

Through controlled hypothesis testing, the authors eliminated hypotheses (a)-(d) through specific experiments:

- **(a) Non-linear data:* LLMs fail on synthetic linear data, falsifying data complexity as the sole cause
- **(b) CSV format:* Reformatting data as JSON or structured text shows no improvement
- **(c) Tokenization:* Direct numeric input representation shows similar failure patterns
- **(d) Query size:* Varying test set size shows failure persists regardless

**The critical finding:** When random linear projections reduce dimensionality across 31 benchmarks, the LLM is the **only method among nine** whose accuracy decreases as dimensionality increases. Every classical baseline (decision trees, SVM, random forests, etc.) remains flat or improves with higher dimensionality.

### Behavioral Insight: Distance-Based Decision Making

In 2D space, LLM predictions align with distance-based methods (kNN, local methods) at **up to 91.6% grid agreement**. This suggests that LLMs implicitly learn distance-based reasoning patterns rather than leveraging structural properties of high-dimensional data that classical methods exploit.

### Technological Contribution: Experimental Framework

The paper establishes a rigorous experimental framework for isolating and testing LLM capabilities on tabular data:
- Controlled hypothesis testing methodology
- Pure inference evaluation regime
- Random linear projection technique for dimensionality control
- Behavioral comparison protocol

## Methodology & Implementation

### Experimental Setup

**Datasets:** 31 benchmark datasets spanning diverse domains and dimensionalities

**Comparison Methods:** 9 different approaches tested:
- LLM (frontier model)
- Multiple classical baselines (decision trees, SVM, Random Forest, etc.)
- Ensemble methods
- Distance-based methods

**Classical Model Configurations:** 252 configured models tested for behavioral comparison

### Evaluation Protocol

1. **Baseline experiments:** Test each hypothesis with specific experiments
2. **Dimensionality sweep:** Apply random linear projections to systematically vary input dimensionality
3. **Accuracy measurement:** Record model accuracy at each dimensionality level
4. **Behavioral analysis:** Compare LLM predictions to classical methods in 2D embedding space
5. **Grid agreement:** Quantify prediction alignment on regular 2D grids

### Results and Metrics

**Hypothesis Falsification Results:**
- Hypotheses (a)-(d): **Falsified** through controlled experiments
- Hypothesis (e): **Confirmed** as the decisive factor

**Dimensionality Effects:**
- **LLM behavior:** Accuracy monotonically decreases with increasing dimensionality
- **Classical methods:** Accuracy remains stable or improves with dimensionality
- **Performance gap:** Widens significantly as dimensionality increases beyond ~10 dimensions

**2D Behavioral Analysis:**
- LLM exhibits **91.6% grid agreement** with distance-based methods in 2D space
- Suggests LLMs operate primarily through local, distance-based decision boundaries
- Classical methods maintain structural sensitivity across dimensionalities that LLMs lose

### Key Metrics

| Metric | Value/Observation |
|--------|------------------|
| Datasets Tested | 31 benchmarks |
| Comparison Methods | 9 different approaches |
| Max 2D Grid Agreement | 91.6% (distance-based methods) |
| Dimensionality at Failure | ~10-15 dimensions |
| LLM Uniqueness | Only method with degrading accuracy vs. dimension |

## Practical Applications & Use Cases

### Where LLMs Succeed
- **Low-dimensional prediction:** Adequate performance on ≤2 dimensional problems
- **Conceptual reasoning:** Tasks combining text and simple numerical relationships
- **Structured formats:** Problems with strong syntactic structure

### Where LLMs Fail
- **High-dimensional tabular prediction:** Standard predictive analytics tasks
- **Numerical optimization:** Problems requiring sensitivity to feature space geometry
- **Statistical learning:** Tasks exploiting high-dimensional statistical regularities

### Implications for Practitioners

1. **LLM Tabular Adaptation:** Generic fine-tuning on tabular tasks unlikely to overcome dimensional limitations
2. **Specialized Models Justified:** Developing dedicated tabular foundation models is the right approach
3. **No Prompt Engineering Solution:** CSV reformatting or prompt engineering cannot address this fundamental limitation
4. **Hybrid Systems:** Combining LLMs with classical methods for mixed tasks remains valuable

## Insights & Implications

### For the Field

1. **Fundamental Architectural Difference:** LLMs and classical ML operate on fundamentally different principles when handling high-dimensional data
2. **Nature of LLM Reasoning:** LLMs appear to rely on local, distance-based decision boundaries rather than leveraging high-dimensional geometric structure
3. **Tokenization ≠ Limitation:** The failure is not due to tokenization or information encoding, suggesting architectural rather than representational issues
4. **Validation of Specialization:** Justifies the growing focus on specialized foundation models for domain-specific tasks

### Research Directions

1. **Architectural Modification:** Can LLM architectures be redesigned to handle high-dimensional continuous data?
2. **Hybrid Approaches:** What combinations of LLMs and classical methods optimize performance?
3. **Dimensionality Reduction:** Can effective preprocessing transform tabular data into regions where LLMs excel?
4. **Alternative Tokenization:** Do numeric-specific tokenization schemes improve performance?
5. **Mechanistic Understanding:** What components of LLM architectures prevent high-dimensional competence?

### Limitations and Open Questions

1. **Single Model Study:** Analysis focuses on a frontier LLM; effects may vary across model families
2. **Scope Limitations:** Study uses pure inference; fine-tuning could potentially overcome some limitations
3. **Task Variety:** Evaluation primarily on numerical prediction; non-numeric tabular tasks not addressed
4. **Causality vs. Correlation:** While dimensionality is the decisive factor, the precise causal mechanism remains unclear

## Code & Resources

**Official Resources:** 
- arXiv Paper: https://arxiv.org/abs/2608.02412
- HTML Version: https://arxiv.org/html/2608.02412

**Code Availability:** [Exact figures unavailable — see full paper for supplementary materials and reproducibility code]

**Reproducibility:** The paper provides sufficient experimental detail for reproduction; check the arXiv page for supplementary materials.

## Related Work & Context

### Prior Work on Tabular Foundation Models

This paper contextualizes emerging research on tabular-specific foundation models:
- **TabR:** Specialized tabular representation learning
- **GBDT alternatives:** Gradient boosting vs. deep learning comparisons
- **Feature engineering:** Prior work on numerical representation for neural networks

### Broader Context

The work fits within the larger narrative of AI specialization:
- **Domain-specific models:** Just as vision transformers revolutionized CV, specialized models may be necessary for tabular data
- **Not all tasks are LLM tasks:** Challenges the assumption that LLMs are universally applicable

### Future Research Directions

1. **Multimodal tabular data:** How do LLMs handle mixed numeric-text tables?
2. **Very large tables:** Does performance improve with billions of rows for in-context learning?
3. **Reasoning over tables:** Higher-level reasoning tasks combining multiple tables
4. **Cross-domain transfer:** Transfer learning from one tabular domain to another using foundation models

---

**Research Significance:** This paper makes a critical contribution by moving beyond "LLMs fail at tabular prediction" as an empirical observation to a principled understanding of why. By systematically eliminating alternative hypotheses and identifying dimensionality as the decisive factor, it provides both theoretical insight and practical guidance for the field's direction in developing specialized tabular machine learning approaches.
