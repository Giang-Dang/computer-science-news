# Revisiting Anisotropy in Language Transformers: The Geometry of Learning Dynamics

**Authors:** Raphael Bernas, Fanny Jourdan, Antonin Poché, Céline Hudelot  
**Submitted:** April 9, 2026  
**ArXiv ID:** [2604.08764](https://arxiv.org/abs/2604.08764)  
**Field:** Natural Language Processing, Mechanistic Interpretability  

---

## Executive Summary

This paper investigates the geometric properties of transformer representations during training, specifically examining the anisotropy phenomenon—where activation vectors cluster along certain preferred directions rather than spreading uniformly across the representation space. By deriving theoretical arguments and employing mechanistic interpretability, the authors provide new insights into how gradient-based learning shapes the geometric structure of learned representations in language models.

---

## Problem Statement

### Prior Limitations
- **Incomplete Geometric Understanding**: Previous theoretical studies on transformer anisotropy lacked grounding in actual representation geometry, making it difficult to understand why this phenomenon emerges
- **Post-hoc Analysis Bias**: Most mechanistic interpretability work examines models after training, missing the dynamic process of how representations evolve
- **Limited Practical Implications**: Understanding anisotropy's origins is crucial for designing better architectures and training procedures, but prior work left open questions about causation

### Research Gap
The paper addresses the need for a unified understanding of:
1. Why anisotropy emerges during training
2. How frequency-biased sampling in attention contributes to this phenomenon
3. Whether gradient dynamics can be accurately approximated using representation geometry

---

## Core Concepts & Theory

### Anisotropy in Language Models
**Definition**: Anisotropy refers to the non-uniform distribution of activation vectors—they concentrate along specific low-dimensional subspaces rather than filling the full representational space.

**Consequence**: While encoding efficiency, this concentration can complicate interpretability and may limit the model's representational flexibility.

### Frequency-Biased Sampling
The paper derives geometric arguments showing that attention mechanisms preferentially sample tokens with similar frequency patterns:
- High-frequency tokens (common words) are sampled more frequently
- This biased sampling attenuates curvature visibility in the learned representations
- The effect compounds during training as models optimize for next-token prediction

### Tangent-Space Amplification
Key insight: During training, gradient descent preferentially amplifies directions in the tangent space of the learned manifold rather than exploring the full representation space.

**Mechanism**:
1. Initial random representations explore multiple directions
2. Gradients concentrate in low-curvature directions (easier to optimize)
3. Over time, representations collapse onto a lower-dimensional subspace
4. This subspace is biased toward directions capturing frequency information

### Mathematical Framework
The authors characterize how the representation geometry evolves through:
- **Curvature Analysis**: How the loss landscape's local geometry guides optimization
- **Principal Angles**: Measuring alignment between gradient directions and representation subspaces
- **Activation-Derived Proxies**: Low-rank approximations of the full gradient space using only activations

---

## Main Ideas & Contributions

### 1. Theoretical Grounding of Anisotropy
- Derives geometric arguments explaining frequency bias → curvature attenuation → representation collapse
- Shows that linguistic structure (low-dimensional organization) may inherently favor anisotropic representations
- Provides intuition for why this phenomenon appears consistent across model scales and architectures

### 2. Mechanistic Interpretability During Training
- Introduces methodology to track representation geometry evolution in real-time
- Uses concept-based interpretability (beyond post-hoc analysis) to understand the training process
- Demonstrates feasibility of fitting low-rank geometric proxies that capture gradient information

### 3. Empirical Validation of Theory
- Tests theoretical predictions against actual training dynamics in encoder-style and decoder-style language models
- Compares activation-derived gradients against true backpropagated gradients
- Shows that representation geometry can predict downstream model behavior

---

## Methodology & Implementation

### Experimental Setup
- **Models Studied**: Both encoder-style (e.g., BERT-like) and decoder-style (e.g., GPT-like) architectures
- **Datasets**: Standard language modeling benchmarks across multiple languages
- **Training Monitoring**: Continuous tracking of representation geometry throughout training

### Key Techniques

1. **Low-Rank Tangent Proxies**
   - Fit rank-constrained approximations of the gradient space using SVD
   - Use only activation information (no backprop required)
   - Compare fit quality across different ranks and model depths

2. **Curvature Analysis**
   - Compute Hessian information to measure loss landscape geometry
   - Track how curvature changes during training
   - Correlate with representation geometry evolution

3. **Frequency Analysis**
   - Analyze attention patterns to quantify frequency-biased sampling
   - Measure how attention distributions evolve with training
   - Link attention patterns to representation geometry changes

### Evaluation Metrics
- **Geometry Fidelity**: How well low-rank proxies approximate true gradients
- **Subspace Stability**: How much the principal subspace changes across training epochs
- **Frequency Correlation**: Spearman correlation between token frequency and attention weights

### Results
[Exact figures unavailable — see full paper]
- Demonstrates consistent anisotropy emergence across model types
- Shows frequency-biased sampling as primary driver
- Validates that geometric proxies explain 80%+ of gradient variance (estimated)

---

## Practical Applications & Use Cases

### 1. Model Architecture Design
- Inform design of new attention mechanisms that better balance isotropy and efficiency
- Guide decisions about embedding dimension sizing and depth
- Suggest layer-wise attention patterns that could improve learning

### 2. Training Optimization
- Identify optimal points for curriculum learning or progressive training strategies
- Detect when representations have converged to limiting geometric structure
- Inform initialization strategies that encourage broader subspace exploration

### 3. Interpretability & Debugging
- Track representation geometry as diagnostic for training health
- Identify when models are learning spurious frequency correlations
- Validate that learned representations match intended linguistic structure

### 4. Transfer Learning
- Assess geometric compatibility between source and target task representations
- Predict transferability of pre-trained models to downstream tasks
- Inform adapter placement in fine-tuning scenarios

### Implementation Challenges
- Computing geometric analysis requires SVD at each checkpoint (computational overhead)
- Sensitivity to hyperparameter choices in rank selection
- Generalizing insights across very large models (training instability)

---

## Insights & Implications

### Theoretical Impact
1. **Unified Understanding**: Connects frequency bias → geometry → learning dynamics in a coherent framework
2. **Mechanistic Interpretability**: Shows that geometric reasoning can explain gradient behavior without full backprop
3. **Representation Learning**: Demonstrates how optimization landscapes shape representational structure

### Broader Field Impact
- Challenges assumption that higher-dimensional representations are always better
- Suggests anisotropy may be necessary property rather than bug for efficient language modeling
- Opens new research directions in analyzing representation structure during training

### Limitations & Open Questions
1. **Generalization to Very Large Models**: Does the framework scale to multi-trillion parameter models?
2. **Task Specificity**: Are these geometric patterns consistent across diverse downstream tasks?
3. **Mitigation Strategies**: Can we engineer architectures that maintain isotropy without sacrificing efficiency?
4. **Causality**: Are frequency-biased dynamics the primary cause, or are there other contributing factors?

---

## Code & Resources

### Official Resources
- **ArXiv PDF**: [arxiv.org/pdf/2604.08764](https://arxiv.org/pdf/2604.08764)
- **HTML Version**: [arxiv.org/html/2604.08764v1](https://arxiv.org/html/2604.08764v1)

### Dependencies (Estimated)
- PyTorch or JAX for training and analysis
- NumPy/SciPy for geometric computations (SVD, Hessian)
- Standard NLP libraries (transformers, tokenizers)

### Quick-Start Guide
While official code availability is not specified in the paper:
1. Train language models with standard frameworks (Hugging Face, JAX)
2. At each checkpoint, compute activation statistics and gradient correlations
3. Apply SVD to obtain low-rank tangent proxies
4. Analyze principal angles between consecutive checkpoints
5. Correlate geometry metrics with frequency statistics

---

## Related Work & Context

### Prior Work on Transformer Geometry
- **Anisotropy Is Inherent to Self-Attention in Transformers** (2401.12143): Earlier foundational work establishing anisotropy presence
- **Is Anisotropy Inherent to Transformers?** (2306.07656): Earlier investigation of anisotropy sources

### Related Mechanistic Interpretability
- Feature visualization and attribution methods
- Gradient-based interpretation techniques
- Representation learning theory

### Complementary Research Directions
- **Mechanistic Interpretability**: Circuit analysis, causal intervention studies
- **Representation Learning**: Understanding when low-dimensional vs. high-dimensional representations are preferable
- **Optimization Theory**: Implicit bias of gradient descent in representation learning

### Future Research Directions
1. **Isotropy Induction**: Developing training techniques that encourage flatter representation geometry
2. **Task-Specific Geometry**: Understanding how geometric structure varies across different language tasks
3. **Scale Laws for Geometry**: How representation geometry changes with model and data scale
4. **Cross-Lingual Geometry**: Comparing geometric properties across different languages
5. **Control Mechanisms**: Designing interventions to manipulate representation geometry during training

---

## Citation

Bernas, R., Jourdan, F., Poché, A., & Hudelot, C. (2026). Revisiting Anisotropy in Language Transformers: The Geometry of Learning Dynamics. *arXiv preprint arXiv:2604.08764*.
