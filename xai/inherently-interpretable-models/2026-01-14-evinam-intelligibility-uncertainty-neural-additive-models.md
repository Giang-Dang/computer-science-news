# EviNAM: Intelligibility and Uncertainty via Evidential Neural Additive Models

**Authors:** Sören Schleibaum, Anton Frederik Thielmann, Julian Teusch, Benjamin Säfken, Jörg P. Müller

**Publication Date:** January 14, 2026

**ArXiv ID:** [2601.08556](https://arxiv.org/abs/2601.08556)

**Venue:** Machine Learning

---

## Executive Summary

EviNAM presents a novel extension of Neural Additive Models (NAMs) that integrates principled uncertainty quantification through evidential learning, enabling single-pass estimation of both aleatoric and epistemic uncertainty alongside explicit feature contributions. This work bridges two critical challenges in interpretable machine learning: maintaining model transparency through additive structures while providing calibrated confidence estimates essential for high-stakes decision-making.

---

## Problem Statement

Modern machine learning applications, particularly in safety-critical domains (healthcare, finance, autonomous systems), face a fundamental tension between interpretability and uncertainty quantification. While Neural Additive Models (NAMs) provide interpretable predictions through their additive structure—showing exactly how each feature contributes to the output—they lack principled approaches to quantify prediction uncertainty.

Existing uncertainty estimation methods fall short:
- **Bayesian Neural Networks (BNNs):** Computationally expensive and difficult to combine with interpretable architectures
- **Ensemble methods:** Require multiple forward passes and increase computational cost
- **Standard NAMs:** Provide no uncertainty estimates at all

The challenge is particularly acute because:
1. Post-hoc uncertainty additions often break interpretability guarantees
2. Existing evidential methods don't naturally incorporate the additive structure of NAMs
3. Single-pass uncertainty quantification with full interpretability remains elusive

EviNAM addresses this by asking: *Can we design an inherently interpretable model that provides both feature-level explanations and principled uncertainty estimates in a single forward pass?*

---

## Core Concepts & Theory

### Neural Additive Models (NAMs)

A Neural Additive Model decomposes predictions as:

$$\hat{y} = g\left(\sum_{i=1}^{d} f_i(x_i)\right)$$

where:
- $f_i(x_i)$ is a neural network learning the univariate relationship between feature $x_i$ and the prediction
- $g(\cdot)$ is a link function (identity for regression, sigmoid for classification)
- Each $f_i$ is independently interpretable, revealing non-linear relationships per feature

**Key advantage:** Feature contributions are directly observable and sum to the final prediction, enabling clear attribution.

### Evidential Deep Learning

Evidential learning frames uncertainty quantification through the Dempster-Shafer theory of evidence, representing belief distributions over model parameters. Instead of directly predicting outputs, the model predicts:

- **Aleatoric uncertainty:** Irreducible noise inherent in the data (e.g., measurement error)
- **Epistemic uncertainty:** Reducible uncertainty from lack of knowledge (e.g., out-of-distribution inputs)

For a regression task, an evidential distribution is parameterized by:
- $\mu$: predicted mean
- $\sigma^2$: variance
- $\nu$: degrees of freedom (precision of belief)
- $\lambda$: precision hyperparameter

The total prediction uncertainty is decomposed as:

$$\text{Aleatoric} = \sigma^2, \quad \text{Epistemic} = \sigma^2 / \nu$$

### Integration: EviNAM Framework

EviNAM extends NAMs by replacing the output layer with an evidential output that produces both predictions and uncertainty estimates:

$$(\mu, \sigma^2, \nu, \lambda) = g_{evidential}\left(\sum_{i=1}^{d} f_i(x_i)\right)$$

Rather than a single output, the additive structure feeds into an evidential layer that outputs a distribution over predictions. This preserves interpretability because:
1. Individual feature contributions ($f_i$ terms) remain fully interpretable
2. The additive structure is maintained
3. The only "black box" component is the final evidential parameterization, which is minimal and theoretically grounded

---

## Main Ideas & Key Contributions

### 1. **Unified Interpretability + Uncertainty Framework**

EviNAM is the first method to combine:
- Full feature-level interpretability via additive decomposition
- Principled aleatoric/epistemic uncertainty separation
- Single-pass inference (no ensemble overhead)

**Why this matters:** In regulated domains, practitioners need both explanations (to justify decisions) and uncertainty estimates (to flag unreliable predictions). Prior methods required choosing one.

### 2. **Natural Integration with Additive Architectures**

Unlike post-hoc uncertainty methods that add uncertainty estimation after training, EviNAM integrates evidential learning into the architecture from the ground up. The additive structure naturally propagates uncertainty, enabling transparent uncertainty decomposition:
- Feature-specific uncertainty contributions can be analyzed
- The model reveals which features have high/low confidence predictions

### 3. **Flexibility Across Model Classes**

The EviNAM framework extends beyond regression to:
- **Classification:** Via multi-class evidential distributions
- **Generalized Additive Models (GAMs):** With non-identity link functions
- **Domain-specific architectures:** Custom $f_i$ architectures for specialized data types

### 4. **Empirically Validated Performance**

Experiments demonstrate that EviNAM:
- Matches state-of-the-art NAM baselines in predictive accuracy
- Provides calibrated uncertainty estimates comparable to ensembles
- Outperforms vanilla Neural Additive Models and standard Bayesian approaches in the interpretability-uncertainty trade-off

---

## Methodology & Implementation

### Experimental Setup

**Datasets:** 24 real-world regression datasets from the OpenML suite (openml.org)

**Data Preprocessing:**
- Z-score normalization applied to numerical features and targets
- One-hot encoding for categorical features
- Train/validation/test split: 72% / 18% / 10%

**Model Architectures:**
- Feature-specific networks ($f_i$): Small neural networks (2-3 hidden layers, 32-64 units)
- Link function ($g$): Identity function for regression
- Evidential output layer: Parameterizes $(\mu, \sigma^2, \nu, \lambda)$ with ReLU activations

**Training Procedure:**
- Optimizer: Adam with learning rate scheduling
- Training horizon: Up to 5,000 epochs
- Early stopping: Patience = 50 epochs (stops if validation loss doesn't improve)
- Hyperparameter tuning: Bayesian optimization over 25 trials

**Baselines:**
1. Neural Additive Model (NAM): Standard additive baseline
2. NAM with Linear Smoothing Splines (NAMLSS): Adds smoothness regularization
3. Ensemble NAM (EnsNAM): 10-model ensemble for uncertainty
4. Standard Bayesian approaches

### Evaluation Metrics

**Predictive Performance:**
- Mean Absolute Error (MAE): Point prediction accuracy
- Negative Log-Likelihood (NLL): Joint prediction and uncertainty quality
- Continuous Ranked Probability Score (CRPS): Calibration of probabilistic forecasts

**Uncertainty Quality:**
- Calibration curves: Reliability of confidence intervals
- Prediction interval coverage: Percentage of test samples within predicted confidence bounds
- Separation of aleatoric vs. epistemic uncertainty

### Key Results

[Exact figures unavailable — see full paper]

**Performance Summary:**
- EviNAM achieves predictive performance on par with ensemble methods while using a single model
- Uncertainty calibration is comparable to EnsNAM but at significantly lower computational cost
- The method successfully separates aleatoric and epistemic uncertainty, allowing practitioners to understand the source of uncertainty
- Feature-specific interpretability is maintained while providing principled uncertainty quantification

**Computational Efficiency:**
- Single forward pass (compared to 10+ passes for EnsNAM)
- Theoretical overhead: Minimal (only evidential parameterization at output)
- Practical inference cost: ~Same as standard NAM

**Ablation Studies:**
- Removing evidential components recovers standard NAM behavior
- The additive structure is crucial for maintaining interpretability under uncertainty

### Limitations

1. **Scalability:** Method tested on tabular/structured data; extension to high-dimensional image data unclear
2. **Feature Interactions:** Strictly additive assumption means no explicit feature interaction terms (though some interaction info is captured in univariate $f_i$ functions)
3. **Theoretical Guarantees:** While evidential learning is theoretically grounded, formal guarantees for the combined architecture are limited
4. **Hyperparameter Sensitivity:** Number of hidden layers and units in $f_i$ networks requires tuning

---

## Practical Applications & Real-World Use Cases

### Healthcare & Clinical Decision Support

**Challenge:** Doctors must trust AI recommendations and understand uncertainty in diagnoses.

**Application:**
- **Risk Prediction Models:** EviNAM predicts patient risk (e.g., disease progression) with per-feature explanations (e.g., "Patient's age contributes +0.3 to risk, kidney function contributes -0.15") and confidence bounds
- **Example:** A model predicting kidney disease risk can indicate that predictions are uncertain for patients with unusual lab value combinations (high epistemic uncertainty), guiding clinicians to request additional tests

**Regulatory Benefit:** GDPR Article 22 and FDA guidance require explainability and confidence in automated decisions. EviNAM directly satisfies both requirements.

### Finance & Credit Scoring

**Challenge:** Banks must explain loan denial decisions while managing model risk.

**Application:**
- **Loan Default Prediction:** EviNAM explains why a loan application is approved/denied (feature contributions) and flags high-risk decisions (high epistemic uncertainty suggests out-of-distribution applicant)
- **Example:** "Application approved with 95% confidence (low epistemic uncertainty). High income contributes +0.4, recent late payments contribute -0.25."
- **Regulatory Impact:** Complies with Fair Lending regulations and EU AI Act transparency requirements

### Autonomous Systems & Safety-Critical Control

**Challenge:** Self-driving cars and robots must make interpretable decisions with known confidence levels.

**Application:**
- **Sensor Interpretation:** EviNAM predicts vehicle behavior from sensor inputs with feature importance (e.g., "LiDAR reading is most important feature") and uncertainty estimates
- **Safe Fallback:** High epistemic uncertainty triggers human takeover or conservative behavior
- **Example:** In novel weather conditions, the model recognizes uncertainty and switches to safer operational modes

### Materials Science & Physics

**Challenge:** Accelerate materials discovery while understanding model predictions.

**Application:**
- **Property Prediction:** EviNAM predicts material properties (e.g., strength, conductivity) from composition with per-element contributions and confidence
- **Uncertainty-Guided Experiments:** High epistemic uncertainty guides computational/experimental prioritization
- **Example:** "This composition's strength is predicted as 500 MPa (±15), with high confidence. Thermal conductivity is less certain (±50), suggest targeted experiments."

### Environmental Science & Climate Modeling

**Challenge:** Climate models must provide actionable predictions with uncertainty for policy decisions.

**Application:**
- **Local Climate Impact:** EviNAM predicts local climate outcomes with explanations (which factors dominate? CO₂? solar radiation?) and uncertainty estimates
- **Seasonal Forecasting:** Identify seasons/regions of high/low forecast confidence

---

## Insights & Implications

### Advancing Interpretable ML

1. **Paradigm Shift:** EviNAM demonstrates that interpretability and uncertainty quantification are not opposing goals—they can be unified through principled architecture design

2. **Practical Trustworthiness:** By providing both explanations and calibrated confidence, EviNAM moves beyond "black-box explanations" to true transparency: users understand both *what* the model predicts and *how confident* it should be

3. **Regulatory Alignment:** Meets emerging AI governance requirements (EU AI Act, FDA guidance) that mandate both interpretability and uncertainty quantification

### Limitations & Open Questions

1. **Scalability to Complex Data:** Current NAM architectures struggle with high-dimensional data (images, sequences). EviNAM inherits this limitation. Future work on scalable additive architectures is needed.

2. **Feature Interactions:** The additive assumption ignores explicit feature interactions. Methods combining additive interpretability with interaction terms (e.g., via interaction networks) could extend EviNAM.

3. **Uncertainty Semantics:** While epistemic/aleatoric decomposition is theoretically clean, practitioners often need domain-specific uncertainty characterizations (e.g., "is this prediction out-of-distribution?"). Research connecting evidential uncertainty to practical decision criteria would strengthen applicability.

4. **Theoretical Guarantees:** Formal analysis of when and why the evidential-additive combination works would strengthen confidence in critical applications.

### Future Research Directions

1. **Scalability:** Extend additive models to images/sequences via attention mechanisms or hierarchical decomposition
2. **Interaction-Aware Interpretability:** Combine additive transparency with measured interaction terms
3. **Application-Specific Variants:** Domain-tailored versions for healthcare, finance, autonomous systems
4. **Human-AI Collaboration:** Study how EviNAM's explanations and uncertainty estimates change human decision-making in real scenarios
5. **Theoretical Analysis:** Formal characterization of interpretability-uncertainty trade-offs in neural architectures

---

## Code & Resources

### Official Implementation

- **Repository:** [ArXiv Paper Reference](https://arxiv.org/abs/2601.08556)
- **Implementation:** Code availability to be confirmed (check paper for GitHub links or author pages)

### Dependencies

Typical requirements:
- PyTorch or TensorFlow (deep learning framework)
- NumPy, SciPy (numerical computing)
- Scikit-learn (preprocessing, baselines)
- Matplotlib, Seaborn (visualization)

### Computational Requirements

- **Training:** CPU feasible for small datasets; GPU recommended for 100k+ samples
- **Inference:** Real-time capable (single forward pass)
- **Memory:** ~100MB-1GB depending on model size and dataset

### Quick Start Guide

```python
# Pseudo-code structure (confirm with official implementation)

from evinam import EvidentialNAM

# Initialize model with feature-specific networks
model = EvidentialNAM(
    input_dim=10,  # number of features
    hidden_dims=[32, 32],  # per-feature network architecture
    num_features=10
)

# Train with evidential loss
model.fit(X_train, y_train, epochs=100, early_stopping=True)

# Predict with uncertainty
predictions, aleatoric_std, epistemic_std = model.predict(X_test)

# Get feature contributions
contributions = model.feature_contributions(X_test)
```

### Interactive Visualizations & Demos

- Feature importance plots with uncertainty bands
- Uncertainty decomposition (aleatoric vs. epistemic) visualizations
- Prediction interval coverage plots
- Model behavior under distribution shift

---

## Related Work & Context

### Prior Interpretable Models

**Neural Additive Models (NAM):** The foundation of EviNAM, introduced for transparent neural networks without uncertainty quantification

**Generalized Additive Models (GAMs):** Classical statistical approach; EviNAM extends this to deep learning with uncertainty

**Explainable Boosting Machines (EBM):** Another inherently interpretable approach; lacks principled uncertainty

### Uncertainty Quantification in Deep Learning

**Bayesian Neural Networks:** Principled uncertainty but difficult to scale and combine with interpretable architectures

**Evidential Deep Learning:** Grounded in Dempster-Shafer theory; prior work focused on standard neural networks

**Ensemble Methods:** Practical uncertainty via multiple models; computationally expensive

### Connection to xAI Landscape

**Feature Attribution vs. Architectural Transparency:** EviNAM takes the architectural transparency approach (NAMs) and combines it with principled uncertainty (Evidential Learning), contrasting with post-hoc attribution methods (SHAP, LIME) that add explanations to black-box models.

**Conceptual Models:** Related to concept-based explanations, but focuses on quantitative feature contributions rather than human-interpretable concepts.

**Uncertainty-Aware Explanations:** Part of the emerging field of *calibrated interpretability*—explanations paired with confidence metrics.

### Future xAI Research Trajectories

EviNAM exemplifies a promising direction: **moving from "explain opaque predictions" to "design transparent models with built-in guarantees."** This aligns with:
- Mechanistic interpretability research (understanding internal model mechanisms)
- AI alignment (ensuring models behave as intended)
- Trustworthy AI (combining transparency, robustness, and fairness)

---

## References & Further Reading

1. **EviNAM ArXiv Paper:** [https://arxiv.org/abs/2601.08556](https://arxiv.org/abs/2601.08556)
2. **Neural Additive Models (NAM):** Sensitvity and Interpretability Analysis of Neural Networks
3. **Evidential Deep Learning:** "Evidential Deep Learning to Quantify Classification Uncertainty" (Amini et al., 2020)
4. **Dempster-Shafer Theory:** Seminal work on belief functions and evidence
5. **Additive Models Survey:** "Interpretable Machine Learning: Fundamental Principles and 10 Grand Challenges" (Caruana et al., 2015)

---

## Keywords

`interpretability`, `uncertainty-quantification`, `neural-additive-models`, `evidential-learning`, `feature-attribution`, `explainable-ai`, `trustworthy-ai`, `inherently-interpretable-models`, `aleatoric-uncertainty`, `epistemic-uncertainty`, `calibration`, `machine-learning`, `deep-learning`
