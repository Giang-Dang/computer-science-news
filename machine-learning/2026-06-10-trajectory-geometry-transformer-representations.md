# Trajectory Geometry of Transformer Representations Across Layers

**Authors:** Vishal Pandey, Gopal Singh, Yacine Mahdid

**ArXiv ID:** [2606.09287](https://arxiv.org/abs/2606.09287)

**Date:** June 2026

---

## Executive Summary

This paper provides a novel geometric perspective on how Transformers process information through their depth. By treating the forward pass as a discrete population trajectory through high-dimensional representation space, the authors employ tools from computational neuroscience to characterize transformer behavior using five geometric metrics. The research reveals universal organizing principles across model families, including semantic convergence in middle layers, curvature encoding computational complexity, and a consistent three-phase structure in representational evolution.

## Problem Statement

While mechanistic interpretability has advanced our understanding of Transformers, critical gaps remain in understanding how information flows through layers:

- **Layer-wise Opacity:** Limited understanding of what individual layers compute beyond low-level features
- **Feature Emergence:** When and how do high-level semantic representations emerge?
- **Computational Flow:** How do token representations evolve as they traverse the network?
- **Generalization Questions:** Are there universal patterns across different model architectures and training regimes?
- **Interpretability Bottleneck:** Existing probing methods require pre-specifying what to look for, potentially missing emergent phenomena

The paper addresses these through a novel geometric lens that doesn't require prior assumptions about what features should exist.

## Core Concepts & Theory

### Representation Manifold and Trajectory Framework

**Core Insight:** Each forward pass can be viewed as a trajectory through high-dimensional representation space:

```
Input Token → Layer 0 → Layer 1 → ... → Layer N → Output
    ↓           ↓         ↓               ↓        ↓
   Token    Embedding  Processing    Late-layer  Logits
Position    Space      Manifold      Output Space
```

Rather than analyzing individual points in representation space, the paper analyzes the **path** each token takes through layers.

### Five Geometric Metrics

**1. Trajectory Length (∫||dx/dt||dt)**
- Measures total distance traveled in representation space
- High length indicates substantial transformation across layers
- Indicates amount of computation applied to representation

**2. Curvature (κ = ||dT/ds||)**
- Measures how sharply trajectory direction changes
- Higher curvature suggests complex, non-linear transformations
- Correlates with computational complexity of tasks

**3. Semantic Convergence Index (CI)**
- Measures how similar trajectories for semantically related inputs become
- Computed using statistical testing of representation similarity
- Values range 0-1; high CI = semantic convergence

**4. Layerwise Cosine Similarity**
- Measures layer-to-layer change in representation
- Identifies phase transitions in processing
- Reveals consistent structure across architectures

**5. Representational Stability**
- Measures variance in trajectory positions
- High stability = consistent processing
- Low stability = variable computational paths

### Mathematical Formulation

For token trajectory **x(l)** at layer **l**:

**Trajectory Length:** 
```
L = Σ_l ||x(l+1) - x(l)||_2
```

**Curvature (discrete approximation):**
```
κ(l) = angle(x(l+1) - x(l), x(l+2) - x(l+1))
```

**Semantic Convergence:**
```
CI(l) = proportion of semantically-similar pairs with cos_sim > threshold
```

## Main Ideas & Contributions

### Universal Three-Phase Structure

The paper's most striking finding: all examined models exhibit a consistent three-phase organization:

**Phase 1: Encoding (Layers 0-10)**
- Early layers extract surface-level features
- Token representations diverge based on content
- Establish foundation for deeper processing
- Cosine similarity between layers ~ 0.7-0.8

**Phase 2: Elaboration (Layers 10-20)**
- Semantic processing and relationship modeling
- Representations converge for semantically related inputs
- Maximum semantic convergence index (CI = 0.41-0.58)
- Complex transformations indicated by high curvature

**Phase 3: Output Preparation (Layers 20-32)**
- Task-specific computation
- Convergence toward output space
- Reduced cosine similarity as head approaches final layer
- Stabilization toward decision boundaries

### Semantic Convergence and Attractor Dynamics

**Key Finding:** Semantically related prompts show strong statistical convergence in middle-to-late layers (p<0.001, Mann-Whitney U test).

**Interpretation:** Middle layers act as semantic attractors—multiple related input variations are drawn toward shared representations, consistent with dynamical systems theory.

**Example Results:**
- Different phrasings of same question converge with CI = 0.41-0.58
- Unrelated prompts remain dispersed (CI = 0.05-0.15)
- Convergence strongest at layers 16-20 (mid-network)

### Curvature Encodes Task Complexity

**Finding:** Reasoning tasks produce significantly higher trajectory curvature than lexical tasks:
- Reasoning: 0.71-0.83 radians average curvature
- Lexical variation: 0.27-0.31 radians average curvature
- ~3x difference between task types

**Interpretation:** Curvature reflects computational complexity—reasoning requires more non-linear transformations through the network.

### Ambiguous Token Bifurcation

**Observation:** Ambiguous tokens exhibit trajectory bifurcation in late layers:
- Initial representations identical to unambiguous controls
- Late-layer representations diverge (up to 5.6x separation)
- Unambiguous tokens show stable trajectory

**Implication:** Models maintain ambiguity through network depth, only resolving context-dependent interpretations in final layers—evidence of sophisticated contextual processing.

## Methodology & Implementation

### Experimental Design

**Model Families Tested:**
- GPT-2 (small, 124M parameters)
- TinyLlama (1.1B parameters)
- Qwen2.5 (various sizes)

**Prompt Families (5 types):**

1. **Semantic Equivalents:**
   - "What is 2+2?" vs. "Compute 2+2" vs. "Calculate 2 plus 2"
   - Expected: High convergence

2. **Lexical Variations:**
   - "dog", "puppy", "canine", "hound"
   - Expected: Moderate divergence

3. **Reasoning Tasks:**
   - Multi-step mathematical problems
   - Logical deduction tasks
   - Expected: High curvature

4. **Ambiguous Tokens:**
   - "bank" (financial vs. riverside)
   - "present" (gift vs. to give)
   - Expected: Late-layer bifurcation

5. **Negations:**
   - "John is tall" vs. "John is not tall"
   - Expected: Phase-dependent divergence

### Computational Considerations

**Data Collection:**
- Extract hidden states at all layers
- Compute pairwise distances for all tokens
- Calculate geometric metrics per prompt per layer

**Statistical Analysis:**
- Mann-Whitney U tests for convergence significance
- Effect sizes reported with 95% confidence intervals
- Multiple comparisons correction applied

**[Exact figures unavailable — see full paper]**

The paper presents comprehensive quantitative results comparing geometric properties across all model families and prompt types, with detailed statistical validation.

## Practical Applications & Use Cases

### Interpretability and Debugging

- **Layer Pruning:** Identify redundant layers based on low curvature
- **Early Exit:** Determine optimal early stopping points for inference
- **Feature Analysis:** Understand when specific capabilities emerge
- **Failure Diagnosis:** Identify at which layers models fail on specific tasks

### Model Design and Architecture

- **Depth Optimization:** Determine appropriate model depth based on task complexity
- **Layer Specialization:** Design layers for specific phases of computation
- **Skip Connection Design:** Understand where shortcuts would benefit/harm processing
- **Attention Head Analysis:** Correlate geometric properties with head function

### Training and Optimization

- **Learning Dynamics:** Monitor trajectory geometry during training
- **Convergence Analysis:** Use geometry to diagnose training issues
- **Curriculum Learning:** Design training progression based on phase structure
- **Regularization:** Geometry-informed regularization terms

### Real-World Applications

1. **Model Compression:** Identify layers for knowledge distillation
2. **Domain Adaptation:** Monitor geometric shift when fine-tuning
3. **Uncertainty Quantification:** Use trajectory stability for confidence estimation
4. **Backdoor Detection:** Identify suspicious geometric patterns from poisoned data

## Insights & Implications

### Broader Field Impact

**Unified Understanding:**
- Geometric framework provides universal lens across different architectures
- Suggests fundamental principles of transformer computation
- Connects deep learning to established dynamical systems theory

**Architecture Design:**
- Three-phase structure suggests optimal architectural innovations
- Guides development of more efficient models
- Informs hybrid architectures combining different processing paradigms

### Theoretical Significance

**Dynamical Systems Perspective:**
- Transformers implement attractor dynamics in representation space
- Middle layers act as semantic attractors
- Late layers prepare for output generation

**Information Theory:**
- Trajectory length and curvature relate to information processing
- Convergence reflects information compression
- Relates to information bottleneck theory

**Computational Complexity:**
- Curvature provides empirical measure of computational complexity
- Task complexity reflected in geometric properties
- Potential for predicting computational requirements

### Limitations and Open Questions

**Current Limitations:**
- Analysis on relatively small models (up to 7-8B parameters)
- Limited to English language models
- Specific to autoregressive transformers
- Fixed-length analysis at single timestep per prompt

**Unresolved Questions:**
- How do these patterns scale to much larger models (70B+)?
- How do geometric properties evolve during training?
- Do vision transformers exhibit similar structure?
- What geometric principles govern multimodal models?
- How do recurrent or mixture-of-experts architectures behave?

## Code & Resources

### Official Resources

- **Paper:** [https://arxiv.org/abs/2606.09287](https://arxiv.org/abs/2606.09287)
- **PDF:** [https://arxiv.org/pdf/2606.09287](https://arxiv.org/pdf/2606.09287)
- **Authors:** Vishal Pandey, Gopal Singh, Yacine Mahdid
- **Authors' Institutions:** [Specific institutions not detailed in search results]

### Implementation Frameworks

**Analysis Tools:**
- PyTorch for hidden state extraction
- Scikit-learn for geometric computations
- SciPy for statistical analysis
- Matplotlib for trajectory visualization

**Key Libraries:**
```python
# Hidden state extraction
from transformers import AutoModel

# Geometric computation
from scipy.spatial.distance import cosine
from scipy import stats

# Visualization
import matplotlib.pyplot as plt
import numpy as np
```

### Compute Requirements

- **Analysis:** Single GPU (8GB+) sufficient for small models
- **Trajectory Computation:** ~2-5 minutes per model per prompt set
- **Statistics:** CPU-bound, minutes to hours depending on scale
- **Large Models:** Distributed computation recommended

### Quick-Start Guide

1. Extract hidden states from model forward pass
2. Compute pairwise distances between representations
3. Calculate geometric metrics per layer
4. Apply statistical tests for convergence/divergence
5. Visualize trajectories in reduced dimensionality (PCA/UMAP)

## Related Work & Context

### Foundational Work

- **"Neural Network Dynamics"** (Saxe et al., 2019): Representation learning through training
- **"Lottery Ticket Hypothesis"** (Frankle & Carbin, 2019): Understanding network structure
- **"Traveling Words: A Geometric Interpretation"** (Pandey et al., 2023): Early trajectory analysis

### Related Recent Research

- **"Beyond Scalars: Evaluating and Understanding LLM Reasoning via Geometric Progress"** (2026): Complementary geometric analysis
- **"Curved Inference: Concern-Sensitive Geometry in Residual Streams"** (2026): Geometry in residual connections
- **"Latent Trajectory Dynamics in Large Language Models"** (2026): Manifold evolution framework
- **"Representational Curvature Modulates Behavioral Uncertainty"** (2026): Curvature and uncertainty
- **"The Curved Spacetime of Transformer Architectures"** (2025): Alternative geometric formulation

### Future Research Directions

1. **Scaling Analysis:** How do geometric properties scale to 100B+ parameter models?
2. **Training Dynamics:** Trajectory evolution during training from random initialization
3. **Multimodal Models:** Geometric analysis of vision-language models
4. **Cross-lingual Study:** Geometric properties across different language families
5. **Alternative Architectures:** State space models (Mamba), attention-free architectures
6. **Optimization:** Use geometric properties for architecture search and hyperparameter tuning
7. **Adversarial Robustness:** Geometric shifts under adversarial inputs
8. **Few-shot Learning:** How geometric structure enables rapid adaptation

---

**Paper Link:** [https://arxiv.org/abs/2606.09287](https://arxiv.org/abs/2606.09287)

**Full PDF:** [https://arxiv.org/pdf/2606.09287](https://arxiv.org/pdf/2606.09287)
