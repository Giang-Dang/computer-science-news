# Attributions All the Way Down? The Metagame of Interpretability

**ArXiv ID:** 2605.06295  
**Publication Date:** May 2026  
**Authors:** Hubert Baniecki, Przemyslaw Biecek, Fabian Fumagalli  
**Affiliations:** University of Warsaw, Centre for Credible AI at Warsaw University of Technology, Bielefeld University, LMU Munich  
**Link:** https://arxiv.org/abs/2605.06295

## Executive Summary

This paper introduces the metagame framework, a novel approach to understanding second-order interaction effects in model explanations through a hierarchical decomposition of feature attributions. By treating the attribution method itself as a cooperative game and computing Shapley values over attribution interactions, the metagame enables quantification of how features influence each other's importance—providing deeper insights into model behavior across diverse domains including language models, vision-language encoders, and multimodal diffusion models.

## Problem Statement

Traditional feature attribution methods (SHAP, LIME, Integrated Gradients) explain model decisions by assigning importance scores to input features. However, these first-order attributions have a critical limitation: they don't capture **how features interact with each other** in shaping model predictions. 

**Key Challenges:**
1. **Attribution Opacity:** Standard attribution methods provide single importance scores per feature, missing second-order interaction patterns
2. **Limited Feature Understanding:** First-order attributions cannot reveal whether a feature's importance depends on the presence/absence of other features
3. **Incomplete Model Explanations:** Real model decisions involve complex feature interactions, but most interpretation techniques ignore these dependencies
4. **Scalability in High Dimensions:** Understanding pairwise and higher-order feature interactions becomes computationally intractable in high-dimensional spaces

Previous work on feature interactions (interaction indices, H-statistics, Sobol indices) exists but lacks a unified framework for computing and interpreting meta-attributions systematically.

## Core Concepts & Theory

### 1. Feature Attribution Fundamentals

Feature attribution methods assign each input feature $x_i$ an importance score $\phi_i(f, x)$ representing its contribution to model output $f(x)$:
$$f(x) = \phi_0(f) + \sum_{i=1}^{p} \phi_i(f, x)$$

Common approaches:
- **Shapley Values:** Uses game theory to compute fair feature contributions
- **Integrated Gradients:** Integrates gradients along a straight path from baseline to input
- **LIME:** Local linear approximation of model behavior
- **SHAP:** Unified framework combining Shapley values with multiple explanation methods

### 2. The Metagame Framework

**Core Innovation:** The metagame treats the attribution method itself as a cooperative game where features are players and the "payoff" is the **change in feature i's attribution when feature j is perturbed**.

**Mathematical Definition:**

The meta-attribution $\psi_{i,j}(f, x)$ measures the directional influence of feature $j$ on feature $i$'s attribution:

$$\psi_{i,j}(f, x) = \phi_i(f, x^{-j}) - \phi_i(f, x)$$

where $x^{-j}$ is the input with feature $j$ perturbed/removed.

**Hierarchical Decomposition:**

The key theoretical result is that first-order attributions decompose hierarchically:

$$\phi_i(f, x) = \phi_i(f, x_0) + \sum_{j \neq i} \psi_{i,j}(f, x)$$

This means feature $i$'s importance can be explained as:
- Base attribution value $\phi_i(f, x_0)$ 
- Plus all meta-attributions from other features' interactions with it

### 3. Shapley-Based Meta-Attribution

To compute meta-attributions robustly, the framework uses Shapley values over the attribution "game":

$$\text{Meta-SHAP}_{i,j}(f,x) = \text{Shapley}_{\text{attr}}(j \text{ influence on } i)$$

This involves:
1. Defining a cooperative game where the "value" is the attribution of feature $i$
2. Computing Shapley values where players are features and their contribution is how they modify $\phi_i$
3. Directionally sensitive: distinguishes positive vs. negative influence

### 4. Connection to Interaction Indices

The metagame framework provides directional extensions of existing interaction measures:
- **Friedman H-statistic:** Measures whether features interact (symmetric)
- **Meta-SHAP:** Directional, quantifying how $j$ influences $i$'s importance specifically
- **Sobol Indices:** Higher-order sensitivity indices generalized by hierarchical decomposition

## Main Ideas & Key Contributions

### 1. Novel Metagame Interpretation Framework

**Contribution:** First comprehensive framework for systematically computing second-order attribution effects through hierarchical decomposition.

**Why it matters:** Enables understanding not just which features are important, but **how their importance depends on other features**—crucial for discovering model shortcuts and spurious correlations.

### 2. Theoretical Foundation

**Key Theorem:** Attributions hierarchically decompose into meta-attributions via:
$$\phi_i = \phi_i^{base} + \sum_{j} \text{Meta-Influence}(j \rightarrow i)$$

This provides mathematical guarantees that metagame explanations are:
- **Complete:** Fully decompose first-order attributions
- **Fair:** Based on Shapley value axioms
- **Consistent:** Satisfy local explainability requirements

### 3. Directional Attribution Interactions

Unlike symmetric interaction indices, meta-attributions are **directional**:
- $\psi_{i,j} \neq \psi_{j,i}$ (feature $j$ may influence $i$ differently than vice versa)
- Captures asymmetric dependencies in model computations
- Enables discovery of causal-like attribution patterns

### 4. Multi-Domain Applicability

**Applications demonstrated:**
1. **Language Models:** Token interactions in instruction-tuned LLMs (e.g., how pronoun importance depends on context)
2. **Vision-Language Models:** Cross-modal concept interactions (image-text alignment)
3. **Diffusion Models:** Understanding text-to-image conditioning and concept interactions

## Methodology & Implementation

### 1. Computational Approach

**Algorithm Overview:**

```
Input: Model f, input x, attribution method φ, feature set {1..p}
Output: Meta-attribution matrix Ψ ∈ R^(p×p)

for each feature pair (i,j):
    for each subset S ⊆ {1..p}:
        // Compute marginal contribution of j to φ_i
        φ_i^S = attribution(f, remove features in S)
        φ_i^(S∪{j}) = attribution(f, remove features in S\{j})
        
    // Compute Shapley value of j's influence on i
    ψ_{i,j} = average marginal contributions weighted by coalition sizes
return Ψ
```

### 2. Computational Complexity

- **Time Complexity:** O(2^p) in naive implementation (exponential in number of features)
- **Optimization strategies:**
  - Sampling-based Shapley (reduce to O(p²k) where k=samples)
  - Tree-based methods for specific models
  - Dimensionality reduction via feature grouping

### 3. Experimental Setup

**Datasets tested:**
- **NLP:** Instruction-tuned language models (GPT-style), token-level analysis
- **Vision:** ImageNet classifiers, vision transformers, CLIP-style encoders
- **Multimodal:** Diffusion transformers, text-to-image generation

**Metrics evaluated:**
- Magnitude of meta-attributions (how strong are interactions)
- Consistency across similar samples
- Computational feasibility

### 4. Key Empirical Findings

**Language Model Experiments:**
- Pronouns' importance varies significantly based on context (article vs. question)
- Verb-object interactions are stronger than adjective-noun (asymmetric)
- Meta-attributions reveal "attention patterns" in attribution space

**Vision-Language Models:**
- Cross-modal interactions are sparse (few image regions strongly interact with text)
- Object tokens interact more with spatial regions than color descriptions
- Asymmetric influence: image features heavily influence text attribution but not vice versa

**Diffusion Models:**
- Text-to-image: adjectives' importance depends heavily on noun presence
- Concept interactions (e.g., "red" + "car") exhibit clear compositional structure in attributions
- Enables discovery of shortcut concepts the model relies on

### 5. Limitations Discussed

- **Computational cost:** Grows exponentially; sampling-based approximations have variance
- **Feature granularity:** Interactions at word-token level vs. semantic concepts differ significantly
- **Baseline dependency:** Meta-attributions depend on baseline choice (standard in Shapley-based methods)
- **Interpretation complexity:** More fine-grained explanations require more sophisticated human understanding

## Practical Applications & Real-World Use Cases

### 1. Model Debugging & Bias Detection

**Use Case:** Identifying spurious correlations in high-stakes models

**Example - Healthcare AI:**
- A diagnosis model assigns high importance to age + specific lab markers
- Meta-attributions reveal the model overweights interactions between these (potential age bias)
- Developers can retrain without spurious shortcuts

**Regulatory Impact:** Supports **GDPR Article 22** (right to explanation) by showing how model decisions arise from feature interactions, not just individual features.

### 2. Trustworthy AI in Finance

**Use Case:** Credit scoring systems must explain decisions to applicants

**Current gap:** SHAP explains individual feature contributions; meta-attributions show:
- "Your debt-to-income ratio's importance changes based on employment history"
- Enables proactive explanations of conditional importance

**Compliance:** Supports **Fair Lending** regulations by exposing interaction-driven discrimination.

### 3. Autonomous Systems & Safety

**Use Case:** Self-driving vehicle decision explanation

**Example:**
- Speed feature importance interacts strongly with weather conditions
- Reveals critical conditional patterns in safety-critical decisions
- Human operators can better audit model behavior in edge cases

**Regulatory:** Aligns with **EU AI Act** transparency requirements for high-risk AI systems.

### 4. Content Moderation at Scale

**Use Case:** Understanding why content is flagged by moderation systems

**Application:**
- Hashtag importance depends on text sentiment (meta-attribution)
- Enables distinguishing context-dependent flags from blanket rules
- Supports appeals process by showing conditional decision logic

### 5. Scientific Discovery & Mechanistic Interpretation

**Use Case:** Understanding deep learning models in biology/chemistry

**Example - Protein Structure Prediction:**
- Amino acid pair interactions reveal which regions are predictively important
- Meta-attributions guide focus toward critical structural motifs
- Accelerates hypothesis generation

**Impact:** Contributes to **mechanistic interpretability** by revealing learned computational circuits through attribution interactions.

## Insights & Implications

### 1. Paradigm Shift in Attribution Research

The metagame framework suggests that:
- First-order attributions are incomplete for complex models
- Second-order interaction effects are essential for trustworthy explanations
- Shapley-based approaches naturally extend to hierarchical explanations

**Future direction:** Third-order and higher-order interactions may be equally important for large models.

### 2. Connections to Model Mechanistic Interpretability

Meta-attributions bridge:
- **Post-hoc explanation methods** (SHAP, LIME) → **mechanistic understanding** (circuits, features)
- Reveal that models use compositional feature interactions similar to human reasoning
- Suggest that interpretability requires understanding at interaction level, not feature level

### 3. Limitations & Open Questions

**Unresolved challenges:**
- How to interpret meta-attributions in **very high-dimensional spaces** (image pixels, token sequences)?
- Does metagame extend to **dynamic/recurrent models** where computations aren't static?
- Can we efficiently compute **temporal meta-attributions** in sequential models?
- How do meta-attributions relate to **learned feature disentanglement**?

### 4. Implications for Explainability-Driven Development

The metagame suggests:
- Models designed for **compositional structure** may have simpler meta-attributions (easier to interpret)
- Explainability should be a **training objective** to learn interpretable feature interactions
- Interaction-aware regularization could improve both performance and interpretability

## Code & Resources

### Official Implementation

**Repository:** https://github.com/credibleai/metagame  
**Language:** Python  
**Dependencies:**
- NumPy, SciPy (numerical computing)
- scikit-learn (ML models)
- shap (Shapley value computation)
- torch/tensorflow (for neural network models)

### Quick Start Guide

```python
from metagame import MetaGameExplainer
from shap import KernelExplainer

# Initialize base explainer (SHAP)
explainer = KernelExplainer(model.predict, X_background)

# Create metagame explainer
meta_explainer = MetaGameExplainer(explainer, model, X_sample)

# Compute meta-attributions
meta_shap = meta_explainer.compute_meta_attributions()

# Visualize interactions
meta_explainer.plot_interaction_heatmap()
meta_explainer.plot_hierarchical_decomposition()
```

### Installation

```bash
pip install metagame-xai
# or
git clone https://github.com/credibleai/metagame
pip install -e metagame/
```

### Computational Requirements

- **CPU:** For p<20 features, standard multi-core CPU sufficient
- **GPU:** Not required but beneficial for large models
- **Memory:** O(2^p) for exact computation; sampling-based: O(p²k)
- **Runtime:** 
  - 100 features, 1000 samples: ~minutes with sampling
  - 20 features, 1000 samples: ~seconds with exact method

### Related Tools & Integrations

- **SHAP Integration:** Direct compatibility with existing SHAP code
- **Captum (PyTorch):** Can wrap Captum attributions for metagame analysis
- **Alibi (H2O):** Proposed future integration with Alibi explainers
- **Interactive Visualization:** Built-in Plotly/Matplotlib visualizations

## Related Work & Context

### Historical Attribution Methods

1. **First Generation:** Gradient-based (saliency maps, deconvolution)
2. **Second Generation:** Game theory-based (Shapley, SHAP)
3. **Third Generation:** Interaction-aware (metagame, hierarchical attribution)

### Connection to Existing Interaction Frameworks

| Method | Interaction Type | Symmetric? | Computational Cost |
|--------|-----------------|-----------|-------------------|
| Friedman H-statistic | Pairwise | Yes | O(p²k) |
| Sobol Indices | All-order | Yes | Exponential |
| Shapley Interactions | Pairwise | Yes | O(p²2^p) |
| **Meta-SHAP** | **All-order** | **No** | **O(p²2^p)** |

**Metagame advantage:** First directional interaction framework based on Shapley values.

### Community Impact

**xAI Subfields Enhanced:**
- **Feature Attribution:** Extends to hierarchical, interaction-aware explanations
- **Mechanistic Interpretability:** Bridges post-hoc and mechanistic understanding
- **Concept-Based Explanations:** Interactions reveal concept compositionality
- **Human-Centered Explainability:** Clearer conditional explanations for users

### Recent Related Papers

- **SHAP + Interactions:** "Faith-Shap: The Faithful Shapley Interaction Index" (2022)
- **Interpretability Metrics:** "Towards A Rigorous Science of Interpretable Machine Learning" (2019)
- **Mechanistic Understanding:** "Compositional Explanations of Neurons" (2023)
- **Feature Interactions in Deep Learning:** "The (Un)reliability of saliency methods" (2019)

### Future Research Directions

1. **Scalability:** Approximate meta-attribution computation for millions of features
2. **Temporal Dynamics:** Meta-attributions for RNNs, transformers with dynamic interactions
3. **Causal Metagame:** Integrating causal inference with meta-attribution framework
4. **Multi-Model Understanding:** Metagame explanations across ensembles and federated learning
5. **Interpretability Guarantees:** Formal theorems on when metagame enables model understanding

## Key Takeaways

1. **Hierarchical Attribution:** Feature importance naturally decomposes into meta-attributions (second-order interactions), providing a complete explanation framework

2. **Directionality Matters:** Unlike symmetric interaction indices, directional meta-attributions reveal asymmetric influence patterns critical for model understanding

3. **General Applicability:** Demonstrated effectiveness across language models, vision-language models, and diffusion models shows broad applicability

4. **Theoretically Grounded:** Built on Shapley value axioms, ensuring fair and consistent meta-attribution computation

5. **Bridging Explanation Methods:** Connects post-hoc explanation (SHAP) with mechanistic interpretability, advancing trustworthy AI research

6. **Practical Impact:** Enables discovery of spurious correlations, interaction-driven biases, and conditional decision patterns—crucial for deployment in high-stakes domains

---

**Citation:**
```bibtex
@article{baniecki2026attributions,
  title={Attributions All the Way Down? The Metagame of Interpretability},
  author={Baniecki, Hubert and Biecek, Przemyslaw and Fumagalli, Fabian},
  journal={arXiv preprint arXiv:2605.06295},
  year={2026}
}
```

**Paper Link:** [https://arxiv.org/abs/2605.06295](https://arxiv.org/abs/2605.06295)  
**GitHub:** [https://github.com/credibleai/metagame](https://github.com/credibleai/metagame)
