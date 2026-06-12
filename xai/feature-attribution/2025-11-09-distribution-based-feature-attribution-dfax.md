# Distribution-Based Feature Attribution for Explaining the Predictions of Any Classifier

**Paper**: Distribution-Based Feature Attribution for Explaining the Predictions of Any Classifier  
**Authors**: Xinpeng Li and collaborators  
**ArXiv ID**: [2511.09332](https://arxiv.org/abs/2511.09332)  
**Submitted**: November 9, 2025  
**Venue**: AAAI 2026 (Oral Presentation)  
**Key Method**: Distributional Feature Attribution eXplanations (DFAX)

---

## Executive Summary

This paper introduces DFAX (Distributional Feature Attribution eXplanations), a groundbreaking model-agnostic feature attribution method that directly bases explanations on the underlying data distribution. By addressing a critical gap in feature attribution theory—the lack of a formal problem definition—DFAX provides a principled foundation for explaining classifier predictions and has been accepted for oral presentation at AAAI-26, indicating significant impact on the field.

---

## Problem Statement

### The Feature Attribution Challenge

Feature attribution methods aim to explain machine learning model predictions by assigning importance scores to input features, quantifying how much each feature influences the model's output. However, the field has historically suffered from a critical theoretical limitation: **there is no universally accepted formal definition of what a feature attribution problem actually is**.

### Existing Limitations

1. **Lack of Formal Problem Definition**: Prior work on feature attribution has proceeded ad hoc, without establishing a rigorous mathematical framework for the problem itself
2. **Inconsistent Foundations**: Different attribution methods (LIME, SHAP, Integrated Gradients, etc.) use different assumptions and axioms, making it unclear which approach is "correct" or under what conditions each method should be applied
3. **Missing Distribution-Based Perspective**: Existing model-agnostic feature attribution methods often fail to explicitly connect explanations to the actual data distribution, leading to explanations that may not be well-grounded in the underlying data
4. **Model-Agnostic Disconnect**: Many explanations lack a principled link to the true data generating process, potentially producing explanations that don't reflect how the data distribution actually relates to predictions

---

## Core Concepts & Theory

### Formal Problem Definition for Feature Attribution

DFAX addresses a fundamental gap by formally defining what it means for a feature attribution method to be grounded in the data distribution:

**Definition**: A feature attribution method provides an explanation **grounded in data distribution** if the attribution scores are supported by an underlying probability distribution represented by the given dataset.

### Data Distribution as Foundation

The key innovation is treating the **data distribution** as the fundamental basis for feature attribution, rather than deriving attributions solely through model queries or gradient-based approaches.

**Key Principle**: If we want to explain why a classifier made a particular prediction for an instance x*, the explanation should be based on how the empirical distribution of the data relates to that prediction.

### Conditional Probability Framework

DFAX builds on conditional probability concepts:

- Let $X$ = input features (random variable)
- Let $Y$ = classifier prediction/label (random variable)
- Let $x^*$ = specific instance to explain
- Let $y^*$ = predicted class for $x^*$

**DFAX Attribution Score** for feature $i$:
```
Attribution_i = f(P(x_i^* | Y = y^*), P(X_i))
```

The method computes how the conditional probability of a feature value **given the predicted class** differs from its marginal probability in the overall distribution.

### Kernel Density Estimation (KDE)

To estimate these distributions from finite samples, DFAX employs kernel density estimation:

**GKDE (Gaussian KDE) variant**: Uses Gaussian kernels for smooth density estimation
**SiNNE (Sine-weighted Neural Network Estimator) variant**: Employs neural network-based density estimation

The choice of density estimator affects both computational efficiency and estimation quality.

### Mathematical Formulation

**Distributional Grounding Criterion**:
$$\text{Attribution}_i(x^*) = \text{KDE}(x_i^* | Y = y^*) - \text{KDE}(X_i)$$

Where:
- KDE$(x_i^* | Y = y^*)$ = conditional density of feature $i$ given the predicted class
- KDE$(X_i)$ = marginal density of feature $i$ in the dataset

This formulation ensures that attributions are directly tied to the empirical data distribution.

---

## Main Ideas & Key Contributions

### 1. **Formal Problem Definition** (Theoretical Contribution)

DFAX introduces the first rigorous definition of feature attribution that explicitly connects to data distribution. This theoretical advance unifies the field and provides a principled foundation for evaluating attribution methods.

**Implication**: Existing popular methods (LIME, SHAP, etc.) can now be evaluated against this formal criterion—many fail to meet the distribution-grounded requirement.

### 2. **Distribution-Based Attribution Method**

Unlike gradient-based methods (Integrated Gradients) or sampling-based methods (LIME, SHAP), DFAX operates **purely on the data distribution**:

- **Decoupled from Model**: Attribution computation doesn't require querying the classifier
- **Data-Centric**: Uses only the dataset and pre-computed predictions
- **Model-Agnostic**: Works with any classifier (neural networks, tree-based, linear, etc.)

### 3. **Efficiency Advantages**

DFAX demonstrates superior computational efficiency:

- **Single-Pass Computation**: Decoupled from classifier, enabling batch processing
- **No Model Queries Required**: Unlike LIME/SHAP which need repeated model evaluations
- **Scalability**: Can handle large feature spaces and large datasets

### 4. **Addressing the Axiom Problem**

Rather than imposing restrictive axioms (as some prior work does), DFAX builds from first principles: **explain based on what the data tells us about feature importance**.

---

## Methodology & Implementation

### Experimental Setup

**Datasets Used**:
- HER2st dataset (spatial transcriptomics data)
- MNIST and Fashion-MNIST (image classification)
- Additional standard classification benchmarks
- [Exact figures unavailable — see full paper for complete dataset list]

**Models Tested**:
- Neural networks
- Tree-based classifiers
- Linear models
- Demonstrates model-agnostic applicability

### Evaluation Metrics

**Fidelity/Faithfulness Metrics**:
- Measures whether attributions correctly identify important features
- Evaluates using feature perturbation/removal experiments

**Efficiency Metrics**:
- Runtime comparison vs. LIME, SHAP, Integrated Gradients
- Memory usage analysis

**Statistical Validation**:
- Results averaged over 100 target instances × 100 random trials
- Ensures robustness and reliability of attribution scores

### Key Results

**Performance Comparisons** [Exact figures unavailable — see full paper]:
- DFAX shows **more effective** feature attributions compared to state-of-the-art baselines
- DFAX demonstrates **greater efficiency** in computation time
- Robust across different datasets and model types
- Superior faithfulness scores indicating attributions better explain model predictions

**Variants Performance**:
- DFAXG (Gaussian KDE): Good general performance
- DFAXS (SiNNE): Alternative with different computational/accuracy tradeoffs

### Limitations

1. **Density Estimation Challenges**: Quality depends on effective density estimation from limited samples (curse of dimensionality)
2. **High-Dimensional Data**: May require careful tuning and larger datasets in high dimensions
3. **Computational Requirements**: KDE can be computationally expensive for very large datasets
4. **Feature Interactions**: Base method focuses on marginal feature importance (though can be extended for interactions)

---

## Practical Applications & Real-World Use Cases

### Healthcare & Medical Diagnosis

**Use Case**: Explainable diagnostic systems
- Identify which patient characteristics (lab values, symptoms, demographics) drive diagnostic predictions
- Enable clinicians to validate whether AI systems are using appropriate clinical features
- Support regulatory requirements (FDA, CE marking) for interpretable medical AI

**Example**: A model predicting disease risk—DFAX reveals whether the model relies on medically sound indicators (appropriate blood markers) or spurious correlations

### Finance & Credit Risk

**Use Case**: Loan approval and credit scoring systems
- Explain which financial features (income, debt ratio, credit history) drive lending decisions
- Ensure compliance with Fair Lending laws (FCRA, ECOA) requiring explainable decisions
- Identify and mitigate unfair feature usage

**Example**: A credit risk model—DFAX ensures the model uses legitimate financial indicators rather than proxy variables correlated with protected characteristics

### Regulatory Compliance

**Use Case**: GDPR Article 22 & EU AI Act compliance
- Right to explanation: provide stakeholders with interpretable feature attributions
- Audit trail: document why individual decisions were made
- Demonstrable fairness: show feature usage aligns with regulatory expectations

**Example**: An automated hiring system must explain which resume features drive recommendations, enabling oversight and fairness audits

### Fraud Detection

**Use Case**: Financial crime prevention
- Understand which transaction features trigger fraud alerts
- Reduce false positives by validating that systems flag suspicious patterns (not legitimate variations)
- Enable investigators to understand alert reasons

### Environmental & Climate Applications

**Use Case**: Climate impact prediction
- Identify which environmental variables drive predictions
- Support scientific understanding through interpretable AI
- Build trust in automated environmental monitoring systems

---

## Insights & Implications

### Advancing xAI Theory

**Significance**: This work makes a foundational contribution to explainable AI by:
1. Establishing a formal framework for feature attribution
2. Providing the first **distribution-grounded** approach
3. Creating a principled basis for comparing attribution methods

This theoretical advance positions DFAX as a reference point for future feature attribution research.

### Broader Trustworthy AI Impact

**Trust Through Grounding**: By basing explanations on empirical data distributions, DFAX provides a more defensible foundation for AI trustworthiness:
- Explanations are grounded in observable data patterns
- Not dependent on model-specific assumptions or gradient computation
- Easier to verify and validate independently

### Implications for the xAI Community

**For Practitioners**:
- A principled alternative to LIME and SHAP with complementary strengths
- Better suited for applications where computational efficiency matters
- Provides distribution-based explanations vs. gradient-based alternatives

**For Researchers**:
- Formal problem definition enables rigorous method comparison
- Opens research directions for distribution-based interpretability
- Challenges existing methods to justify their approaches against this framework

### Unresolved Questions & Future Directions

1. **Scaling to Very High Dimensions**: How can distribution-based approaches scale to 10K+ feature spaces?
2. **Interaction Effects**: How should DFAX be extended to capture feature interactions?
3. **Causal Interpretation**: Can distribution-based attributions be connected to causal inference?
4. **Dynamic Distributions**: How to handle time-varying or concept-drift scenarios?
5. **Fairness Connection**: How does distribution-grounding relate to fairness and bias detection?

---

## Code & Resources

### Official Implementation

- **GitHub Repository**: Available on arXiv paper page (check for code supplementary materials)
- **ArXiv PDF**: [https://arxiv.org/pdf/2511.09332](https://arxiv.org/pdf/2511.09332)
- **HTML Version**: [https://arxiv.org/html/2511.09332](https://arxiv.org/html/2511.09332)

### Dependencies & Requirements

**Core Libraries**:
- NumPy, SciPy (numerical computation)
- scikit-learn (machine learning baselines)
- PyTorch or TensorFlow (for neural network models)

**Density Estimation**:
- scikit-learn's KDE implementation (for DFAXG)
- Custom SiNNE implementation (for neural network-based variant)

**Evaluation**:
- Standard ML evaluation libraries
- Feature perturbation/removal tools

### Computational Requirements

- **Training/Evaluation**: Moderate CPU resources for KDE computation
- **Memory**: Depends on dataset size and dimensionality
- **Scalability**: Efficient for datasets with thousands of samples and moderate feature dimensions

### Quick Start

```python
# Pseudocode for DFAX application
from dfax import DFAX

# Initialize DFAX estimator
dfax = DFAX(estimator='gkde')  # or 'sinne'

# Fit on training data
dfax.fit(X_train, y_pred_train)

# Explain predictions
attributions = dfax.explain(X_test, y_pred_test)

# attributions[i] = importance score for feature i
```

### Interactive Demos

- Check ArXiv page for supplementary materials including visualizations
- Experiment notebooks if provided in official implementation

---

## Related Work & Context

### Connection to Feature Attribution Literature

**DFAX builds on and relates to**:

1. **SHAP (SHapley Additive exPlanations)**
   - SHAP uses game theory (Shapley values) as foundation
   - DFAX uses data distribution instead
   - Complementary perspectives on feature importance

2. **LIME (Local Interpretable Model-agnostic Explanations)**
   - LIME uses local linear approximation
   - DFAX uses global distribution grounding
   - DFAX more efficient (no repeated model queries)

3. **Integrated Gradients**
   - Gradient-based approach for neural networks
   - DFAX model-agnostic and doesn't require gradient information
   - Fundamental difference: distribution vs. gradient grounding

4. **Permutation Importance**
   - Measures feature importance via removal
   - DFAX: theoretically grounded in distribution
   - DFAX: avoids out-of-distribution scenarios from permutation

5. **Concept-Based Methods**
   - Network Dissection, TCAV focus on learned concepts
   - DFAX focuses on input feature importance
   - Complementary approaches to interpretability

### Relationship to Other xAI Subfields

**Fairness & Bias Detection**:
- Distribution-grounded attributions can reveal biased feature usage
- Natural connection to fairness auditing

**Causal Interpretability**:
- Distribution-based approach differs from causal inference
- Future work: connecting causal and distributional perspectives

**Mechanistic Interpretability**:
- DFAX is model-agnostic (doesn't interpret internals)
- Complements mechanistic approaches for full interpretability stack

**Human-Centered xAI**:
- Distribution-based explanations may be more intuitive
- Grounding in observable data patterns supports human understanding

### Recent Developments in Feature Attribution

**2025-2026 xAI Papers Building on Similar Ideas**:
- Higher-order feature attribution methods
- Formal approaches to explanation quality
- Distribution-based interpretability extensions

### Where This Research Leads

**Immediate Extensions**:
1. **Higher-Order Interactions**: Extending DFAX to capture feature interactions beyond marginal importance
2. **Causal Extensions**: Connecting distribution-grounding to causal inference frameworks
3. **Temporal Dynamics**: Handling time-varying distributions and concept drift

**Broader Impact Areas**:
1. **Foundation for xAI Standards**: Distribution-grounded approach could become new standard
2. **Fairness Verification**: Primary tool for auditing feature fairness
3. **Unified Attribution Framework**: Bringing together disparate attribution methods under distribution-based lens

**Open Research Directions**:
1. Formal theoretical guarantees on attribution quality
2. Scalability to 100K+ feature spaces
3. Integration with causal inference for causal attribution
4. Human evaluation studies on distribution-grounded explanations

---

## Summary & Key Takeaways

### What DFAX Solves

✓ **Formal Problem Definition**: First rigorous definition of feature attribution  
✓ **Distribution Grounding**: Explanations based on empirical data patterns  
✓ **Model-Agnostic**: Works with any classifier  
✓ **Computational Efficiency**: No repeated model queries needed  
✓ **Theoretical Soundness**: Principled foundation vs. ad hoc approaches  

### Why It Matters

- **For XAI Theory**: Foundational contribution establishing what feature attribution should be
- **For Practice**: Efficient, principled alternative to LIME/SHAP
- **For Regulation**: Distribution-based explanations support compliance needs
- **For Trust**: Grounding in observable data patterns increases AI trustworthiness

### How It Advances XAI

DFAX represents a paradigm shift in feature attribution from:
- **Ad hoc methods** → **Formally grounded approach**
- **Multiple conflicting definitions** → **Unified framework**
- **Gradient/local approximation** → **Global distribution perspective**
- **Model queries** → **Data-driven explanation**

This work is likely to influence the field significantly, as evidenced by its acceptance as an oral presentation at AAAI 2026.
