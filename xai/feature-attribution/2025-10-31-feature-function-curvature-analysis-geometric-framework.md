# Feature-Function Curvature Analysis: A Geometric Framework for Explaining Differentiable Models

**ArXiv ID:** 2510.27207  
**Submission Date:** October 31, 2025  
**Authors:** Hamed Najafi, Dongsheng Luo, Jason Liu (Florida International University)  
**Paper Link:** [ArXiv](https://arxiv.org/abs/2510.27207)

---

## Executive Summary

Feature-Function Curvature Analysis (FFCA) introduces a novel geometric framework for explaining differentiable models by analyzing the curvature properties of learned functions. Rather than collapsing feature importance into a single attribution score, FFCA produces a 4-dimensional signature for each feature that simultaneously captures impact, volatility, non-linearity, and feature interactions. By extending this framework with Dynamic Archetype Analysis, the paper provides the first direct empirical evidence that neural networks learn in a hierarchical fashion—consistently mastering simple linear relationships before learning complex interactions. This work transforms interpretability from a post-hoc static analysis into a dynamic window into how models actually learn.

---

## Problem Statement

### Limitations of Current Attribution Methods

Existing feature attribution methods (such as SHAP, LIME, and Integrated Gradients) suffer from critical limitations:

1. **Reductionism**: They collapse the multifaceted role of features into a single attribution score, losing important nuance
2. **Confounded Explanations**: Attribution scores become confounded by non-linearity and feature interactions, making it unclear what a high score actually means
3. **Static Analysis**: Traditional methods explain only the final trained model, not the learning process itself
4. **Incomplete Picture**: They cannot answer fundamental questions about how models learn or what mechanisms drive their predictions

### Research Gap

While neural network interpretability has made significant strides, there remains a critical gap: **we lack methods that can explain both what a model has learned AND how it learned it**. Furthermore, the interaction between features—often the most interesting aspect of model behavior—remains largely unexplored in explainability research.

---

## Core Concepts & Theory

### 1. The Function Geometry Perspective

FFCA adopts a geometric perspective on neural network functions. Rather than thinking of a model as a "black box" that maps inputs to outputs, FFCA asks: **What is the geometric structure of the learned function?**

Key insight: The geometry of a function is determined by its derivatives. First derivatives (gradients) tell us how much a function changes locally, while second derivatives (Hessian) tell us how the gradient itself changes—i.e., the **curvature**.

### 2. The Four-Dimensional Feature Signature

FFCA characterizes each feature with four orthogonal dimensions:

#### **Impact (I)**
Measures the magnitude of the feature's direct effect on model predictions:
- Computed from the gradient of the output with respect to the feature
- Similar to existing attribution methods (e.g., SHAP, gradient-based methods)
- Captures "how much does this feature matter?"

#### **Volatility (V)**
Measures how sensitive the feature's impact is to changes in other inputs:
- Captures instability and sensitivity of the attribution itself
- Addresses the known problem that attribution scores can be unstable
- Quantifies "how consistently important is this feature across different input variations?"

#### **Non-linearity (N)**
Measures the degree to which the feature's relationship to the output is non-linear:
- Derived from the feature's contribution to the Hessian diagonal
- Captures curvature in the feature-output relationship
- Indicates "is this relationship simple (linear) or complex (non-linear)?"

#### **Interaction (I)**
Measures how much a feature's effect depends on the values of other features:
- Extracted from off-diagonal Hessian elements
- Provides direct access to feature interactions through geometric analysis
- Answers "does the importance of this feature depend on other features?"

### 3. Mathematical Foundation: The Hessian Matrix

The Hessian matrix H is the matrix of second partial derivatives:

```
H[i,j] = ∂²f / ∂x_i ∂x_j
```

For differentiable models:
- **Diagonal elements** H[i,i] encode the non-linearity and curvature of feature i's relationship to the output
- **Off-diagonal elements** H[i,j] encode interactions between features i and j
- The Hessian provides a principled, parameter-free way to measure feature interactions

### 4. Handling Non-Smooth Activations

Standard neural networks use non-smooth activation functions (ReLU), which have undefined second derivatives at certain points. FFCA addresses this by:
- Temporarily replacing ReLU with smooth surrogate (Softplus) during analysis
- **Crucially**: Keeping all trained model weights fixed during this substitution
- This enables meaningful second-order derivatives without altering model behavior

This approach preserves model predictions while enabling rigorous geometric analysis.

### 5. Feature Archetypes

FFCA identifies eight distinct feature archetypes based on combinations of high/low Impact-Volatility-Non-linearity:

| Archetype | Impact | Volatility | Non-linearity | Interpretation |
|-----------|--------|-----------|----------------|-----------------|
| **Robust Linear** | High | Low | Low | Consistently important, simple relationship |
| **Critical Non-linear** | High | Low | High | Important but operates via complex function |
| **Volatile Linear** | High | High | Low | Important but unstable across inputs |
| **Volatile Non-linear** | High | High | High | Important but unreliable and complex |
| **Marginal Linear** | Low | Low | Low | Minimal contribution, simple relationship |
| **Marginal Non-linear** | Low | Low | High | Minimal contribution despite complexity |
| **Spurious Linear** | Low | High | Low | Noisy, often irrelevant signal |
| **Spurious Non-linear** | Low | High | High | Noise with complex structure |

These archetypes provide interpretable categories for understanding feature roles beyond simple importance rankings.

---

## Main Ideas & Key Contributions

### 1. **4D Feature Signatures Instead of Single Scores**

**Contribution**: Traditional attribution reduces features to scalars; FFCA provides 4D vectors capturing distinct aspects.

**Why it matters**: A feature can be (a) highly impactful but volatile, (b) important but non-linear, or (c) marginally interacting with others. A single score obscures these distinctions.

**Example**: In a medical prediction model:
- Feature A: High Impact, Low Volatility, Low Non-linearity → "Robust Linear" (trustworthy signal)
- Feature B: High Impact, High Volatility, High Non-linearity → "Volatile Non-linear" (important but unreliable)
- Same impact score, but vastly different interpretability and reliability

### 2. **Dynamic Archetype Analysis: Explaining the Learning Process**

**Contribution**: Computing feature signatures at regular intervals during training reveals how models learn over time.

**Key Finding**: Models learn hierarchically:
1. **Early training**: Features develop simple, linear relationships (high Impact, low Non-linearity)
2. **Mid training**: Non-linearity emerges as models capture nuanced patterns
3. **Late training**: Interactions become more prominent as models encode cross-feature dependencies

**Why it matters**: This provides the first direct evidence of feature learning phases in neural networks, suggesting that:
- Models prioritize learning simple patterns first
- Complexity is built on top of linear foundations
- Interaction learning is a sophisticated late-stage process

### 3. **Hessian-Based Interaction Measurement**

**Contribution**: Using the Hessian's off-diagonal elements to measure feature interactions naturally.

**Why it matters**: Previous work on feature interactions relies on heuristics or expensive counterfactual sampling. FFCA provides:
- A principled, mathematically grounded measure
- Direct computation from model geometry
- No additional hyperparameters or approximations

### 4. **Framework Agnostic to Architecture**

**Contribution**: FFCA works on any differentiable model (MLPs, CNNs, attention networks, custom architectures).

**Why it matters**: Unlike circuit-based interpretability (specific to transformers) or tree-based explanations, FFCA is broadly applicable across the ML ecosystem.

---

## Methodology & Implementation

### 1. **Core Algorithm**

**Inputs:**
- Trained differentiable model f
- Input sample x = (x₁, x₂, ..., x_n)
- Activation function substitution (ReLU → Softplus)

**Processing Steps:**

1. **Forward Pass**: Compute model output f(x)

2. **Gradient Computation**: Compute first derivatives (Jacobian):
   - ∇f(x) = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂x_n]

3. **Hessian Computation**: Compute second derivatives:
   - H(x) = [∂²f/∂x_i∂x_j] for all pairs i,j

4. **Feature Signature Extraction** for feature i:
   - **Impact**: |∂f/∂x_i| (absolute gradient)
   - **Volatility**: Standard deviation of ∂f/∂x_i across input variations or ensemble
   - **Non-linearity**: Magnitude of H[i,i] (diagonal Hessian element)
   - **Interaction**: Sum of |H[i,j]| for j ≠ i (off-diagonal contributions)

5. **Archetype Classification**: Assign feature i to one of eight archetypes based on quartile membership

**Computational Complexity:**
- One forward pass + one Hessian computation per sample
- O(n²) in number of features for dense Hessian computation
- [Exact computational costs unavailable—see full paper]

### 2. **Dynamic Archetype Analysis**

**Checkpoint-Based Learning Tracking:**

1. Save model at regular training intervals (e.g., every 10% of training)
2. Compute feature signatures at each checkpoint
3. Track how each feature's 4D signature evolves
4. Visualize learning trajectories in 4D signature space

**Analysis Questions Answered:**
- When does each feature become important?
- Does non-linearity increase monotonically during training?
- How do interactions emerge and stabilize?
- Are there distinct learning phases?

### 3. **Experimental Setup**

**Models Tested:**
- MLPs (fully connected networks) on tabular data
- CNNs on image classification tasks
- Regression and classification architectures
- Models of varying depths and widths

**Datasets:**
- Tabular datasets: [Specific datasets not detailed in search results]
- Image datasets: [Specific image datasets not detailed in search results]
- [Exact figures unavailable—see full paper]

**Baselines:**
- SHAP (expected value-based)
- LIME (local linear approximation)
- Integrated Gradients (path-integrated attribution)
- Gradient-based methods

### 4. **Evaluation Methodology**

**Faithfulness Metrics:**
- Feature removal (how much does removing a feature degrade performance?)
- Feature attribution correlation with ground truth feature importance
- Interaction detection accuracy vs. synthetic data with known interactions

**Stability Metrics:**
- Attribution consistency across similar inputs
- Volatility measure's ability to identify unstable features
- Robustness to small input perturbations

**Hierarchy Validation:**
- Temporal ordering of feature learning phases
- Consistency across different model initializations
- Alignment with known learning dynamics from literature

---

## Practical Applications & Real-World Use Cases

### 1. **Healthcare & Medical Diagnostics**

**Challenge**: Medical professionals need to understand not just which features matter, but whether they're reliable signals.

**FFCA Solution**:
- Distinguish "Robust Linear" biomarkers (high impact, stable) from "Volatile Non-linear" ones (unreliable despite apparent importance)
- Track how a model learns medical relationships: does it first learn simple correlations before complex interactions?
- Identify features with dangerous interactions (e.g., drug-drug or disease-disease synergies)

**Regulatory Alignment**: FDA approval for AI diagnostics increasingly requires demonstrating stability and interpretability—FFCA provides both.

### 2. **Finance & Credit Scoring**

**Challenge**: Financial institutions must explain credit decisions and detect bias in feature interactions.

**FFCA Solution**:
- Identify which features are "robust" decision drivers vs. spurious correlations
- Detect and explain feature interactions that might encode protected attributes (e.g., zip code interactions with income)
- Monitor model stability during market regime changes via volatility scores
- Track learning to ensure model wasn't overfitting to recent anomalies

**Regulatory Alignment**: GDPR "right to explanation" and fair lending regulations benefit from FFCA's principled feature characterization.

### 3. **Autonomous Systems & Safety-Critical AI**

**Challenge**: In autonomous driving or robotics, some decision factors are safety-critical and must be reliable.

**FFCA Solution**:
- Distinguish critical features (low volatility) from unreliable ones
- Understand feature interactions: how does the system's decision change when multiple conditions occur simultaneously?
- Track learning dynamics to ensure the system learns robust features, not spurious correlations
- Identify features with dangerous non-linearity (where small input changes cause large output jumps)

**Example**: In autonomous driving, identify which features are "robust linear" (e.g., lane detection) vs. "volatile non-linear" (e.g., weather interaction with road detection).

### 4. **Model Debugging & Development**

**Challenge**: Machine learning engineers need to understand why models fail or behave unexpectedly.

**FFCA Solution**:
- Detect if a model's decision is based on "Robust Linear" features or "Spurious Non-linear" noise
- Identify features with surprisingly high non-linearity (potential signs of overfitting)
- Discover unexpected interactions between features that might indicate data leakage
- Understand learning dynamics: if a feature's non-linearity surges late in training, it might indicate overfitting

### 5. **Fair AI & Bias Detection**

**Challenge**: Detect subtle bias encoded in feature interactions rather than individual features.

**FFCA Solution**:
- Discover hidden interactions: if protected attributes interact with other features in non-linear ways, this can encode bias
- Quantify interaction-level fairness: measure whether protected attribute interactions are important drivers of predictions
- Track fairness during training: monitor when potentially biased feature interactions emerge

---

## Insights & Implications

### 1. **Hierarchical Feature Learning is Fundamental**

The paper's finding that models learn simple linear relationships before complex interactions suggests this might be an intrinsic property of neural network learning, not architecture-specific.

**Implication**: This could inform:
- Better training curricula (teach simple patterns first)
- Improved generalization (ensure robust linear foundations before complex learning)
- Better understanding of why neural networks generalize

### 2. **Feature Roles are Multidimensional**

The limitations of single-score attribution methods are confirmed empirically: features cannot be ranked on importance alone.

**Implication**: Future interpretability research should:
- Move beyond scalar attribution to vector-valued explanations
- Recognize that "important" has multiple meanings
- Develop user studies on how humans interpret 4D vs. 1D feature characterizations

### 3. **Geometry is a Powerful Lens for Interpretability**

Using the Hessian (function curvature) naturally captures non-linearity and interactions without ad-hoc methods.

**Implication**: Second-order methods (Hessian-based) should become more standard in interpretability:
- They provide principled, parameter-free feature interaction measurement
- They scale better than sampling-based interaction detection methods
- They connect interpretability to differential geometry

### 4. **Open Questions and Limitations**

**Limitation - High-Dimensional Scaling**:
The Hessian computation scales as O(n²) in feature dimension. For models with thousands of features, this becomes expensive.
- Sparse Hessian approximations could help
- Feature selection before FFCA analysis could reduce dimensionality

**Limitation - Interpretation Complexity**:
While 4D signatures are richer than scalar scores, they're also more complex to interpret.
- Interactive visualizations needed for practical adoption
- User studies required to validate that practitioners find 4D explanations more useful

**Open Question - Causality**:
FFCA measures correlational structure (geometry), not causal relationships.
- Can FFCA be combined with causal inference methods for stronger guarantees?
- Does learning hierarchy correspond to causal hierarchy?

**Open Question - Generalization Across Models**:
Do all model architectures follow the same hierarchical learning pattern?
- Vision transformers vs. CNNs vs. MLPs: do they learn differently?
- Implications for transfer learning and architecture selection

### 5. **Connections to Broader XAI Research**

**To Feature Attribution Methods**:
- FFCA extends SHAP/LIME by providing richer feature characterizations
- Complementary to faithfulness metrics—understanding volatility helps interpret faithfulness limitations

**To Mechanistic Interpretability**:
- Shares the goal of understanding model internals
- FFCA is more general (applies to any architecture) but less detailed (doesn't trace specific computations)
- Potential synergy: could FFCA identify which parts of circuits to focus on?

**To Fairness & Bias Detection**:
- Interaction measurement directly addresses fairness concerns
- Can detect subtle biases encoded in non-linear feature relationships

---

## Code & Resources

### Official Links

- **ArXiv Paper**: https://arxiv.org/abs/2510.27207
- **Full PDF**: https://arxiv.org/pdf/2510.27207
- **HTML Version**: https://arxiv.org/html/2510.27207

### Code Availability
[Code availability not confirmed in official sources—check ArXiv page for supplementary materials or author GitHub]

### Dependencies & Requirements
- PyTorch or TensorFlow (for Hessian computation)
- NumPy, Pandas (for data processing)
- Matplotlib, Plotly (for 4D signature visualization)
- [Exact dependency list unavailable—see full paper]

### Getting Started

**Pseudocode for Basic Implementation**:
```python
# 1. Load trained model
model = load_model('path/to/model')

# 2. Prepare input sample
x = prepare_input(data)

# 3. Replace non-smooth activations
model = replace_activations(model, relu_to_softplus=True)

# 4. Compute feature signatures
impact = compute_gradient(model, x)
volatility = compute_gradient_variance(model, x, perturbations)
hessian = compute_hessian(model, x)
non_linearity = diagonal(hessian)
interaction = off_diagonal_sum(hessian)

# 5. Create 4D signature
signature = [impact, volatility, non_linearity, interaction]

# 6. Classify into archetype
archetype = classify_archetype(signature)
```

### Interactive Tools
- Interactive 4D visualization tool: [Status unknown—see supplementary materials]
- Feature archetype classifier: [Status unknown—see paper release]

---

## Related Work & Context

### Relationship to Other Attribution Methods

| Method | Focus | Advantages | Limitations |
|--------|-------|-----------|------------|
| **SHAP** | Shapley-based coalitional game theory | Theoretically grounded | Computationally expensive, scalar output |
| **LIME** | Local linear approximation | Model-agnostic, interpretable | Unstable, local scope only |
| **Integrated Gradients** | Path-accumulated gradients | Saturation/completeness axioms | Hyperparameter dependent (path choice) |
| **FFCA (This Work)** | Function geometry via Hessian | Multi-dimensional, principled interactions, dynamic | O(n²) complexity, requires differentiability |

### Connections to Mechanistic Interpretability

While mechanistic interpretability (circuits, sparse autoencoders) focuses on understanding internal mechanisms, FFCA operates at the input-output level:
- **Circuit Analysis**: "What specific neural components compute this function?"
- **FFCA**: "What does the geometry of the learned function tell us about feature roles?"
- **Synergy**: FFCA could identify high-priority input features for circuit analysis

### Foundational Work Cited or Built Upon

- Gradient-based attribution methods (Simonyan et al., 2014; Sundararajan et al., 2017)
- Feature interaction detection via partial dependence (Friedman & Popescu, 2008)
- Hessian-based sensitivity analysis in classical statistics
- Differential geometry approaches to neural networks

### Future Research Directions

1. **Efficient Hessian Approximations**: Block diagonal or low-rank approximations for high-dimensional models
2. **Causal FFCA**: Integrate with causal inference to distinguish correlation from causation
3. **Temporal FFCA**: Extend to recurrent models and time-series (how do signatures evolve temporally?)
4. **Multi-Output FFCA**: Handling multi-task models where different features matter for different outputs
5. **FFCA for Graph Networks**: Extending to relational and graph-structured data
6. **User Studies**: Empirical evaluation of whether practitioners find 4D explanations more useful than scalar scores

### Broader XAI Ecosystem Position

FFCA occupies a unique space:
- **More detailed than** scalar attribution methods (SHAP, LIME)
- **More general than** circuit-based mechanistic interpretability
- **Complementary to** causal inference methods
- **Applicable to** all differentiable models, not just transformers

---

## Summary & Impact

Feature-Function Curvature Analysis represents a significant advance in explainable AI by:

1. **Breaking the scalar attribution paradigm**: Features deserve multidimensional characterization
2. **Revealing learning dynamics**: Understanding not just what models learn, but how they learn it
3. **Principled interaction measurement**: Using model geometry (Hessian) instead of heuristics
4. **Broad applicability**: Working across all differentiable architectures
5. **Actionable insights**: Eight feature archetypes provide interpretable categories for practitioners

The finding that neural networks learn hierarchically—mastering simple patterns before complexity—has profound implications for understanding, training, and improving machine learning models. This work opens a new geometric perspective on model interpretability that could inspire future research in understanding the intrinsic structure of learned functions.

---

## References & Sources

- [ArXiv:2510.27207 - Feature-Function Curvature Analysis: A Geometric Framework for Explaining Differentiable Models](https://arxiv.org/abs/2510.27207)
- [ArXiv HTML Version](https://arxiv.org/html/2510.27207)
- [ArXiv PDF](https://arxiv.org/pdf/2510.27207)

---

**Last Updated:** July 9, 2026  
**Documentation Status:** Complete Summary
