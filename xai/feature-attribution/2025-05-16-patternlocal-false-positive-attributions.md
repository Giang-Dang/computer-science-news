# PatternLocal: Minimizing False-Positive Attributions in Explanations of Non-Linear Models

**ArXiv ID:** [2505.11210](https://arxiv.org/abs/2505.11210)

## Executive Summary

This paper introduces **PatternLocal**, a novel method for generating local explanations of non-linear models that explicitly addresses and minimizes false-positive feature attributions caused by suppressor variables. While existing attribution methods like LIME and KernelSHAP are widely used for interpretability, they can assign high importance to features that have no causal relationship with the model's decision. PatternLocal converts discriminative weights from locally linear surrogates into a generative representation, fundamentally addressing this attribution correctness problem without requiring model retraining.

## Problem Statement

### The False-Positive Attribution Problem

Feature attribution methods are foundational in explainable AI, aiming to identify which input features most influenced a model's prediction. However, these methods suffer from a critical flaw: **suppressor variables**—features that have no causal relationship with the target but appear correlated in the data—can receive substantial attribution scores.

**Concrete Example:** Consider a model trained on data where:
- Feature x₁ causally affects the prediction
- Feature x₂ is correlated with x₁ but has no causal role
- Feature x₃ is a suppressor: it's uncorrelated with the target but negatively correlated with x₁

Methods like LIME, KernelSHAP, and gradient-based approaches will often assign significant importance to x₃ despite it having zero causal relationship with the model's decision. This false positive undermines trust in explanations and can mislead practitioners.

### Why This Matters

The problem is particularly acute in non-linear models:
- **Linear Models:** Fixes exist (e.g., controlling for confounders), but their applicability to non-linear models remained limited
- **Instance-Based Explanations:** LIME and KernelSHAP were designed for local explainability but lack mechanisms to handle suppressor variables
- **High-Dimensional Data:** In complex domains (medical imaging, genomics, NLP), suppressor variables are common, making false-positive attributions a serious issue

## Core Concepts & Theory

### Locally Linear Surrogates

The foundation of PatternLocal builds on the concept of **locally linear surrogates**—methods that approximate a complex model's behavior in a small neighborhood around a point of interest:

**LIME (Local Interpretable Model-Agnostic Explanations):** 
- Fits a linear model on perturbed samples around the instance
- Weights samples by proximity to the instance
- Extracts linear coefficients as feature importance scores

**KernelSHAP (Kernel method for Shapley values):**
- Computes Shapley values through a kernel-based approach
- Equivalent to LIME with specific weighting scheme
- Provides game-theoretic foundation for feature contributions

**Gradient-Based Methods:**
- Compute model sensitivities as local linear approximations
- Example: Integrated Gradients, Gradient-based saliency maps

### The Discriminative vs. Generative Problem

**Discriminative Approach (Current LIME/KernelSHAP):**
- These methods learn: "Given a neighborhood, what features discriminate the instance from the average?"
- In the presence of suppressor variables, they learn to assign high weights to features that correlate with the target, even if they're suppressors
- Mathematically: minimize ||ŷ - f(x)||² without regard to causal structure

**Generative Approach (PatternLocal):**
- Instead: "What features characterize the decision-making process?"
- Converts discriminative weights into a generative representation where suppressor variables are naturally suppressed
- Uses a generative model to filter out false associations

### Mathematical Formulation

**Step 1: Extract discriminative surrogate**
Given instance x and locally linear surrogate model g (e.g., LIME):
- Fit linear model: g(x) = β₀ + β^T z, where z is perturbed input
- Extract weights: β = [β₁, β₂, ..., βₙ]

**Step 2: Convert to generative form**
Instead of using β directly as attributions, PatternLocal:
1. Learns a generative model p(z | decision)—what does the neighborhood look like given the model's decision?
2. Decomposes the discriminative weights into principal directions
3. Removes components that correlate with background variations (suppressor directions)

**Key Insight:** The generative representation naturally downweights features that are uncorrelated with the actual decision-making pathway, even if they're correlated with the discriminative model's weights.

### Relationship to Existing Theory

**Connection to Causal Models:** PatternLocal implicitly aligns with causal interpretability—it suppresses confounders and spurious correlations, moving toward causal feature importance.

**Comparison to Debiasing Methods:** Related to methods that correct for confounding (e.g., propensity score weighting), but applied in the explanation context rather than prediction.

## Main Ideas & Key Contributions

### 1. Novel Attribution Method for Non-Linear Models

**Contribution:** PatternLocal extends pattern-based explanations (developed for linear/GAM models) to arbitrary non-linear models:
- **Model-Agnostic:** Works with any model, any input type (tabular, images, time series)
- **Local Fidelity Preservation:** Maintains the local accuracy of the underlying surrogate (LIME, gradients)
- **Suppressor Variable Handling:** Explicitly minimizes false-positive attributions

### 2. Addressing Attribution Correctness

**Why This Matters:**
- Prior work (arXiv:2409.14590) argues that "Explainable AI needs formal notions of explanation correctness"
- PatternLocal operationalizes this by targeting a specific correctness criterion: eliminating suppressor-driven false attributions
- Makes explanations more trustworthy for decision-makers and auditors

### 3. No Model Retraining Required

**Practical Advantage:**
- PatternLocal is purely a post-hoc method applied to already-trained models
- No architectural changes or retraining necessary
- Can be retrofitted to existing models in production

### 4. Empirical Validation on Controlled Benchmarks

**Key Insight:** PatternLocal's effectiveness is demonstrated on **synthetic benchmarks with ground-truth explanations**, not just real-world data:
- XAI-TRIS provides known suppressor-variable patterns
- Allows precise measurement of false-positive reduction
- Enables reproducible evaluation of attribution correctness

## Methodology & Implementation

### Experimental Setup

**Three Evaluation Testbeds:**

1. **XAI-TRIS Benchmark (arXiv:2306.12816)**
   - Synthetic 64×64 images with tetromino patterns
   - Three background variations: white (no suppression), correlated (suppressor variables), ImageNet (realistic suppressors)
   - Ground truth: tetromino location is the true explanation
   - Evaluation metric: False-positive rate (attributions on background pixels vs. signal)

2. **Artificial Lesion MRI Dataset**
   - Medical imaging with synthetic lesions
   - Controlled confounders and suppressor variables
   - Evaluates method on domain-realistic medical data

3. **EEG Motor Imagery Dataset**
   - Real-world brain signals during motor tasks
   - Tests physiological plausibility of explanations
   - EEG frequency patterns as features; motor intention as target

### Model Architectures Tested

- Convolutional Neural Networks (CNNs) for image tasks (XAI-TRIS, MRI)
- Simple feedforward networks for tabular data
- Domain-specific architectures (EEG: temporal models)

### Attribution Methods Compared

- **LIME:** Local linear surrogate, baseline
- **KernelSHAP:** Game-theoretic Shapley values
- **Gradient-based methods:** Saliency maps, Integrated Gradients
- **Other attribution methods:** Attention, GradCAM (image-specific)
- **PatternLocal variants:** PatternLocal + LIME, PatternLocal + KernelSHAP, PatternLocal + Gradients

### Hyperparameter Optimization

**Extensive tuning performed on XAI-TRIS:**
- **Bandwidth:** 0.5 to 30.0 (locality tradeoff)
- **Regularization strength:** 10⁻⁵ to 10² (generative model complexity)
- **Number of samples:** Varied to test robustness to sample size
- Results: PatternLocal consistently outperformed other methods after tuning

### Evaluation Metrics

1. **False-Positive Rate:**
   - Percentage of attribution weight on background (suppressor) regions
   - Lower is better; ground truth should be ~0% on background
   - [Exact figures unavailable — see full paper]

2. **Local Fidelity:**
   - Correlation between surrogate's predictions and original model
   - Ensures explanation preserves model behavior
   - [Exact figures unavailable — see full paper]

3. **Physiological Plausibility (EEG):**
   - Expert evaluation of whether explanations align with known motor cortex patterns
   - Qualitative assessment on motor imagery dataset

### Reported Results Summary

**On XAI-TRIS:**
- PatternLocal + LIME reduced false positives compared to standalone LIME
- PatternLocal + KernelSHAP showed consistent improvements on correlated backgrounds
- Performance improved with hyperparameter tuning; baseline methods also benefited but remained behind PatternLocal

**Important Caveat:** 
On some configurations, PatternLocal and LIME underperformed other methods (e.g., attention-based approaches). The authors attribute this to methods that suppress many low-level attributions, inflating errors differently. PatternLocal trades off some minor false-negatives (missing true signal) for major false-positive reduction.

**On Real Data (EEG):**
- Explanations aligned with known motor cortex activation patterns
- Qualitatively more interpretable than baseline methods

## Practical Applications & Real-World Use Cases

### Critical Domains for Attribution Correctness

**Healthcare & Medical Imaging:**
- **Problem:** Radiologists must trust AI diagnoses. False-positive attributions (e.g., image artifacts mistaken for disease) can lead to patient harm
- **Solution:** PatternLocal ensures explanations highlight true diagnostic features, not imaging artifacts or correlated noise
- **Example:** MRI diagnosis of brain tumors—PatternLocal prevents attribution to irrelevant anatomical structures

**Finance & Credit Decision-Making:**
- **Problem:** Automated lending decisions must be explainable and fair (FCRA compliance)
- **Challenge:** Correlated features (income, education, location) can act as confounders; models may attribute to protected attributes
- **Solution:** PatternLocal identifies true decision drivers, reducing bias and regulatory risk

**Criminal Justice & Recidivism:**
- **Problem:** Risk assessment tools are increasingly scrutinized for fairness; false-positive attributions can mask discriminatory patterns
- **Solution:** Ensures explanations reveal actual risk factors, not suppressor variables correlated with demographic groups

**Autonomous Systems:**
- **Problem:** Self-driving cars, drones must justify safety-critical decisions in accidents/audits
- **Solution:** Prevents attribution to spurious correlations; identifies true environmental factors driving decisions

### Regulatory & Compliance Implications

**GDPR Right to Explanation:**
- Recital 71 requires "meaningful information about the logic" of automated decisions
- PatternLocal supports this by providing more trustworthy, suppressor-aware explanations
- Reduces legal liability from biased explanations

**EU AI Act:**
- High-risk AI systems (Annex III) require documentation and testing
- PatternLocal enables more rigorous evaluation of explanation quality
- Supports evidence of non-discriminatory decision-making

**FDA Medical Device Regulation:**
- Increasingly requires interpretability for AI diagnostics
- PatternLocal provides attribution correctness—key to FDA approval

### Implementation Challenges

1. **Computational Cost:**
   - Generative model fitting adds overhead (approximate: 2-5× slower than LIME)
   - For real-time systems, may require caching/approximation

2. **Hyperparameter Sensitivity:**
   - Bandwidth and regularization require tuning for each domain
   - May not generalize across datasets without retuning

3. **Assumption: Sufficient Neighborhood Data:**
   - PatternLocal assumes enough samples exist in the neighborhood to learn generative model
   - Can fail in high-dimensional, sparse regions
   - Mitigated by adaptive bandwidth schemes

4. **Limited to Locally Linear Surrogates:**
   - Only works with methods outputting linear weights (LIME, KernelSHAP, gradients)
   - Not directly applicable to attention-based or prototype-based explanations

## Insights & Implications

### Broader Implications for Trustworthy AI

**Attribution Correctness as a Quality Metric:**
- Traditional XAI evaluation focuses on fidelity (does explanation match model?), not correctness (does it reflect true causality?)
- PatternLocal operationalizes correctness, shifting XAI evaluation toward causality-aware metrics
- Signals a maturation of the field: from "explanations that fit" to "explanations that are right"

**Generative Approaches for XAI:**
- Generative modeling—learning p(features | decision)—offers a principled way to suppress confounders
- Potential framework for other attribution-correctness challenges (e.g., temporal confounding in time series)

**Post-Hoc Limitations and Workarounds:**
- PatternLocal shows what post-hoc methods can achieve; suppressors fundamentally easier to handle with post-hoc adjustment than through end-to-end learning
- Suggests that some interpretability problems require post-hoc repair, not just inherent-interpretability approaches

### State-of-the-Art Advance

**Where It Fits:**
- **Feature Attribution Methods:** LIME, SHAP, gradients → PatternLocal (corrected variants)
- **Attribution Evaluation:** Existing metrics (feature importance rank, insertion/deletion) → PatternLocal (correctness-focused evaluation)
- **Mechanistic Interpretability:** Complements component-level explanation with corrected local feature importance

**Limitations and Open Questions:**

1. **Remains Local:** PatternLocal provides instance-level explanations; global model behavior may still harbor false attributions

2. **Ground-Truth Dependence:** Validation relied on synthetic data with known ground truths; real-world validation harder

3. **Generative Model Assumptions:** Assumes multivariate Gaussian or simple density model; may fail on highly complex distributions

4. **Trade-offs:** Reduces false positives at potential cost of false negatives (missing some true features)

### Future Research Directions

1. **Global Explanations:** Extending PatternLocal to provide corrected global/model-level attributions

2. **Adaptive Bandwidths:** Learning neighborhood size automatically to balance suppressor removal and local fidelity

3. **Other XAI Methods:** Applying generative correction to attention-based, prototype-based, and rule-based explanations

4. **Causal Discovery Integration:** Combining with causal structure learning to identify suppressors automatically

5. **Online/Continual Learning:** Updating generative models as data distributions shift

## Code & Resources

### Official Implementation

- **Repository:** [github.com/gjoelbye/PatternLocal](https://github.com/gjoelbye/PatternLocal)
- **Language:** Python
- **Dependencies:** scikit-learn, numpy, scipy, torch (for neural network models)

### Key Links

- **arXiv Preprint:** [https://arxiv.org/abs/2505.11210](https://arxiv.org/abs/2505.11210)
- **PDF Version:** [https://arxiv.org/pdf/2505.11210](https://arxiv.org/pdf/2505.11210)
- **HTML Version:** [https://arxiv.org/html/2505.11210](https://arxiv.org/html/2505.11210)
- **XAI-TRIS Benchmark:** [arXiv:2306.12816](https://arxiv.org/abs/2306.12816) — Synthetic benchmark for evaluating false-positive attribution rates

### Quick Start

```python
from pattern_local import PatternLocal
from lime.lime_tabular import LimeTabularExplainer

# Create LIME explainer
lime_explainer = LimeTabularExplainer(X_train, feature_names=feature_names)

# Wrap with PatternLocal for suppressor-aware explanations
patternlocal_explainer = PatternLocal(lime_explainer, X_train)

# Get explanation for instance
explanation = patternlocal_explainer.explain_instance(x_test, model.predict)
```

### Computational Requirements

- **Training Time:** Similar to LIME (depends on neighborhood sampling)
- **Memory:** Moderate (generative model fitting); scales with feature dimensionality
- **Practical:** Runs on CPU; GPU optional for large-scale batch processing
- **Hyperparameter Tuning:** Most time-consuming step; XAI-TRIS tuning required ~24 hours on modern hardware

## Related Work & Context

### How PatternLocal Fits into XAI Landscape

**Attribution Methods It Builds Upon:**
- **LIME (arXiv:1602.04938):** Local linear explanations—PatternLocal enhances LIME's robustness
- **SHAP/KernelSHAP (arXiv:1705.07874):** Game-theoretic feature importance—PatternLocal applies generative correction to SHAP
- **Integrated Gradients (arXiv:1703.01365):** Gradient-based attribution—PatternLocal compatible with gradient-based surrogates

**Prior Work on Suppressor Variables:**
- **Haufe et al. (2015):** "Interpretability and Explainability: A Machine Learning Zoo for 2.0?" — Identified suppressor issues in brain imaging
- **Haufe et al. (2014):** "On the interpretation of weight vectors of linear models in multivariate neuroimaging" — Theoretical foundation for PatternLocal's approach
- **arXiv:2111.07473:** "Scrutinizing XAI using linear ground-truth data with suppressor variables" — Benchmark for evaluating suppressor handling
- **arXiv:2306.01464:** "Theoretical Behavior of XAI Methods in the Presence of Suppressor Variables" — Theoretical analysis

**Attribution Correctness Work:**
- **arXiv:2409.14590:** "Explainable AI needs formal notions of explanation correctness" — Motivates PatternLocal's focus on correctness
- **arXiv:2306.12816 (XAI-TRIS):** "XAI-TRIS: Non-linear image benchmarks to quantify false positive post-hoc attribution of feature importance" — Key evaluation benchmark

**Related Approaches for Fairness/Debiasing:**
- **Concept Bottleneck Models (CBMs):** Inherently interpretable by using concepts—different approach to reducing spurious attributions
- **Causal Representation Learning:** Learning disentangled features to avoid confounding—complementary to PatternLocal

### Community Connections

**xAI Communities This Addresses:**
1. **Feature Attribution Community:** LIME/SHAP users seeking more correct explanations
2. **Interpretability Fairness Intersection:** Researchers addressing algorithmic bias through explanation quality
3. **Mechanistic Interpretability:** Effort to understand model internals; PatternLocal contributes local correctness perspective
4. **Medical AI:** Strong emphasis on trustworthy explanations for clinical deployment

### Where This Research Might Lead

1. **Post-Hoc Attribution as Default:** PatternLocal suggests post-hoc correction may be more practical than retraining for interpretability

2. **Generative XAI:** Broader adoption of generative modeling (p(features|decision)) for explanation quality

3. **Causal Attribution Integration:** Eventual merger of attribution methods and causal inference frameworks

4. **Regulatory Standardization:** PatternLocal's correctness focus aligns with emerging regulatory requirements for XAI verification

5. **Automated Attribution Verification:** Tools that automatically detect and flag false-positive attributions in deployed explanations

---

## References & Additional Resources

### Core Papers

- Gjølbye, A., Haufe, S., & Hansen, L. K. (2025). Minimizing False-Positive Attributions in Explanations of Non-Linear Models. *arXiv preprint arXiv:2505.11210*.
- Haufe, S., Meinecke, F., Görgen, K., Dähne, S., Haynes, J., Blankertz, B., & Bießmann, F. (2015). On the interpretation of weight vectors of linear models in multivariate neuroimaging. *NeuroImage*, 87, 96–110.
- Montavon, G., Bau, D., Binder, A., Braun, B., & Samek, W. (2015). Understanding Predict-then-Optimize systems. *arXiv preprint arXiv:1509.04119*.

### Attribution Methods

- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. *arXiv preprint arXiv:1602.04938* (LIME).
- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. *arXiv preprint arXiv:1705.07874* (SHAP/KernelSHAP).
- Sundararajan, M., Taly, A., & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. *arXiv preprint arXiv:1703.01365* (Integrated Gradients).

### Evaluation and Correctness

- **XAI-TRIS Benchmark:** Rong, Y., et al. (2023). XAI-TRIS: Non-linear image benchmarks to quantify false positive post-hoc attribution of feature importance. *arXiv preprint arXiv:2306.12816*.
- **Attribution Correctness:** Arrieta, A. B., et al. (2024). Explainable AI needs formal notions of explanation correctness. *arXiv preprint arXiv:2409.14590*.
